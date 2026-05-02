#####################################################################
# Copyright
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
"""
Parse a ANSI X12 data file.

Maintain context state
Start saving context and segments
Interface to read and alter segments

TODO: Attach errors to returned dicts
"""

from __future__ import annotations

from collections.abc import Iterator
from types import TracebackType
from typing import Any, Literal, TextIO

# Intrapackage imports
import pyx12
import pyx12.segment

from . import error_handler, errors, map_if, map_index, path, x12file
from .map_walker import pop_to_parent_loop, walk_tree


class X12DataNode:
    """
    Capture the segment data and X12 definition for a loop subtree
    Alter relational data
    Iterate over contents
    """

    x12_map_node: Any
    type: str | None
    seg_data: pyx12.segment.Segment | None
    parent: X12DataNode | None
    children: list[X12DataNode]
    errors: list[Any]
    seg_count: int | None
    cur_line_number: int | None

    def __init__(
        self, x12_node: Any, seg_data: pyx12.segment.Segment | None, ntype: str = "seg"
    ) -> None:
        """ """
        self.x12_map_node = x12_node
        self.type = ntype
        self.seg_data = seg_data
        self.parent = None
        self.children = []
        self.errors = []
        self.seg_count = None
        self.cur_line_number = None

    # { Public Methods
    def delete(self) -> None:
        """
        Delete this node.  Mark type as deleted.
        """
        self.x12_map_node = None
        self.type = None
        self.seg_data = None
        self.parent = None
        self.children = []
        self.errors = []

    def iterate_segments(self) -> Iterator[dict[str, Any]]:
        """
        Iterate over this node and children, return any segments found
        """
        raise NotImplementedError("Override in sub-class")

    def iterate_loop_segments(self) -> Iterator[dict[str, Any]]:
        """
        Iterate over this node and children, return loop start and loop end
        and any segments found
        """
        raise NotImplementedError("Override in sub-class")

    def get_value(self, x12_path: str) -> str | None:
        """
        :return: the element value at the relative X12 path
        :rtype: string
        """
        raise NotImplementedError("Override in sub-class")

    def set_value(self, x12_path: str, val: str) -> None:
        """
        Set the value of simple element at the first found segment at the given path
        :param x12_path: An X12 path
        :type x12_path: string
        :param val: The new element value
        :type val: string
        """
        raise NotImplementedError("Override in sub-class")

    def exists(self, x12_path_str: str) -> bool:
        """
        Does at least one child at the x12 path exist?
        :param x12_path_str: Relative X12 path - 2400/2430
        :type x12_path_str: string
        :return: True if found
        :rtype: boolean
        """
        curr, new_path = self._get_start_node(x12_path_str)
        xpath = path.X12Path(new_path)
        for n in curr._select(xpath):
            return True
        return False

    def select(self, x12_path_str: str) -> Iterator[X12DataNode]:
        """
        Get a slice of sub-nodes at the relative X12 path.
        Note: All interaction/modification with a X12DataNode tree (having a loop
        root) is done in place.
        :param x12_path_str: Relative X12 path - 2400/2430
        :type x12_path_str: string
        :return: Iterator on the matching sub-nodes, relative to the instance.
        :rtype: L{node<x12context.X12DataNode>}
        """
        curr, new_path = self._get_start_node(x12_path_str)
        xpath = path.X12Path(new_path)
        for n in curr._select(xpath):
            if xpath.seg_id is not None:
                if n.id != xpath.seg_id:
                    raise errors.EngineError(
                        'Selected node id "%s" does not match xpath seg_id "%s"'
                        % (n.id, xpath.seg_id)
                    )
            else:
                if len(xpath.loop_list) == 0:
                    raise errors.EngineError("xpath has no seg_id and an empty loop list")
                if n.id != xpath.loop_list[-1]:
                    raise errors.EngineError(
                        'Selected node id "%s" does not match xpath final loop "%s"'
                        % (n.id, xpath.loop_list[-1])
                    )
            if n.parent is None:
                raise errors.EngineError('Node "%s" has no parent' % (n.id))
            yield n

    def first(self, x12_path_str: str) -> X12DataNode | None:
        """
        Get the first sub-node matching the relative X12 path.
        Note: All interaction/modification with a X12DataNode tree (having a loop
        root) is done in place.
        :param x12_path_str: Relative X12 path - ie 2400/2430
        :type x12_path_str: string
        :return: The matching sub-node, relative to the instance.
        :rtype: L{node<x12context.X12DataNode>}
        """
        if not self.exists(x12_path_str):
            return None
        for node in self.select(x12_path_str):
            return node
        return None

    def count(self, x12_path_str: str) -> int:
        """
        Get a count of sub-nodes at the relative X12 path.
        :param x12_path_str: Relative X12 path - 2400/2430
        :type x12_path_str: string
        :return: Count of matching sub-nodes
        :rtype: int
        """
        ct = 0
        curr, new_path = self._get_start_node(x12_path_str)
        xpath = path.X12Path(new_path)
        for n in curr._select(xpath):
            ct += 1
        return ct

    # { Private Methods
    def _cleanup(self) -> None:
        """
        Remove deleted nodes
        """
        self.children = [x for x in self.children if x.type is not None]

    def _get_insert_idx(self, x12_node: Any) -> int:
        """
        Find the index of self.children before which the x12_node belongs
        Nodes will be inserted after the last node with matching ordinals
        """
        self._cleanup()
        map_idx = x12_node.pos
        idx: int | None = None
        for i in range(len(self.children)):
            if self.children[i].x12_map_node.pos <= map_idx:
                idx = i
        if idx is not None:
            return idx + 1
        return len(self.children)

    def get_first_matching_segment(self, x12_path_str: str) -> pyx12.segment.Segment | None:
        """
        Get first found Segment at the given relative path.  If the path is not a
        valid relative path or if the given segment index does not exist, the function
        returns None.

        :param x12_path_str: Relative X12 Path
        :type x12_path_str: string
        :return: First matching data segment
        :rtype: L{node<segment.Segment>}
        :raises X12PathError: On blank or invalid path
        """
        raise NotImplementedError("Override in sub-class")

    def _get_start_node(self, x12_path_str: str) -> tuple[X12DataNode, str]:
        """
        Move up the tree.  Get the new starting node and the altered path
        """
        curr: X12DataNode = self
        while x12_path_str[:3] == "../":
            if curr.parent is None:
                raise errors.X12PathError(
                    "Current node %s does not have a parent: %s" % (self.id, x12_path_str)
                )
            curr = curr.parent
            x12_path_str = x12_path_str[3:]
        return (curr, x12_path_str)

    def _select(self, x12path: path.X12Path) -> Iterator[X12DataNode]:
        """
        Get the child node at the path
        :param x12path: x12 map path
        :type x12path: L{path<path.X12Path>}
        """
        if len(x12path.loop_list) == 0:
            # Only segment left
            cur_node_id = x12path.seg_id
            qual = x12path.id_val
            for child in [x for x in self.children if x.type is not None]:
                if child.type == "seg":
                    is_match, qual_code, ele_idx, subele_idx = child.x12_map_node.is_match_qual(
                        child.seg_data, cur_node_id, qual
                    )
                    if is_match:
                        yield child
                else:
                    if child.id == cur_node_id:
                        yield child
        else:
            cur_node_id = x12path.loop_list[0]
            cur_loop_list = x12path.loop_list[1:]
            for child in [x for x in self.children if x.type is not None]:
                if child.id == cur_node_id:
                    if len(cur_loop_list) == 0 and x12path.seg_id is None:
                        yield child
                    else:
                        child_path = path.X12Path(x12path.format())
                        child_path.loop_list = cur_loop_list
                        for n in child._select(child_path):
                            yield n

    def __copy__(self) -> X12DataNode:
        """
        Returns a copy of this node
        """
        raise NotImplementedError("Override in sub-class")

    def copy(self) -> X12DataNode:
        return self.__copy__()

    # { Property Accessors
    @property
    def id(self) -> str | None:
        """
        :return: x12 node id
        :rtype: string
        """
        if self.x12_map_node is None:
            raise errors.EngineError("This node has been deleted")
        result: str | None = self.x12_map_node.id
        return result

    @property
    def cur_path(self) -> str:
        """
        :return: x12 node path
        :rtype: string
        """
        if self.x12_map_node is None:
            raise errors.EngineError("This node has been deleted")
        result: str = self.x12_map_node.get_path()
        return result


