"""Simulation run logic.

Functions:
run_eagers_core - read from excel files, pre-load dictionaries and call run_project
run_project - Initializes data structures and calls run_simulation().
run_simulation - Low-level simulation run logic.
load_actual_data
simulate_response
"""

import datetime
import warnings

from tables.exceptions import NaturalNameWarning

from eagers.basic.build_time_vector import build_time_vector
from eagers.basic.find_gen_node import find_gen_node
from eagers.basic.get_data import get_data
from eagers.basic.logger import logger, start_logger
from eagers.basic.messages import sim_loop_iteration, sim_loop_start
from eagers.basic.result_template import result_template
from eagers.basic.auto_set_startdate import auto_set_startdate
from eagers.config.simulation import DEFAULT_INITIAL_SOC
from eagers.extras import bplus_forecast_dr_capacity, bplus_load_actual_building_data
from eagers.forecasting.calculate_fits import calculate_fits
from eagers.forecasting.update_forecast import update_forecast
from eagers.forecasting.hydro_forecast import hydro_forecast
from eagers.forecasting.water_year_forecast import water_year_forecast
from eagers.plot.dispatch_step import new_figure, plot_component_dispatch
from eagers.read.excel_interface import ProjectTemplateReader, TestDataTemplateReader
from eagers.read.read_test_data import read_test_data
from eagers.read.read_network import read_network
from eagers.read.read_market import read_market
from eagers.setup.preload import preload
from eagers.setup.automatic_ic import automatic_ic
from eagers.setup.initialize_observer import initialize_observer, initialize_building_observer
from eagers.simulate.plant_response import plant_response
from eagers.simulate.renewable_output import renewable_output
from eagers.solver.dispatch_loop import dispatch_loop
from eagers.solver.generate_bids import generate_bids
from eagers.update.dispatch_record import dispatch_record, predict_record
from eagers.update.update_cost import update_cost
from eagers.update.update_market import update_market
from eagers.update.update_observer import update_observer
from eagers.write.result_file import new_result_file, result_file_setup, append_step_solution


def demo():
    run_eagers_core('default_project', 'default_testdata', plot_step=True) #Run default project


def demo_result():
    from eagers.plot.dispatch_result_excel import plot_dispatch_result
    plot_dispatch_result('default_project', 'default_testdata')


def run_eagers_core(
    project_filename, testdata_filename, *, message_step=True, plot_step=True
):
    """Load from excel then run a project 

        Keyword arguments:
        message_step - (bool) (Default: True) Whether to output messages
            at each simulation iteration.
        plot_step - (bool) (Default: True) Whether dispatch should be
            plotted at each simulation iteration.
    """
    # Filter out NaturalNameWarnings.  https://stackoverflow.com/q/58414068/7232335
    warnings.filterwarnings("ignore", category=NaturalNameWarning)
    proj = ProjectTemplateReader.read_userfile(project_filename)
    proj['test_data'] = read_test_data(TestDataTemplateReader.read_userfile(testdata_filename))
    read_network(proj['plant']['network']) 
    proj['plant']['market'] = read_market(None)
    if proj['options']['start_date'] is None:
        if len(proj['plant']['building'])>0:
            proj['options']['start_date'] = proj['plant']['building'][0]['sim_date'][0]
        else:
            proj['options']['start_date'] = auto_set_startdate(proj['test_data'])
    proj['preload'] = preload(proj['plant'], proj['test_data'] ,proj['options'])
    if message_step:
        start_logger(proj['name'])
    run_project(proj, message_step, plot_step)


