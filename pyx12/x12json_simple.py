from os.path import commonprefix
import logging

from .x12xml_simple import x12xml_simple
from .jsonwriter import JSONriter
from .errors import EngineError
from .map_walker import pop_to_parent_loop

logger = logging.getLogger('pyx12.x12json.simple')

class X12JsonSimple(x12xml_simple):
    def __init__(self, fd):
        self.writer = JSONriter(fd)
        self.last_path = []
        self.visited = []

    def __del__(self):
        while len(self.writer) > 0:
            self.writer.pop()

    def seg(self, seg_node, seg_data, last_seg=False):
        """
        Generate JSON for the segment data and matching map node

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
        if self.last_path == cur_path and seg_node.is_first_seg_in_loop():
            # loop repeat
            self.writer.pop()
            (xname, attrib) = self._get_loop_info(cur_path[-1])
            self.writer.push(xname, attrib, first=False)
        else:
            last_path = self.last_path
            match_idx = self._get_path_match_idx(last_path, cur_path)
            root_path = self._path_list(commonprefix(['/'.join(cur_path), '/'.join(last_path)]))
            if seg_node.is_first_seg_in_loop() and root_path == cur_path:
                match_idx -= 1
            loop_struct = range(len(last_path) - 1, match_idx - 1, -1)
            for i in loop_struct:
                if i == loop_struct[-1]:
                    self.writer.pop()
                else:
                    self.writer.pop()
            for i in range(match_idx, len(cur_path)):
                (xname, attrib) = self._get_loop_info(cur_path[i])
                # Write a Loop
                parent_loop = cur_path[i-1]
                if parent_loop not in self.visited:
                    self.visited.append(parent_loop)
                    self.writer.push(xname, attrib, first=True)
                else:
                    self.writer.push(xname, attrib, first=False)
        seg_node_id = self._get_node_id(seg_node, parent, seg_data)
        (xname, attrib) = self._get_seg_info(seg_node_id)
        if seg_node.is_first_seg_in_loop():
            self.writer.push(xname, attrib, first=True)
        else:
            self.writer.push(xname, attrib, first=False)
        loop_struct = range(len(seg_data))
        for i in loop_struct:
            if i == loop_struct[-1]:
                last = True
            else:
                # Check to see if any of the next children exist. 
                # If no, then we are on last node
                try:
                    next_children = [seg_node.get_child_node_by_idx(index) for index in loop_struct[i+1:]]
                except IndexError:
                    next_children = []
                next_node_exists = [not(child_node.usage == 'N' or seg_data.get('%02i' % (i + 1)).is_empty()) for child_node in next_children]
                if any(next_node_exists):
                    last = False
                else:
                    last = True
            child_node = seg_node.get_child_node_by_idx(i)
            if child_node.usage == 'N' or seg_data.get('%02i' % (i + 1)).is_empty():
                pass  # Do not try to ouput for invalid or empty elements
            elif child_node.is_composite():
                (xname, attrib) = self._get_comp_info(seg_node_id)
                if i == loop_struct[0]:
                    self.writer.push(xname, attrib, first=True)
                else:
                    self.writer.push(xname, attrib, first=False)
                comp_data = seg_data.get('%02i' % (i + 1))
                for j in range(len(comp_data)):
                    subele_node = child_node.get_child_node_by_idx(j)
                    (xname, attrib) = self._get_subele_info(subele_node.id)
                    self.writer.elem(xname, comp_data[j].get_value(), attrib, last)
                # self.writer.pop()  # end composite
            elif child_node.is_element():
                if seg_data.get_value('%02i' % (i + 1)) == '':
                    pass
                    #self.writer.empty(u"ele", attrs={u'id': child_node.id})
                else:
                    (xname, attrib) = self._get_ele_info(child_node.id)
                    self.writer.elem(xname, seg_data.get_value('%02i' % (i + 1)), attrib, last)
            else:
                raise EngineError('Node must be a either an element or a composite')
        self.writer.pop()  # end segment
        if parent.id not in self.visited:
            self.visited.append(parent.id)
        self.last_path = cur_path