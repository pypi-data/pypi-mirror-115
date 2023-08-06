"""
#   Name

k3fmt

It provides with several string operation functions.

#   Status

This library is considered production ready.

"""

# from .proc import CalledProcessError
# from .proc import ProcError

__version__ = "0.1.0"
__name__ = "k3fmt"

from .strutil import (
    format_line,
    break_line,
    parse_colon_kvs,
    tokenize,
    line_pad,
    struct_repr,
    format_table,
    filter_invisible_chars,
    utf8str,
    page,
)


__all__ = [
    'format_line',

    'parse_colon_kvs',
    'tokenize',
    'line_pad',
    'break_line',
    'struct_repr',
    'format_table',
    'filter_invisible_chars',
    'utf8str',
    'page',
]
