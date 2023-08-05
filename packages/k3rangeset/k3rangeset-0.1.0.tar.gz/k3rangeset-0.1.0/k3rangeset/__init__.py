"""
Segmented range which is represented in a list of sorted interleaving range.

A range set can be thought as: `[[1, 2], [5, 7]]`.

"""

# from .proc import CalledProcessError
# from .proc import ProcError

__version__ = "0.1.0"
__name__ = "k3rangeset"

from .rangeset import (
    IntIncRange,
    IntIncRangeSet,
    Range,
    RangeDict,
    RangeSet,
    ValueRange,

    RangeException,

    substract_range,

    intersect,
    substract,
    union,
)

__all__ = [
    "IntIncRange",
    "IntIncRangeSet",
    "Range",
    "RangeDict",
    "RangeSet",
    "ValueRange",

    "RangeException",

    "substract_range",

    "intersect",
    "substract",
    "union",
]
