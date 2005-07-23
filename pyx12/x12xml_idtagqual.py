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
Create a XML rendering of the X12 document
Uses node IDs as the tag names
Append ID value for non-unique segments IDs
"""

import logging
#import pdb
#import string
#import os.path

# Intrapackage imports
from errors import *
from x12xml import x12xml
from xmlwriter import XMLWriter
from map_walker import pop_to_parent_loop

logger = logging.getLogger('pyx12.x12xml.idtagqual')
#logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)

class x12xml_idtagqual(x12xml):
    def __init__(self, fd, dtd_urn=None):
        x12xml.__init__(self)
        logger.debug('idtagqual')
        self.writer = XMLWriter(fd)
        if dtd_urn:
            self.writer.doctype(
                u"x12idtagqual", u"-//J Holland//DTD XML X12 Document Conversion1.0//EN//XML",
                u"%s" % (dtd_urn))
        self.writer.push(u"x12idtagqual")
        self.path = '/'

    def __del__(self):
        while len(self.writer) > 0:
            self.writer.pop()

    def seg(self, seg_node, seg_data):
        """
        Generate XML for the segment data and matching map node

        @param seg_node: Map Node 
        @type seg_node: L{node<map_if.x12_node>}
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.segment>}
        """
        if not seg_node.is_segment():
            raise EngineError, 'Node must be a segment'
        parent = pop_to_parent_loop(seg_node) # Get enclosing loop
        # check path for new loops to be added
        path = parent.get_path()
        if self.path != path:
            last_path = filter(lambda x: x!='', self.path.split('/'))
            cur_path = filter(lambda x: x!='', parent.get_path().split('/'))
            match_idx = 0
            for i in range(min(len(cur_path), len(last_path))):
                if cur_path[i] != last_path[i]:
                    break
                match_idx += 1
            for i in range(len(last_path)-1, match_idx-1, -1):
                self.writer.pop()
            for i in range(match_idx, len(cur_path)):
                self.writer.push('L'+cur_path[i])
        seg_node_id = self.get_node_id(seg_node, parent, seg_data)
        self.writer.push(seg_node_id)
        for i in range(len(seg_data)):
            child_node = seg_node.get_child_node_by_idx(i)
            if child_node.usage == 'N' or seg_data.get('%02i' % (i+1)).is_empty():
                pass # Do not try to ouput for invalid or empty elements
            elif child_node.is_composite():
                self.writer.push(seg_node_id)
                comp_data = seg_data.get('%02i' % (i+1))
                for j in range(len(comp_data)):
                    subele_node = child_node.get_child_node_by_idx(j)
                    self.writer.elem(subele_node.id, comp_data[j].get_value())
                self.writer.pop() #end composite
            elif child_node.is_element():
                if seg_data.get_value('%02i' % (i+1)) == '':
                    pass
                    #self.writer.empty(child_node.id)
                else:
                    self.writer.elem(child_node.id, 
                        seg_data.get_value('%02i' % (i+1)))
            else:
                raise EngineError, 'Node must be a either an element or a composite'
        self.writer.pop() #end segment
        self.path = path
        
    def get_node_id(self, seg_node, parent, seg_data):
        """
        Get a unique node ID string
        @param seg_node: L{node<map_if.segment_if>}
        @param parent: L{node<map_if.segment_if>}
        @param seg_data: L{node<segment.segment>}
        @return: Unique node representation
        @rtype: string
        """
        if len(parent.pos_map[seg_node.pos]) > 1:
            id_val = seg_data.get_value('01')
            if seg_node.children[0].is_element() \
                    and seg_node.children[0].data_type == 'ID' \
                    and len(seg_node.children[0].valid_codes) > 0 \
                    and id_val in seg_node.children[0].valid_codes:
                return seg_node.id + '_' + id_val
            elif seg_node.children[0].is_composite() \
                    and seg_node.children[0].children[0].data_type == 'ID' \
                    and len(seg_node.children[0].children[0].valid_codes) > 0 \
                    and id_val in seg_node.children[0].children[0].valid_codes:
                return seg_node.id + '_' + id_val
        return seg_node.id
