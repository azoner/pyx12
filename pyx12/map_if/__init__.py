######################################################################
# Copyright (c)
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
"""
Interface to a X12N IG Map.

This package re-exports the classes that previously lived in a single
map_if.py module so that `import pyx12.map_if` and
`from pyx12.map_if import X` keep working unchanged.
"""

from __future__ import annotations

from ..syntax import is_syntax_valid
from ._base import MAXINT, _required_attr, x12_node
from ._composite import composite_if
from ._element import element_if
from ._loader import load_map_file
from ._loop import loop_if
from ._root import map_if
from ._segment import segment_if

__all__ = [
    "MAXINT",
    "_required_attr",
    "composite_if",
    "element_if",
    "is_syntax_valid",
    "load_map_file",
    "loop_if",
    "map_if",
    "segment_if",
    "x12_node",
]
