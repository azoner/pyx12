######################################################################
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Walk a tree of x12_map nodes.  Find the correct node.

If seg indicates a loop has been entered, returns the first child segment node.
If seg indicates a segment has been entered, returns the segment node.
"""

import logging
import pdb

# Intrapackage imports
from errors import *
import pyx12.segment

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
        raise EngineError, "Node is None: %s" % (node.name)
    while not (map_node.is_loop() or map_node.is_map_root()): 
        map_node = map_node.parent
    if not (map_node.is_loop() or map_node.is_map_root()):
        raise EngineError, "Called pop_to_parent_loop, can't find parent loop"
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
            return False # seg does not match the first segment in loop, so not valid
    return False


class walk_tree(object):
    """
    Walks a map_if tree.  Tracks loop/segment counting, missing loop/segment.
    """
    def __init__(self):
#        end_tag_stack = []
        #self.cur_seg_count = 0
        self.mandatory_segs_missing = []  # Store errors until we know we have an error
        pass

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
        @return: The matching x12_node
        @rtype: L{node<map_if.x12_node>}

        @todo: check single segment loop repeat
        """

        #if seg_data.get_seg_id() == 'LX':
        #    pdb.set_trace()
        #logger.debug('start walk %s' % (node))
        orig_node = node
        #logger.info('%s seg_count=%i / cur_line=%i' % (node.id, seg_count, cur_line))
        self.mandatory_segs_missing = []
        node_pos = node.pos # Get original position ordinal of starting node
        if not (node.is_loop() or node.is_map_root()): 
            node = pop_to_parent_loop(node) # Get enclosing loop
        while True:
            #logger.debug('seg_data.id % ' % (seg_data.get_seg_id()))
            # Iterate through nodes with position >= current position
            pos_keys = filter(lambda a: a>= node_pos, node.pos_map.keys())
            pos_keys.sort()
            for ord1 in pos_keys:
            #for child in node.children:
                #logger.debug('id=%s child.index=%i node_pos=%i' % \
                #    (child.id, child.index, node_pos))
                for child in node.pos_map[ord1]:
                #if child.pos >= node_pos:
                    if child.is_segment():
                        #logger.debug('id=%s cur_count=%i max_repeat=%i' \
                        #    % (child.id, child.cur_count, child.get_max_repeat()))
                        if child.is_match(seg_data):
                            # Is the matched segment the beginning of a loop?
                            if node.is_loop() \
                                    and self._is_loop_match(node, seg_data, errh, seg_count, cur_line, ls_id):
                                node1 = self._goto_seg_match(node, seg_data, \
                                    errh, seg_count, cur_line, ls_id)
                                return node1
                                #return node1.get_child_node_by_idx(0)
                            child.incr_cur_count()
                            #logger.debug('MATCH segment %s (%s*%s)' % (child.id,\
                            #   seg_data.get_seg_id(), seg_data[0].get_value()))
                            if child.usage == 'N':
                                err_str = "Segment %s found but marked as not used" % (child.id)
                                errh.seg_error('2', err_str, None)
                            elif child.usage == 'R' or child.usage == 'S':
                                if child.get_cur_count() > child.get_max_repeat():  # handle seg repeat count
                                    err_str = "Segment %s exceeded max count.  Found %i, should have %i" \
                                        % (seg_data.get_seg_id(), child.get_cur_count(), child.get_max_repeat())
                                    errh.add_seg(child, seg_data, seg_count, cur_line, ls_id)
                                    errh.seg_error('5', err_str, None)
                            else:
                                raise EngineError, 'Usage must be R, S, or N'
                            # Remove any previously missing errors for this segment
                            self.mandatory_segs_missing = filter(lambda x: x[0]!=child, 
                                self.mandatory_segs_missing)
                            self._flush_mandatory_segs(errh, child.pos)
                            return child
                        elif child.usage == 'R' and child.get_cur_count() < 1:
                            fake_seg = pyx12.segment.Segment('%s'% (child.id), '~', '*', ':')
                            #errh.add_seg(child, fake_seg, seg_count, cur_line, ls_id)
                            err_str = 'Mandatory segment "%s" (%s) missing' % (child.name, child.id)
                            self.mandatory_segs_missing.append((child, fake_seg,
                                '3', err_str, seg_count, cur_line, ls_id))
                        #else:
                            #logger.debug('Segment %s is not a match for (%s*%s)' % \
                            #   (child.id, seg_data.get_seg_id(), seg_data[0].get_value()))
                    elif child.is_loop(): 
                        #logger.debug('child_node id=%s' % (child.id))
                        if self._is_loop_match(child, seg_data, errh, \
                                seg_count, cur_line, ls_id):
                            node_seg = self._goto_seg_match(child, seg_data, \
                                errh, seg_count, cur_line, ls_id)
                            #node_seg = child.get_child_node_by_idx(0)
                            return node_seg
            if node.is_map_root(): # If at root and we haven't found the segment yet.
                self._seg_not_found(orig_node, seg_data, errh, seg_count, \
                    cur_line, ls_id)
                return None
            node_pos = node.pos # Get position ordinal of current node in tree
            node = pop_to_parent_loop(node) # Get enclosing parent loop

        self._seg_not_found(orig_node, seg_data, errh, seg_count, cur_line, ls_id)
        return None

#    def _is_loop_repeat(self, node, seg_data):
#        if not (node.is_loop() or node.is_map_root()): 
#            node = pop_to_parent_loop(node) # Get enclosing loop
#        return self._is_first_seg_match(node, seg_data):

    def _seg_not_found(self, orig_node, seg_data, errh, seg_count, cur_line, ls_id):
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
        #raise EngineError, "Could not find segment %s*%s.  Started at %s" % \
        #    (seg.get_seg_id(), seg[1], orig_node.get_path())

