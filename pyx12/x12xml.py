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
Interface to create a XML rendering of the X12 document
"""

# Intrapackage imports
from errors import *
from xmlwriter import XMLWriter
from map_walker import pop_to_parent_loop

class x12xml(object):
    def __init__(self, fd, type, dtd_urn):
        self.writer = XMLWriter(fd)
        if dtd_urn:
            self.writer.doctype(
                type, u"-//J Holland//DTD XML X12 Document Conversion1.0//EN//XML",
                u"%s" % (dtd_urn))
        self.writer.push(type)

    def __del__(self):
        pass

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
        cur_path = self._path_list(parent.get_path())
        if self.last_path != cur_path:
            last_path = self.last_path
            match_idx = self._get_path_match_idx(last_path, cur_path)
            root_path = self._path_list(os.path.commonprefix(
                ['/'.join(cur_path), '/'.join(last_path)]))
            if seg_node.is_first_seg_in_loop() and root_path==cur_path:
                match_idx -= 1
            for i in range(len(last_path)-1, match_idx-1, -1):
                self.writer.pop()
            for i in range(match_idx, len(cur_path)):
                (xname, attrib) = self._get_loop_info(cur_path[i])
                self.writer.push(xname, attrib)
        seg_node_id = self._get_node_id(seg_node, parent, seg_data)
        (xname, attrib) = self._get_seg_info(seg_node_id)
        self.writer.push(xname, attrib)
        for i in range(len(seg_data)):
            child_node = seg_node.get_child_node_by_idx(i)
            if child_node.usage == 'N' or seg_data.get('%02i' % (i+1)).is_empty():
                pass # Do not try to ouput for invalid or empty elements
            elif child_node.is_composite():
                (xname, attrib) = self._get_comp_info(seg_node_id)
                self.writer.push(xname, attrib)
                comp_data = seg_data.get('%02i' % (i+1))
                for j in range(len(comp_data)):
                    subele_node = child_node.get_child_node_by_idx(j)
                    (xname, attrib) = self._get_subele_info(subele_node.id)
                    self.writer.elem(xname, comp_data[j].get_value(), attrib)
                self.writer.pop() #end composite
            elif child_node.is_element():
                if seg_data.get_value('%02i' % (i+1)) == '':
                    pass
                    #self.writer.empty(u"ele", attrs={u'id': child_node.id})
                else:
                    (xname, attrib) = self._get_ele_info(child_node.id)
                    self.writer.elem(xname, seg_data.get_value('%02i' % (i+1)), attrib)
            else:
                raise EngineError, 'Node must be a either an element or a composite'
        self.writer.pop() #end segment
        self.last_path = cur_path


    def _path_list(self, path_str):
        """
        Get list of path nodes from path string
        @rtype: list
        """
        return filter(lambda x: x!='', path_str.split('/'))

    def _get_path_match_idx(self, last_path, cur_path):
        """
        Get the index of the last matching path nodes
        """
        match_idx = 0
        for i in range(min(len(cur_path), len(last_path))):
            if cur_path[i] != last_path[i]:
                break
            match_idx += 1
        return match_idx

    def _get_node_id(self, seg_node, parent=None, seg_data=None):
        """
        Base node id function
        """
        return seg_node.id

    def _get_loop_info(self, loop_id):
        """
        Base loop node value
        """
        loop_name = loop_id
        attrib = {}
        return (loop_name, attrib)

    def _get_seg_info(self, seg_id):
        """
        Base segment node value
        """
        seg_name = seg_id
        attrib = {}
        return (seg_name, attrib)

    def _get_comp_info(self, comp_id):
        """
        Base composite node value
        """
        comp_name = comp_id
        attrib = {}
        return (comp_name, attrib)

    def _get_ele_info(self, ele_id):
        """
        Base element node value
        """
        name = ele_id
        attrib = {}
        return (name, attrib)

    def _get_subele_info(self, subele_id):
        """
        Base sub-element node value
        """
        name = subele_id
        attrib = {}
        return (name, attrib)
