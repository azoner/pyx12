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
Create a XML rendering of the X12 document
"""

import logging
import pdb
import string
import os.path

# Intrapackage imports
from errors import *
#from utils import *
from x12xml import x12xml
from xmlwriter import XMLWriter

logger = logging.getLogger('pyx12.x12xml.simple')
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)

class x12xml_simple(x12xml):
    def __init__(self, fd):
        self.writer = XMLWriter(fd)
        self.writer.doctype(
            u"x12doc", u"-//J Holland//DTD XML X12 Document Conversion1.0//EN//XML",
            u"http://www.kazoocmh.org/x12simple.dtd")

        self.writer.push(u"x12doc")
        self.path = '/'

    def __del__(self):
        self.writer.pop()

    def seg(self, seg_node, seg):
        """
        """
        parent = x12xml.pop_to_parent_loop(self, seg_node) # Get enclosing loop
        # check path for new loops to be added
        #path = parent.get_path()
        pop_loops = []
        push_loops = []
        old_path = [] 
        new_path = [] 
        self_path = self.path.split('/')
        path = parent.get_path().split('/')
        for i in range(len(old_path)):
            if old_path[i] != '':
                old_path
                
        
        match_idx = 0
        for i in range(min(len(path), len(self.path))):
            if path[i] != self.path[i]:
                break
            match_idx += 1

        for i = range(len(self.path)-1, match_idx-1, -1):
            pop_loops.append(self.path[i])
            
        #for i in range(max(len(path), len(self.path))):
        #    try:
        #        if path[i] != self.path[i]:
                    
        #    if i < len(path):
        #        pass

        
        # find new loops
        base = os.path.commonprefix([path, self.path])

        if  path != self.path:
            logger.debug('self.path=%s path=%s base=%s' % (self.path, path, base))
        # add loops
        if path != self.path and len(path) > len(self.path):
            if path[len(base):] != '':
                path_diff = path[len(base):].split('/')
            else:
                path_diff = []

            for loop_id in path_diff:
                if loop_id != '':
                    #pdb.set_trace()
                    logger.debug('PUSH=%s' % (loop_id))
                    logger.debug(path_diff)
                    self.writer.push(u"loop", {u'id': loop_id})
            
        #self.writer.elem(u'segment', content, attrs={}):

        # find closed loops
        # close them, reverse order
        if path != self.path and len(path) < len(self.path):
            if self.path[len(base):] != '':
                path_diff = self.path[len(base):].split('/')
            else:
                path_diff = []

            for i in range(len(path_diff)-1, 0, -1):
                if path_diff[i] != '':
                    #pdb.set_trace()
                    logger.debug('POP=%s' % (path_diff[i]))
                    logger.debug(path_diff)
                    self.writer.pop()

        self.path = path

        
        #self.writer.empty(u"any")
        
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
        