def run_project(proj, message_step, plot_step):
    """Run the given project. Initializes data structures and then
    passes them on to run_simulation().

    Positional arguments:
    proj - (Project) Project to run.
    plot_step - (bool) Whether dispatch should be plotted at each
        simulation iteration.
    """
    date = [proj['options']['start_date']]
    date_v = build_time_vector(proj['options']['start_date'], proj['options'], to_timedelta=True)
    
    building_observer,zones,pl = initialize_building_observer(proj['plant']['building'],proj['test_data']['weather'],date)    
    names, dimensions, minimization_directives = result_file_setup(
        proj['preload'], proj['plant'], date_v, zones, pl
    )
    new_result_file(proj['name'], names, dimensions, minimization_directives, zones, pl)

    # Create typical day fits if necessary.
    proj['hist_prof'] = calculate_fits(
        proj['test_data'], proj['options'], proj['preload']['subnet'])
    market = proj['plant']['market']
    fluid_loop = create_fluid_loop(proj['plant'])
    
    scale_cost = update_cost(date, proj['preload']['gen_qp_form'], market)
    ic, data_t0, _ = automatic_ic(
        proj['preload']['gen_qp_form'], proj['plant']['building'], fluid_loop,
        market, proj['preload']['subnet'], date, proj['preload']['one_step'], proj['options'],
        proj['test_data'], building_observer, scale_cost)
    
    all_data_nodes = count_nodes(proj['preload']['subnet'],proj['test_data'])
    proj['observer'] = initialize_observer(proj['preload']['gen_qp_form'], proj['preload']['subnet'], fluid_loop,all_data_nodes, names, zones, pl, proj['test_data'], 
                            building_observer, ic, DEFAULT_INITIAL_SOC, date, data_t0, proj['name'])
    
    # If October 1st, run a yearly forecast for hydrology.
    proj['observer'] = water_year_forecast(proj['preload']['gen_qp_form'], proj['plant']['building'],
         fluid_loop, proj['observer'], all_data_nodes, names, zones, pl,
        market, proj['preload']['subnet'], proj['options'], date_v, proj['test_data'])
    run_simulation(data_t0, date,  proj['test_data'], proj['preload'],
        proj['plant']['building'], fluid_loop, all_data_nodes, names, zones, pl,
        proj['observer'], market,proj['options'], proj['name'], message_step, plot_step)


def run_simulation(
        data_t0, date, test_data, preload, building,
        fluid_loop, all_data_nodes, names, zones, pl,
        observer, market, options, project_name, message_step, plot_step):
    """Low-level simulation run logic.

    Positional arguments:
    ...
    plot_step - (bool) Whether to plot at each simulation step.
    """
    # Break up preload into smaller variables.
    gen = preload['gen_qp_form']
    subnet = preload['subnet']
    
    # Get figure and axes for plotting simulation step results.
    if plot_step:
        fig, axs = new_figure(project_name, gen, subnet)

    # Set up vector of time interval.
    date = build_time_vector(options['start_date'], options, to_timedelta=True)

    # Get start time for console logging.
    if message_step:
        t_start = datetime.datetime.now()
        logger.info(sim_loop_start(project_name, t_start))

    # Simulation loop.
    if options['method'] == 'planning':
        num_steps = int(options['interval'] * 24 / (options['resolution']*options['horizon']) + 1)
    else:
        num_steps = int(options['interval'] * 24 / options['resolution'] + 1)
    timer =  []
    prediction = None
    predicted = result_template(all_data_nodes,names, zones, pl)
    for k in predicted['building']:
        del predicted['building'][k]['supply']
        del predicted['building'][k]['return_']
    dispatch = result_template(all_data_nodes,names, zones, pl)
    while date[0] < options['start_date']+ datetime.timedelta(days=options['interval']):
        market = update_market(gen, market, date)# Assign any previous market bids if a bidding period has closed.
        
        observer = water_year_forecast(
            gen, building, fluid_loop, observer, all_data_nodes, names, zones, pl, market, subnet, options, date,test_data)# If October 1st, run a yearly forecast for hydrology.
        forecast = update_forecast(options, date[1:], test_data, subnet)
        if 'weather' in forecast and 'dir_norm_irr' in forecast['weather']:
            forecast['renewable'] = []
            for g in gen:
                if g['type'] in ('Renewable', 'Solar', 'Wind') and g['enabled']:
                    gen_network, i_node = find_gen_node(g, subnet)
                    location = subnet[gen_network]["location"][i_node]
                    gen_output = renewable_output(
                        g, date[1:], forecast['weather']['dir_norm_irr'], location
                    )
                else:
                    gen_output = []
                forecast['renewable'].append(gen_output)
        if building:
            forecast['building'] = bplus_forecast_dr_capacity(building, observer, forecast['weather'], date)
        else:
            forecast['building'] = None
        forecast = hydro_forecast(forecast, test_data, date[1:], subnet, observer, options)

        solution, _ = dispatch_loop(gen, observer, market, subnet, names, preload['op_mat_a'], 
                                    preload['op_mat_b'], preload['one_step'], options, date, forecast, prediction)
        timer.append(solution['timer'])
        
        predict_record(gen, predicted, observer, market, subnet, date, forecast, solution, project_name)
        market = generate_bids(gen, solution['dispatch'], date, market)  # Generate new bids for next time steps.

        if options['method'] == 'planning':
            actual_data = forecast# Assumes forecast is perfect (no disparity).
        elif  options['method'] in ('dispatch', 'control'):   
            actual_data = load_actual_data(options, observer, test_data, 
                forecast, date, building, subnet)         
        plant_response(gen, building, fluid_loop, observer, market, subnet, names, actual_data,
                       preload, options, forecast, date, solution)

        dispatch_record(gen, dispatch, observer, market, subnet, actual_data, solution, project_name)
        date = update_observer(gen, subnet, observer, date, options, solution, actual_data, forecast)
        prediction = next_prediction(gen,observer,solution['dispatch'])
        del solution['dispatch']
        append_step_solution(project_name, solution)# Write result of simulation step to HDF5 file.)
        # Plot.
        if plot_step:
            try:
                plot_component_dispatch(
                    axs, observer['history'], observer['future'], gen, subnet)
            except:
                # Stop plotting at every step so the simulation can
                # continue.
                plot_step = False
        if message_step:
            logger.info(sim_loop_iteration(project_name, t_start, len(timer), num_steps))


