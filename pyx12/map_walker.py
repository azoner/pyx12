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

import logging

# Intrapackage imports
from errors import EngineError
import pyx12.segment
from nodeCounter import NodeCounter

logger = logging.getLogger('pyx12.walk_tree')
#logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)


def pop_to_parent_loop(node):
    """
    @param node: Loop Node
    @type node: L{node<map_if.x12_node>}
    @return: Closest parent loop node
    @rtype: L{node<map_if.x12_node>}
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


def is_first_seg_match2(child, seg_data):
    """
    Find the first segment in loop, verify it matches segment

    @param child: child node
    @type child: L{node<map_if.x12_node>}
    @param seg_data: Segment object
    @type seg_data: L{segment<segment.Segment>}
    @rtype: boolean
    """
    if child.is_segment():
        if child.is_match(seg_data):
            return True
        else:
            # seg does not match the first segment in loop, so not valid
            return False
    return False


def get_id_list(node_list):
    # get_id_list(pop)
    ret = []
    for node in node_list:
        if node is not None:
            ret.append(node.id)
    return ret


def traverse_path(start_node, pop_loops, push_loops):
    """
    Debug function - From the start path, pop up then push down to get a path string
    """
    start_path = pop_to_parent_loop(start_node).get_path()
    p1 = [p for p in start_path.split('/') if p != '']
    for loop_id in get_id_list(pop_loops):
        assert loop_id == p1[-1], 'Path %s does not contain %s' % (start_path, loop_id)
        p1 = p1[:-1]
    for loop_id in get_id_list(push_loops):
        p1.append(loop_id)
    return '/' + '/'.join(p1)


class walk_tree(object):
    """
    Walks a map_if tree.  Tracks loop/segment counting, missing loop/segment.
    """
    def __init__(self, initialCounts=None):
        # Store errors until we know we have an error
        self.mandatory_segs_missing = []
        if initialCounts is None:
            initialCounts = {}
        self.counter = NodeCounter(initialCounts)

    def walk(self, node, seg_data, errh, seg_count, cur_line, ls_id):
        """
        Walk the node tree from the starting node to the node matching
        seg_data. Catch any counting or requirement errors along the way.

        Handle required segment/loop missed (not found in seg)
        Handle found segment = Not used

        @param node: Starting node
        @type node: L{node<map_if.x12_node>}
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        @param seg_count: Count of current segment in the ST Loop
        @type seg_count: int
        @param cur_line: Current line number in the file
        @type cur_line: int
        @param ls_id: The current LS loop identifier
        @type ls_id: string
        @return: The matching x12 segment node, a list of x12 popped loops, and a list
            of x12 pushed loops from the start segment to the found segment
        @rtype: (L{node<map_if.segment_if>}, [L{node<map_if.loop_if>}], [L{node<map_if.loop_if>}])

        @todo: check single segment loop repeat
        """
        pop_node_list = []
        push_node_list = []
        orig_node = node
        #logger.info('%s seg_count=%i / cur_line=%i' % (node.id, seg_count, cur_line))
        self.mandatory_segs_missing = []
        node_pos = node.pos  # Get original position ordinal of starting node
        if not (node.is_loop() or node.is_map_root()):
            node = pop_to_parent_loop(node)  # Get enclosing loop
            #node_list.append(node)
        while True:
            # Iterate through nodes with position >= current position
            for ord1 in [a for a in sorted(node.pos_map) if a >= node_pos]:
                for child in node.pos_map[ord1]:
                    if child.is_segment():
                        if child.is_match(seg_data):
                            # Is the matched segment the beginning of a loop?
                            if node.is_loop() \
                                    and self._is_loop_match(node, seg_data, errh, seg_count, cur_line, ls_id):
                                (
                                    node1, push_node_list) = self._goto_seg_match(node, seg_data,
                                                                                  errh, seg_count, cur_line, ls_id)
                                if orig_node.is_loop() or orig_node.is_map_root():
                                    orig_loop = orig_node
                                else:
                                    orig_loop = pop_to_parent_loop(orig_node)  # Get enclosing loop
                                if node == orig_loop:
                                    pop_node_list = [node]
                                    push_node_list = [node]
                                return (node1, pop_node_list, push_node_list)  # segment node
                            #child.incr_cur_count()
                            self.counter.increment(child.x12path)
                            #assert child.get_cur_count() == self.counter.get_count(child.x12path), \
                            #    'child counts not equal: old is %s=%i : new is %s=%i' % (
                            #    child.get_path(), child.get_cur_count(),
                            #    child.x12path.format(), self.counter.get_count(child.x12path))
                            self._check_seg_usage(child, seg_data, seg_count, cur_line, ls_id, errh)
                            # Remove any previously missing errors for this segment
                            self.mandatory_segs_missing = [x for x in self.mandatory_segs_missing if x[0] != child]
                            self._flush_mandatory_segs(errh, child.pos)
                            return (child, pop_node_list, push_node_list)  # segment node
                        elif child.usage == 'R' and self.counter.get_count(child.x12path) < 1:
                            fake_seg = pyx12.segment.Segment('%s' % (child.id), '~', '*', ':')
                            err_str = 'Mandatory segment "%s" (%s) missing' % (child.name, child.id)
                            self.mandatory_segs_missing.append((child, fake_seg, '3', err_str, seg_count, cur_line, ls_id))
                        #else:
                            #logger.debug('Segment %s is not a match for (%s*%s)' % \
                            #   (child.id, seg_data.get_seg_id(), seg_data[0].get_value()))
                    elif child.is_loop():
                        if self._is_loop_match(child, seg_data, errh, seg_count, cur_line, ls_id):
                            (node_seg, push_node_list) = self._goto_seg_match(child, seg_data, errh, seg_count, cur_line, ls_id)
                            return (node_seg, pop_node_list, push_node_list)  # segment node
            # End for ord1 in pos_keys
            if node.is_map_root():  # If at root and we haven't found the segment yet.
                walk_tree._seg_not_found_error(orig_node, seg_data,
                                               errh, seg_count, cur_line, ls_id)
                return (None, [], [])
            node_pos = node.pos  # Get position ordinal of current node in tree
            pop_node_list.append(node)
            node = pop_to_parent_loop(node)  # Get enclosing parent loop

        walk_tree._seg_not_found_error(orig_node, seg_data, errh, seg_count, cur_line, ls_id)
        return (None, [], [])

    def getCountState(self):
        return self.counter.getState()

    def setCountState(self, initialCounts={}):
        self.counter = NodeCounter(initialCounts)

    def forceWalkCounterToLoopStart(self, x12_path, child_path):
        # delete child counts under the x12_path, no longer needed
        self.counter.reset_to_node(x12_path)
        self.counter.increment(x12_path)  # add a count for this path
        self.counter.increment(child_path) # count the loop start segment

    def _check_seg_usage(self, seg_node, seg_data, seg_count, cur_line, ls_id, errh):
        """
        Check segment usage requirement and count

        @param seg_node: Segment X12 node to verify
        @type seg_node: L{node<map_if.segment_if>}
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        @param seg_count: Count of current segment in the ST Loop
        @type seg_count: int
        @param cur_line: Current line number in the file
        @type cur_line: int
        @param ls_id: The current LS loop identifier
        @type ls_id: string
        @param errh: Error handler
        @type errh: L{error_handler.err_handler}
        @raise EngineError: On invalid usage code
        """
        assert seg_node.usage in ('N', 'R', 'S'), 'Segment usage must be R, S, or N'
        if seg_node.usage == 'N':
            err_str = "Segment %s found but marked as not used" % (seg_node.id)
            errh.seg_error('2', err_str, None)
        elif seg_node.usage == 'R' or seg_node.usage == 'S':
            #assert seg_node.get_cur_count() == self.counter.get_count(seg_node.x12path), 'seg_node counts not equal'
            if self.counter.get_count(seg_node.x12path) > seg_node.get_max_repeat():  # handle seg repeat count
                err_str = "Segment %s exceeded max count.  Found %i, should have %i" \
                    % (seg_data.get_seg_id(), self.counter.get_count(seg_node.x12path), seg_node.get_max_repeat())
                errh.add_seg(seg_node, seg_data, seg_count, cur_line, ls_id)
                errh.seg_error('5', err_str, None)

    @staticmethod
    def _seg_not_found_error(orig_node, seg_data, errh, seg_count, cur_line, ls_id):
        """
        Create error for not found segments

        @param orig_node: Original starting node
        @type orig_node: L{node<map_if.x12_node>}
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        @param errh: Error handler
        @type errh: L{error_handler.err_handler}
        """
        if seg_data.get_seg_id() == 'HL':
            seg_str = seg_data.format('', '*', ':')
        else:
            seg_str = '%s*%s' % (seg_data.get_seg_id(), seg_data.get_value('01'))
        err_str = 'Segment %s not found.  Started at %s' % (seg_str, orig_node.get_path())
        errh.add_seg(orig_node, seg_data, seg_count, cur_line, ls_id)
        errh.seg_error('1', err_str, None)

    def _flush_mandatory_segs(self, errh, cur_pos=None):
        """
        Handle error reporting for any outstanding missing mandatory segments

        @param errh: Error handler
        @type errh: L{error_handler.err_handler}
        """
        for (seg_node, seg_data, err_cde, err_str, seg_count, cur_line, ls_id) in self.mandatory_segs_missing:
            # Create errors if not also at current position
            if seg_node.pos != cur_pos:
                errh.add_seg(seg_node, seg_data, seg_count, cur_line, ls_id)
                errh.seg_error(err_cde, err_str, None)
        self.mandatory_segs_missing = [x for x in self.mandatory_segs_missing if x[0].pos == cur_pos]

    def _is_loop_match(self, loop_node, seg_data, errh, seg_count, cur_line, ls_id):
        """
        Try to match the current loop to the segment
        Handle loop and segment counting.
        Check for used/missing

        @param loop_node: Loop Node
        @type loop_node: L{node<map_if.loop_if>}
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        @param errh: Error handler
        @type errh: L{error_handler.err_handler}

        @return: Does the segment match the first segment node in the loop?
        @rtype: boolean
        """
        assert loop_node.is_loop(), "Call to first_seg_match failed, node %s is not a loop. seg %s" \
            % (loop_node.id, seg_data.get_seg_id())
        #if loop_node.id not in ('ISA_LOOP', 'GS_LOOP'):
        #    assert loop_node.get_cur_count() == self.counter.get_count(loop_node.x12path), \
        #        'loop_node counts not equal: old is %s=%i : new is %s=%i' % (
        #        loop_node.get_path(), loop_node.get_cur_count(),
        #        loop_node.x12path.format(), self.counter.get_count(loop_node.x12path))
        if len(loop_node) <= 0:  # Has no children
            return False
        first_child_node = loop_node.get_first_node()
        assert first_child_node is not None, 'get_first_node failed from loop %s' % (loop_node.id)
        if first_child_node.is_loop():
            #If any loop node matches
            for child_node in loop_node.childIterator():
                if child_node.is_loop() and self._is_loop_match(child_node,
                                                                seg_data, errh, seg_count, cur_line, ls_id):
                    return True
        elif is_first_seg_match2(first_child_node, seg_data):
            return True
        elif loop_node.usage == 'R' and self.counter.get_count(loop_node.x12path) < 1:
            fake_seg = pyx12.segment.Segment('%s' % (first_child_node.id), '~', '*', ':')
            err_str = 'Mandatory loop "%s" (%s) missing' % \
                (loop_node.name, loop_node.id)
            self.mandatory_segs_missing.append((first_child_node, fake_seg,
                                                '3', err_str, seg_count, cur_line, ls_id))
        return False

    def _goto_seg_match(self, loop_node, seg_data, errh, seg_count, cur_line, ls_id):
        """
        A child loop has matched the segment.  Return that segment node.
        Handle loop counting and requirement errors.

        @param loop_node: The starting loop node.
        @type loop_node: L{node<map_if.loop_if>}
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        @param errh: Error handler
        @type errh: L{error_handler.err_handler}
        @param seg_count: Current segment count for ST loop
        @type seg_count: int
        @param cur_line: File line counter
        @type cur_line: int
        @type ls_id: string

        @return: The matching segment node and a list of the push loop nodes
        @rtype: (L{node<map_if.segment_if>}, [L{node<map_if.loop_if>}])
        """
        assert loop_node.is_loop(), "_goto_seg_match failed, node %s is not a loop. seg %s" \
            % (loop_node.id, seg_data.get_seg_id())
        first_child_node = loop_node.get_first_seg()
        if first_child_node is not None and is_first_seg_match2(first_child_node, seg_data):
            self._check_loop_usage(loop_node, seg_data,
                                   seg_count, cur_line, ls_id, errh)
            #first_child_node.incr_cur_count()
            self.counter.increment(first_child_node.x12path)
            #assert first_child_node.get_cur_count() == self.counter.get_count(first_child_node.x12path), 'first_child_node counts not equal'
            self._flush_mandatory_segs(errh)
            return (first_child_node, [loop_node])
        else:
            for child in loop_node.childIterator():
                if child.is_loop():
                    (
                        node1, push1) = self._goto_seg_match(child, seg_data, errh,
                                                             seg_count, cur_line, ls_id)
                    if node1:
                        push_node_list = [loop_node]
                        push_node_list.extend(push1)
                        return (node1, push_node_list)
        return (None, [])

    def _check_loop_usage(self, loop_node, seg_data, seg_count, cur_line, ls_id, errh):
        """
        Check loop usage requirement and count

        @param loop_node: Loop X12 node to verify
        @type loop_node: L{node<map_if.loop_if>}
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        @param seg_count: Count of current segment in the ST Loop
        @type seg_count: int
        @param cur_line: Current line number in the file
        @type cur_line: int
        @param ls_id: The current LS loop identifier
        @type ls_id: string
        @param errh: Error handler
        @type errh: L{error_handler.err_handler}
        @raise EngineError: On invalid usage code
        """
        assert loop_node.is_loop(), "Node %s is not a loop. seg %s" % (
            loop_node.id, seg_data.get_seg_id())
        assert loop_node.usage in ('N', 'R', 'S'), 'Loop usage must be R, S, or N'
        if loop_node.usage == 'N':
            err_str = "Loop %s found but marked as not used" % (loop_node.id)
            errh.seg_error('2', err_str, None)
        elif loop_node.usage in ('R', 'S'):
            #if loop_node.id == '2110':
            #    import ipdb; ipdb.set_trace()
            #loop_node.reset_child_count()
            self.counter.reset_to_node(loop_node.x12path)
            #loop_node.incr_cur_count()
            self.counter.increment(loop_node.x12path)
            #assert loop_node.get_cur_count() == self.counter.get_count(loop_node.x12path), \
            #    'loop_node counts not equal: old is %s=%i : new is %s=%i' % (
            #    loop_node.get_path(), loop_node.get_cur_count(),
            #    loop_node.x12path.format(), self.counter.get_count(loop_node.x12path))
            #logger.debug('incr loop_node %s %i' % (loop_node.id, loop_node.cur_count))
            #logger.debug('incr first_child_node %s %i' % (first_child_node.id, first_child_node.cur_count))
            if self.counter.get_count(loop_node.x12path) > loop_node.get_max_repeat():
                err_str = "Loop %s exceeded max count.  Found %i, should have %i" \
                    % (loop_node.id, self.counter.get_count(loop_node.x12path), loop_node.get_max_repeat())
                errh.add_seg(loop_node, seg_data, seg_count, cur_line, ls_id)
                errh.seg_error('4', err_str, None)
            #logger.debug('MATCH Loop %s / Segment %s (%s*%s)' \
            #    % (child.id, first_child_node.id, seg_data.get_seg_id(), seg[0].get_value()))
