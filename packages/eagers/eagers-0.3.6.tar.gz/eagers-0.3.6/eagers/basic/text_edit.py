"""Utilities for editing text.

Functions:
truncate
"""


def truncate(text, max_len, tail=0, rep='...', *, spill_to_newlines=False):
    """Truncate the input string, keeping a number of characters at the end.

    Positional arguments:
    text -- String to be shortened.
    max_len -- Maximum length of string.

    Keyword arguments:
    tail -- Number of characters to keep at the end. Default: 0
    rep -- String to replace removed text. Default: "..."
    """
    assert (
        max_len > len(rep) + tail
    ), "Character limit does not allow enough room for shortening."
    if len(text) <= max_len:
        return text
    elif spill_to_newlines:
        return '\n'.join(
            text[i:i+max_len] for i in range(0, len(text), max_len))
    else:
        assert tail > -1, "tail must be non-negative."
        cutoff = max_len - tail - len(rep)
        tail_str = '' if tail == 0 else text[-tail:]
        return text[:cutoff] + rep + tail_str
