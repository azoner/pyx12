#####################################################################
# Copyright 
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Parse a ANSI X12 data file.

Maintain context state
Start saving context and segments
Interface to read and alter segments

@todo: Attach errors to returned dicts
"""
#G{classtree X12DataNode}

#import os
#import os.path

# Intrapackage imports
import pyx12
import error_handler
import errors
import map_index
import map_if
import x12file
import path
from map_walker import walk_tree, pop_to_parent_loop  # get_pop_loops, get_push_loops


class X12DataNode(object):
    """
    Capture the segment data and X12 definition for a loop subtree
    Alter relational data
    Iterate over contents
    """
    def __init__(self, x12_node, seg_data, ntype='seg'):
        """
        """
        self.x12_map_node = x12_node
        self.type = ntype
        self.seg_data = seg_data
        self.parent = None
        self.children = []
        self.errors = []
        self.seg_count = None
        self.cur_line_number = None

    #{ Public Methods
    def delete(self):
        """
        Delete this node.  Mark type as deleted.
        """
        self.x12_map_node = None
        self.type = None
        self.seg_data = None
        self.parent = None
        self.children = []
        self.errors = []

    def iterate_segments(self):
        """
        Iterate over this node and children, return any segments found
        """
        raise NotImplementedError('Override in sub-class')

    def iterate_loop_segments(self):
        """
        Iterate over this node and children, return loop start and loop end
        and any segments found
        """
        raise NotImplementedError('Override in sub-class')

    def get_value(self, x12_path):
        """
        @return: the element value at the relative X12 path
        @rtype: string
        """
        raise NotImplementedError('Override in sub-class')

    def set_value(self, x12_path, val):
        """
        Set the value of simple element at the first found segment at the given path
        @param x12_path: An X12 path
        @type x12_path: string
        @param val: The new element value
        @type val: string
        """
        raise NotImplementedError('Override in sub-class')

    def exists(self, x12_path_str):
        """
        Does at least one child at the x12 path exist?
        @param x12_path_str: Relative X12 path - 2400/2430
        @type x12_path_str: string
        @return: True if found
        @rtype: boolean
        """
        (curr, new_path) = self._get_start_node(x12_path_str)
        xpath = path.X12Path(new_path)
        for n in curr._select(xpath):
            return True
        return False

    def select(self, x12_path_str):
        """
        Get a slice of sub-nodes at the relative X12 path.
        @note: All interaction/modification with a X12DataNode tree (having a loop
        root) is done in place.
        @param x12_path_str: Relative X12 path - 2400/2430
        @type x12_path_str: string
        @return: Iterator on the matching sub-nodes, relative to the instance.
        @rtype: L{node<x12context.X12DataNode>}
        """
        (curr, new_path) = self._get_start_node(x12_path_str)
        xpath = path.X12Path(new_path)
        for n in curr._select(xpath):
            if xpath.seg_id is not None:
                assert n.id == xpath.seg_id
            else:
                assert len(xpath.loop_list) > 0
                assert n.id == xpath.loop_list[-1]
            assert n.parent is not None, 'Node "%s" has no parent' % (n.id)
            yield n

    def first(self, x12_path_str):
        """
        Get the first sub-node matching the relative X12 path.
        @note: All interaction/modification with a X12DataNode tree (having a loop
        root) is done in place.
        @param x12_path_str: Relative X12 path - ie 2400/2430
        @type x12_path_str: string
        @return: The matching sub-node, relative to the instance.
        @rtype: L{node<x12context.X12DataNode>}
        """
        if not self.exists(x12_path_str):
            return None
        for node in self.select(x12_path_str):
            return node

    def count(self, x12_path_str):
        """
        Get a count of sub-nodes at the relative X12 path.
        @param x12_path_str: Relative X12 path - 2400/2430
        @type x12_path_str: string
        @return: Count of matching sub-nodes
        @rtype: int
        """
        ct = 0
        (curr, new_path) = self._get_start_node(x12_path_str)
        xpath = path.X12Path(new_path)
        for n in curr._select(xpath):
            ct += 1
        return ct

    #{ Private Methods
    def _cleanup(self):
        """
        Remove deleted nodes
        """
        self.children = [x for x in self.children if x.type is not None]

    def _get_insert_idx(self, x12_node):
        """
        Find the index of self.children before which the x12_node belongs
        Nodes will be inserted after the last node with matching ordinals
        """
        self._cleanup()
        map_idx = x12_node.pos
        idx = None
        for i in range(len(self.children)):
            if self.children[i].x12_map_node.pos <= map_idx:
                idx = i
        if idx is not None:
            return idx + 1
        return len(self.children)

    def get_first_matching_segment(self, x12_path_str):
        """
        Get first found Segment at the given relative path.  If the path is not a
        valid relative path or if the given segment index does not exist, the function
        returns None.

        @param x12_path_str: Relative X12 Path
        @type x12_path_str: string
        @return: First matching data segment
        @rtype: L{node<segment.Segment>}
        @raise X12PathError: On blank or invalid path
        """
        raise NotImplementedError('Override in sub-class')

    def _get_start_node(self, x12_path_str):
        """
        Move up the tree.  Get the new starting node and the altered path
        """
        curr = self
        while x12_path_str[:3] == '../':
            if curr.parent is None:
                raise errors.X12PathError('Current node %s does not have a parent: %s' % (self.id, x12_path_str))
            curr = curr.parent
            x12_path_str = x12_path_str[3:]
        return (curr, x12_path_str)

    def _select(self, x12path):
        """
        Get the child node at the path
        @param x12path: x12 map path
        @type x12path: L{path<path.X12Path>}
        """
        if len(x12path.loop_list) == 0:
            # Only segment left
            cur_node_id = x12path.seg_id
            qual = x12path.id_val
            for child in [x for x in self.children if x.type is not None]:
                if child.type == 'seg':
                    if child.x12_map_node.is_match_qual(child.seg_data, cur_node_id, qual):
                        yield child
                else:
                    if child.id == cur_node_id:
                        yield child
        else:
            cur_node_id = x12path.loop_list[0]
            cur_loop_list = x12path.loop_list[1:]
            for child in [x for x in self.children if x.type is not None]:
                if child.id == cur_node_id:
                    if len(cur_loop_list) == 0 and x12path.seg_id is None:
                        yield child
                    else:
                        child_path = path.X12Path(x12path.format())
                        child_path.loop_list = cur_loop_list
                        for n in child._select(child_path):
                            yield n

    def __copy__(self):
        """
        Returns a copy of this node
        """
        raise NotImplementedError('Override in sub-class')

    #{ Property Accessors
    @property
    def id(self):
        """
        @return: x12 node id
        @rtype: string
        """
        if self.x12_map_node is None:
            raise errors.EngineError('This node has been deleted')
        return self.x12_map_node.id

    @property
    def cur_path(self):
        """
        @return: x12 node path
        @rtype: string
        """
        if self.x12_map_node is None:
            raise errors.EngineError('This node has been deleted')
        return self.x12_map_node.get_path()


class X12LoopDataNode(X12DataNode):
    """
    Capture the X12 definition for a loop subtree
    Alter relational data
    Iterate over contents
    """
    def __init__(self, x12_node, end_loops=[], parent=None):
        """
        Construct an X12LoopDataNode
        """
        self.x12_map_node = x12_node
        self.type = 'loop'
        #self.seg_data = None
        self.parent = parent
        self.children = []
        self.errors = []
        self.end_loops = end_loops  # we might need to close a preceeding loop

    #{ Public Methods
    def delete(self):
        """
        Delete this node.  Mark type as deleted.
        """
        self.end_loops = []
        X12DataNode.delete(self)

    def get_value(self, x12_path_str):
        """
        Returns the element value at the given relative path.  If the path is not a
        valid relative path or if the given segment index does not exist, the function
        returns None.  If multiple values exist, this function returns the first.

        @param x12_path_str: Relative X12 Path
        @type x12_path_str: string
        @return: the element value at the relative X12 path
        @rtype: string
        @raise X12PathError: On blank or invalid path
        """
        (curr, new_path) = self._get_start_node(x12_path_str)
        seg_data = curr.get_first_matching_segment(new_path)
        if seg_data is None:
            return None
        xpath = path.X12Path(new_path)
        xpath.loop_list = []
        xpath.id_val = None
        seg_part = xpath.format()
        return seg_data.get_value(seg_part)

    def set_value(self, x12_path_str, val):
        """
        Set the value of simple element at the first found segment at the given path
        @param x12_path_str: Relative X12 Path
        @type x12_path_str: string
        @param val: The new element value
        @type val: string
        """
        (curr, new_path) = self._get_start_node(x12_path_str)
        seg_data = curr.get_first_matching_segment(new_path)
        if seg_data is None:
            raise errors.X12PathError('X12 Path is invalid or was not found: %s' % (x12_path_str))
        xpath = path.X12Path(new_path)
        xpath.loop_list = []
        xpath.id_val = None
        seg_part = xpath.format()
        seg_data.set(seg_part, val)

    def iterate_segments(self):
        """
        Iterate over this node and children
        """
        for child in [x for x in self.children if x.type is not None]:
            for a in child.iterate_segments():
                yield a

    def iterate_loop_segments(self):
        """
        Iterate over this node and children, return loop start and loop end
        """
        for loop in self.end_loops:
            yield {'node': loop, 'type': 'loop_end', 'id': loop.id}
        yield {'type': 'loop_start', 'id': self.id, 'node': self.x12_map_node}
        for child in [x for x in self.children if x.type is not None]:
            for a in child.iterate_loop_segments():
                yield a
        yield {'type': 'loop_end', 'id': self.id, 'node': self.x12_map_node}

    def add_segment(self, seg_data):
        """
        Add the segment to this loop node
        iif the segment is the anchor for a child loop, also adds the loop

        @param seg_data: Segment data
        @type seg_data: L{node<segment.Segment>} or string
        @return: New segment, or None if failed
        @rtype: L{node<x12context.X12SegmentDataNode>}
        @raise pyx12.errors.X12PathError: If invalid segment
        @todo: Check counts?
        """
        seg_data = self._get_segment(seg_data)
        x12_seg_node = self.x12_map_node.get_child_seg_node(seg_data)
        if x12_seg_node is None:
            raise errors.X12PathError('The segment %s is not a member of loop %s' %
                                      (seg_data.__repr__(), self.id))
        new_data_node = X12SegmentDataNode(x12_seg_node, seg_data, self)
        child_idx = self._get_insert_idx(x12_seg_node)
        self.children.insert(child_idx, new_data_node)
        return new_data_node

    def add_loop(self, seg_data):
        """
        Add a new loop in the correct location
        @param seg_data: Segment data
        @type seg_data: L{node<segment.Segment>} or string
        @return: New loop_data_node, or None if failed
        @rtype: L{node<x12context.X12LoopDataNode>}
        """
        seg_data = self._get_segment(seg_data)
        x12_loop_node = self.x12_map_node.get_child_loop_node(seg_data)
        if x12_loop_node is None:
            raise errors.X12PathError('The segment %s is not a member of loop %s' %
                                      (seg_data.__repr__(), self.id))
        new_data_loop = self._add_loop_node(x12_loop_node)
        # Now, add the segment
        x12_seg_node = new_data_loop.x12_map_node.get_child_seg_node(seg_data)
        new_data_node = X12SegmentDataNode(
            x12_seg_node, seg_data, new_data_loop)
        new_data_loop.add_node(new_data_node)
        return new_data_loop

    def add_node(self, data_node):
        """
        Add a X12DataNode instance
        The x12_map_node of the given data_node must be a direct child of this
        object's x12_map_node
        @param data_node: The child loop node to add
        @type data_node : L{node<x12context.X12DataNode>}
        @raise errors.X12PathError: On blank or invalid path
        """
        if data_node.x12_map_node.parent != self.x12_map_node:
            raise errors.X12PathError('The loop_data_node "%s" is not a child of "%s"' %
                                      (data_node.x12_map_node.id, self.x12_map_node.id))
        data_node.parent = self
        child_idx = self._get_insert_idx(data_node.x12_map_node)
        self.children.insert(child_idx, data_node)

    def delete_segment(self, seg_data):
        """
        Delete the given segment from this loop node
         - Do not delete the first segment in a loop
         - Does not descend into child loops
         - Only delete the first found matching segment

        @param seg_data: Segment data
        @type seg_data: L{node<segment.Segment>} or string
        @return: True if found and deleted, else False
        @rtype: Boolean
        @todo: Check counts?
        """
        seg_data = self._get_segment(seg_data)
        x12_seg_node = self.x12_map_node.get_child_seg_node(seg_data)
        if x12_seg_node is None:
            return False
            #raise errors.X12PathError, 'The segment %s is not a member of loop %s' % \
            #    (seg_data.__repr__(), self.id)
        # Iterate over data nodes, except first
        self._cleanup()
        for i in range(1, len(self.children)):
            if self.children[i].type == 'seg' and self.children[i].seg_data == seg_data:
                del self.children[i]
                return True
        return False

    def delete_node(self, x12_path_str):
        """
        Delete the first node at the given relative path.  If the path is not a
        valid relative path, return False If multiple values exist, this
        function deletes the first.

        @return: True if found and deleted, else False
        @rtype: Boolean
        @raise X12PathError: On blank or invalid path
        @todo: Check counts?
        """
        (curr, new_path) = self._get_start_node(x12_path_str)
        xpath = path.X12Path(new_path)
        for n in curr._select(xpath):
            n.delete()
            return True
        return False

    def _add_loop_node(self, x12_loop_node):
        """
        Add a loop data node to the current tree
        @param x12_loop_node: X12 Loop node
        @type x12_loop_node: L{node<map_if.loop_if>}
        @return: New X12 Loop Data Node
        @rtype: L{node<x12context.X12LoopDataNode>}
        """
        new_node = X12LoopDataNode(x12_loop_node, parent=self)
        # Iterate over data nodes
        child_idx = self._get_insert_idx(x12_loop_node)
        self.children.insert(child_idx, new_node)
        return new_node

    def get_first_matching_segment(self, x12_path_str):
        """
        Get first found Segment at the given relative path.  If the path is not a
        valid relative path or if the given segment index does not exist, the function
        returns None.

        @param x12_path_str: Relative X12 Path
        @type x12_path_str: string
        @return: First matching data segment
        @rtype: L{node<segment.Segment>}
        @raise X12PathError: On blank or invalid path
        """
        if len(x12_path_str) == 0:
            raise errors.X12PathError('Blank X12 Path')
        (curr, new_path) = self._get_start_node(x12_path_str)
        xpath = path.X12Path(new_path)
        if xpath.seg_id is None:
            return None
        if len(xpath.loop_list) == 0:
            seg_id = xpath.seg_id
            qual = xpath.id_val
            try:
                for seg in [seg for seg in curr.children if seg.type == 'seg']:
                    if seg.x12_map_node.is_match_qual(seg.seg_data, seg_id, qual):
                        return seg.seg_data
                return None
            except errors.EngineError as e:
                raise errors.X12PathError('X12 Path is invalid or was not found: %s' % (x12_path_str))
        else:
            next_id = xpath.loop_list[0]
            del xpath.loop_list[0]
            try:
                for loop in [loop for loop in curr.children if loop.type == 'loop']:
                    if loop.id == next_id:
                        return loop.get_first_matching_segment(xpath.format())
                return None
            except errors.EngineError as e:
                raise errors.X12PathError('X12 Path is invalid or was not found: %s' % (x12_path_str))

    def _get_segment(self, seg_obj):
        """
        Get a pyx12.segment.Segment instance, building one from a string
        """
        if isinstance(seg_obj, pyx12.segment.Segment):
            return seg_obj
        elif isinstance(seg_obj, str):
            (seg_term, ele_term, subele_term) = self._get_terminators()
            assert seg_term is not None, 'seg_term is none, node contains no X12SegmentDataNode children?'
            assert ele_term is not None, 'seg_term is none, node contains no X12SegmentDataNode children?'
            assert subele_term is not None, 'seg_term is none, node contains no X12SegmentDataNode children?'
            return pyx12.segment.Segment(seg_obj, seg_term, ele_term, subele_term)
        else:
            raise errors.EngineError('Unknown type %s for seg_obj %i.  Expecting a pyx12.segment.Segment or a str'
                                     % (seg_obj.__class__, seg_obj))

    def _get_terminators(self):
        for child in self.children:
            if isinstance(child, X12SegmentDataNode) and child.seg_data is not None \
                    and child.seg_data.seg_term is not None:
                return (child.seg_data.seg_term, child.seg_data.ele_term, child.seg_data.subele_term)
        return self.parent._get_terminators()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        """
        Returns a copy of this node
        """
        ret = X12LoopDataNode(self.x12_map_node)
        ret.end_loops = list(self.end_loops)
        ret.parent = self.parent
        for child in self.children:
            ret.children.append(child.copy())
        return ret

    @property
    def seg_count(self):
        for child in [x for x in self.children if x.type == 'seg']:
            return child.seg_count
        
    @property
    def cur_line_number(self):
        for child in [x for x in self.children if x.type == 'seg']:
            return child.cur_line_number


class X12SegmentDataNode(X12DataNode):
    """
    Capture the segment data and X12 definition
    Alter relational data
    Iterate over contents
    """
    def __init__(self, x12_node, seg_data, parent=None, start_loops=[],
                 end_loops=[]):
        self.x12_map_node = x12_node
        self.type = 'seg'
        self.seg_data = seg_data
        self.parent = parent
        self.start_loops = start_loops
        self.end_loops = end_loops
        self.errors = []
        self.err_isa = []
        self.err_gs = []
        self.err_st = []
        self.err_seg = []
        self.err_ele = []
        self.seg_count = None
        self.cur_line_number = None

    #{ Public Methods
    def handle_errh_errors(self, errh):
        """
        Attach validation errors to segment node

        @todo: move errors to parent loops if necessary
        """
        self.err_isa.extend(errh.err_isa)
        self.err_gs.extend(errh.err_gs)
        self.err_st.extend(errh.err_st)
        self.err_seg.extend(errh.err_seg)
        self.err_ele.extend(errh.err_ele)

    def delete(self):
        """
        Delete this node.  Mark type as deleted.
        """
        self.start_loops = []
        self.end_loops = []
        X12DataNode.delete(self)

    def get_value(self, x12_path_str):
        """
        Get the value of the first found element at the given path
        @param x12_path_str: Relative X12 Path
        @type x12_path_str: string
        @return: the element value at the relative X12 path
        @rtype: string
        """
        seg_data = self.get_first_matching_segment(x12_path_str)
        if seg_data is None:
            return None
        return seg_data.get_value(x12_path_str)

    def set_value(self, x12_path_str, val):
        """
        Set the value of simple element at the first found segment at the given path
        @param x12_path_str: Relative X12 Path
        @type x12_path_str: string
        @param val: The new element value
        @type val: string
        """
        seg_data = self.get_first_matching_segment(x12_path_str)
        if seg_data is None:
            raise errors.X12PathError('X12 Path is invalid or was not found: %s' % (x12_path_str))
        #ele_idx = self.get_ele_idx(x12_path_str)
        #seg_data.set(ele_idx, val)
        seg_data.set(x12_path_str, val)

    def get_first_matching_segment(self, x12_path_str):
        """
        Get first found Segment at the given relative path.  If the path is not a
        valid relative path or if the given segment index does not exist, the function
        returns None.

        @param x12_path_str: Relative X12 Path
        @type x12_path_str: string
        @return: First matching data segment
        @rtype: L{node<segment.Segment>}
        @raise X12PathError: On blank or invalid path
        """
        (curr, new_path_str) = self._get_start_node(x12_path_str)
        xpath = path.X12Path(new_path_str)
        if len(xpath.loop_list) != 0:
            raise errors.X12PathError('This X12 Path should not contain loops: %s' % (x12_path_str))
        seg_id = xpath.seg_id
        qual = xpath.id_val
        ele_idx = xpath.ele_idx
        if ele_idx is not None and seg_id is None:
            return self.seg_data
        #subele_idx = xpath.subele_idx
        try:
            if curr.x12_map_node.is_match_qual(curr.seg_data, seg_id, qual):
                return curr.seg_data
            return None
        except errors.EngineError as e:
            raise errors.X12PathError('X12 Path is invalid or was not found: %s' % (x12_path_str))
        return None

#    @staticmethod
#    def get_seg_id_parts(x12_path):
#        """
#        Split a X12 segment reference designation into component parts
#        @return: (segment ID, qualifier part, index)
#        @rtype: (string, string, string)
#        @raise X12PathError: On blank or invalid path
#        """
#        if x12_path.find('/') != -1:
#            x12_path = x12_path[x12_path.rfind('/')+1:]
#        pos = x12_path.find('[')
#        if pos != -1:
#            end = x12_path.find(']')
#            if end == -1 or end < pos:
#                raise errors.X12PathError, 'Bad X12 path: %s' % (x12_path)
#            qual = x12_path[pos+1:end]
#            seg_id = x12_path[:pos]
#            idx = x12_path[end+1:]
#            return (seg_part, qual, idx)
#        else:
#            return (x12_path, None)

    def iterate_segments(self):
        """
        Iterate on this node, return the segment
        """
        yield {'type': 'seg', 'id': self.x12_map_node.id, 'path': self.x12_map_node.x12path,
               'segment': self.seg_data, 'seg_count': self.seg_count, 'cur_line_number': self.cur_line_number}

    def iterate_loop_segments(self):
        """
        Iterate over this node and children, return loop start and loop end
        and any segments found
        """
        for loop in self.end_loops:
            yield {'node': loop, 'type': 'loop_end', 'id': loop.id}
        for loop in self.start_loops:
            yield {'node': loop, 'type': 'loop_start', 'id': loop.id}
        yield {'type': 'seg', 'id': self.id, 'segment': self.seg_data,
               'start_loops': self.start_loops, 'end_loops': self.end_loops, 
               'seg_count': self.seg_count, 'cur_line_number': self.cur_line_number,}

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        """
        Returns a copy of this node
        """
        seg_data = self.seg_data.copy()
        ret = X12SegmentDataNode(self.x12_map_node, seg_data, self.parent)
        ret.start_loops = list(self.start_loops)
        ret.end_loops = list(self.end_loops)
        return ret

    def select(self, x12_path_str):
        """
        Segment nodes have no sub-nodes so return None
        @param x12_path_str: Relative X12 path - 2400/2430
        @type x12_path_str: string
        @return: Iterator on the matching sub-nodes, relative to the instance.
        @rtype: L{node<x12context.X12DataNode>}
        """
        return []

    def _select(self, x12path):
        """
        Empty iter for segment nodes
        @param x12path: x12 map path
        @type x12path: L{path<path.X12Path>}
        """
        return []

    #{ Property Accessors
    @property
    def err_ct(self):
        """
        @return: Count of errors for this segment
        @rtype: int
        """
        return len(self.err_isa) + len(self.err_gs) + len(self.err_st) + len(self.err_seg) + len(self.err_ele)