class X12LoopDataNode(X12DataNode):
    """
    Capture the X12 definition for a loop subtree
    Alter relational data
    Iterate over contents
    """

    end_loops: list[Any]

    def __init__(
        self,
        x12_node: Any,
        end_loops: list[Any] | None = None,
        parent: X12DataNode | None = None,
    ) -> None:
        """
        Construct an X12LoopDataNode
        """
        if end_loops is None:
            end_loops = []
        self.x12_map_node = x12_node
        self.type = "loop"
        self.seg_data = None
        self.parent = parent
        self.children = []
        self.errors = []
        self.end_loops = end_loops  # we might need to close a preceeding loop

    # { Public Methods
    def delete(self) -> None:
        """
        Delete this node.  Mark type as deleted.
        """
        self.end_loops = []
        X12DataNode.delete(self)

    def get_value(self, x12_path_str: str) -> str | None:
        """
        Returns the element value at the given relative path.  If the path is not a
        valid relative path or if the given segment index does not exist, the function
        returns None.  If multiple values exist, this function returns the first.

        :param x12_path_str: Relative X12 Path
        :type x12_path_str: string
        :return: the element value at the relative X12 path
        :rtype: string
        :raises X12PathError: On blank or invalid path
        """
        curr, new_path = self._get_start_node(x12_path_str)
        seg_data = curr.get_first_matching_segment(new_path)
        if seg_data is None:
            return None
        xpath = path.X12Path(new_path)
        xpath.loop_list = []
        xpath.id_val = None
        seg_part = xpath.format()
        return seg_data.get_value(seg_part)

    def set_value(self, x12_path_str: str, val: str) -> None:
        """
        Set the value of simple element at the first found segment at the given path
        :param x12_path_str: Relative X12 Path
        :type x12_path_str: string
        :param val: The new element value
        :type val: string
        """
        curr, new_path = self._get_start_node(x12_path_str)
        seg_data = curr.get_first_matching_segment(new_path)
        if seg_data is None:
            raise errors.X12PathError("X12 Path is invalid or was not found: %s" % (x12_path_str))
        xpath = path.X12Path(new_path)
        xpath.loop_list = []
        xpath.id_val = None
        seg_part = xpath.format()
        seg_data.set(seg_part, val)

    def iterate_segments(self) -> Iterator[dict[str, Any]]:
        """
        Iterate over this node and children
        """
        for child in [x for x in self.children if x.type is not None]:
            for a in child.iterate_segments():
                yield a

    def iterate_loop_segments(self) -> Iterator[dict[str, Any]]:
        """
        Iterate over this node and children, return loop start and loop end
        """
        for loop in self.end_loops:
            yield {"node": loop, "type": "loop_end", "id": loop.id}
        yield {"type": "loop_start", "id": self.id, "node": self.x12_map_node}
        for child in [x for x in self.children if x.type is not None]:
            for a in child.iterate_loop_segments():
                yield a
        yield {"type": "loop_end", "id": self.id, "node": self.x12_map_node}

    def add_segment(self, seg_data: pyx12.segment.Segment | str) -> X12SegmentDataNode:
        """
        Add the segment to this loop node
        iif the segment is the anchor for a child loop, also adds the loop

        :param seg_data: Segment data
        :type seg_data: L{node<segment.Segment>} or string
        :return: New segment, or None if failed
        :rtype: L{node<x12context.X12SegmentDataNode>}
        :raises pyx12.errors.X12PathError: If invalid segment

        TODO: Check counts?
        """
        seg_data = self._get_segment(seg_data)
        x12_seg_node = self.x12_map_node.get_child_seg_node(seg_data)
        if x12_seg_node is None:
            raise errors.X12PathError(
                "The segment %s is not a member of loop %s" % (seg_data.__repr__(), self.id)
            )
        new_data_node = X12SegmentDataNode(x12_seg_node, seg_data, self)
        child_idx = self._get_insert_idx(x12_seg_node)
        self.children.insert(child_idx, new_data_node)
        return new_data_node

    def add_loop(self, seg_data: pyx12.segment.Segment | str) -> X12LoopDataNode:
        """
        Add a new loop in the correct location
        :param seg_data: Segment data
        :type seg_data: L{node<segment.Segment>} or string
        :return: New loop_data_node, or None if failed
        :rtype: L{node<x12context.X12LoopDataNode>}
        """
        seg_data = self._get_segment(seg_data)
        x12_loop_node = self.x12_map_node.get_child_loop_node(seg_data)
        if x12_loop_node is None:
            raise errors.X12PathError(
                "The segment %s is not a member of loop %s" % (seg_data.__repr__(), self.id)
            )
        new_data_loop = self._add_loop_node(x12_loop_node)
        # Now, add the segment
        x12_seg_node = new_data_loop.x12_map_node.get_child_seg_node(seg_data)
        new_data_node = X12SegmentDataNode(x12_seg_node, seg_data, new_data_loop)
        new_data_loop.add_node(new_data_node)
        return new_data_loop

    def add_node(self, data_node: X12DataNode) -> None:
        """
        Add a X12DataNode instance
        The x12_map_node of the given data_node must be a direct child of this
        object's x12_map_node
        :param data_node: The child loop node to add
        :type data_node : L{node<x12context.X12DataNode>}
        :raises errors.X12PathError: On blank or invalid path
        """
        if data_node.x12_map_node.parent != self.x12_map_node:
            raise errors.X12PathError(
                'The loop_data_node "%s" is not a child of "%s"'
                % (data_node.x12_map_node.id, self.x12_map_node.id)
            )
        data_node.parent = self
        child_idx = self._get_insert_idx(data_node.x12_map_node)
        self.children.insert(child_idx, data_node)

    def delete_segment(self, seg_data: pyx12.segment.Segment | str) -> bool:
        """
        Delete the given segment from this loop node
         - Do not delete the first segment in a loop
         - Does not descend into child loops
         - Only delete the first found matching segment

        :param seg_data: Segment data
        :type seg_data: L{node<segment.Segment>} or string
        :return: True if found and deleted, else False
        :rtype: Boolean

        TODO: Check counts?
        """
        seg_data = self._get_segment(seg_data)
        x12_seg_node = self.x12_map_node.get_child_seg_node(seg_data)
        if x12_seg_node is None:
            return False
        # Iterate over data nodes, except first
        self._cleanup()
        for i in range(1, len(self.children)):
            if self.children[i].type == "seg" and self.children[i].seg_data == seg_data:
                del self.children[i]
                return True
        return False

    def delete_node(self, x12_path_str: str) -> bool:
        """
        Delete the first node at the given relative path.  If the path is not a
        valid relative path, return False If multiple values exist, this
        function deletes the first.

        :return: True if found and deleted, else False
        :rtype: Boolean
        :raises X12PathError: On blank or invalid path

        TODO: Check counts?
        """
        curr, new_path = self._get_start_node(x12_path_str)
        xpath = path.X12Path(new_path)
        for n in curr._select(xpath):
            n.delete()
            return True
        return False

    def _add_loop_node(self, x12_loop_node: Any) -> X12LoopDataNode:
        """
        Add a loop data node to the current tree
        :param x12_loop_node: X12 Loop node
        :type x12_loop_node: L{node<map_if.loop_if>}
        :return: New X12 Loop Data Node
        :rtype: L{node<x12context.X12LoopDataNode>}
        """
        new_node = X12LoopDataNode(x12_loop_node, parent=self)
        # Iterate over data nodes
        child_idx = self._get_insert_idx(x12_loop_node)
        self.children.insert(child_idx, new_node)
        return new_node

    def get_first_matching_segment(self, x12_path_str: str) -> pyx12.segment.Segment | None:
        """
        Get first found Segment at the given relative path.  If the path is not a
        valid relative path or if the given segment index does not exist, the function
        returns None.

        :param x12_path_str: Relative X12 Path
        :type x12_path_str: string
        :return: First matching data segment
        :rtype: L{node<segment.Segment>}
        :raises X12PathError: On blank or invalid path
        """
        if len(x12_path_str) == 0:
            raise errors.X12PathError("Blank X12 Path")
        curr, new_path = self._get_start_node(x12_path_str)
        xpath = path.X12Path(new_path)
        if xpath.seg_id is None:
            return None
        if len(xpath.loop_list) == 0:
            seg_id = xpath.seg_id
            qual = xpath.id_val
            try:
                for seg in [seg for seg in curr.children if seg.type == "seg"]:
                    is_match, qual_code, ele_idx, subele_idx = seg.x12_map_node.is_match_qual(
                        seg.seg_data, seg_id, qual
                    )
                    if is_match:
                        return seg.seg_data
                return None
            except errors.EngineError as e:
                raise errors.X12PathError(
                    "X12 Path is invalid or was not found: %s" % (x12_path_str)
                )
        else:
            next_id = xpath.loop_list[0]
            del xpath.loop_list[0]
            try:
                for loop in [loop for loop in curr.children if loop.type == "loop"]:
                    if loop.id == next_id:
                        result: pyx12.segment.Segment | None = loop.get_first_matching_segment(
                            xpath.format()
                        )
                        return result
                return None
            except errors.EngineError as e:
                raise errors.X12PathError(
                    "X12 Path is invalid or was not found: %s" % (x12_path_str)
                )

    def _get_segment(self, seg_obj: pyx12.segment.Segment | str) -> pyx12.segment.Segment:
        """
        Get a pyx12.segment.Segment instance, building one from a string
        """
        if isinstance(seg_obj, pyx12.segment.Segment):
            return seg_obj
        elif isinstance(seg_obj, str):
            seg_term, ele_term, subele_term = self._get_terminators()
            if seg_term is None or ele_term is None or subele_term is None:
                raise errors.EngineError(
                    "Cannot build Segment: terminators unknown (node has no X12SegmentDataNode children)"
                )
            return pyx12.segment.Segment(seg_obj, seg_term, ele_term, subele_term)
        else:
            raise errors.EngineError(
                "Unknown type %s for seg_obj %i.  Expecting a pyx12.segment.Segment or a str"
                % (seg_obj.__class__, seg_obj)
            )

    def _get_terminators(self) -> tuple[str | None, str | None, str | None]:
        for child in self.children:
            if (
                isinstance(child, X12SegmentDataNode)
                and child.seg_data is not None
                and child.seg_data.seg_term is not None
            ):
                return (
                    child.seg_data.seg_term,
                    child.seg_data.ele_term,
                    child.seg_data.subele_term,
                )
        if self.parent is None:
            raise errors.EngineError("Cannot find terminators: no parent loop")
        result: tuple[str | None, str | None, str | None] = self.parent._get_terminators()  # type: ignore[attr-defined]
        return result

    def __copy__(self) -> X12LoopDataNode:
        """
        Returns a copy of this node
        """
        ret = X12LoopDataNode(self.x12_map_node)
        ret.end_loops = list(self.end_loops)
        ret.parent = self.parent
        for child in self.children:
            ret.children.append(child.copy())
        return ret

    @property
    def seg_count(self) -> int | None:  # type: ignore[override]
        for child in [x for x in self.children if x.type == "seg"]:
            return child.seg_count
        return None

    @property
    def cur_line_number(self) -> int | None:  # type: ignore[override]
        for child in [x for x in self.children if x.type == "seg"]:
            return child.cur_line_number
        return None


