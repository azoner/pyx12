######################################################################
# Copyright 
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Create a XML rendering of the X12 document
"""

from os.path import commonprefix
import logging

# Intrapackage imports
from errors import EngineError
from x12xml import x12xml
from map_walker import pop_to_parent_loop

logger = logging.getLogger('pyx12.x12xml.simple')


class x12xml_simple(x12xml):
    def __init__(self, fd, dtd_urn=None):
        x12xml.__init__(self, fd, "x12simple", dtd_urn)
        self.last_path = []

    def __del__(self):
        while len(self.writer) > 0:
            self.writer.pop()

    def seg(self, seg_node, seg_data):
        """
        Generate XML for the segment data and matching map node

        @param seg_node: Map Node
        @type seg_node: L{node<map_if.x12_node>}
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        """
        if not seg_node.is_segment():
            raise EngineError('Node must be a segment')
        parent = pop_to_parent_loop(seg_node)  # Get enclosing loop
        # check path for new loops to be added
        cur_path = self._path_list(parent.get_path())
        #if seg_node.id == 'GS':
        #    import ipdb; ipdb.set_trace()
        if self.last_path == cur_path and seg_node.is_first_seg_in_loop():
            # loop repeat
            self.writer.pop()
            (xname, attrib) = self._get_loop_info(cur_path[-1])
            self.writer.push(xname, attrib)
        else:
            last_path = self.last_path
            match_idx = self._get_path_match_idx(last_path, cur_path)
            root_path = self._path_list(commonprefix(['/'.join(cur_path), '/'.join(last_path)]))
            if seg_node.is_first_seg_in_loop() and root_path == cur_path:
                match_idx -= 1
            for i in range(len(last_path) - 1, match_idx - 1, -1):
                self.writer.pop()
            for i in range(match_idx, len(cur_path)):
                (xname, attrib) = self._get_loop_info(cur_path[i])
                self.writer.push(xname, attrib)
        seg_node_id = self._get_node_id(seg_node, parent, seg_data)
        (xname, attrib) = self._get_seg_info(seg_node_id)
        self.writer.push(xname, attrib)
        for i in range(len(seg_data)):
            child_node = seg_node.get_child_node_by_idx(i)
            if child_node.usage == 'N' or seg_data.get('%02i' % (i + 1)).is_empty():
                pass  # Do not try to ouput for invalid or empty elements
            elif child_node.is_composite():
                (xname, attrib) = self._get_comp_info(seg_node_id)
                self.writer.push(xname, attrib)
                comp_data = seg_data.get('%02i' % (i + 1))
                for j in range(len(comp_data)):
                    subele_node = child_node.get_child_node_by_idx(j)
                    (xname, attrib) = self._get_subele_info(subele_node.id)
                    self.writer.elem(xname, comp_data[j].get_value(), attrib)
                self.writer.pop()  # end composite
            elif child_node.is_element():
                if seg_data.get_value('%02i' % (i + 1)) == '':
                    pass
                    #self.writer.empty(u"ele", attrs={u'id': child_node.id})
                else:
                    (xname, attrib) = self._get_ele_info(child_node.id)
                    self.writer.elem(xname, seg_data.get_value('%02i' % (i + 1)), attrib)
            else:
                raise EngineError('Node must be a either an element or a composite')
        self.writer.pop()  # end segment
        self.last_path = cur_path

    def _get_loop_info(self, loop_id):
        """
        Override loop node value
        """
        return ("loop", {'id': loop_id})

    def _get_seg_info(self, seg_id):
        """
        Override segment node value
        """
        return ("seg", {'id': seg_id})

    def _get_comp_info(self, comp_id):
        """
        Override composite node value
        """
        return ("comp",  {'id': comp_id})

    def _get_ele_info(self, ele_id):
        """
        Override element node value
        """
        return ("ele", {'id': ele_id})

    def _get_subele_info(self, subele_id):
        """
        Override sub-element node value
        """
        return ("subele", {'id': subele_id})
