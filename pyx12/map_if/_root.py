######################################################################
# Copyright (c)
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
"""
Map root - the X12N IG transaction-level interface.
"""

from __future__ import annotations

import os.path
import sys
from collections.abc import Iterator
from xml.etree.ElementTree import Element

from .. import codes, dataele
from ..errors import EngineError
from ..params import ParamsBase
from ..path import X12Path
from ._base import x12_node
from ._element import element_if
from ._loop import loop_if
from ._segment import segment_if


############################################################
class map_if(x12_node):
    """
    Map file interface
    """

    pos_map: dict[int, list[x12_node]]
    cur_path: str
    param: ParamsBase
    ext_codes: codes.ExternalCodes
    data_elements: dataele.DataElements
    base_name: str
    icvn: str | None

    def __init__(self, eroot: Element, param: ParamsBase, base_path: str | None = None) -> None:
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
            isa = self.getnodebypath(ipath)
            assert isinstance(isa, segment_if)
            node = isa.children[11]
            assert isinstance(node, element_if)
            return node.valid_codes[0]
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

    def get_first_node(self) -> x12_node | None:
        pos_keys = sorted(self.pos_map)
        if len(pos_keys) > 0:
            return self.pos_map[pos_keys[0]][0]
        else:
            return None

    def get_first_seg(self) -> segment_if | None:
        first = self.get_first_node()
        if isinstance(first, segment_if):
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

    def get_child_node_by_idx(self, idx: int) -> x12_node | None:
        """
        :param idx: zero based
        """
        raise EngineError("map_if.get_child_node_by_idx is not a valid call")

    def getnodebypath(self, spath: str) -> x12_node | None:
        """
        :param spath: Path string; /1000/2000/2000A/NM102-3
        :type spath: string
        """
        pathl = spath.split("/")[1:]
        if len(pathl) == 0:
            return None
        for ord1 in sorted(self.pos_map):
            for child in self.pos_map[ord1]:
                assert child.id is not None
                if child.id.lower() == pathl[0].lower():
                    if len(pathl) == 1:
                        return child
                    else:
                        return child.getnodebypath("/".join(pathl[1:]))
        raise EngineError('getnodebypath failed. Path "%s" not found' % spath)

    def getnodebypath2(self, path_str: str) -> x12_node | None:
        """
        :param path: Path string; /1000/2000/2000A/NM102-3
        :type path: string
        """
        x12path = X12Path(path_str)
        if x12path.empty():
            return None
        for ord1 in sorted(self.pos_map):
            for child in self.pos_map[ord1]:
                assert child.id is not None
                if child.id.upper() == x12path.loop_list[0]:
                    if len(x12path.loop_list) == 1:
                        return child
                    else:
                        del x12path.loop_list[0]
                        if isinstance(child, loop_if):
                            return child.getnodebypath2(x12path.format())
                        return None
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

    def loop_segment_iterator(self) -> Iterator[x12_node]:
        yield self
        for ord1 in sorted(self.pos_map):
            for child in self.pos_map[ord1]:
                if isinstance(child, loop_if):
                    yield from child.loop_segment_iterator()
                elif isinstance(child, segment_if):
                    yield child
