######################################################################
# Copyright (c)
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
"""
Interface to a X12N IG Map
"""

from __future__ import annotations

import logging
import os.path
import re
import sys
from collections.abc import Iterator
from importlib.resources import files as _res_files
from typing import IO, Any, cast
from xml.etree.ElementTree import Element

import defusedxml.ElementTree as et

# Intrapackage imports
import pyx12.segment

from . import codes, dataele, validation
from . import path as _path
from .dataele import _DataEle
from .errors import EngineError
from .path import X12Path
from .syntax import is_syntax_valid

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
############################################################
class map_if(x12_node):
    """
    Map file interface
    """

    pos_map: dict[int, list[Any]]
    cur_path: str
    param: Any
    ext_codes: codes.ExternalCodes
    data_elements: dataele.DataElements
    base_name: str
    icvn: str | None

    def __init__(self, eroot: Element, param: Any, base_path: str | None = None) -> None:
        """
        :param eroot: ElementTree root
        :param param: map of parameters
        """
        x12_node.__init__(self)
        self.children = None  # type: ignore[assignment]
        self.pos_map = {}
        self.cur_path = "/transaction"
        self.path = "/"
        # self.cur_iter_node = self
        self.param = param
        # global codes
        self.ext_codes = codes.ExternalCodes(base_path, param.get("exclude_external_codes"))
        self.data_elements = dataele.DataElements(base_path)

        self.id = eroot.get("xid")

        self.name = eroot.get("name") if eroot.get("name") else eroot.findtext("name")
        self.base_name = "transaction"
        for e in eroot.findall("loop"):
            loop_node = loop_if(self, self, e)
            try:
                self.pos_map[loop_node.pos].append(loop_node)
            except KeyError:
                self.pos_map[loop_node.pos] = [loop_node]
        for e in eroot.findall("segment"):
            seg_node = segment_if(self, self, e)
            try:
                self.pos_map[seg_node.pos].append(seg_node)
            except KeyError:
                self.pos_map[seg_node.pos] = [seg_node]
        self.icvn = self._get_icvn()

    def _get_icvn(self) -> str | None:
        """
        Get the Interchange version of this map
        Map must have a first ISA segment
        ISA12
        """
        ipath = "/ISA_LOOP/ISA"
        try:
            node = self.getnodebypath(ipath).children[11]
            return cast(str, node.valid_codes[0])
        except Exception:
            return None

    def debug_print(self) -> None:
        sys.stdout.write(self.__repr__())
        for ord1 in sorted(self.pos_map):
            for node in self.pos_map[ord1]:
                node.debug_print()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, map_if):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return (self.id or "").__hash__()

    def __len__(self) -> int:
        i = 0
        for ord1 in sorted(self.pos_map):
            i += len(self.pos_map[ord1])
        return i

    def get_child_count(self) -> int:
        return self.__len__()

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

    def __repr__(self) -> str:
        """
        :rtype: string
        """
        return "%s\n" % (self.id)

    def _path_parent(self) -> str:
        """
        :rtype: string
        """
        return os.path.basename(os.path.dirname(self.cur_path))

    def get_path(self) -> str:
        """
        :rtype: string
        """
        return self.path

    def get_child_node_by_idx(self, idx: int) -> Any:
        """
        :param idx: zero based
        """
        raise EngineError("map_if.get_child_node_by_idx is not a valid call")

    def getnodebypath(self, spath: str) -> Any:
        """
        :param spath: Path string; /1000/2000/2000A/NM102-3
        :type spath: string
        """
        pathl = spath.split("/")[1:]
        if len(pathl) == 0:
            return None
        # logger.debug('%s %s %s' % (self.base_name, self.id, pathl[1]))
        for ord1 in sorted(self.pos_map):
            for child in self.pos_map[ord1]:
                if child.id.lower() == pathl[0].lower():
                    if len(pathl) == 1:
                        return child
                    else:
                        return child.getnodebypath("/".join(pathl[1:]))
        raise EngineError('getnodebypath failed. Path "%s" not found' % spath)

    def getnodebypath2(self, path_str: str) -> Any:
        """
        :param path: Path string; /1000/2000/2000A/NM102-3
        :type path: string
        """
        x12path = X12Path(path_str)
        if x12path.empty():
            return None
        for ord1 in sorted(self.pos_map):
            for child in self.pos_map[ord1]:
                if child.id.upper() == x12path.loop_list[0]:
                    if len(x12path.loop_list) == 1:
                        return child
                    else:
                        del x12path.loop_list[0]
                        return child.getnodebypath2(x12path.format())
        raise EngineError('getnodebypath2 failed. Path "%s" not found' % path_str)

    def is_map_root(self) -> bool:
        """
        :rtype: boolean
        """
        return True

    def reset_child_count(self) -> None:
        """
        Set cur_count of child nodes to zero
        """
        raise DeprecationWarning("Moved to nodeCounter")

    def reset_cur_count(self) -> None:
        """
        Set cur_count of child nodes to zero
        """
        raise DeprecationWarning("Moved to nodeCounter")

    def __iter__(self) -> map_if:
        return self

    def loop_segment_iterator(self) -> Iterator[Any]:
        yield self
        for ord1 in sorted(self.pos_map):
            for child in self.pos_map[ord1]:
                if child.is_loop() or child.is_segment():
                    for c in child.loop_segment_iterator():
                        yield c


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


