######################################################################
# Copyright (c) 2001-2013
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Walk a tree of x12_map nodes.  Find the correct node.

If seg indicates a loop has been entered, returns the first child segment node.
If seg indicates a segment has been entered, returns the segment node.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any, NamedTuple

import pyx12.path
import pyx12.segment

# Intrapackage imports
from .error_item import SegError
from .errors import EngineError
from .nodeCounter import NodeCounter

logger = logging.getLogger("pyx12.walk_tree")
# logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.ERROR)


class MissingMandatorySeg(NamedTuple):
    """A pending 'mandatory missing' error to be flushed once the loop has moved on."""

    seg_node: Any
    seg_data: pyx12.segment.Segment
    err_cde: str
    err_str: str
    seg_count: int
    cur_line: int
    ls_id: str | None


def pop_to_parent_loop(node: Any) -> Any:
    """
    :param node: Loop Node
    :type node: L{node<map_if.x12_node>}
    :return: Closest parent loop node
    :rtype: L{node<map_if.x12_node>}
    """
    if node.is_map_root():
        return node
    map_node = node.parent
    if map_node is None:
        raise EngineError("Node is None: %s" % (node.name))
    while not (map_node.is_loop() or map_node.is_map_root()):
        map_node = map_node.parent
    if not (map_node.is_loop() or map_node.is_map_root()):
        raise EngineError("Called pop_to_parent_loop, can't find parent loop")
    return map_node


def is_first_seg_match2(child: Any, seg_data: pyx12.segment.Segment) -> bool:
    """
    Find the first segment in loop, verify it matches segment

    :param child: child node
    :type child: L{node<map_if.x12_node>}
    :param seg_data: Segment object
    :type seg_data: L{segment<segment.Segment>}
    :rtype: boolean
    """
    if child.is_segment():
        if child.is_match(seg_data):
            return True
        else:
            # seg does not match the first segment in loop, so not valid
            return False
    return False


def get_id_list(node_list: list[Any]) -> list[str]:
    # get_id_list(pop)
    ret: list[str] = []
    for node in node_list:
        if node is not None:
            ret.append(node.id)
    return ret


def traverse_path(start_node: Any, pop_loops: list[Any], push_loops: list[Any]) -> str:
    """
    Debug function - From the start path, pop up then push down to get a path string
    """
    start_path = pop_to_parent_loop(start_node).get_path()
    p1 = [p for p in start_path.split("/") if p != ""]
    for loop_id in get_id_list(pop_loops):
        if loop_id != p1[-1]:
            raise EngineError("Path %s does not contain %s" % (start_path, loop_id))
        p1 = p1[:-1]
    for loop_id in get_id_list(push_loops):
        p1.append(loop_id)
    return "/" + "/".join(p1)


def apply_walk_errors(errh: Any, errors: list[SegError]) -> None:
    """
    Forward walker SegErrors to an err_handler. Each error with a non-None
    map_node triggers errh.add_seg(...) before errh.seg_error(...);
    map_node=None preserves the existing cursor (used for usage='N'
    emissions that historically attach to the prior segment).

    :param errh: Error handler
    :type errh: L{error_handler.err_handler}
    :param errors: SegErrors accumulated by walk_errors()
    :type errors: [L{SegError}]
    """
    for e in errors:
        if e.map_node is not None:
            errh.add_seg(e.map_node, e.seg_data, e.seg_count, e.src_line, e.ls_id)
        errh.seg_error(e.err_cde, e.err_str, e.err_val, e.src_line)