class X12SegmentDataNode(X12DataNode):
    """
    Capture the segment data and X12 definition
    Alter relational data
    Iterate over contents
    """

    start_loops: list[Any]
    end_loops: list[Any]
    err_isa: list[Any]
    err_gs: list[Any]
    err_st: list[Any]
    err_seg: list[Any]
    err_ele: list[Any]

    def __init__(
        self,
        x12_node: Any,
        seg_data: pyx12.segment.Segment,
        parent: X12DataNode | None = None,
        start_loops: list[Any] | None = None,
        end_loops: list[Any] | None = None,
    ) -> None:
        if start_loops is None:
            start_loops = []
        if end_loops is None:
            end_loops = []
        self.x12_map_node = x12_node
        self.type = "seg"
        self.seg_data = seg_data
        self.parent = parent
        self.start_loops = start_loops
        self.end_loops = end_loops
        self.errors = []
        self.err_isa = []
        self.err_gs = []
        self.err_st = []
        self.err_seg = []
        self.err_ele = []
        self.seg_count = None
        self.cur_line_number = None

    # { Public Methods
    def handle_errh_errors(self, errh: Any) -> None:
        """
        Attach validation errors to segment node

        TODO: move errors to parent loops if necessary
        """
        self.err_isa.extend(errh.err_isa)
        self.err_gs.extend(errh.err_gs)
        self.err_st.extend(errh.err_st)
        self.err_seg.extend(errh.err_seg)
        self.err_ele.extend(errh.err_ele)

    def delete(self) -> None:
        """
        Delete this node.  Mark type as deleted.
        """
        self.start_loops = []
        self.end_loops = []
        X12DataNode.delete(self)

    def get_value(self, x12_path_str: str) -> str | None:
        """
        Get the value of the first found element at the given path
        :param x12_path_str: Relative X12 Path
        :type x12_path_str: string
        :return: the element value at the relative X12 path
        :rtype: string
        """
        seg_data = self.get_first_matching_segment(x12_path_str)
        if seg_data is None:
            return None
        return seg_data.get_value(x12_path_str)

    def set_value(self, x12_path_str: str, val: str) -> None:
        """
        Set the value of simple element at the first found segment at the given path
        :param x12_path_str: Relative X12 Path
        :type x12_path_str: string
        :param val: The new element value
        :type val: string
        """
        seg_data = self.get_first_matching_segment(x12_path_str)
        if seg_data is None:
            raise errors.X12PathError("X12 Path is invalid or was not found: %s" % (x12_path_str))
        seg_data.set(x12_path_str, val)

    def get_first_matching_segment(self, x12_path_str: str) -> pyx12.segment.Segment | None:
        """
        Get first found Segment at the given relative path.  If the path is not a
        valid relative path or if the given segment index does not exist, the function
        returns None.

        :param x12_path_str: Relative X12 Path
        :type x12_path_str: string
        :return: First matching data segment
        :rtype: L{node<segment.Segment>}
        :raises X12PathError: On blank or invalid path
        """
        curr, new_path_str = self._get_start_node(x12_path_str)
        xpath = path.X12Path(new_path_str)
        if len(xpath.loop_list) != 0:
            raise errors.X12PathError("This X12 Path should not contain loops: %s" % (x12_path_str))
        seg_id = xpath.seg_id
        qual = xpath.id_val
        ele_idx = xpath.ele_idx
        if ele_idx is not None and seg_id is None:
            return self.seg_data
        try:
            is_match, qual_code, matched_ele_idx, matched_subele_idx = (
                curr.x12_map_node.is_match_qual(curr.seg_data, seg_id, qual)
            )
            if is_match:
                seg_result: pyx12.segment.Segment | None = curr.seg_data
                return seg_result
            return None
        except errors.EngineError as e:
            raise errors.X12PathError("X12 Path is invalid or was not found: %s" % (x12_path_str))

    def iterate_segments(self) -> Iterator[dict[str, Any]]:
        """
        Iterate on this node, return the segment
        """
        yield {
            "type": "seg",
            "id": self.x12_map_node.id,
            "path": self.x12_map_node.x12path,
            "segment": self.seg_data,
            "seg_count": self.seg_count,
            "cur_line_number": self.cur_line_number,
        }

    def iterate_loop_segments(self) -> Iterator[dict[str, Any]]:
        """
        Iterate over this node and children, return loop start and loop end
        and any segments found
        """
        for loop in self.end_loops:
            yield {"node": loop, "type": "loop_end", "id": loop.id}
        for loop in self.start_loops:
            yield {"node": loop, "type": "loop_start", "id": loop.id}
        yield {
            "type": "seg",
            "id": self.id,
            "segment": self.seg_data,
            "start_loops": self.start_loops,
            "end_loops": self.end_loops,
            "seg_count": self.seg_count,
            "cur_line_number": self.cur_line_number,
        }

    def __copy__(self) -> X12SegmentDataNode:
        """
        Returns a copy of this node
        """
        if self.seg_data is None:
            raise errors.EngineError("Cannot copy X12SegmentDataNode with no seg_data")
        seg_data = self.seg_data.copy()
        ret = X12SegmentDataNode(self.x12_map_node, seg_data, self.parent)
        ret.start_loops = list(self.start_loops)
        ret.end_loops = list(self.end_loops)
        return ret

    def select(self, x12_path_str: str) -> Iterator[X12DataNode]:
        """
        Segment nodes have no sub-nodes so return None
        :param x12_path_str: Relative X12 path - 2400/2430
        :type x12_path_str: string
        :return: Iterator on the matching sub-nodes, relative to the instance.
        :rtype: L{node<x12context.X12DataNode>}
        """
        return iter([])

    def _select(self, x12path: path.X12Path) -> Iterator[X12DataNode]:
        """
        Empty iter for segment nodes
        :param x12path: x12 map path
        :type x12path: L{path<path.X12Path>}
        """
        return iter([])

    # { Property Accessors
    @property
    def err_ct(self) -> int:
        """
        :return: Count of errors for this segment
        :rtype: int
        """
        return (
            len(self.err_isa)
            + len(self.err_gs)
            + len(self.err_st)
            + len(self.err_seg)
            + len(self.err_ele)
        )


