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
Create a XML rendering of the X12 document
Uses node IDs as the tag names
"""

import logging
import pdb
#import string
#import os.path

# Intrapackage imports
from errors import *
#from utils import *
from x12xml import x12xml
from xmlwriter import XMLWriter

logger = logging.getLogger('pyx12.x12xml.simple')
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)

class x12xml_idtag(x12xml):
    def __init__(self, fd, dtd_urn):
        x12xml.__init__(self)
        self.writer = XMLWriter(fd)
        self.writer.doctype(
            u"x12doc", u"-//J Holland//DTD XML X12 Document Conversion1.0//EN//XML",
            u"%s" % (dtd_urn))

        self.writer.push(u"x12doc")
        self.path = '/'

    def __del__(self):
        self.writer.pop()

    def seg(self, seg_node, seg_data):
        """
        """
        if not seg_node.is_segment():
            raise EngineError, 'Node must be a segment'
        parent = x12xml.pop_to_parent_loop(self, seg_node) # Get enclosing loop
        # check path for new loops to be added
        path = parent.get_path()
        if self.path != path:
            #pdb.set_trace()
            #logger.debug('self.path=%s path=%s' % (self.path, path))
            #pop_loops = []
            #push_loops = []
            last_path = filter(lambda x: x!='', self.path.split('/'))
            cur_path = filter(lambda x: x!='', parent.get_path().split('/'))
            
            match_idx = 0
            for i in range(min(len(cur_path), len(last_path))):
                if cur_path[i] != last_path[i]:
                    break
                match_idx += 1

            for i in range(len(last_path)-1, match_idx-1, -1):
                #pop_loops.append(last_path[i])
                #logger.debug('POP=%s' % (last_path[i]))
                self.writer.pop()

            for i in range(match_idx, len(cur_path)):
                #push_loops.append(cur_path[i])
                #logger.debug('PUSH=%s' % (cur_path[i]))
                self.writer.push('L'+cur_path[i])
            
        self.writer.push(seg_node.id)
        for i in range(len(seg_data)):
            child_node = seg_node.get_child_node_by_idx(i)
            if child_node.is_composite():
                self.writer.push(seg_node.id)
                comp_data = seg_data[i]
                for j in range(len(comp_data)):
                    subele_node = child_node.get_child_node_by_idx(j)
                    self.writer.elem(subele_node.id, comp_data[j].get_value())
                self.writer.pop() #end composite
            elif child_node.is_element():
                if seg_data[i].get_value() == '':
                    pass
                    #self.writer.empty(child_node.id)
                else:
                    self.writer.elem(child_node.id, seg_data[i].get_value())
            else:
                raise EngineError, 'Node must be a either an element or a composite'
        self.writer.pop() #end segment

        self.path = path
        
        
        #if not (node.is_loop() or node.is_map_root()): 
        #    node = x12xml.pop_to_parent_loop(node) # Get enclosing loop


#    def pop_to_parent_loop(self, node):
#        if node.is_map_root():
#            return node
#        map_node = node.parent
#        if map_node is None:
#            raise EngineError, "Node is None: %s" % (node.name)
#        while not (map_node.is_loop() or map_node.is_map_root()): 
#            map_node = map_node.parent
#        if not (map_node.is_loop() or map_node.is_map_root()):
#            raise EngineError, "Called pop_to_parent_loop, can't find parent loop"
#        return map_node
        

def is_not_blank(x):
    return x != ''