class walk_tree:
    """
    Walks a map_if tree.  Tracks loop/segment counting, missing loop/segment.
    """

    mandatory_segs_missing: list[MissingMandatorySeg]
    counter: NodeCounter
    errors_pending: list[SegError]

    def __init__(
        self,
        initialCounts: Mapping[str | pyx12.path.X12Path, int] | None = None,
    ) -> None:
        # Pending 'mandatory missing' errors — buffered until the loop has
        # certainly moved on, since a later segment in the same loop can
        # still satisfy the requirement.
        self.mandatory_segs_missing = []
        self.errors_pending = []
        if initialCounts is None:
            initialCounts = {}
        self.counter = NodeCounter(initialCounts)

    def walk_errors(
        self,
        node: Any,
        seg_data: pyx12.segment.Segment,
        seg_count: int,
        cur_line: int,
        ls_id: str | None,
    ) -> tuple[Any, list[Any], list[Any], list[SegError]]:
        """
        Walk the node tree from the starting node to the node matching
        seg_data. Catch any counting or requirement errors along the way.

        Handle required segment/loop missed (not found in seg)
        Handle found segment = Not used

        :param node: Starting node
        :type node: L{node<map_if.x12_node>}
        :param seg_data: Segment object
        :type seg_data: L{segment<segment.Segment>}
        :param seg_count: Count of current segment in the ST Loop
        :type seg_count: int
        :param cur_line: Current line number in the file
        :type cur_line: int
        :param ls_id: The current LS loop identifier
        :type ls_id: string
        :return: The matching x12 segment node, a list of x12 popped loops,
            a list of x12 pushed loops from the start segment to the found
            segment, and the list of accumulated SegErrors found along the way.
        :rtype: (L{node<map_if.segment_if>}, [L{node<map_if.loop_if>}], [L{node<map_if.loop_if>}], [L{SegError}])

        TODO: check single segment loop repeat
        """
        pop_node_list: list[Any] = []
        orig_node = node
        self.mandatory_segs_missing = []
        self.errors_pending = []
        node, node_pos = walk_tree._resolve_starting_loop(node)
        while True:
            result = self._scan_loop_at_position(
                node,
                node_pos,
                seg_data,
                orig_node,
                seg_count,
                cur_line,
                ls_id,
                pop_node_list,
            )
            if result is not None:
                return (*result, self.errors_pending)
            if node.is_map_root():
                self._seg_not_found_error(orig_node, seg_data, seg_count, cur_line, ls_id)
                return (None, [], [], self.errors_pending)
            node_pos = node.pos
            pop_node_list.append(node)
            node = pop_to_parent_loop(node)

    def getCountState(self) -> Any:
        return self.counter.getState()

    def setCountState(
        self, initialCounts: Mapping[str | pyx12.path.X12Path, int] | None = None
    ) -> None:
        if initialCounts is None:
            initialCounts = {}
        self.counter = NodeCounter(initialCounts)

    def forceWalkCounterToLoopStart(self, x12_path: str, child_path: str) -> None:
        # delete child counts under the x12_path, no longer needed
        self.counter.reset_to_node(x12_path)
        self.counter.increment(x12_path)  # add a count for this path
        self.counter.increment(child_path)  # count the loop start segment

    def _check_seg_usage(
        self,
        seg_node: Any,
        seg_data: pyx12.segment.Segment,
        seg_count: int,
        cur_line: int,
        ls_id: str | None,
    ) -> None:
        """
        Check segment usage requirement and count. Any violations are
        appended to self.errors_pending; the caller flushes them via
        apply_walk_errors at the end of walk_errors().

        :param seg_node: Segment X12 node to verify
        :type seg_node: L{node<map_if.segment_if>}
        :param seg_data: Segment object
        :type seg_data: L{segment<segment.Segment>}
        :param seg_count: Count of current segment in the ST Loop
        :type seg_count: int
        :param cur_line: Current line number in the file
        :type cur_line: int
        :param ls_id: The current LS loop identifier
        :type ls_id: string
        :raises EngineError: On invalid usage code
        """
        if seg_node.usage not in ("N", "R", "S"):
            raise EngineError("Segment usage must be R, S, or N (got %r)" % (seg_node.usage,))
        if seg_node.usage == "N":
            err_str = "Segment %s found but marked as not used" % (seg_node.id)
            self.errors_pending.append(SegError(err_cde="2", err_str=err_str, src_line=cur_line))
        elif seg_node.usage == "R" or seg_node.usage == "S":
            if (
                self.counter.get_count(seg_node.x12path) > seg_node.get_max_repeat()
            ):  # handle seg repeat count
                err_str = "Segment %s exceeded max count.  Found %i, should have %i" % (
                    seg_data.get_seg_id(),
                    self.counter.get_count(seg_node.x12path),
                    seg_node.get_max_repeat(),
                )
                self.errors_pending.append(
                    SegError(
                        err_cde="5",
                        err_str=err_str,
                        src_line=cur_line,
                        map_node=seg_node,
                        seg_data=seg_data,
                        seg_count=seg_count,
                        ls_id=ls_id,
                    )
                )

    def _try_match_segment_child(
        self,
        node: Any,
        child: Any,
        seg_data: pyx12.segment.Segment,
        orig_node: Any,
        seg_count: int,
        cur_line: int,
        ls_id: str | None,
        pop_node_list: list[Any],
    ) -> tuple[Any, list[Any], list[Any]] | None:
        """
        Try to match a segment-typed child against seg_data.

        On match, returns (segment_node, pop_loops, push_loops). When the
        matched segment is also the first segment of an enclosing loop, the
        loop's counters/usage are updated via _goto_seg_match and the result
        encodes the necessary pop/push loops.

        On no match, returns None. If the child is mandatory (R) and has not
        yet been counted, also accumulates a missing-segment error for later
        reporting.
        """
        if child.is_match(seg_data):
            # Is the matched segment the beginning of a loop?
            if node.is_loop() and self._is_loop_match(node, seg_data, seg_count, cur_line, ls_id):
                return self._match_segment_at_loop_entry(
                    node,
                    seg_data,
                    orig_node,
                    seg_count,
                    cur_line,
                    ls_id,
                    pop_node_list,
                )
            self.counter.increment(child.x12path)
            self._check_seg_usage(child, seg_data, seg_count, cur_line, ls_id)
            # Remove any previously missing errors for this segment
            self.mandatory_segs_missing = [
                m for m in self.mandatory_segs_missing if m.seg_node != child
            ]
            self._flush_mandatory_segs(child.pos)
            return (child, pop_node_list, [])
        if child.usage == "R" and self.counter.get_count(child.x12path) < 1:
            fake_seg = pyx12.segment.Segment("%s" % (child.id), "~", "*", ":")
            err_str = 'Mandatory segment "%s" (%s) missing' % (child.name, child.id)
            self.mandatory_segs_missing.append(
                MissingMandatorySeg(child, fake_seg, "3", err_str, seg_count, cur_line, ls_id)
            )
        return None

    def _match_segment_at_loop_entry(
        self,
        node: Any,
        seg_data: pyx12.segment.Segment,
        orig_node: Any,
        seg_count: int,
        cur_line: int,
        ls_id: str | None,
        pop_node_list: list[Any],
    ) -> tuple[Any, list[Any], list[Any]]:
        """
        Handle a matched segment that is also the first segment of `node`
        (the enclosing loop being scanned). Descend via _goto_seg_match,
        then adjust pop/push when `node` equals the starting node's
        enclosing loop — in that case both lists collapse to [node],
        signalling "we re-entered the same loop we started in".
        """
        (node_seg, push_node_list) = self._goto_seg_match(
            node, seg_data, seg_count, cur_line, ls_id
        )
        orig_loop = (
            orig_node
            if (orig_node.is_loop() or orig_node.is_map_root())
            else pop_to_parent_loop(orig_node)
        )
        if node == orig_loop:
            return (node_seg, [node], [node])
        return (node_seg, pop_node_list, push_node_list)

    def _try_match_loop_child(
        self,
        child: Any,
        seg_data: pyx12.segment.Segment,
        seg_count: int,
        cur_line: int,
        ls_id: str | None,
        pop_node_list: list[Any],
    ) -> tuple[Any, list[Any], list[Any]] | None:
        """
        Try to match a loop-typed child against seg_data by descending into
        it via _is_loop_match / _goto_seg_match.

        On match, returns (segment_node, pop_loops, push_loops) where the
        push list is the chain of loops entered to reach the segment.
        On no match, returns None.
        """
        if not self._is_loop_match(child, seg_data, seg_count, cur_line, ls_id):
            return None
        (node_seg, push_node_list) = self._goto_seg_match(
            child, seg_data, seg_count, cur_line, ls_id
        )
        return (node_seg, pop_node_list, push_node_list)

    def _scan_loop_at_position(
        self,
        node: Any,
        node_pos: int,
        seg_data: pyx12.segment.Segment,
        orig_node: Any,
        seg_count: int,
        cur_line: int,
        ls_id: str | None,
        pop_node_list: list[Any],
    ) -> tuple[Any, list[Any], list[Any]] | None:
        """
        Scan all children of `node` whose position ordinal is >= node_pos,
        delegating each to the segment- or loop-match helper. Returns the
        first match's tuple, or None if no child matches (caller pops up
        and tries again at the parent loop).
        """
        for ord1 in [a for a in sorted(node.pos_map) if a >= node_pos]:
            for child in node.pos_map[ord1]:
                if child.is_segment():
                    result = self._try_match_segment_child(
                        node,
                        child,
                        seg_data,
                        orig_node,
                        seg_count,
                        cur_line,
                        ls_id,
                        pop_node_list,
                    )
                    if result is not None:
                        return result
                elif child.is_loop():
                    result = self._try_match_loop_child(
                        child,
                        seg_data,
                        seg_count,
                        cur_line,
                        ls_id,
                        pop_node_list,
                    )
                    if result is not None:
                        return result
        return None

    @staticmethod
    def _resolve_starting_loop(node: Any) -> tuple[Any, int]:
        """
        Return the enclosing loop (or map root) for the starting node, plus
        the original node's position ordinal — used to filter pos_map keys
        when scanning siblings at or after the start position.
        """
        node_pos = node.pos
        if not (node.is_loop() or node.is_map_root()):
            node = pop_to_parent_loop(node)
        return node, node_pos

    def _seg_not_found_error(
        self,
        orig_node: Any,
        seg_data: pyx12.segment.Segment,
        seg_count: int,
        cur_line: int,
        ls_id: str | None,
    ) -> None:
        """
        Accumulate a 'segment not found' error onto self.errors_pending.

        :param orig_node: Original starting node
        :type orig_node: L{node<map_if.x12_node>}
        :param seg_data: Segment object
        :type seg_data: L{segment<segment.Segment>}
        :param seg_count: Count of current segment in the ST Loop
        :type seg_count: int
        :param cur_line: Current line number in the file
        :type cur_line: int
        :param ls_id: The current LS loop identifier
        :type ls_id: string
        """
        if seg_data.get_seg_id() == "HL":
            seg_str = seg_data.format("", "*", ":")
        else:
            seg_str = "%s*%s" % (seg_data.get_seg_id(), seg_data.get_value("01"))
        err_str = "Segment %s not found.  Started at %s" % (seg_str, orig_node.get_path())
        self.errors_pending.append(
            SegError(
                err_cde="1",
                err_str=err_str,
                src_line=cur_line,
                map_node=orig_node,
                seg_data=seg_data,
                seg_count=seg_count,
                ls_id=ls_id,
            )
        )

    def _flush_mandatory_segs(self, cur_pos: int | None = None) -> None:
        """
        Move any outstanding mandatory-missing errors out of
        self.mandatory_segs_missing into self.errors_pending — except
        those whose seg_node.pos matches cur_pos (those can still be
        satisfied at the current position).

        :param cur_pos: Current segment position; entries at this
            position are kept in the buffer for possible later
            satisfaction.
        :type cur_pos: int or None
        """
        for m in self.mandatory_segs_missing:
            # Create errors if not also at current position
            if m.seg_node.pos != cur_pos:
                self.errors_pending.append(
                    SegError(
                        err_cde=m.err_cde,
                        err_str=m.err_str,
                        src_line=m.cur_line,
                        map_node=m.seg_node,
                        seg_data=m.seg_data,
                        seg_count=m.seg_count,
                        ls_id=m.ls_id,
                    )
                )
        self.mandatory_segs_missing = [
            m for m in self.mandatory_segs_missing if m.seg_node.pos == cur_pos
        ]

    def _record_loop_missing_if_required(
        self,
        loop_node: Any,
        first_child_node: Any,
        seg_count: int,
        cur_line: int,
        ls_id: str | None,
    ) -> None:
        """
        Accumulate a 'Mandatory loop missing' error if loop_node is required (R)
        and has not yet been entered. The error is filed against the loop's
        first child segment for later flushing via _flush_mandatory_segs.
        """
        if loop_node.usage != "R" or self.counter.get_count(loop_node.x12path) >= 1:
            return
        fake_seg = pyx12.segment.Segment(first_child_node.id, "~", "*", ":")
        err_str = 'Mandatory loop "%s" (%s) missing' % (loop_node.name, loop_node.id)
        self.mandatory_segs_missing.append(
            MissingMandatorySeg(
                first_child_node, fake_seg, "3", err_str, seg_count, cur_line, ls_id
            )
        )

    def _is_loop_match(
        self,
        loop_node: Any,
        seg_data: pyx12.segment.Segment,
        seg_count: int,
        cur_line: int,
        ls_id: str | None,
    ) -> bool:
        """
        Try to match the current loop to the segment.
        Handle loop and segment counting.
        Check for used/missing.

        :param loop_node: Loop Node
        :type loop_node: L{node<map_if.loop_if>}
        :param seg_data: Segment object
        :type seg_data: L{segment<segment.Segment>}
        :param seg_count: Count of current segment in the ST Loop
        :type seg_count: int
        :param cur_line: Current line number in the file
        :type cur_line: int
        :param ls_id: The current LS loop identifier
        :type ls_id: string

        :return: Does the segment match the first segment node in the loop?
        :rtype: boolean
        """
        if not loop_node.is_loop():
            raise EngineError(
                "Call to first_seg_match failed, node %s is not a loop. seg %s"
                % (loop_node.id, seg_data.get_seg_id())
            )
        if len(loop_node) <= 0:  # Has no children
            return False
        first_child_node = loop_node.get_first_node()
        if first_child_node is None:
            raise EngineError("get_first_node failed from loop %s" % (loop_node.id))
        if first_child_node.is_loop():
            # Wrapper loop: match if any direct child loop matches.
            return any(
                child.is_loop() and self._is_loop_match(child, seg_data, seg_count, cur_line, ls_id)
                for child in loop_node.childIterator()
            )
        if is_first_seg_match2(first_child_node, seg_data):
            return True
        self._record_loop_missing_if_required(
            loop_node, first_child_node, seg_count, cur_line, ls_id
        )
        return False

    def _enter_loop_at_first_seg(
        self,
        loop_node: Any,
        first_seg: Any,
        seg_data: pyx12.segment.Segment,
        seg_count: int,
        cur_line: int,
        ls_id: str | None,
    ) -> tuple[Any, list[Any]]:
        """
        Record entering loop_node via its first segment: check loop usage
        (counts/'4' if exceeded), increment the segment counter, flush
        any pending mandatory-missing errors. Returns the matched segment
        and the single-element push list [loop_node].
        """
        self._check_loop_usage(loop_node, seg_data, seg_count, cur_line, ls_id)
        self.counter.increment(first_seg.x12path)
        self._flush_mandatory_segs()
        return (first_seg, [loop_node])

    def _goto_seg_match(
        self,
        loop_node: Any,
        seg_data: pyx12.segment.Segment,
        seg_count: int,
        cur_line: int,
        ls_id: str | None,
    ) -> tuple[Any, list[Any]]:
        """
        A child loop has matched the segment.  Return that segment node.
        Handle loop counting and requirement errors.

        :param loop_node: The starting loop node.
        :type loop_node: L{node<map_if.loop_if>}
        :param seg_data: Segment object
        :type seg_data: L{segment<segment.Segment>}
        :param seg_count: Current segment count for ST loop
        :type seg_count: int
        :param cur_line: File line counter
        :type cur_line: int
        :param ls_id: The current LS loop identifier
        :type ls_id: string

        :return: The matching segment node and a list of the push loop nodes
        :rtype: (L{node<map_if.segment_if>}, [L{node<map_if.loop_if>}])
        """
        if not loop_node.is_loop():
            raise EngineError(
                "_goto_seg_match failed, node %s is not a loop. seg %s"
                % (loop_node.id, seg_data.get_seg_id())
            )
        first_seg = loop_node.get_first_seg()
        if first_seg is not None and is_first_seg_match2(first_seg, seg_data):
            return self._enter_loop_at_first_seg(
                loop_node, first_seg, seg_data, seg_count, cur_line, ls_id
            )
        for child in loop_node.childIterator():
            if not child.is_loop():
                continue
            seg_node, push = self._goto_seg_match(child, seg_data, seg_count, cur_line, ls_id)
            if seg_node is not None:
                return (seg_node, [loop_node, *push])
        return (None, [])

    def _check_loop_usage(
        self,
        loop_node: Any,
        seg_data: pyx12.segment.Segment,
        seg_count: int,
        cur_line: int,
        ls_id: str | None,
    ) -> None:
        """
        Check loop usage requirement and count. Any violations are
        appended to self.errors_pending; the caller flushes them via
        apply_walk_errors at the end of walk_errors().

        :param loop_node: Loop X12 node to verify
        :type loop_node: L{node<map_if.loop_if>}
        :param seg_data: Segment object
        :type seg_data: L{segment<segment.Segment>}
        :param seg_count: Count of current segment in the ST Loop
        :type seg_count: int
        :param cur_line: Current line number in the file
        :type cur_line: int
        :param ls_id: The current LS loop identifier
        :type ls_id: string
        :raises EngineError: On invalid usage code
        """
        if not loop_node.is_loop():
            raise EngineError(
                "Node %s is not a loop. seg %s" % (loop_node.id, seg_data.get_seg_id())
            )
        if loop_node.usage not in ("N", "R", "S"):
            raise EngineError("Loop usage must be R, S, or N (got %r)" % (loop_node.usage,))
        if loop_node.usage == "N":
            err_str = "Loop %s found but marked as not used" % (loop_node.id)
            self.errors_pending.append(SegError(err_cde="2", err_str=err_str, src_line=cur_line))
        elif loop_node.usage in ("R", "S"):
            self.counter.reset_to_node(loop_node.x12path)
            self.counter.increment(loop_node.x12path)
            if self.counter.get_count(loop_node.x12path) > loop_node.get_max_repeat():
                err_str = "Loop %s exceeded max count.  Found %i, should have %i" % (
                    loop_node.id,
                    self.counter.get_count(loop_node.x12path),
                    loop_node.get_max_repeat(),
                )
                self.errors_pending.append(
                    SegError(
                        err_cde="4",
                        err_str=err_str,
                        src_line=cur_line,
                        map_node=loop_node,
                        seg_data=seg_data,
                        seg_count=seg_count,
                        ls_id=ls_id,
                    )
                )