class X12ContextReader:
    """
    Read an X12 input stream
    Keep context when needed
    """

    param: Any
    map_path: str | None
    errh: error_handler.errh_list
    icvn: str | None
    fic: str | None
    vriic: str | None
    tspc: str | None
    src: x12file.X12Reader
    map_file: str | None
    control_map: Any
    map_index_if: map_index.map_index
    x12_map_node: Any
    walker: walk_tree

    def __init__(
        self,
        param: Any,
        errh: Any,
        src_file_obj: str | TextIO,
        xslt_files: Any = None,
        map_path: str | None = None,
    ) -> None:
        """
        :param param: pyx12.param instance
        :param errh: Error Handler object
        :param src_file_obj: Source document
        :type src_file_obj: string
        :rtype: boolean
        """
        self.param = param
        self.map_path = map_path
        self.errh = error_handler.errh_list()
        self.icvn = None
        self.fic = None
        self.vriic = None
        self.tspc = None

        # Get X12 DATA file
        self.src = x12file.X12Reader(src_file_obj)

        # Get Map of Control Segments
        self.map_file = (
            "x12.control.00501.xml" if self.src.icvn == "00501" else "x12.control.00401.xml"
        )
        self.control_map = map_if.load_map_file(self.map_file, param, self.map_path)
        self.map_index_if = map_index.map_index(self.map_path)
        self.x12_map_node = self.control_map.getnodebypath("/ISA_LOOP/ISA")
        self.walker = walk_tree()

    def close(self) -> None:
        """Close the underlying X12Reader. Idempotent."""
        self.src.close()

    def __enter__(self) -> X12ContextReader:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> Literal[False]:
        self.close()
        return False

    # { Public Methods
    def iter_segments(self, loop_id: str | None = None) -> Iterator[X12DataNode]:
        """
        Simple segment or tree iterator
        :return: X12 Data Node - simple segment or tree
        :rtype: L{node<x12context.X12DataNode>}
        """
        cur_tree: X12LoopDataNode | None = None
        cur_data_node: X12DataNode | None = None
        icvn: str | None = None
        fic: str | None = None
        vriic: str | None = None
        cur_map: Any = None
        for seg in self.src:
            # find node
            orig_node = self.x12_map_node
            pop_loops: list[Any] = []
            push_loops: list[Any] = []
            errh = error_handler.errh_list()

            if seg.get_seg_id() == "ISA":
                tpath = "/ISA_LOOP/ISA"
                self.x12_map_node = self.control_map.getnodebypath(tpath)
            elif seg.get_seg_id() == "GS":
                tpath = "/ISA_LOOP/GS_LOOP/GS"
                self.x12_map_node = self.control_map.getnodebypath(tpath)
            else:
                try:
                    seg_node, pop_loops, push_loops = self.walker.walk(
                        self.x12_map_node,
                        seg,
                        errh,
                        self.src.get_seg_count(),
                        self.src.get_cur_line(),
                        self.src.get_ls_id(),
                    )
                    self.x12_map_node = seg_node
                except errors.EngineError:
                    raise
            if self.x12_map_node is None:
                self.x12_map_node = orig_node
            else:
                seg_id = seg.get_seg_id()
                if seg_id == "ISA":
                    icvn = seg.get_value("ISA12")
                elif seg_id == "GS":
                    fic = seg.get_value("GS01")
                    vriic = seg.get_value("GS08")
                    map_file_new = self.map_index_if.get_filename(icvn, vriic, fic)
                    if self.map_file != map_file_new:
                        self.map_file = map_file_new
                        if self.map_file is None:
                            raise pyx12.errors.EngineError(
                                "Map not found.  icvn=%s, fic=%s, vriic=%s" % (icvn, fic, vriic)
                            )
                        cur_map = map_if.load_map_file(self.map_file, self.param, self.map_path)
                        if cur_map.id == "837":
                            self.src.check_837_lx = True
                        else:
                            self.src.check_837_lx = False
                        self._reset_counter_to_isa_counts()
                    self._reset_counter_to_gs_counts()
                    tpath = "/ISA_LOOP/GS_LOOP/GS"
                    self.x12_map_node = cur_map.getnodebypath(tpath)
                elif seg_id == "BHT":
                    if vriic in ("004010X094", "004010X094A1"):
                        tspc = seg.get_value("BHT02")
                        map_file_new = self.map_index_if.get_filename(icvn, vriic, fic, tspc)
                        if self.map_file != map_file_new:
                            self.map_file = map_file_new
                            if self.map_file is None:
                                err_str = "Map not found.  icvn=%s, fic=%s, vriic=%s, tspc=%s" % (
                                    icvn,
                                    fic,
                                    vriic,
                                    tspc,
                                )
                                raise pyx12.errors.EngineError(err_str)
                            cur_map = map_if.load_map_file(self.map_file, self.param, self.map_path)
                            if cur_map.id == "837":
                                self.src.check_837_lx = True
                            else:
                                self.src.check_837_lx = False
                            self._apply_loop_count(self.x12_map_node, cur_map)
                            tpath = "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BHT"
                            self.x12_map_node = cur_map.getnodebypath(tpath)

            node_x12path = self.x12_map_node.x12path
            # If we are in the requested tree, wait until we have the whole thing
            if loop_id is not None and loop_id in node_x12path.loop_list:
                # Are we at the start of the requested tree?
                if (
                    node_x12path.loop_list[-1] == loop_id
                    and self.x12_map_node.is_first_seg_in_loop()
                ):
                    if cur_tree is not None:
                        # Found root loop repeat. Yield existing, create new tree
                        yield cur_tree
                    # Make new tree on parent loop
                    cur_tree = X12LoopDataNode(
                        x12_node=self.x12_map_node.parent, end_loops=pop_loops
                    )
                    cur_data_node = self._add_segment(
                        cur_tree, self.x12_map_node, seg, pop_loops, push_loops
                    )
                    cur_data_node.seg_count = self.src.get_seg_count()
                    cur_data_node.cur_line_number = self.src.get_cur_line()
                else:
                    if cur_data_node is None or self.x12_map_node is None:
                        raise errors.EngineError(
                            "Either cur_data_node or self.x12_map_node is None"
                        )
                    cur_data_node = self._add_segment(
                        cur_data_node, self.x12_map_node, seg, pop_loops, push_loops
                    )
                    cur_data_node.seg_count = self.src.get_seg_count()
                    cur_data_node.cur_line_number = self.src.get_cur_line()
            else:
                if cur_tree is not None:
                    # We have completed a tree
                    yield cur_tree
                    cur_tree = None
                if cur_data_node is not None:
                    if loop_id:
                        pop_loops = [
                            x12_node
                            for x12_node in pop_loops
                            if x12_node.get_path().find(loop_id) == -1
                        ]
                    if loop_id in [x12.id for x12 in push_loops]:
                        raise errors.EngineError(
                            "Loop ID %s should not be in push loops" % (loop_id)
                        )
                    if loop_id in [x12.id for x12 in pop_loops]:
                        raise errors.EngineError(
                            "Loop ID %s should not be in pop loops" % (loop_id)
                        )
                    # NOTE: positional args here are intentionally what they
                    # appear to be even though it looks wrong (`parent` gets
                    # `push_loops` which is a list). The downstream None-check
                    # for `parent` relies on this list being truthy. See the
                    # test_x12context.TreeCopy tests.
                    cur_data_node = X12SegmentDataNode(
                        self.x12_map_node, seg, push_loops, pop_loops
                    )  # type: ignore[arg-type]
                    cur_data_node.seg_count = self.src.get_seg_count()
                    cur_data_node.cur_line_number = self.src.get_cur_line()
                else:
                    cur_data_node = X12SegmentDataNode(self.x12_map_node, seg)
                    cur_data_node.seg_count = self.src.get_seg_count()
                    cur_data_node.cur_line_number = self.src.get_cur_line()
                # Get errors caught by x12Reader
                errh.handle_errors(self.src.pop_errors())
                # Handle errors captured in errh_list
                cur_data_node.handle_errh_errors(errh)
                if cur_data_node.id != "ISA" and cur_data_node is not None:
                    if cur_data_node.parent is None:
                        raise errors.EngineError('Node "%s" has no parent' % (cur_data_node.id))
                yield cur_data_node

    def register_error_callback(self, callback: Any, err_type: str) -> None:
        """
        Future:  Callbacks for X12 validation errors
        """
        pass

    # { Property Accessors
    @property
    def seg_term(self) -> str | None:
        """
        :return: Current X12 segment terminator
        :rtype: string
        """
        return self.src.seg_term

    @property
    def ele_term(self) -> str | None:
        """
        :return: Current X12 element terminator
        :rtype: string
        """
        return self.src.ele_term

    @property
    def subele_term(self) -> str | None:
        """
        :return: Current X12 sub-element terminator
        :rtype: string
        """
        return self.src.subele_term

    @property
    def cur_seg_count(self) -> int:
        return self.src.get_seg_count()

    @property
    def get_cur_line(self) -> int:
        return self.src.get_cur_line()

    # { Private Methods
    def _add_segment(
        self,
        cur_data_node: X12DataNode,
        segment_x12_node: Any,
        seg_data: pyx12.segment.Segment,
        pop_loops: list[Any],
        push_loops: list[Any],
    ) -> X12SegmentDataNode:
        """
        From the last position in the X12 Data Node Tree, find the correct
        position for the new segment; moving up or down the tree as appropriate.

        G{callgraph}

        :param cur_data_node: Current X12 Data Node
        :type cur_data_node: L{node<x12context.X12DataNode>}
        :param segment_x12_node: Segment Map Node
        :type segment_x12_node: L{node<map_if.x12_node>}
        :return: New X12 Data Node
        :rtype: L{node<x12context.X12DataNode>}
        """
        if not segment_x12_node.is_segment():
            raise errors.EngineError("Node must be a segment")
        # Get enclosing loop
        orig_data_node = cur_data_node
        parent_x12_node = pop_to_parent_loop(segment_x12_node)
        cur_loop_node: X12DataNode | None = cur_data_node
        if cur_loop_node is not None and cur_loop_node.type == "seg":
            cur_loop_node = cur_loop_node.parent
        # check path for new loops to be added
        new_path = parent_x12_node.x12path
        if cur_loop_node is None:
            raise errors.EngineError("cur_loop_node is None")
        last_path = cur_loop_node.x12_map_node.x12path
        if last_path != new_path:
            for x12_loop in pop_loops:
                if cur_loop_node is None or cur_loop_node.id != x12_loop.id:
                    raise errors.EngineError(
                        "Loop pop: %s != %s"
                        % (cur_loop_node.id if cur_loop_node else None, x12_loop.id)
                    )
                cur_loop_node = cur_loop_node.parent
            for x12_loop in push_loops:
                if cur_loop_node is None:
                    raise errors.EngineError("cur_loop_node is None. x12_loop: %s" % (x12_loop.id))
                # push new loop nodes, if needed
                cur_loop_node = cur_loop_node._add_loop_node(x12_loop)  # type: ignore[attr-defined]
        else:
            # handle loop repeat
            if (
                cur_loop_node is not None
                and cur_loop_node.parent is not None
                and segment_x12_node.is_first_seg_in_loop()
            ):
                cur_loop_node = cur_loop_node.parent._add_loop_node(  # type: ignore[attr-defined]
                    segment_x12_node.parent
                )
        try:
            new_node = X12SegmentDataNode(self.x12_map_node, seg_data)
        except Exception:
            mypath = self.x12_map_node.get_path()
            err_str = "X12SegmentDataNode failed: x12_path={}, seg_date={}".format(mypath, seg_data)
            raise errors.EngineError(err_str)
        try:
            new_node.parent = cur_loop_node
            if cur_loop_node is None:
                raise errors.EngineError("cur_loop_node is None")
            cur_loop_node.children.append(new_node)
        except Exception:
            err_str = "X12SegmentDataNode child append failed:"
            err_str += " seg_x12_path=%s" % (segment_x12_node.get_path())
            err_str += ", orig_datanode=%s" % (orig_data_node.cur_path)
            err_str += ", cur_datanode=%s" % (cur_data_node.cur_path)
            err_str += ", seg_data=%s" % (seg_data)
            raise errors.EngineError(err_str)
        return new_node

    def _apply_loop_count(self, orig_node: Any, new_map: Any) -> None:
        """Stub - referenced from iter_segments BHT branch."""
        pass

    def _reset_counter_to_isa_counts(self) -> None:
        """
        Reset ISA instance counts
        """
        self.walker.counter.reset_to_node("/ISA_LOOP")
        self.walker.counter.increment("/ISA_LOOP")
        self.walker.counter.increment("/ISA_LOOP/ISA")

    def _reset_counter_to_gs_counts(self) -> None:
        """
        Reset GS instance counts
        """
        self.walker.counter.reset_to_node("/ISA_LOOP/GS_LOOP")
        self.walker.counter.increment("/ISA_LOOP/GS_LOOP")
        self.walker.counter.increment("/ISA_LOOP/GS_LOOP/GS")
