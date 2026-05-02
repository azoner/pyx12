######################################################################
# Copyright (c)
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
"""
Base node and shared helpers for the X12N IG map interface.
"""

from __future__ import annotations

from typing import Any
from xml.etree.ElementTree import Element

from ..errors import EngineError
from ..path import X12Path

MAXINT = 2147483647


def _required_attr(elem: Element, name: str) -> str:
    v = elem.get(name) or elem.findtext(name)
    if v is None:
        raise EngineError(f"Required attribute or child {name!r} missing on <{elem.tag}>")
    return v


class x12_node:
    """
    X12 Node Superclass
    """

    id: str | None
    name: str | None
    parent: Any
    children: list[Any]
    path: str
    _x12path: X12Path | None
    _fullpath: str | None

    def __init__(self) -> None:
        self.id = None
        self.name = None
        self.parent = None
        self.children = []
        self.path = ""
        self._x12path = None
        self._fullpath = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, x12_node):
            return self.id == other.id and self.parent.id == other.parent.id
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        return NotImplemented

    __le__ = __lt__
    __le__ = __lt__
    __gt__ = __lt__
    __ge__ = __lt__

    def __hash__(self) -> int:
        return ((self.id or "") + (self.parent.id or "")).__hash__()

    def __len__(self) -> int:
        return len(self.children)

    def __repr__(self) -> str:
        """
        :rtype: string
        """
        return self.name or ""

    def getnodebypath(self, path: str) -> Any:
        """ """
        pathl = path.split("/")
        if len(pathl) == 0:
            return None
        for child in self.children:
            if child.id.lower() == pathl[0].lower():
                if len(pathl) == 1:
                    return child
                else:
                    if child.is_loop():
                        return child.getnodebypath("/".join(pathl[1:]))
                    else:
                        break
        raise EngineError('getnodebypath failed. Path "%s" not found' % path)

    def get_child_count(self) -> int:
        return len(self.children)

    def get_child_node_by_idx(self, idx: int) -> Any:
        """
        :param idx: zero based
        """
        if idx >= len(self.children):
            return None
        else:
            return self.children[idx]

    def get_child_node_by_ordinal(self, ordinal: int) -> Any:
        """
        Get a child element or composite by the X12 ordinal
        :param ord: one based element/composite index.  Corresponds to the map <seq> element
        :type ord: int
        """
        return self.get_child_node_by_idx(ordinal - 1)

    def get_path(self) -> str:
        """
        :return: path - XPath style
        :rtype: string
        """
        if self._fullpath:
            return self._fullpath
        parent_path = self.parent.get_path()
        if parent_path == "/":
            self._fullpath = "/" + self.path
            return self._fullpath
        else:
            self._fullpath = parent_path + "/" + self.path
            return self._fullpath

    def _get_x12_path(self) -> X12Path:
        """
        :return: X12 node path
        :rtype: L{path<X12Path>}
        """
        if self._x12path:
            return self._x12path
        p = X12Path(self.get_path())
        self._x12path = p
        return p

    x12path = property(_get_x12_path, None, None)

    def is_first_seg_in_loop(self) -> bool:
        """
        :rtype: boolean
        """
        return False

    def is_map_root(self) -> bool:
        """
        :rtype: boolean
        """
        return False

    def is_loop(self) -> bool:
        """
        :rtype: boolean
        """
        return False

    def is_segment(self) -> bool:
        """
        :rtype: boolean
        """
        return False

    def is_element(self) -> bool:
        """
        :rtype: boolean
        """
        return False

    def is_composite(self) -> bool:
        """
        :rtype: boolean
        """
        return False


############################################################
# Map file interface
