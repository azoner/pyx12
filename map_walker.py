#! /usr/bin/env /usr/local/bin/python
#
#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#                John Holland <jholland@kazoocmh.org> <john@zoner.org>
#
#    All rights reserved.
#
#        Redistribution and use in source and binary forms, with or without modification, 
#        are permitted provided that the following conditions are met:
#
#        1. Redistributions of source code must retain the above copyright notice, this list 
#           of conditions and the following disclaimer. 
#        
#        2. Redistributions in binary form must reproduce the above copyright notice, this 
#           list of conditions and the following disclaimer in the documentation and/or other 
#           materials provided with the distribution. 
#        
#        3. The name of the author may not be used to endorse or promote products derived 
#           from this software without specific prior written permission. 
#
#        THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED 
#        WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
#        MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
#        EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#        EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
#        OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
#        INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
#        CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
#        ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
#        THE POSSIBILITY OF SUCH DAMAGE.

"""
Walk a tree of x12_map nodes.  Find the correct node.

If seg indicates a loop has been entered, returns the loop node
If seg indicates a segment has been entered, returns the segment node
"""

import logging
import pdb

# Intrapackage imports
from errors import *
#import codes
#import map_index
#import map_if
#import x12file
#from utils import *

class walk_tree:
    def __init__(self):
#        end_tag_stack = []
        self.cur_seg_count = 0

    def walk(self, node, seg, err_codes):
        """
        Handle required segment/loop missed (not found in seg)
        Handle found segment = Not used
        """

        logger = logging.getLogger('pyx12')
        orig_node = node

        node_idx = node.index # Get original index of starting node
        if not (node.is_loop() or node.is_map_root()): 
            node = self.pop_to_parent_loop(node) # Get enclosing loop
        while 1:
            for child in node.children:
                #logger.debug('id=%s child.index=%i node_idx=%i' % \
                #    (child.id, child.index, node_idx))
                if child.index >= node_idx:
                    logger.debug('id=%s cur_count=%i max_repeat=%i' \
                        % (child.id, child.cur_count, child.get_max_repeat()))
                    if child.is_segment():
                        if child.is_match(seg):
                            logger.debug('MATCH segment %s (%s*%s)' % (child.id, seg[0], seg[1]))
                            if seg[0] == 'INS':
                                pdb.set_trace()
                            if child.usage == 'N':
                                err_str = "Segment %s found but marked as not used" % (child.id)
                                err_codes.append(['2', err_str])
                                #raise WEDIError, err_str
                            if child is orig_node:
                                logger.debug('child %s IS orig_node %s' % (child.id, orig_node.id))
                                child.cur_count += 1
                            else:
                                if orig_node.is_segment():
                                    orig_node.cur_count = 0
                                    logger.debug('Set orig_node %s cur_count = 0' % (orig_node.id))
                                child.cur_count = 1
                                logger.debug('Set child %s cur_count = 1' % (orig_node.id))
                            if child.cur_count > child.get_max_repeat():  # handle seg repeat count
                                err_str = "Segment %s exceeded max count.  Found %i, should have %i" \
                                    % (seg[0], child.cur_count, child.get_max_repeat())
                                err_codes.append(['5', err_str])
                                #raise WEDIError, err_str
                            return child
                        elif child.usage == 'R' and child.cur_count < 1:
                            # if child.cur_count == 0:
                            err_str = "Mandatory segment %s missing" % (child.id)
                            err_codes.append(['3', err_str])
                            #raise WEDIError, err_str
                        else:
                            logger.debug('Segment %s is not a match for (%s*%s)' % (child.id, seg[0], seg[1]))
                    elif child.is_loop(): 
                        #logger.debug('child_node id=%s' % (child.id))
                        if self.is_first_seg_match(child, seg): 
                            child.cur_count += 1
                            child.reset_cur_count()
                            node = child.children[0]
                            node.cur_count = 1
                            logger.debug('MATCH Loop %s / Segment %s (%s*%s)' \
                                % (child.id, node.id, seg[0], seg[1]))
                            return node # Return the first segment in node
                        else:
                            logger.debug('Loop id=%s is not a match for (%s*%s)' % (child.id, seg[0], seg[1]))
            if node.is_map_root(): # If at root and we haven't found the segment yet.
                err_str = "Segment %s not found" % (seg[0])
                err_codes.append(['1', err_str])
                #raise WEDIError, err_str
            node_idx = node.index # Get index of current node in tree
            node = self.pop_to_parent_loop(node) # Get enclosing parent loop

        err_str = "Segment %s not found" % (seg[0])
        err_codes.append(['1', err_str])
        #raise EngineError, "Could not find seg %s*%s.  Started at %s" % (seg[0], seg[1], orig_node.id)

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
        

    def is_first_seg_match(self, node, seg):
        """
        Find the first segment in loop, verify it matches segment
        Return: boolean
        """
        if not node.is_loop(): raise EngineError, \
            "Call to first_seg_match failed, node is not a loop"
        for child in node.children:
            if child.is_segment():
                if child.is_match(seg):
                    return True
                else:
                    return False # seg does not match the first segment in loop, so not valid
        return False