class X12ContextReader(object):
    """
    Read an X12 input stream
    Keep context when needed
    """

    def __init__(self, param, errh, src_file_obj, xslt_files=None, map_path=None):
        """
        @param param: pyx12.param instance
        @param errh: Error Handler object
        @param src_file_obj: Source document
        @type src_file_obj: string
        @rtype: boolean
        """
        self.param = param
        self.map_path = map_path
        self.errh = error_handler.errh_list()
        self.icvn = None
        self.fic = None
        self.vriic = None
        self.tspc = None

        # Get X12 DATA file
        self.src = x12file.X12Reader(src_file_obj)

        #Get Map of Control Segments
        self.map_file = 'x12.control.00501.xml' if self.src.icvn == '00501' else 'x12.control.00401.xml'
        self.control_map = map_if.load_map_file(self.map_file, param, self.map_path)
        self.map_index_if = map_index.map_index(self.map_path)
        self.x12_map_node = self.control_map.getnodebypath('/ISA_LOOP/ISA')
        self.walker = walk_tree()

    #{ Public Methods
    def iter_segments(self, loop_id=None):
        """
        Simple segment or tree iterator
        @return: X12 Data Node - simple segment or tree
        @rtype: L{node<x12context.X12DataNode>}
        """
        cur_tree = None
        cur_data_node = None
        for seg in self.src:
            #find node
            orig_node = self.x12_map_node
            pop_loops = []
            push_loops = []
            errh = error_handler.errh_list()

            if seg.get_seg_id() == 'ISA':
                tpath = '/ISA_LOOP/ISA'
                self.x12_map_node = self.control_map.getnodebypath(tpath)
            elif seg.get_seg_id() == 'GS':
                tpath = '/ISA_LOOP/GS_LOOP/GS'
                self.x12_map_node = self.control_map.getnodebypath(tpath)
            else:
                try:
                    (seg_node, pop_loops, push_loops) = self.walker.walk(self.x12_map_node,
                            seg, errh, self.src.get_seg_count(),
                            self.src.get_cur_line(), self.src.get_ls_id())
                    self.x12_map_node = seg_node
                except errors.EngineError:
                    raise
            if self.x12_map_node is None:
                self.x12_map_node = orig_node
            else:
                seg_id = seg.get_seg_id()
                if seg_id == 'ISA':
                    icvn = seg.get_value('ISA12')
                elif seg_id == 'GS':
                    fic = seg.get_value('GS01')
                    vriic = seg.get_value('GS08')
                    map_file_new = self.map_index_if.get_filename(icvn, vriic, fic)
                    if self.map_file != map_file_new:
                        self.map_file = map_file_new
                        if self.map_file is None:
                            raise pyx12.errors.EngineError("Map not found.  icvn=%s, fic=%s, vriic=%s" %
                                                           (icvn, fic, vriic))
                        cur_map = map_if.load_map_file(self.map_file, self.param, self.map_path)
                        if cur_map.id == '837':
                            self.src.check_837_lx = True
                        else:
                            self.src.check_837_lx = False
                        #self._apply_loop_count(orig_node, cur_map)
                        #self._reset_isa_counts(cur_map)
                        self._reset_counter_to_isa_counts()
                    #self._reset_gs_counts(cur_map)
                    self._reset_counter_to_gs_counts()
                    tpath = '/ISA_LOOP/GS_LOOP/GS'
                    self.x12_map_node = cur_map.getnodebypath(tpath)
                    #self.walker.forceWalkCounterToLoopStart('/ISA_LOOP/GS_LOOP', '/ISA_LOOP/GS_LOOP/GS')
                elif seg_id == 'BHT':
                    if vriic in ('004010X094', '004010X094A1'):
                        tspc = seg.get_value('BHT02')
                        map_file_new = self.map_index_if.get_filename(icvn, vriic, fic, tspc)
                        if self.map_file != map_file_new:
                            self.map_file = map_file_new
                            if self.map_file is None:
                                err_str = "Map not found.  icvn=%s, fic=%s, vriic=%s, tspc=%s" % \
                                    (icvn, fic, vriic, tspc)
                                raise pyx12.errors.EngineError(err_str)
                            cur_map = map_if.load_map_file(self.map_file, self.param, self.map_path)
                            if cur_map.id == '837':
                                self.src.check_837_lx = True
                            else:
                                self.src.check_837_lx = False
                            self._apply_loop_count(self.x12_map_node, cur_map)
                            tpath = '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BHT'
                            self.x12_map_node = cur_map.getnodebypath(tpath)

            node_x12path = self.x12_map_node.x12path
            # If we are in the requested tree, wait until we have the whole thing
            if loop_id is not None and loop_id in node_x12path.loop_list:
                # Are we at the start of the requested tree?
                if node_x12path.loop_list[-1] == loop_id and \
                        self.x12_map_node.is_first_seg_in_loop():
                    if cur_tree is not None:
                        # Found root loop repeat. Yield existing, create new tree
                        yield cur_tree
                    # Make new tree on parent loop
                    #pop_loops = get_pop_loops(cur_data_node.x12_map_node, self.x12_map_node)
                    #pop_loops = [x12_node for x12_node in pop_loops if x12_node.get_path().find(loop_id) == -1]
                    cur_tree = X12LoopDataNode(x12_node=self.x12_map_node.parent, end_loops=pop_loops)  # parent=cur_data_node)
                    cur_data_node = self._add_segment(cur_tree, self.x12_map_node, seg, pop_loops, push_loops)
                    cur_data_node.seg_count = self.src.get_seg_count()
                    cur_data_node.cur_line_number = self.src.get_cur_line()
                else:
                    if cur_data_node is None or self.x12_map_node is None:
                        raise errors.EngineError('Either cur_data_node or self.x12_map_node is None')
                    cur_data_node = self._add_segment(cur_data_node, self.x12_map_node, seg, pop_loops, push_loops)
                    cur_data_node.seg_count = self.src.get_seg_count()
                    cur_data_node.cur_line_number = self.src.get_cur_line()
            else:
                if cur_tree is not None:
                    # We have completed a tree
                    yield cur_tree
                    cur_tree = None
                if cur_data_node is not None:
                    #push_loops = get_push_loops(cur_data_node.x12_map_node, self.x12_map_node)
                    #pop_loops = get_pop_loops(cur_data_node.x12_map_node, self.x12_map_node)
                    if loop_id:
                        pop_loops = [x12_node for x12_node in pop_loops if x12_node.get_path().find(loop_id) == -1]
                    assert loop_id not in [x12.id for x12 in push_loops], 'Loop ID %s should not be in push loops' % (loop_id)
                    assert loop_id not in [x12.id for x12 in pop_loops], 'Loop ID %s should not be in pop loops' % (loop_id)
                    cur_data_node = X12SegmentDataNode(self.x12_map_node, seg, push_loops, pop_loops)
                    cur_data_node.seg_count = self.src.get_seg_count()
                    cur_data_node.cur_line_number = self.src.get_cur_line()
                else:
                    cur_data_node = X12SegmentDataNode(self.x12_map_node, seg)
                    cur_data_node.seg_count = self.src.get_seg_count()
                    cur_data_node.cur_line_number = self.src.get_cur_line()
                # Get errors caught by x12Reader
                errh.handle_errors(self.src.pop_errors())
                # Handle errors captured in errh_list
                cur_data_node.handle_errh_errors(errh)
                if cur_data_node.id != 'ISA' and cur_data_node is not None:
                    assert cur_data_node.parent is not None, 'Node "%s" has no parent' % (cur_data_node.id)
                yield cur_data_node

    def register_error_callback(self, callback, err_type):
        """
        Future:  Callbacks for X12 validation errors
        """
        pass

    #{ Property Accessors
    @property
    def seg_term(self):
        """
        @return: Current X12 segment terminator
        @rtype: string
        """
        return self.src.seg_term

    @property
    def ele_term(self):
        """
        @return: Current X12 element terminator
        @rtype: string
        """
        return self.src.ele_term

    @property
    def subele_term(self):
        """
        @return: Current X12 sub-element terminator
        @rtype: string
        """
        return self.src.subele_term

    @property
    def cur_seg_count(self):
        return self.src.get_seg_count()

    @property
    def get_cur_line(self):
        return self.src.get_cur_line()

    #{ Private Methods
    def _add_segment(self, cur_data_node, segment_x12_node, seg_data, pop_loops, push_loops):
        """
        From the last position in the X12 Data Node Tree, find the correct
        position for the new segment; moving up or down the tree as appropriate.

        G{callgraph}

        @param cur_data_node: Current X12 Data Node
        @type cur_data_node: L{node<x12context.X12DataNode>}
        @param segment_x12_node: Segment Map Node
        @type segment_x12_node: L{node<map_if.x12_node>}
        @return: New X12 Data Node
        @rtype: L{node<x12context.X12DataNode>}
        """
        if not segment_x12_node.is_segment():
            raise errors.EngineError('Node must be a segment')
        # Get enclosing loop
        orig_data_node = cur_data_node
        parent_x12_node = pop_to_parent_loop(segment_x12_node)
        cur_loop_node = cur_data_node
        if cur_loop_node.type == 'seg':
            cur_loop_node = cur_loop_node.parent
        # check path for new loops to be added
        new_path = parent_x12_node.x12path
        last_path = cur_loop_node.x12_map_node.x12path
        if last_path != new_path:
            for x12_loop in pop_loops:
                if cur_loop_node.id != x12_loop.id:
                    raise errors.EngineError('Loop pop: %s != %s' %
                                             (cur_loop_node.id, x12_loop.id))
                cur_loop_node = cur_loop_node.parent
            for x12_loop in push_loops:
                if cur_loop_node is None:
                    raise errors.EngineError('cur_loop_node is None. x12_loop: %s' % (x12_loop.id))
                # push new loop nodes, if needed
                cur_loop_node = cur_loop_node._add_loop_node(x12_loop)
        else:
            # handle loop repeat
            if cur_loop_node.parent is not None and segment_x12_node.is_first_seg_in_loop():
                cur_loop_node = cur_loop_node.parent._add_loop_node(
                    segment_x12_node.parent)
        try:
            new_node = X12SegmentDataNode(self.x12_map_node, seg_data)
        except Exception:
            mypath = self.x12_map_node.get_path()
            err_str = 'X12SegmentDataNode failed: x12_path={}, seg_date={}'.format(mypath, seg_data)
            raise errors.EngineError(err_str)
        try:
            new_node.parent = cur_loop_node
            cur_loop_node.children.append(new_node)
        except Exception:
            err_str = 'X12SegmentDataNode child append failed:'
            err_str += ' seg_x12_path=%s' % (segment_x12_node.get_path())
            err_str += ', orig_datanode=%s' % (orig_data_node.cur_path)
            err_str += ', cur_datanode=%s' % (cur_data_node.cur_path)
            err_str += ', seg_data=%s' % (seg_data)
            raise errors.EngineError(err_str)
        return new_node

    #def _apply_loop_count(self, orig_node, new_map):
    #    """
    #    Apply loop counts to current map
    #    """
    #    ct_list = []
    #    orig_node.get_counts_list(ct_list)
    #    for (path1, ct) in ct_list:
    #        curnode = new_map.getnodebypath(path1)
    #        curnode.set_cur_count(ct)

    #def _reset_isa_counts(self, cur_map):
    #    """
    #    Reset ISA instance counts
    #    """
    #    cur_map.getnodebypath('/ISA_LOOP').set_cur_count(1)
    #    cur_map.getnodebypath('/ISA_LOOP/ISA').set_cur_count(1)

    #def _reset_gs_counts(self, cur_map):
    #    """
    #    Reset GS instance counts
    #    """
    #    cur_map.getnodebypath('/ISA_LOOP/GS_LOOP').reset_cur_count()
    #    cur_map.getnodebypath('/ISA_LOOP/GS_LOOP').set_cur_count(1)
    #    cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS').set_cur_count(1)

    def _reset_counter_to_isa_counts(self):
        """
        Reset ISA instance counts
        """
        self.walker.counter.reset_to_node('/ISA_LOOP')
        self.walker.counter.increment('/ISA_LOOP')
        self.walker.counter.increment('/ISA_LOOP/ISA')

    def _reset_counter_to_gs_counts(self):
        """
        Reset GS instance counts
        """
        self.walker.counter.reset_to_node('/ISA_LOOP/GS_LOOP')
        self.walker.counter.increment('/ISA_LOOP/GS_LOOP')
        self.walker.counter.increment('/ISA_LOOP/GS_LOOP/GS')
