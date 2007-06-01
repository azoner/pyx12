######################################################################
# Copyright (c) 2001-2007 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Create a XML rendering of the X12 document
"""

import os.path
import logging

# Intrapackage imports
from errors import *
from x12xml import x12xml
from xmlwriter import XMLWriter
from map_walker import pop_to_parent_loop

logger = logging.getLogger('pyx12.x12xml.simple')

class x12xml_simple(x12xml):
    def __init__(self, fd, dtd_urn):
        x12xml.__init__(self)
        self.writer = XMLWriter(fd)
        if dtd_urn:
            self.writer.doctype(
                u"x12simple", u"-//J Holland//DTD XML X12 Document Conversion1.0//EN//XML",
                u"%s" % (dtd_urn))
        self.writer.push(u"x12simple")
        self.last_path = []

    def __del__(self):
        while len(self.writer) > 0:
            self.writer.pop()

    def __path_list(self, path_str):
        """
        Get list of path nodes from path string
        @rtype: list
        """
        return filter(lambda x: x!='', path_str.split('/'))

    def seg(self, seg_node, seg_data):
        """
        Generate XML for the segment data and matching map node

        @param seg_node: Map Node
        @type seg_node: L{node<map_if.x12_node>}
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        """
        if not seg_node.is_segment():
            raise EngineError, 'Node must be a segment'
        parent = pop_to_parent_loop(seg_node) # Get enclosing loop
        # check path for new loops to be added
        cur_path = self.__path_list(parent.get_path())
        if self.last_path != cur_path:
            last_path = self.last_path
            match_idx = 0
            for i in range(min(len(cur_path), len(last_path))):
                if cur_path[i] != last_path[i]:
                    break
                match_idx += 1
            #root_path = cur_path[:match_idx]
            root_path = self.__path_list(os.path.commonprefix(
                ['/'.join(cur_path), '/'.join(last_path)]))
            if seg_node.is_first_seg_in_loop() and root_path==cur_path:
                match_idx -= 1
            for i in range(len(last_path)-1, match_idx-1, -1):
                self.writer.pop()
            for i in range(match_idx, len(cur_path)):
                self.writer.push(u"loop", {u'id': cur_path[i]})
        self.writer.push(u"seg", {u'id': seg_node.id})
        for i in range(len(seg_data)):
            child_node = seg_node.get_child_node_by_idx(i)
            if child_node.usage == 'N' or seg_data.get('%02i' % (i+1)).is_empty():
                pass # Do not try to ouput for invalid or empty elements
            elif child_node.is_composite():
                self.writer.push(u"comp", {u'id': seg_node.id})
                comp_data = seg_data.get('%02i' % (i+1))
                for j in range(len(comp_data)):
                    subele_node = child_node.get_child_node_by_idx(j)
                    self.writer.elem(u'subele', comp_data[j].get_value(), \
                        attrs={u'id': subele_node.id})
                self.writer.pop() #end composite
            elif child_node.is_element():
                if seg_data.get_value('%02i' % (i+1)) == '':
                    pass
                    #self.writer.empty(u"ele", attrs={u'id': child_node.id})
                else:
                    #pdb.set_trace()
                    self.writer.elem(u'ele', seg_data.get_value('%02i' % (i+1)), 
                        attrs={u'id': child_node.id})
            else:
                raise EngineError, 'Node must be a either an element or a composite'
        self.writer.pop() #end segment
        self.last_path = cur_path

def is_not_blank(x):
    """
    @rtype: boolean
    """
    return x != ''
