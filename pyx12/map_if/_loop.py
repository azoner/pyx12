######################################################################
# Copyright (c)
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
"""
Loop interface ------ recursive container of loops and segments.
"""

from __future__ import annotations

import sys
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any
from xml.etree.ElementTree import Element

import pyx12.segment

from ..errors import EngineError
from ..path import X12Path
from ._base import MAXINT, _required_attr, x12_node

if TYPE_CHECKING:
    from . import segment_if  # noqa: F401  -- referenced only at runtime via local import


############################################################
# Loop Interface
############################################################
class loop_if(x12_node):
    """
    Loop Interface
    """

    root: Any
    pos_map: dict[int, list[Any]]
    base_name: str
    _cur_count: int
    type: str | None
    usage: str | None
    pos: int
    repeat: str | None

    def __init__(self, root: Any, parent: Any, elem: Element) -> None:
        """ """
        # Local import to break the import cycle: segment_if is defined in
        # the package's __init__.py, which itself imports this module.
        from . import segment_if

        x12_node.__init__(self)
        self.root = root
        self.parent = parent
        self.pos_map = {}
        self.base_name = "loop"
        self._cur_count = 0

        self.id = elem.get("xid")
        self.path = self.id or ""
        self.type = elem.get("type")

        self.name = elem.get("name") if elem.get("name") else elem.findtext("name")
        self.usage = elem.get("usage") if elem.get("usage") else elem.findtext("usage")
        self.pos = int(_required_attr(elem, "pos"))
        self.repeat = elem.get("repeat") if elem.get("repeat") else elem.findtext("repeat")

        for e in elem.findall("loop"):
            loop_node = loop_if(self.root, self, e)
            try:
                self.pos_map[loop_node.pos].append(loop_node)
            except KeyError:
                self.pos_map[loop_node.pos] = [loop_node]
        for e in elem.findall("segment"):
            seg_node = segment_if(self.root, self, e)
            try:
                self.pos_map[seg_node.pos].append(seg_node)
            except KeyError:
                self.pos_map[seg_node.pos] = [seg_node]

        # For the segments with duplicate ordinals, adjust the path to be unique
        for ord1 in sorted(self.pos_map):
            if len(self.pos_map[ord1]) > 1:
                for seg_node in [n for n in self.pos_map[ord1] if n.is_segment()]:
                    id_elem = seg_node.guess_unique_key_id_element()
                    if id_elem is not None:
                        seg_node.path = seg_node.path + "[" + id_elem.valid_codes[0] + "]"

    def debug_print(self) -> None:
        sys.stdout.write(self.__repr__())
        for ord1 in sorted(self.pos_map):
            for node in self.pos_map[ord1]:
                node.debug_print()

    def __len__(self) -> int:
        i = 0
        for ord1 in sorted(self.pos_map):
            i += len(self.pos_map[ord1])
        return i

    def __repr__(self) -> str:
        """
        :rtype: string
        """
        out = ""
        if self.id:
            out += "LOOP %s" % (self.id)
        if self.name:
            out += '  "%s"' % (self.name)
        if self.usage:
            out += "  usage: %s" % (self.usage)
        if self.pos:
            out += "  pos: %s" % (self.pos)
        if self.repeat:
            out += "  repeat: %s" % (self.repeat)
        out += "\n"
        return out

    def get_max_repeat(self) -> int:
        if self.repeat is None:
            return MAXINT
        if self.repeat == "&gt;1" or self.repeat == ">1":
            return MAXINT
        return int(self.repeat)

    def get_parent(self) -> Any:
        return self.parent

    def get_first_node(self) -> Any:
        pos_keys = sorted(self.pos_map)
        if len(pos_keys) > 0:
            return self.pos_map[pos_keys[0]][0]
        else:
            return None

    def get_first_seg(self) -> Any:
        first = self.get_first_node()
        if first.is_segment():
            return first
        else:
            return None

    def childIterator(self) -> Iterator[Any]:
        for ord1 in sorted(self.pos_map):
            for child in self.pos_map[ord1]:
                yield child

    def getnodebypath(self, spath: str) -> Any:
        """
        :param spath: remaining path to match
        :type spath: string
        :return: matching node, or None is no match
        """
        pathl = spath.split("/")
        if len(pathl) == 0:
            return None
        for ord1 in sorted(self.pos_map):
            for child in self.pos_map[ord1]:
                if child.is_loop():
                    if child.id.upper() == pathl[0].upper():
                        if len(pathl) == 1:
                            return child
                        else:
                            return child.getnodebypath("/".join(pathl[1:]))
                elif child.is_segment() and len(pathl) == 1:
                    if pathl[0].find("[") == -1:  # No id to match
                        if pathl[0] == child.id:
                            return child
                    else:
                        seg_id = pathl[0][0 : pathl[0].find("[")]
                        id_val = pathl[0][pathl[0].find("[") + 1 : pathl[0].find("]")]
                        if seg_id == child.id:
                            possible = child.get_unique_key_id_element(id_val)
                            if possible is not None:
                                return child
        raise EngineError('getnodebypath failed. Path "%s" not found' % spath)

    def getnodebypath2(self, path_str: str) -> Any:
        """
        Try x12 path

        :param path_str: remaining path to match
        :type path_str: string
        :return: matching node, or None is no match
        """
        x12path = X12Path(path_str)
        if x12path.empty():
            return None
        for ord1 in sorted(self.pos_map):
            for child in self.pos_map[ord1]:
                if child.is_loop() and len(x12path.loop_list) > 0:
                    if child.id.upper() == x12path.loop_list[0].upper():
                        if len(x12path.loop_list) == 1 and x12path.seg_id is None:
                            return child
                        else:
                            del x12path.loop_list[0]
                            return child.getnodebypath2(x12path.format())
                elif (
                    child.is_segment()
                    and len(x12path.loop_list) == 0
                    and x12path.seg_id is not None
                ):
                    if x12path.id_val is None:
                        if x12path.seg_id == child.id:
                            return child.getnodebypath2(x12path.format())
                    else:
                        seg_id = x12path.seg_id
                        id_val = x12path.id_val
                        if seg_id == child.id:
                            possible = child.get_unique_key_id_element(id_val)
                            if possible is not None:
                                return child.getnodebypath2(x12path.format())
        raise EngineError('getnodebypath2 failed. Path "%s" not found' % path_str)

    def get_child_count(self) -> int:
        return self.__len__()

    def get_child_node_by_idx(self, idx: int) -> Any:
        """
        :param idx: zero based
        """
        raise EngineError("loop_if.get_child_node_by_idx is not a valid call for a loop_if")

    def get_seg_count(self) -> int:
        """
        :return: Number of child segments
        :rtype: integer
        """
        i = 0
        for ord1 in sorted(self.pos_map):
            for child in self.pos_map[ord1]:
                if child.is_segment():
                    i += 1
        return i

    def is_loop(self) -> bool:
        """
        :rtype: boolean
        """
        return True

    def is_match(self, seg_data: pyx12.segment.Segment) -> bool:
        """
        :type seg_data: L{segment<segment.Segment>}
        :return: Is the segment a match to this loop?
        :rtype: boolean
        """
        pos_keys = sorted(self.pos_map)
        child = self.pos_map[pos_keys[0]][0]
        if child.is_loop():
            return bool(child.is_match(seg_data))
        elif child.is_segment():
            if child.is_match(seg_data):
                return True
            else:
                return False  # seg does not match the first segment in loop, so not valid
        else:
            return False

    def get_child_seg_node(self, seg_data: pyx12.segment.Segment) -> Any:
        """
        Return the child segment matching the segment data
        """
        for child in self.childIterator():
            if child.is_segment() and child.is_match(seg_data):
                return child
        return None

    def get_child_loop_node(self, seg_data: pyx12.segment.Segment) -> Any:
        """
        Return the child segment matching the segment data
        """
        for child in self.childIterator():
            if child.is_loop() and child.is_match(seg_data):
                return child
        return None

    def get_cur_count(self) -> int:
        """
        :return: current count
        :rtype: int
        """
        raise DeprecationWarning("Moved to nodeCounter")

    def incr_cur_count(self) -> None:
        raise DeprecationWarning("Moved to nodeCounter")

    def reset_child_count(self) -> None:
        """
        Set cur_count of child nodes to zero
        """
        raise DeprecationWarning("Moved to nodeCounter")

    def reset_cur_count(self) -> None:
        """
        Set cur_count of node and child nodes to zero
        """
        raise DeprecationWarning("Moved to nodeCounter")

    def set_cur_count(self, ct: int) -> None:
        raise DeprecationWarning("Moved to nodeCounter")

    def get_counts_list(self, ct_list: list[tuple[str, int]]) -> bool:
        """
        Build a list of (path, ct) of the current node and parents
        Gets the node counts to apply to another map
        :param ct_list: List to append to
        :type ct_list: list[(string, int)]
        """
        raise DeprecationWarning("Moved to nodeCounter")

    def loop_segment_iterator(self) -> Iterator[Any]:
        yield self
        for ord1 in sorted(self.pos_map):
            for child in self.pos_map[ord1]:
                if child.is_loop() or child.is_segment():
                    for c in child.loop_segment_iterator():
                        yield c
