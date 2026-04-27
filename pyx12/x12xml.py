######################################################################
# Copyright
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Create an XML rendering of the X12 document
"""
from __future__ import annotations
from typing import Any, Literal, TextIO

import os.path

# Intrapackage imports
import pyx12.segment
from .errors import EngineError
from .xmlwriter import XMLWriter
from .map_walker import pop_to_parent_loop


class x12xml:

    writer: XMLWriter
    last_path: list[str]

    def __init__(self, fd: TextIO, type: str, dtd_urn: str | None) -> None:
        self.writer = XMLWriter(fd)
        if dtd_urn:
            self.writer.doctype( \
                type, \
                "-//J Holland//DTD XML X12 Document Conversion1.0//EN//XML", \
                dtd_urn)
        self.writer.push(type)
        self.last_path = []

    def close(self) -> None:
        """
        Pop any XML elements still on the writer's stack. Idempotent.
        """
        while len(self.writer) > 0:
            self.writer.pop()

    def __enter__(self) -> x12xml:
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> Literal[False]:
        self.close()
        return False

    def seg(self, seg_node: Any, seg_data: pyx12.segment.Segment) -> None:
        """
        Generate XML for the segment data and matching map node

        :param seg_node: Map Node
        :type seg_node: L{node<map_if.x12_node>}
        :param seg_data: Segment object
        :type seg_data: L{segment<segment.Segment>}
        """
        if not seg_node.is_segment():
            raise EngineError('Node must be a segment')
        parent = pop_to_parent_loop(seg_node)  # Get enclosing loop
        # check path for new loops to be added
        cur_path = self._path_list(parent.get_path())
        if self.last_path != cur_path:
            last_path = self.last_path
            match_idx = self._get_path_match_idx(last_path, cur_path)
            root_path = self._path_list(os.path.commonprefix(
                ['/'.join(cur_path), '/'.join(last_path)]))
            if seg_node.is_first_seg_in_loop() and root_path == cur_path:
                match_idx -= 1
            for i in range(len(last_path) - 1, match_idx - 1, -1):
                self.writer.pop()
            for i in range(match_idx, len(cur_path)):
                (xname, attrib) = self._get_loop_info(cur_path[i])
                self.writer.push(xname, attrib)
        seg_node_id = self._get_node_id(seg_node, parent, seg_data)
        (xname, attrib) = self._get_seg_info(seg_node_id)
        self.writer.push(xname, attrib)
        for i in range(len(seg_data)):
            child_node = seg_node.get_child_node_by_idx(i)
            _ele = seg_data.get('{idx:02d}'.format(idx=i + 1))
            assert _ele is not None  # within range(len(seg_data))
            if child_node.usage == 'N' or _ele.is_empty():
                pass  # Do not try to ouput for invalid or empty elements
            elif child_node.is_composite():
                (xname, attrib) = self._get_comp_info(seg_node_id)
                self.writer.push(xname, attrib)
                comp_data = seg_data.get('{idx:02d}'.format(idx=i + 1))
                assert isinstance(comp_data, pyx12.segment.Composite)
                for j in range(len(comp_data)):
                    subele_node = child_node.get_child_node_by_idx(j)
                    (xname, attrib) = self._get_subele_info(subele_node.id)
                    self.writer.elem(xname, comp_data[j].get_value(), attrib)
                self.writer.pop()  # end composite
            elif child_node.is_element():
                ele_val = seg_data.get_value('{idx:02d}'.format(idx=i + 1))
                if ele_val == '' or ele_val is None:
                    pass
                    #self.writer.empty(u"ele", attrs={u'id': child_node.id})
                else:
                    (xname, attrib) = self._get_ele_info(child_node.id)
                    self.writer.elem(xname, ele_val, attrib)
            else:
                raise EngineError('Node must be a either an element or a composite')
        self.writer.pop()  # end segment
        self.last_path = cur_path

    def seg_context(
        self,
        seg_node: Any,
        seg_data: pyx12.segment.Segment,
        pop_loops: list[Any],
        push_loops: list[Any],
    ) -> None:
        """
        Generate XML for the segment data and matching map node

        :param seg_node: Map Node
        :type seg_node: L{node<map_if.x12_node>}
        :param seg_data: Segment object
        :type seg_data: L{segment<segment.Segment>}
        """
        if not seg_node.is_segment():
            raise EngineError('Node must be a segment')
        parent = pop_to_parent_loop(seg_node)  # Get enclosing loop
        for loop in pop_loops:
            self.writer.pop()
        for loop in push_loops:
            (xname, attrib) = self._get_loop_info(loop.id)
            self.writer.push(xname, attrib)
        (xname, attrib) = self._get_seg_info(seg_node.id)
        self.writer.push(xname, attrib)
        for i in range(len(seg_data)):
            child_node = seg_node.get_child_node_by_idx(i)
            _ele = seg_data.get('{idx:02d}'.format(idx=i + 1))
            assert _ele is not None  # within range(len(seg_data))
            if child_node.usage == 'N' or _ele.is_empty():
                pass  # Do not try to ouput for invalid or empty elements
            elif child_node.is_composite():
                (xname, attrib) = self._get_comp_info(seg_node.id)
                self.writer.push(xname, attrib)
                comp_data = seg_data.get('{idx:02d}'.format(idx=i + 1))
                assert isinstance(comp_data, pyx12.segment.Composite)
                for j in range(len(comp_data)):
                    subele_node = child_node.get_child_node_by_idx(j)
                    (xname, attrib) = self._get_subele_info(subele_node.id)
                    self.writer.elem(xname, comp_data[j].get_value(), attrib)
                self.writer.pop()  # end composite
            elif child_node.is_element():
                ele_val = seg_data.get_value('{idx:02d}'.format(idx=i + 1))
                if ele_val == '' or ele_val is None:
                    pass
                    #self.writer.empty(u"ele", attrs={u'id': child_node.id})
                else:
                    (xname, attrib) = self._get_ele_info(child_node.id)
                    self.writer.elem(xname, ele_val, attrib)
            else:
                raise EngineError('Node must be a either an element or a composite')
        self.writer.pop()  # end segment

    def _path_list(self, path_str: str) -> list[str]:
        """
        Get list of path nodes from path string
        :rtype: list
        """
        return [x for x in path_str.split('/') if x != '']

    def _get_path_match_idx(self, last_path: list[str], cur_path: list[str]) -> int:
        """
        Get the index of the last matching path nodes
        """
        match_idx = 0
        for i in range(min(len(cur_path), len(last_path))):
            if cur_path[i] != last_path[i]:
                break
            match_idx += 1
        return match_idx

    def _get_node_id(
        self,
        seg_node: Any,
        parent: Any = None,
        seg_data: pyx12.segment.Segment | None = None,
    ) -> str:
        """
        Base node id function
        """
        result: str = seg_node.id
        return result

    def _get_loop_info(self, loop_id: str) -> tuple[str, dict[str, str]]:
        """
        Base loop node value
        """
        loop_name = loop_id
        attrib: dict[str, str] = {}
        return (loop_name, attrib)

    def _get_seg_info(self, seg_id: str) -> tuple[str, dict[str, str]]:
        """
        Base segment node value
        """
        seg_name = seg_id
        attrib: dict[str, str] = {}
        return (seg_name, attrib)

    def _get_comp_info(self, comp_id: str) -> tuple[str, dict[str, str]]:
        """
        Base composite node value
        """
        comp_name = comp_id
        attrib: dict[str, str] = {}
        return (comp_name, attrib)

    def _get_ele_info(self, ele_id: str) -> tuple[str, dict[str, str]]:
        """
        Base element node value
        """
        name = ele_id
        attrib: dict[str, str] = {}
        return (name, attrib)

    def _get_subele_info(self, subele_id: str) -> tuple[str, dict[str, str]]:
        """
        Base sub-element node value
        """
        name = subele_id
        attrib: dict[str, str] = {}
        return (name, attrib)