class segment_if(x12_node):
    """
    Segment Interface
    """

    root: Any
    base_name: str
    _cur_count: int
    syntax: list[list[Any]]
    type: str | None
    usage: str | None
    pos: int
    max_use: str | None
    repeat: str | None
    end_tag: str | None

    def __init__(self, root: Any, parent: Any, elem: Element) -> None:
        """
        :param parent: parent node
        """

        x12_node.__init__(self)
        self.root = root
        self.parent = parent
        self.children = []
        self.base_name = "segment"
        self._cur_count = 0
        self.syntax = []

        self.id = elem.get("xid")
        self.path = self.id or ""
        self.type = elem.get("type")

        self.name = elem.get("name") if elem.get("name") else elem.findtext("name")
        self.usage = elem.get("usage") if elem.get("usage") else elem.findtext("usage")
        self.pos = int(_required_attr(elem, "pos"))
        self.max_use = elem.get("max_use") if elem.get("max_use") else elem.findtext("max_use")
        self.repeat = elem.get("repeat") if elem.get("repeat") else elem.findtext("repeat")

        self.end_tag = elem.get("end_tag") if elem.get("end_tag") else elem.findtext("end_tag")

        for s in elem.findall("syntax"):
            syn_list = self._split_syntax(s.text)
            if syn_list is not None:
                self.syntax.append(syn_list)

        children_map: dict[int, Element] = {}
        for e in elem.findall("element"):
            seq = int(_required_attr(e, "seq"))
            children_map[seq] = e

        for e in elem.findall("composite"):
            seq = int(_required_attr(e, "seq"))
            children_map[seq] = e

        for seq in sorted(children_map.keys()):
            if children_map[seq].tag == "element":
                self.children.append(element_if(self.root, self, children_map[seq]))
            elif children_map[seq].tag == "composite":
                self.children.append(composite_if(self.root, self, children_map[seq]))

    def debug_print(self) -> None:
        sys.stdout.write(self.__repr__())
        for node in self.children:
            node.debug_print()

    def __repr__(self) -> str:
        """
        :rtype: string
        """
        out = '%s "%s"' % (self.id, self.name)
        if self.usage:
            out += "  usage: %s" % (self.usage)
        if self.pos:
            out += "  pos: %i" % (self.pos)
        if self.max_use:
            out += "  max_use: %s" % (self.max_use)
        out += "\n"
        return out

    def get_child_node_by_idx(self, idx: int) -> Any:
        """
        :param idx: zero based
        """
        if idx >= len(self.children):
            return None
        else:
            m = [c for c in self.children if c.seq == idx + 1]
            if len(m) == 1:
                return m[0]
            else:
                raise EngineError("idx %i not found in %s" % (idx, self.id))

    def get_child_node_by_ordinal(self, ord: int) -> Any:
        """
        Get a child element or composite by the X12 ordinal
        :param ord: one based element/composite index.  Corresponds to the map <seq> element
        :type ord: int
        """
        return self.get_child_node_by_idx(ord - 1)

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
        if x12path.ele_idx is None:
            return self  # matched segment only
        ele = self.get_child_node_by_ordinal(x12path.ele_idx)
        if x12path.subele_idx is None:
            return ele
        return ele.get_child_node_by_ordinal(x12path.subele_idx)

    def get_max_repeat(self) -> int:
        if self.max_use is None or self.max_use == ">1":
            return MAXINT
        return int(self.max_use)

    def get_parent(self) -> Any:
        """
        :return: ref to parent class instance
        :rtype: pyx12.x12_node
        """
        return self.parent

    def is_first_seg_in_loop(self) -> bool:
        """
        :rtype: boolean
        """
        if self is self.get_parent().get_first_seg():
            return True
        else:
            return False

    def is_match(self, seg: pyx12.segment.Segment) -> bool:
        """
        Is data segment given a match to this segment node?
        :param seg: data segment instance
        :return: boolean
        :rtype: boolean
        """
        if seg.get_seg_id() != self.id:
            return False
        key = self._resolve_unique_key_field(seg.get_seg_id(), with_qual=False)
        if key is None:
            return True
        child, ele_idx, subele_idx = key
        path = f"{ele_idx:02d}-{subele_idx}" if subele_idx else f"{ele_idx:02d}"
        return seg.get_value(path) in child.valid_codes

    def is_match_qual(
        self,
        seg_data: pyx12.segment.Segment,
        seg_id: str | None,
        qual_code: str | None,
    ) -> tuple[bool, str | None, int | None, int | None]:
        """
        Is segment id and qualifier a match to this segment node and to this particular segment data?
        :param seg_data: data segment instance
        :type seg_data: L{segment<segment.Segment>}
        :param seg_id: data segment ID
        :param qual_code: an ID qualifier code
        :return: (True if a match, qual_code, element_index, subelement_index)
        :rtype: tuple(boolean, string, int, int)
        """
        if seg_id != self.id:
            return (False, None, None, None)
        if qual_code is None:
            return (True, None, None, None)
        key = self._resolve_unique_key_field(seg_id, with_qual=True)
        if key is None:
            return (True, None, None, None)
        child, ele_idx, subele_idx = key
        path = f"{ele_idx:02d}-{subele_idx}" if subele_idx else f"{ele_idx:02d}"
        if qual_code in child.valid_codes and seg_data.get_value(path) == qual_code:
            return (True, qual_code, ele_idx, subele_idx)
        return (False, None, None, None)

    def _resolve_unique_key_field(
        self, seg_id: str | None, *, with_qual: bool
    ) -> tuple[Any, int, int | None] | None:
        """
        Locate the child node carrying this segment's qualifier (if any).

        Returns ``(validating_child, ele_idx, subele_idx_or_None)`` describing
        where to read the qualifier value from a data segment, or ``None`` if
        the segment has no recognizable qualifier field.

        ``with_qual=False`` (used by ``is_match``) accepts the AN-typed CTX
        composite as a valid qualifier carrier; ``with_qual=True`` (used by
        ``is_match_qual``) only honors ID-typed qualifier fields.
        """
        # Element at position 01 — the common case
        if (
            self.children[0].is_element()
            and self.children[0].get_data_type() == "ID"
            and self.children[0].usage == "R"
            and len(self.children[0].valid_codes) > 0
        ):
            return (self.children[0], 1, None)
        # ENT-segment carries its qualifier at element 02 (820 special case)
        if (
            seg_id == "ENT"
            and self.children[1].is_element()
            and self.children[1].get_data_type() == "ID"
            and len(self.children[1].valid_codes) > 0
        ):
            return (self.children[1], 2, None)
        # CTX-segment can have an AN-typed composite at 01-1 (999 special case);
        # is_match_qual ignores this branch.
        if (
            not with_qual
            and seg_id == "CTX"
            and self.children[0].is_composite()
            and self.children[0].children[0].get_data_type() == "AN"
            and len(self.children[0].children[0].valid_codes) > 0
        ):
            return (self.children[0].children[0], 1, 1)
        # General ID-typed composite at 01-1
        if (
            self.children[0].is_composite()
            and self.children[0].children[0].get_data_type() == "ID"
            and len(self.children[0].children[0].valid_codes) > 0
        ):
            return (self.children[0].children[0], 1, 1)
        # HL-segment carries its qualifier at element 03
        if (
            seg_id == "HL"
            and self.children[2].is_element()
            and len(self.children[2].valid_codes) > 0
        ):
            return (self.children[2], 3, None)
        return None

    def guess_unique_key_id_element(self) -> Any:
        """
        Some segments, like REF, DTP, and DTP are duplicated.  They are matched using the value of an ID element.
        Which element to use varies.  This function tries to find a good candidate.
        """
        if (
            self.children[0].is_element()
            and self.children[0].get_data_type() == "ID"
            and len(self.children[0].valid_codes) > 0
        ):
            return self.children[0]
        # Special Case for 820
        elif (
            self.id == "ENT"
            and self.children[1].is_element()
            and self.children[1].get_data_type() == "ID"
            and len(self.children[1].valid_codes) > 0
        ):
            return self.children[1]
        elif (
            self.children[0].is_composite()
            and self.children[0].children[0].get_data_type() == "ID"
            and len(self.children[0].children[0].valid_codes) > 0
        ):
            return self.children[0].children[0]
        elif (
            self.id == "HL"
            and self.children[2].is_element()
            and len(self.children[2].valid_codes) > 0
        ):
            return self.children[2]
        return None

    def get_unique_key_id_element(self, id_val: str) -> Any:
        """
        Some segments, like REF, DTP, and DTP are duplicated.  They are matched using the value of an ID element.
        Which element to use varies.  This function tries to find a good candidate, using a key value
        """

        if (
            self.children[0].is_element()
            and self.children[0].get_data_type() == "ID"
            and len(self.children[0].valid_codes) > 0
            and id_val in self.children[0].valid_codes
        ):
            return self.children[0]
        # Special Case for 820
        elif (
            self.id == "ENT"
            and self.children[1].is_element()
            and self.children[1].get_data_type() == "ID"
            and len(self.children[1].valid_codes) > 0
            and id_val in self.children[1].valid_codes
        ):
            return self.children[1]
        elif (
            self.children[0].is_composite()
            and self.children[0].children[0].get_data_type() == "ID"
            and len(self.children[0].children[0].valid_codes) > 0
            and id_val in self.children[0].children[0].valid_codes
        ):
            return self.children[0].children[0]
        elif (
            self.id == "HL"
            and self.children[2].is_element()
            and len(self.children[2].valid_codes) > 0
            and id_val in self.children[2].valid_codes
        ):
            return self.children[2]
        return None

    def is_segment(self) -> bool:
        """
        :rtype: boolean
        """
        return True

    def is_valid(self, seg_data: pyx12.segment.Segment, errh: Any) -> bool:
        """
        :param seg_data: data segment instance
        :type seg_data: L{segment<segment.Segment>}
        :param errh: instance of error_handler
        :rtype: boolean
        """
        valid = True
        child_count = self.get_child_count()
        if len(seg_data) > child_count:
            err_str = 'Too many elements in segment "%s" (%s). Has %i, should have %i' % (
                self.name,
                seg_data.get_seg_id(),
                len(seg_data),
                child_count,
            )
            ref_des = "%02i" % (child_count + 1)
            err_value = seg_data.get_value(ref_des)
            errh.ele_error("3", err_str, err_value, ref_des)
            valid = False

        dtype: list[str | None] = []
        type_list: list[str | None] = []
        for i in range(min(len(seg_data), child_count)):
            child_node = self.get_child_node_by_idx(i)
            if child_node.is_composite():
                # Validate composite
                ref_des = "%02i" % (i + 1)
                comp_data = seg_data.get(ref_des)
                subele_count = child_node.get_child_count()
                if seg_data.ele_len(ref_des) > subele_count and child_node.usage != "N":
                    subele_node = child_node.get_child_node_by_idx(subele_count + 1)
                    err_str = 'Too many sub-elements in composite "%s" (%s)' % (
                        subele_node.name,
                        subele_node.refdes,
                    )
                    err_value = seg_data.get_value(ref_des)
                    errh.ele_error("3", err_str, err_value, ref_des)
                valid &= child_node.is_valid(comp_data, errh)
            elif child_node.is_element():
                # Validate Element
                if (
                    i == 1
                    and seg_data.get_seg_id() == "DTP"
                    and seg_data.get_value("02") in ("RD8", "D8", "D6", "DT", "TM")
                ):
                    dtype = [seg_data.get_value("02")]
                if child_node.data_ele == "1250":
                    type_list.extend(child_node.valid_codes)
                ele_data = seg_data.get("%02i" % (i + 1))
                if i == 2 and seg_data.get_seg_id() == "DTP":
                    valid &= child_node.is_valid(ele_data, errh, dtype)
                elif child_node.data_ele == "1251" and len(type_list) > 0:
                    valid &= child_node.is_valid(ele_data, errh, type_list)
                else:
                    valid &= child_node.is_valid(ele_data, errh)

        for i in range(min(len(seg_data), child_count), child_count):
            # missing required elements?
            child_node = self.get_child_node_by_idx(i)
            valid &= child_node.is_valid(None, errh)

        for syn in self.syntax:
            (bResult, syn_err) = is_syntax_valid(seg_data, syn)
            if not bResult:
                syn_type = syn[0]
                if syn_type == "E":
                    errh.ele_error("10", syn_err, None, syn[1])
                else:
                    errh.ele_error("2", syn_err, None, syn[1])
                valid &= False

        return valid

    def _split_syntax(self, syntax: str | None) -> list[Any] | None:
        """
        Split a Syntax string into a list
        """
        if syntax is None or syntax[0] not in ["P", "R", "C", "L", "E"]:
            return None
        syn: list[Any] = [syntax[0]]
        for i in range(len(syntax[1:]) // 2):
            syn.append(int(syntax[i * 2 + 1 : i * 2 + 3]))
        return syn

    def get_cur_count(self) -> int:
        """
        :return: current count
        :rtype: int
        """
        raise DeprecationWarning("Moved to nodeCounter")

    def incr_cur_count(self) -> None:
        raise DeprecationWarning("Moved to nodeCounter")

    def reset_cur_count(self) -> None:
        """
        Set cur_count of node to zero
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


############################################################
# Element Interface
############################################################
class element_if(x12_node):
    """
    Element Interface
    """

    root: Any
    base_name: str
    valid_codes: list[str | None]
    external_codes: str | None
    rec: re.Pattern[str] | None
    refdes: str | None
    data_ele: str | None
    _data_ele: _DataEle | None
    usage: str | None
    seq: int
    max_use: str | None
    res: str | None

    def __init__(self, root: Any, parent: Any, elem: Element) -> None:
        """
        :param parent: parent node
        """
        x12_node.__init__(self)
        self.children = []
        self.root = root
        self.parent = parent
        self.base_name = "element"
        self.valid_codes = []
        self.external_codes = None
        self.rec = None

        self.id = elem.get("xid")
        self.refdes = self.id
        self.data_ele = elem.get("data_ele") if elem.get("data_ele") else elem.findtext("data_ele")
        # Eagerly cache the data element definition; a map that references an
        # undefined data_ele fails at validation time, matching legacy behavior.
        try:
            self._data_ele = (
                self.root.data_elements.get_by_elem_num(self.data_ele) if self.data_ele else None
            )
        except EngineError:
            self._data_ele = None
        self.usage = elem.get("usage") if elem.get("usage") else elem.findtext("usage")
        self.name = elem.get("name") if elem.get("name") else elem.findtext("name")
        self.seq = int(_required_attr(elem, "seq"))
        self.path = elem.get("seq") if elem.get("seq") else (elem.findtext("seq") or "")  # type: ignore[assignment]
        self.max_use = elem.get("max_use") if elem.get("max_use") else elem.findtext("max_use")
        self.res = elem.findtext("regex")
        try:
            if self.res is not None and self.res != "":
                self.rec = re.compile(self.res, re.S)
        except Exception:
            raise EngineError('Element regex "%s" failed to compile' % (self.res))

        v = elem.find("valid_codes")
        if v is not None:
            self.external_codes = v.get("external")
            for c in v.findall("code"):
                self.valid_codes.append(c.text)

    def debug_print(self) -> None:
        sys.stdout.write(self.__repr__())
        for node in self.children:
            node.debug_print()

    def __repr__(self) -> str:
        """
        :rtype: string
        """
        data_ele = self._resolve_data_ele()
        out = '%s "%s"' % (self.refdes, self.name)
        if self.data_ele:
            out += "  data_ele: %s" % (self.data_ele)
        if self.usage:
            out += "  usage: %s" % (self.usage)
        if self.seq:
            out += "  seq: %i" % (self.seq)
        out += "  %s(%i, %i)" % (data_ele["data_type"], data_ele["min_len"], data_ele["max_len"])
        if self.external_codes:
            out += "   external codes: %s" % (self.external_codes)
        out += "\n"
        return out

    def _resolve_data_ele(self) -> _DataEle:
        if self._data_ele is not None:
            return self._data_ele
        return cast(_DataEle, self.root.data_elements.get_by_elem_num(self.data_ele))

    def _error(self, errh: Any, err_str: str, err_cde: str, elem_val: str | None) -> None:
        """
        Forward the error to an error_handler
        """
        errh.ele_error(err_cde, err_str, elem_val, self.refdes)

    def _valid_code(self, code: str | None) -> bool:
        """
        Verify the x12 element value is in the given list of valid codes
        :return: True if found, else False
        :rtype: boolean
        """
        if code in self.valid_codes:
            return True
        return False

    def get_parent(self) -> Any:
        """
        :return: ref to parent class instance
        """
        return self.parent

    def is_match(self) -> bool:
        """
        :return:
        :rtype: boolean
        """
        # match also by ID
        raise NotImplementedError("Override in sub-class")

    def is_valid(self, elem: Any, errh: Any, type_list: list[str | None] | None = None) -> bool:
        """
        Is this a valid element?

        :param elem: element instance
        :type elem: L{element<segment.Element>}
        :param errh: instance of error_handler
        :param type_list: Optional data/time type list
        :type type_list: list[string]
        :return: True if valid
        :rtype: boolean
        """
        if type_list is None:
            type_list = []
        errh.add_ele(self)

        if elem and elem.is_composite():
            err_str = 'Data element "%s" (%s) is an invalid composite' % (self.name, self.refdes)
            self._error(errh, err_str, "6", elem.__repr__())
            return False
        if elem is None or elem.get_value() == "":
            return self._validate_when_empty(errh)
        if self.usage == "N" and elem.get_value() != "":
            err_str = 'Data element "%s" (%s) is marked as Not Used' % (self.name, self.refdes)
            self._error(errh, err_str, "10", None)
            return False

        elem_val = elem.get_value()
        valid = self._validate_length(elem_val, errh)
        if not self._validate_control_chars(elem_val, errh):
            return False  # control char errors trump later checks
        valid &= self._validate_trailing_spaces(elem_val, errh)
        valid &= self._is_valid_code(elem_val, errh)
        valid &= self._validate_data_type(elem_val, errh)
        if type_list:
            valid &= self._validate_type_list(elem_val, type_list, errh)
        valid &= self._validate_regex(elem_val, errh)
        return bool(valid)

    def _validate_when_empty(self, errh: Any) -> bool:
        if self.usage in ("N", "S"):
            return True
        if self.usage == "R" and (
            self.seq != 1 or not self.parent.is_composite() or self.parent.usage == "R"
        ):
            err_str = 'Mandatory data element "%s" (%s) is missing' % (self.name, self.refdes)
            self._error(errh, err_str, "1", None)
            return False
        return True

    def _validate_length(self, elem_val: str, errh: Any) -> bool:
        data_ele = self._resolve_data_ele()
        data_type = data_ele["data_type"]
        min_len = data_ele["min_len"]
        max_len = data_ele["max_len"]
        # Numeric types ignore "-" and "." for length purposes.
        if data_type is not None and (data_type == "R" or data_type[0] == "N"):
            measured = elem_val.replace("-", "").replace(".", "")
        else:
            measured = elem_val
        elem_len = len(measured)
        valid = True
        if elem_len < min_len:
            err_str = 'Data element "%s" (%s) is too short: len("%s") = %i < %i (min_len)' % (
                self.name,
                self.refdes,
                elem_val,
                elem_len,
                min_len,
            )
            self._error(errh, err_str, "4", elem_val)
            valid = False
        if elem_len > max_len:
            err_str = 'Data element "%s" (%s) is too long: len("%s") = %i > %i (max_len)' % (
                self.name,
                self.refdes,
                elem_val,
                elem_len,
                max_len,
            )
            self._error(errh, err_str, "5", elem_val)
            valid = False
        return valid

    def _validate_control_chars(self, elem_val: str, errh: Any) -> bool:
        res, bad_string = validation.contains_control_character(elem_val)
        if not res:
            return True
        err_str = 'Data element "%s" (%s), contains an invalid control character(%s)' % (
            self.name,
            self.refdes,
            bad_string,
        )
        self._error(errh, err_str, "6", bad_string)
        return False

    def _validate_trailing_spaces(self, elem_val: str, errh: Any) -> bool:
        data_ele = self._resolve_data_ele()
        if data_ele["data_type"] not in ("AN", "ID") or elem_val[-1] != " ":
            return True
        if len(elem_val.rstrip()) < data_ele["min_len"]:
            return True
        err_str = 'Data element "%s" (%s) has unnecessary trailing spaces. (%s)' % (
            self.name,
            self.refdes,
            elem_val,
        )
        self._error(errh, err_str, "6", elem_val)
        return False

    def _validate_data_type(self, elem_val: str, errh: Any) -> bool:
        data_type = self._resolve_data_ele()["data_type"]
        if validation.IsValidDataType(
            elem_val, cast(str, data_type), self.root.param.get("charset"), self.root.icvn
        ):
            return True
        if data_type in ("RD8", "DT", "D8", "D6"):
            err_str = 'Data element "%s" (%s) contains an invalid date (%s)' % (
                self.name,
                self.refdes,
                elem_val,
            )
            self._error(errh, err_str, "8", elem_val)
        elif data_type == "TM":
            err_str = 'Data element "%s" (%s) contains an invalid time (%s)' % (
                self.name,
                self.refdes,
                elem_val,
            )
            self._error(errh, err_str, "9", elem_val)
        else:
            err_str = 'Data element "%s" (%s) is type %s, contains an invalid character(%s)' % (
                self.name,
                self.refdes,
                data_type,
                elem_val,
            )
            self._error(errh, err_str, "6", elem_val)
        return False

    def _validate_type_list(self, elem_val: str, type_list: list[str | None], errh: Any) -> bool:
        valid_type = False
        for dtype in type_list:
            if dtype is not None:
                valid_type |= validation.IsValidDataType(
                    elem_val, dtype, self.root.param.get("charset")
                )
        if valid_type:
            return True
        if "TM" in type_list:
            err_str = 'Data element "%s" (%s) contains an invalid time (%s)' % (
                self.name,
                self.refdes,
                elem_val,
            )
            self._error(errh, err_str, "9", elem_val)
        elif any(t in type_list for t in ("RD8", "DT", "D8", "D6")):
            err_str = 'Data element "%s" (%s) contains an invalid date (%s)' % (
                self.name,
                self.refdes,
                elem_val,
            )
            self._error(errh, err_str, "8", elem_val)
        return False

    def _validate_regex(self, elem_val: str, errh: Any) -> bool:
        if self.rec is None or self.rec.search(elem_val):
            return True
        err_str = 'Data element "%s" with a value of (%s)' % (self.name, elem_val)
        err_str += ' failed to match the regular expression "%s"' % (self.res)
        self._error(errh, err_str, "7", elem_val)
        return False

    def _is_valid_code(self, elem_val: str, errh: Any) -> bool:
        """
        :rtype: boolean
        """
        bValidCode = False
        if len(self.valid_codes) == 0 and self.external_codes is None:
            bValidCode = True
        if elem_val in self.valid_codes:
            bValidCode = True
        if self.external_codes is not None and self.root.ext_codes.isValid(
            self.external_codes, elem_val
        ):
            bValidCode = True
        if not bValidCode:
            err_str = "(%s) is not a valid code for %s (%s)" % (elem_val, self.name, self.refdes)
            self._error(errh, err_str, "7", elem_val)
            return False
        return True

    def get_data_type(self) -> str | None:
        return self._resolve_data_ele()["data_type"]

    @property
    def data_type(self) -> str | None:
        return self._resolve_data_ele()["data_type"]

    @property
    def min_len(self) -> int:
        return self._resolve_data_ele()["min_len"]

    @property
    def max_len(self) -> int:
        return self._resolve_data_ele()["max_len"]

    @property
    def data_element_name(self) -> str | None:
        return self._resolve_data_ele()["name"]

    def get_seg_count(self) -> None:
        """ """
        pass

    def is_element(self) -> bool:
        """
        :rtype: boolean
        """
        return True

    def get_path(self) -> str:
        """
        :return: path - XPath style
        :rtype: string
        """
        if self._fullpath:
            return self._fullpath
        # get enclosing loop
        parent_path = self.get_parent_segment().parent.get_path()
        # add the segment, element, and sub-element path
        self._fullpath = parent_path + "/" + (self.id or "")
        return self._fullpath

    def get_parent_segment(self) -> Any:
        # pop to enclosing loop
        p = self.parent
        while not p.is_segment():
            p = p.parent
        return p


############################################################
# Composite Interface
############################################################
class composite_if(x12_node):
    """
    Composite Node Interface
    """

    root: Any
    base_name: str
    refdes: str | None
    data_ele: str | None
    usage: str | None
    seq: int
    repeat: int

    def __init__(self, root: Any, parent: Any, elem: Element) -> None:
        """
        Get the values for this composite
        :param parent: parent node
        """
        x12_node.__init__(self)

        self.children = []
        self.root = root
        self.parent = parent
        self.path = ""
        self.base_name = "composite"

        self.id = elem.get("xid")
        self.refdes = elem.findtext("refdes") if elem.findtext("refdes") else self.id
        self.data_ele = elem.get("data_ele") if elem.get("data_ele") else elem.findtext("data_ele")
        self.usage = elem.get("usage") if elem.get("usage") else elem.findtext("usage")
        self.seq = int(_required_attr(elem, "seq"))
        if (r := elem.get("repeat")) is not None:
            self.repeat = int(r)
        elif (r := elem.findtext("repeat")) is not None:
            self.repeat = int(r)
        else:
            self.repeat = 1
        self.name = elem.get("name") if elem.get("name") else elem.findtext("name")

        for e in elem.findall("element"):
            self.children.append(element_if(self.root, self, e))

    def _error(self, errh: Any, err_str: str, err_cde: str, elem_val: str) -> None:
        """
        Forward the error to an error_handler
        """
        err_str2 = err_str.replace("\n", "").replace("\r", "")
        elem_val2 = elem_val.replace("\n", "").replace("\r", "")
        errh.ele_error(err_cde, err_str2, elem_val2, self.refdes)

    def debug_print(self) -> None:
        sys.stdout.write(self.__repr__())
        for node in self.children:
            node.debug_print()

    def __repr__(self) -> str:
        """
        :rtype: string
        """
        out = '%s "%s"' % (self.id, self.name)
        if self.usage:
            out += "  usage %s" % (self.usage)
        if self.seq:
            out += "  seq %i" % (self.seq)
        if self.refdes:
            out += "  refdes %s" % (self.refdes)
        out += "\n"
        return out

    def xml(self) -> None:
        """
        Sends an xml representation of the composite to stdout
        """
        sys.stdout.write("<composite>\n")
        for sub_elem in self.children:
            sub_elem.xml()
        sys.stdout.write("</composite>\n")

    def is_valid(self, comp_data: Any, errh: Any) -> bool:
        """
        Validates the composite
        :param comp_data: data composite instance, has multiple values
        :param errh: instance of error_handler
        :rtype: boolean
        """
        valid = True
        if (comp_data is None or comp_data.is_empty()) and self.usage in ("N", "S"):
            return True

        if self.usage == "R":
            good_flag = False
            if comp_data is not None:
                for sub_ele in comp_data:
                    if sub_ele is not None and len(sub_ele.get_value()) > 0:
                        good_flag = True
                        break
            if not good_flag:
                err_str = 'At least one component of composite "%s" (%s) is required' % (
                    self.name,
                    self.refdes,
                )
                errh.ele_error("2", err_str, None, self.refdes)
                return False

        if self.usage == "N" and not comp_data.is_empty():
            err_str = 'Composite "%s" (%s) is marked as Not Used' % (self.name, self.refdes)
            errh.ele_error("5", err_str, None, self.refdes)
            return False

        if len(comp_data) > self.get_child_count():
            err_str = 'Too many sub-elements in composite "%s" (%s)' % (self.name, self.refdes)
            errh.ele_error("3", err_str, None, self.refdes)
            valid = False
        for i in range(min(len(comp_data), self.get_child_count())):
            valid &= self.get_child_node_by_idx(i).is_valid(comp_data[i], errh)
        for i in range(min(len(comp_data), self.get_child_count()), self.get_child_count()):
            if i < self.get_child_count():
                # Check missing required elements
                valid &= self.get_child_node_by_idx(i).is_valid(None, errh)
        return valid

    def is_composite(self) -> bool:
        """
        :rtype: boolean
        """
        return True


def load_map_file(map_file: str, param: Any, map_path: str | None = None) -> map_if:
    """
    Create the map object from a file

    :param map_file: filename (basename) of the map xml file to load
    :type map_file: string
    :param map_path: Override directory containing map xml files.  If None,
        uses package resource folder
    :type map_path: string
    :rtype: pyx12.map_if
    """
    logger = logging.getLogger("pyx12")
    # Reject any path component in map_file to prevent traversal out of map_path
    if map_file != os.path.basename(map_file) or os.path.isabs(map_file):
        raise EngineError("Invalid map file name: {}".format(map_file))
    map_fd: IO[Any]
    if map_path is not None:
        logger.debug("Looking for map file '{}' in map_path '{}'".format(map_file, map_path))
        if not os.path.isdir(map_path):
            raise OSError(2, "Map path does not exist", map_path)
        full_path = os.path.join(map_path, map_file)
        if not os.path.isfile(full_path):
            raise OSError(
                2, "Pyx12 map file '{}' does not exist in map path".format(map_file), map_path
            )
        map_fd = open(full_path, encoding="utf-8")
    else:
        logger.debug("Looking for map file '{}' in package resources".format(map_file))
        map_fd = _res_files("pyx12").joinpath("map", map_file).open("rb")
    with map_fd:
        logger.debug("Create map from %s" % (map_file))
        parser = et.XMLParser(encoding="utf-8")
        etree = et.parse(map_fd, parser=parser)
        return map_if(etree.getroot(), param, map_path)
