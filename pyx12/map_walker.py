#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#                John Holland <jholland@kazoocmh.org> <john@zoner.org>
#
#    All rights reserved.
#
#        Redistribution and use in source and binary forms, with or without
#        modification, are permitted provided that the following conditions are
#        met:
#
#        1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer. 
#        
#        2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution. 
#        
#        3. The name of the author may not be used to endorse or promote
#        products derived from this software without specific prior written
#        permission. 
#
#        THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#        IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#        DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
#        INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#        (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#        SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#        HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#        STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#        IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#        POSSIBILITY OF SUCH DAMAGE.

"""
Walk a tree of x12_map nodes.  Find the correct node.

If seg indicates a loop has been entered, returns the loop node
If seg indicates a segment has been entered, returns the segment node
"""

import logging
import pdb
#import string

# Intrapackage imports
from errors import *
#import codes
#import map_index
#import map_if
#import x12file
#from utils import *
import pyx12.segment

logger = logging.getLogger('pyx12.walk_tree')
#logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)

class walk_tree:
    def __init__(self):
#        end_tag_stack = []
        #self.cur_seg_count = 0
        #self.mandatory_segs_missing = []  # Store errors until we know we have an error
        pass

    def walk(self, node, seg_data, errh, seg_count, cur_line, ls_id):
        """
        Handle required segment/loop missed (not found in seg)
        Handle found segment = Not used
        """

        #logger.info('%s seg_count=%i / cur_line=%i' % (node.id, seg_count, cur_line))
        if not seg_data.get_seg_id():
            err_str = 'Segment identifier is blank'
            errh.seg_error('1', err_str)
            return None

        if not self.is_seg_id_valid(seg_data.get_seg_id()):
            err_str = 'Segment identifier %s is invalid' % (seg_data.get_seg_id())
            errh.seg_error('1', err_str)
            return None

        orig_node = node

        # Special Handlers for ISA, GS, ST
        while not node.is_map_root():
            node = self.pop_to_parent_loop(node) # Get root node
        if orig_node.id == 'SE' and seg_data.get_seg_id() == 'ST':
            return node.getnodebypath('/ST')
        if orig_node.id == 'GE' and seg_data.get_seg_id() == 'GS':
            return node.getnodebypath('/GS')
        if orig_node.id == 'IEA' and seg_data.get_seg_id() == 'ISA':
            return node.getnodebypath('/ISA')

        if orig_node.id in ['ST']: #, 'GS', 'ISA']:
            orig_node.cur_count = 1

        node = orig_node
        #self.mandatory_segs_missing = []
        node_idx = node.index # Get original index of starting node
        if not (node.is_loop() or node.is_map_root()): 
            node = self.pop_to_parent_loop(node) # Get enclosing loop
        while 1:
            #logger.debug(seg_data.get_seg_id())
            for child in node.children:
                #logger.debug('id=%s child.index=%i node_idx=%i' % \
                #    (child.id, child.index, node_idx))
                if child.index >= node_idx:
                    #logger.debug('id=%s cur_count=%i max_repeat=%i' \
                    #    % (child.id, child.cur_count, child.get_max_repeat()))
                    if child.is_segment():
                        if child.is_match(seg_data):
                            #logger.debug('MATCH segment %s (%s*%s)' % (child.id,\
                            #   seg_data.get_seg_id(), seg_data[0].get_value()))
                            if child.usage == 'N':
                                err_str = "Segment %s found but marked as not used" % (child.id)
                                errh.seg_error('2', err_str, None)
                            elif child.usage == 'R' or child.usage == 'S':
                                if child is orig_node:
                                    #logger.debug('child %s IS orig_node %s' % (child.id, orig_node.id))
                                    child.cur_count += 1 # Repeat of segment
                                else:
                                    if orig_node.is_segment():
                                        orig_node.cur_count = 0 # Reset count of original node
                                        #logger.debug('Set orig_node %s cur_count = 0' % (orig_node.id))
                                    child.cur_count = 1
                                    #logger.debug('Set child %s cur_count = 1' % (orig_node.id))
                                if child.cur_count > child.get_max_repeat():  # handle seg repeat count
                                    if self._is_loop_match(node, seg_data, errh, seg_count, cur_line, ls_id):
                                        return node.get_child_node_by_idx(0)
                                    else:
                                        err_str = "Segment %s exceeded max count.  Found %i, should have %i" \
                                            % (seg_data.get_seg_id(), child.cur_count, child.get_max_repeat())
                                        errh.seg_error('5', err_str, None)
                            else:
                                raise EngineError, 'Usage must be R, S, or N'
                            #self._flush_mandatory_segs(errh)
                            return child
                        elif child.usage == 'R' and child.cur_count < 1:
                            fake_seg = pyx12.segment.segment('%s'% (child.id), '~', '*', ':')
                            errh.add_seg(child, fake_seg, seg_count, cur_line, ls_id)
                            err_str = "Mandatory segment %s missing" % (child.id)
                            #self.mandatory_segs_missing.append((seg_data.get_seg_id(), '3', err_str))
                            errh.seg_error('3', err_str, None)
                        #else:
                            #logger.debug('Segment %s is not a match for (%s*%s)' % \
                            #   (child.id, seg_data.get_seg_id(), seg_data[0].get_value()))
                    elif child.is_loop(): 
                        #logger.debug('child_node id=%s' % (child.id))
                        if self._is_loop_match(child, seg_data, errh, seg_count, cur_line, ls_id):
                            return child.get_child_node_by_idx(0)
            if node.is_map_root(): # If at root and we haven't found the segment yet.
                self._seg_not_found(orig_node, seg_data, errh)
                return None
            node_idx = node.index # Get index of current node in tree
            node = self.pop_to_parent_loop(node) # Get enclosing parent loop

        self._seg_not_found(orig_node, seg_data, errh)
        return None