#    def _is_first_seg_match(self, node, seg_data):
#        """
#        Find the first segment in loop, verify it matches segment
#        @rtype: boolean
#        """
#        if not node.is_loop(): raise EngineError, \
#            "Call to first_seg_match failed, node is not a loop"
#        child = node.get_child_node_by_idx(0)
#        if child.is_segment():
#            if child.is_match(seg_data):
#                return True
#            else:
#                return False # seg does not match the first segment in loop, so not valid
#        return False

    def _flush_mandatory_segs(self, errh, cur_pos = None):
        """
        Handle error reporting for any outstanding missing mandatory segments

        @param errh: Error handler
        @type errh: L{error_handler.err_handler}
        """
        #if self.mandatory_segs_missing: pdb.set_trace()
        for (seg_node, seg_data, err_cde, err_str, 
                seg_count, cur_line, ls_id) in self.mandatory_segs_missing:
            # Create errors if not also at current position
            if seg_node.pos != cur_pos:
                errh.add_seg(seg_node, seg_data, seg_count, cur_line, ls_id)
                errh.seg_error(err_cde, err_str, None)
        self.mandatory_segs_missing = filter(lambda x: x[0].pos==cur_pos, 
            self.mandatory_segs_missing)
        #self.mandatory_segs_missing = []

    #def _is_loop_match(self, loop_node, seg_data, errh, seg_count, cur_line, ls_id):
    #    if not loop_node.is_loop(): raise EngineError, \
    #        "Call to first_seg_match failed, node %s is not a loop. seg %s" \
    #        % (loop_node.id, seg_data.get_seg_id())

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
        #if seg_data.get_seg_id() == 'HL':
        #    pdb.set_trace()
        if not loop_node.is_loop(): raise EngineError, \
            "Call to first_seg_match failed, node %s is not a loop. seg %s" \
            % (loop_node.id, seg_data.get_seg_id())
        if len(loop_node) <= 0: # Has no children
            return False
        #first_child_node = loop_node.get_child_node_by_idx(0)
        pos_keys = loop_node.pos_map.keys()
        pos_keys.sort()
        #min_pos = reduce(min, loop_node.pos_map.keys())
        first_child_node = loop_node.pos_map[pos_keys[0]][0]
        if first_child_node.is_loop():
            #If any loop node matches
            for ord1 in pos_keys:
                for child_node in loop_node.pos_map[ord1]:
                    if child_node.is_loop() and self._is_loop_match(child_node, \
                            seg_data, errh, seg_count, cur_line, ls_id):
                        return True
        elif is_first_seg_match2(first_child_node, seg_data): 
            return True
        elif loop_node.usage == 'R' and loop_node.get_cur_count() < 1:
            #pdb.set_trace()
            fake_seg = pyx12.segment.Segment('%s' % \
                (first_child_node.id), '~', '*', ':')
            #errh.add_seg(first_child_node, fake_seg, seg_count, cur_line, ls_id)
            err_str = 'Mandatory loop "%s" (%s) missing' % \
                (loop_node.name, loop_node.id)
            self.mandatory_segs_missing.append((first_child_node, fake_seg, \
                '3', err_str, seg_count, cur_line, ls_id))
            #errh.seg_error('3', err_str, None)
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

        @return: The matching segment node
        @rtype: L{node<map_if.segment_if>}
        """
        if not loop_node.is_loop(): raise EngineError, \
            "_goto_seg_match failed, node %s is not a loop. seg %s" \
            % (loop_node.id, seg_data.get_seg_id())
        #first_child_node = loop_node.get_child_node_by_idx(0)
        pos_keys = loop_node.pos_map.keys()
        pos_keys.sort()
        first_child_node = loop_node.pos_map[pos_keys[0]][0]
        if is_first_seg_match2(first_child_node, seg_data): 
            if loop_node.usage == 'N':
                err_str = "Loop %s found but marked as not used" % (loop_node.id)
                errh.seg_error('2', err_str, None)
            elif loop_node.usage in ('R', 'S'):
                loop_node.reset_child_count()
                loop_node.incr_cur_count()
                #logger.debug('incr loop_node %s %i' % (loop_node.id, loop_node.cur_count))
                first_child_node.incr_cur_count()
                #logger.debug('incr first_child_node %s %i' % (first_child_node.id, first_child_node.cur_count))
                if loop_node.get_cur_count() > loop_node.get_max_repeat():
                    err_str = "Loop %s exceeded max count.  Found %i, should have %i" \
                        % (loop_node.id, loop_node.get_cur_count(), loop_node.get_max_repeat())
                    errh.add_seg(loop_node, seg_data, seg_count, cur_line, ls_id)
                    errh.seg_error('4', err_str, None)
                #logger.debug('MATCH Loop %s / Segment %s (%s*%s)' \
                #    % (child.id, first_child_node.id, seg_data.get_seg_id(), seg[0].get_value()))
            else:
                raise EngineError, 'Usage must be R, S, or N'
            self._flush_mandatory_segs(errh)
            return first_child_node
        else:
            #for child in loop_node.children:
            for ord1 in pos_keys:
                for child in loop_node.pos_map[ord1]:
                    if child.is_loop():
                        node1 = self._goto_seg_match(child, seg_data, errh, \
                            seg_count, cur_line, ls_id)
                        if node1:
                            return node1
        return None