def load_actual_data(options, observer, test_data, forecast, date, buildings, subnet):
    # Count forward 1 step, rounded to nearest second.
    d_now = [date[0] + datetime.timedelta(hours=options['resolution'])]
    actual_data = get_data(test_data, d_now, subnet['network_names'])
    if buildings:
        actual_data['building'] = bplus_load_actual_building_data(buildings,observer,actual_data['weather'],forecast['building'],d_now,options['resolution']*3600)
    else:
        actual_data['building'] = None
    return actual_data


def next_prediction(gen,observer,forecast):
    n_g = len(gen)
    prediction = [[] for j in range(n_g)]
    for i in range(n_g):
        if 'stor' in gen[i]:
            prediction[i] = [observer['stor_state'][i]]
        else:
            prediction[i] = [observer['gen_state'][i]]
        prediction[i].extend(forecast[i][2:])
        prediction[i].append(forecast[i][-1])
    return prediction


def create_fluid_loop(plant):
    fluid_loop = {}
    if len(plant['fluid_loop'])>0:
        kys = list(plant['fluid_loop'][0].__dict__.keys())
        for k in kys:
            fluid_loop[k] = []
        for j in range(len(plant['fluid_loop'])):
            for k in kys:
                fluid_loop[k].append(getattr(plant['fluid_loop'][j],k))
    else:
        fluid_loop['name'] = []
    return fluid_loop


def count_nodes(subnet,test_data):
    all_data_nodes = []
    for net in subnet['network_names']:
        if net in test_data['nodedata_network_info']:
            all_nodes = []
            net_nodes = []
            data_nodes = [test_data['nodedata_network_info'][net][i]['node'] for i in range(len(test_data['nodedata_network_info'][net]))]
            for i in range(len(subnet[net]['nodes'])):
                ag_nodes = subnet[net]['nodes'][i]
                all_nodes.extend(ag_nodes)
                net_nodes.extend([i for j in range(len(ag_nodes))])
            for j in range(len(data_nodes)):
                n = net_nodes[all_nodes.index(data_nodes[j])]
                if 'demand' in test_data['nodedata_network_info'][net][j]:
                    subnet[net]['load'][n].append(test_data['nodedata_network_info'][net][j]['demand'])
            all_data_nodes.extend(data_nodes)
    return all_data_nodes
