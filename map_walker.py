#! /usr/bin/env /usr/local/bin/python
#
#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
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


# Intrapackage imports
from errors import *
import pdb
#import codes
#import map_index
#import map_if
#import x12file
#from utils import *

class walk_tree:
    def __init__(self):
        end_tag_stack = []

    def walk(self, node, seg):
        """
        Handle required segment/loop missed (not found in seg)
        Handle found segment = Not used
        """

        logger = logging.getLogger('pyx12')
        orig_node = node

        # Repeat of current segment
        if node.is_segment():
            if node.is_match(seg):
                return node
        #handle seg repeat count


        if seg[0] == 'NM1':
            pdb.set_trace()
        if node.is_loop() or node.is_map_root(): 
            # print node.name, node.id
            for child in node.children:
                if child.is_segment():
                    #print child.id
                    if child.is_match(seg):
                        if child.usage == 'N':
                            raise WEDIError, "Segment %s found but marked as not used" % (child.id)
                        return child
                    elif child.usage == 'R':
                        raise WEDIError, "Required segment %s not found" % (child.id)
     
        # Next segment in loop
        node_idx = None
        if node.is_segment(): 
            node_idx = node.index
            node = self.pop_to_parent_loop(node)
            for child in node.children:
                if child.is_segment() and child.index > node_idx:
                    #print child.id, child.index, node_idx
                    if child.is_match(seg):
                        if child.usage == 'N':
                            raise WEDIError, "Segment %s found but marked as not used" % (child.id)
                        return child
                    elif child.usage == 'R':
                        raise WEDIError, "Required segment %s not found" % (child.id)
            
        # Child loop
        node = orig_node
        logger.debug('map_walker: orig_node id=%s' % (node.id))
        node = self.pop_to_parent_loop(node)
        logger.debug('map_walker: parent_node id=%s' % (node.id))
        for child in node.children:
            if child.is_loop():
                logger.debug('map_walker: child_node id=%s' % (child.id))
                if self.is_first_seg_match(child, seg): 
                    return child # Return the loop node
                else:
                    logger.debug('map_walker: child_node id=%s is node a match' % (child.id))
                    
                    
        # Repeat loop
        node = orig_node
        node = self.pop_to_parent_loop(node) # We are in a segment
        if self.is_first_seg_match(node, seg): 
            return node # Return the loop node

                                  
        # Sibling Loop
        node = orig_node
        node_idx = None
        while not node.is_loop(): 
            node = node.parent
        if node.is_loop():
            node_idx = node.index
        for child in node.children:
            if child.is_loop() and child.index > node_idx:
                if self.is_first_seg_match(child, seg): return child
        node = orig_node

        # Parent Loop
        node = self.pop_to_parent_loop(node) # Get my loop
        node = self.pop_to_parent_loop(node) # Then get its loop
        if self.is_first_seg_match(node, seg): 
            return node


        raise EngineError, "Could not find seg %s*%s.  Started at %s" % (seg[0], seg[1], orig_node.id)

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