#    def _is_loop_repeat(self, node, seg_data):
#        if not (node.is_loop() or node.is_map_root()): 
#            node = self.pop_to_parent_loop(node) # Get enclosing loop
#        return self.is_first_seg_match(node, seg_data):

    def _seg_not_found(self, orig_node, seg_data, errh):
        if seg_data.get_seg_id() == 'HL':
            seg_str = seg_data.format('', '*', ':')
        else:
            seg_str = '%s*%s' % (seg_data.get_seg_id(), seg_data[0][0].get_value())
        err_str = 'Segment %s not found.  Started at %s' % (seg_str, orig_node.get_path()) 
        errh.seg_error('1', err_str, None)
        #raise EngineError, "Could not find segment %s*%s.  Started at %s" % \
        #    (seg.get_seg_id(), seg[1], orig_node.get_path())

    def pop_to_parent_loop(self, node):
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

    def is_seg_id_valid(self, seg_id):
        if len(seg_id) < 2 or len(seg_id) > 3:
            return False
        else:
            return True

    def is_first_seg_match(self, node, seg_data):
        """
        Find the first segment in loop, verify it matches segment
        Return: boolean
        """
        if not node.is_loop(): raise EngineError, \
            "Call to first_seg_match failed, node is not a loop"
        child = node.get_child_node_by_idx(0)
        if child.is_segment():
            if child.is_match(seg_data):
                return True
            else:
                return False # seg does not match the first segment in loop, so not valid
        return False

    def is_first_seg_match2(self, child, seg_data):
        """
        Find the first segment in loop, verify it matches segment
        Return: boolean
        """
        if child.is_segment():
            if child.is_match(seg_data):
                return True
            else:
                return False # seg does not match the first segment in loop, so not valid
        return False


    #def _flush_mandatory_segs(self, errh):
    #    for (seg_id, err_cde, err_str) in self.mandatory_segs_missing:
    #        errh.seg_error(err_cde, err_str, None)
    #    self.mandatory_segs_missing = []

    def _is_loop_match(self, loop_node, seg_data, errh, seg_count, cur_line, ls_id):
        """
        Try to match the current loop to the segment
        Handle loop and segment counting.
        Check for used/missing
        """
        if not loop_node.is_loop(): raise EngineError, \
            "Call to first_seg_match failed, node is not a loop"
        first_child_node = loop_node.get_child_node_by_idx(0)
        if self.is_first_seg_match2(first_child_node, seg_data): 
            #node = loop_node.children[0]
            if loop_node.usage == 'N':
                err_str = "Loop %s found but marked as not used" % (loop_node.id)
                errh.seg_error('2', err_str, None)
            elif loop_node.usage == 'R' or loop_node.usage == 'S':
                loop_node.cur_count += 1
                loop_node.reset_cur_count()
                first_child_node.cur_count = 1
                #logger.debug('MATCH Loop %s / Segment %s (%s*%s)' \
                #    % (child.id, first_child_node.id, seg_data.get_seg_id(), seg[0].get_value()))
            else:
                raise EngineError, 'Usage must be R, S, or N'
            #self._flush_mandatory_segs(errh)
            return True
        elif loop_node.usage == 'R' and loop_node.cur_count < 1:
            fake_seg = pyx12.segment.segment('%s' % \
                (first_child_node.id), '~', '*', ':')
            errh.add_seg(first_child_node, fake_seg, seg_count, cur_line, ls_id)
            err_str = "Mandatory segment %s missing" % (first_child_node.id)
            #self.mandatory_segs_missing.append((seg_data.get_seg_id(), '3', err_str))
            errh.seg_error('3', err_str, None)
        return False
