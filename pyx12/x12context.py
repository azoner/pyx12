#####################################################################
# Copyright (c) 2008-2009 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Parse a ANSI X12 data file.

Maintain context state
Start saving context and segments
Interface to read and alter segments

@todo: Attach errors to returned dicts
"""
#G{classtree X12DataNode}

import os, os.path

# Intrapackage imports
import pyx12
import error_handler
import errors
import map_index
import map_if
import x12file
from map_walker import walk_tree, pop_to_parent_loop #, get_pop_loops, get_push_loops

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
        raise NotImplementedError, 'Override in sub-class'

    def iterate_loop_segments(self):
        """
        Iterate over this node and children, return loop start and loop end 
        and any segments found 
        """
        raise NotImplementedError, 'Override in sub-class'

    def get_value(self, x12_path):
        """
        @return: the element value at the relative X12 path
        @rtype: string
        """
        raise NotImplementedError, 'Override in sub-class'

    def exists(self, x12_path):
        """
        Does at least one child at the x12-path exist?
        @param x12_path: Relative X12 path - 2400/2430
        @type x12_path: string
        @return: True if found
        @rtype: boolean
        """
        path_list = self._get_path_list(x12_path)
        for n in self._select(path_list):
            return True
        return False

    def select(self, x12_path):
        """
        Get a slice of sub-nodes at the relative X12 path.
        @note: All interaction/modification with a X12DataNode tree (having a loop 
        root) is done in place.
        @param x12_path: Relative X12 path - 2400/2430
        @type x12_path: string
        @return: Iterator on the matching sub-nodes, relative to the instance.
        @rtype: L{node<x12context.X12DataNode>}
        """
        path_list = self._get_path_list(x12_path)
        for n in self._select(path_list):
            yield n

    def count(self, x12_path):
        """
        Get a count of sub-nodes at the relative X12 path.
        @param x12_path: Relative X12 path - 2400/2430
        @type x12_path: string
        @return: Count of matching sub-nodes
        @rtype: int
        """
        ct = 0
        path_list = self._get_path_list(x12_path)
        for n in self._select(path_list):
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
        """
        self._cleanup()
        map_idx = x12_node.index
        for i in range(len(self.children)):
            if self.children[i].x12_map_node.index > map_idx:
                return i
        return len(self.children)

    def _get_path_list(self, path_str):
        """
        Get list of path nodes from path string
        @rtype: list
        """
        return [x for x in path_str.split('/') if x!='']

    def _is_child_path(self, root_path, child_path):
        """
        Is the child path really a child of the root path?
        @type root_path: string
        @type child_path: string
        @return: True if a child
        @rtype: boolean
        """
        root = root_path.split('/')
        child = child_path.split('/')
        if len(root) >= len(child):
            return False
        for i in range(len(root)):
            if root[i] != child[i]:
                return False
        return True

    def _select(self, path_list):
        """
        Get the child node at the path
        @param path_list: List of x12_map_node IDs
        @type path_list: [string]
        """
        if len(path_list) == 1:
            cur_node_id = path_list[0]
            for child in [x for x in self.children if x.type is not None]:
                if child.id == cur_node_id:
                    yield child
        elif len(path_list) > 1:
            cur_node_id = path_list[0]
            #del path_list[0]
            new_path = path_list[1:]
            for child in [x for x in self.children if x.type is not None]:
                if child.id == cur_node_id:
                    for n in child._select(new_path):
                        yield n

    #{ Property Accessors
    def _get_id(self):
        """
        @return: x12 node id
        @rtype: string
        """
        return self.x12_map_node.id

    id = property(_get_id, None, None)

    def _get_cur_path(self):
        """
        @return: x12 node path
        @rtype: string
        """
        return self.x12_map_node.get_path()

    cur_path = property(_get_cur_path, None, None)


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
        self.end_loops = end_loops # we might need to close a preceeding loop

    #{ Public Methods
    def delete(self):
        """
        Delete this node.  Mark type as deleted.
        """
        self.end_loops = []
        X12DataNode.delete(self)

    def get_value(self, x12_path):
        """
        Returns the element value at the given relative path.  If the path is not a
        valid relative path or if the given segment index does not exist, the function
        returns None.  If multiple values exist, this function returns the first.

        @param x12_path: Relative X12 Path
        @type x12_path: string
        @return: the element value at the relative X12 path
        @rtype: string
        @raise X12PathError: On blank or invalid path
        """
        if len(x12_path) == 0:
            raise errors.X12PathError, 'Blank X12 Path'
        elif x12_path.find('/') == -1:
            try:
                for seg in [seg for seg in self.children if seg.type == 'seg']:
                    if x12_path.startswith(seg.id):
                        val = seg.get_value(x12_path)
                        if val is not None:
                            return val
                return None
                    #raise 'X12PathError', 'X12 Path is invalid or was not found: %s' % (x12_path)
            except errors.EngineError, e:
                raise
                #raise X12PathError, e.message
                raise errors.X12PathError, 'X12 Path is invalid or was not found: %s' % (x12_path)
        else:
            plist = x12_path.split('/')
            next_id = plist[0]
            plist = plist[1:]
            try:
                for loop in [loop for loop in self.children if loop.type == 'loop']:
                    if loop.id == next_id:
                        return loop.get_value('/'.join(plist))
                return None
                    #raise 'X12PathError', 'X12 Path is invalid or was not found: %s' % (x12_path)
            except errors.EngineError, e:
                raise
                raise errors.X12PathError, 'X12 Path is invalid or was not found: %s' % (x12_path)

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
            raise errors.X12PathError, 'The segment %s is not a member of loop %s' % \
                (seg_data.__repr__(), self.id)
        new_data_node = X12SegmentDataNode(x12_seg_node, seg_data, self)
        #idx = x12_seg_node.index
        # Iterate over data nodes
        #self._cleanup()
        #child_idx = len(self.children)
        #for i in range(len(self.children)):
        #    if self.children[i].x12_map_node.index > idx:
        #        child_idx = i
        #        break
        #self.children.insert(self._get_insert_idx(x12_seg_node), new_data_node)
        #assert(child_idx==self._get_insert_idx(x12_seg_node))
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
            raise errors.X12PathError, 'The segment %s is not a member of loop %s' % \
                (seg_data.__repr__(), self.id)
        new_data_loop = self._add_loop_node(x12_loop_node)
        # Now, add the segment
        x12_seg_node = new_data_loop.x12_map_node.get_child_seg_node(seg_data)
        new_data_node = X12SegmentDataNode(x12_seg_node, seg_data, new_data_loop)
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
            raise errors.X12PathError, 'The loop_data_node "%s" is not a child of "%s"' % \
                (data_node.x12_map_node.id,  self.x12_map_node.id)
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
        for i in range(1,len(self.children)):
            if self.children[i].type == 'seg' and self.children[i].seg_data == seg_data:
                del self.children[i]
                return True
        return False

    def delete_node(self, x12_path):
        """
        Delete the first node at the given relative path.  If the path is not a
        valid relative path, return False If multiple values exist, this
        function deletes the first.

        @return: True if found and deleted, else False
        @rtype: Boolean
        @raise X12PathError: On blank or invalid path
        @todo: Check counts?
        """
        if len(x12_path) == 0:
            raise errors.X12PathError, 'Blank X12 Path'
        elif x12_path.find('/') == -1:
            try:
                for i in range(len(self.children)):
                    if self.children[i].type == 'seg' and x12_path.startswith(self.children[i].id):
                        del self.children[i]
                        return True
                    elif self.children[i].type == 'loop' and self.children[i].id == x12_path:
                        del self.children[i]
                        return True
                return False
            except errors.EngineError, e:
                raise errors.X12PathError, 'X12 Path is invalid or was not found: %s' % (x12_path)
        else:
            plist = x12_path.split('/')
            next_id = plist[0]
            plist = plist[1:]
            try:
                for i in range(len(self.children)):
                    if self.children[i].type == 'loop' and self.children[i].id == next_id:
                        if len(plist) > 1:
                            return self.children[i].delete_node('/'.join(plist))
                return False
            except errors.EngineError, e:
                raise errors.X12PathError, 'X12 Path is invalid or was not found: %s' % (x12_path)

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
        #idx = x12_loop_node.index
        #self._cleanup()
        #child_idx = len(self.children)
        #for i in range(len(self.children)):
        #    if self.children[i].x12_map_node.index > idx:
        #        child_idx = i
        #        break
        #self.children.insert(self._get_insert_idx(x12_loop_node), new_node)
        #assert(child_idx==self._get_insert_idx(x12_loop_node))
        child_idx = self._get_insert_idx(x12_loop_node)
        self.children.insert(child_idx, new_node)
        return new_node

    def _get_segment(self, seg_obj):
        """
        Get a  pyx12.segment.Segment instance, building one from a string
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
            raise errors.EngineError, 'Unknown type for seg_obj %s' % (seg_obj)

    def _get_terminators(self):
        #import pdb
        #pdb.set_trace()
        for child in self.children:
            if isinstance(child, X12SegmentDataNode) and child.seg_data is not None \
                    and child.seg_data.seg_term is not None:
                return (child.seg_data.seg_term, child.seg_data.ele_term, child.seg_data.subele_term)
        return self.parent._get_terminators()

class X12SegmentDataNode(X12DataNode):
    """
    Capture the segment data and X12 definition
    Alter relational data
    Iterate over contents
    """
    def __init__(self, x12_node, seg_data, parent=None, start_loops=[], \
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

    def get_value(self, x12_path):
        """
        @return: the element value at the relative X12 path
        @rtype: string
        """
        try:
            (seg_part, qual) = X12SegmentDataNode.get_seg_id(x12_path)
            if qual is not None:
                if self.seg_data.get_value('01') == qual:
                    return self.seg_data.get_value(seg_part)
                else:
                    return None
            else:
                return self.seg_data.get_value(x12_path)
        except errors.EngineError:
            raise
        return None

    @staticmethod
    def get_seg_id(x12_path):
        """
        Split a X12 segment reference designation into the segment part 
        and the qualifier part.
        @return: (segment part, qualifier part)
        @rtype: (string, string)
        """
        pos = x12_path.find('[')
        if pos != -1:
            end = x12_path.find(']')
            if end == -1 or end < pos:
                raise errors.X12PathError, 'Bad X12 path: %s' % (x12_path)
            qual = x12_path[pos+1:end]
            seg_part = x12_path[:pos] + x12_path[end+1:]
            return (seg_part, qual)
        else:
            return (x12_path, None)

    def iterate_segments(self):
        """
        Iterate on this node, return the segment
        """
        yield {'type': 'seg', 'id': self.x12_map_node.id, \
            'segment': self.seg_data}

    def iterate_loop_segments(self):
        """
        Iterate over this node and children, return loop start and loop end 
        and any segments found 
        """
        for loop in self.end_loops:
            yield {'node': loop, 'type': 'loop_end', 'id': loop.id}
        for loop in self.start_loops:
            yield {'node': loop, 'type': 'loop_start', 'id': loop.id}
        yield {'type': 'seg', 'id': self.id, 'segment': self.seg_data, \
            'start_loops': self.start_loops, 'end_loops': self.end_loops}

    #{ Property Accessors
    def _get_err_ct(self):
        """
        @return: Count of errors for this segment
        @rtype: int
        """
        return len(self.err_isa) + len(self.err_gs) + len(self.err_st) + len(self.err_seg) + len(self.err_ele)

    err_ct = property(_get_err_ct, None, None)


class X12ContextReader(object):
    """
    Read an X12 input stream
    Keep context when needed
    """

    def __init__(self, param, errh, src_file_obj, xslt_files = []):
        """
        @param param: pyx12.param instance
        @param errh: Error Handler object
        @param src_file_obj: Source document
        @type src_file_obj: string
        @rtype: boolean
        """
        map_path = param.get('map_path')
        self.param = param
        self.errh = error_handler.errh_list()
        self.xslt_files = xslt_files
        self.icvn = None
        self.fic = None
        self.vriic = None
        self.tspc = None
        
        # Get X12 DATA file
        self.src = x12file.X12Reader(src_file_obj) 

        #Get Map of Control Segments
        self.map_file = 'x12.control.00401.xml'
        self.control_map = map_if.load_map_file(os.path.join(map_path, self.map_file), param)
        self.map_index_if = map_index.map_index(os.path.join(map_path, 'maps.xml'))
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
                    (seg_node, pop_loops, push_loops) = self.walker.walk(self.x12_map_node, \
                        seg, errh, self.src.get_seg_count(), \
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
                        #map_abbr = self.map_index_if.get_abbr(icvn, vriic, fic)
                        self.map_file = map_file_new
                        if self.map_file is None:
                            raise pyx12.errors.EngineError, \
                                "Map not found.  icvn=%s, fic=%s, vriic=%s" % \
                                (icvn, fic, vriic)
                        cur_map = map_if.load_map_file(self.map_file, self.param, self.xslt_files)
                        self._apply_loop_count(orig_node, cur_map)
                        self._reset_isa_counts(cur_map)
                    self._reset_gs_counts(cur_map)
                    tpath = '/ISA_LOOP/GS_LOOP/GS'
                    self.x12_map_node = cur_map.getnodebypath(tpath)
                elif seg_id == 'BHT':
                    if vriic in ('004010X094', '004010X094A1'):
                        tspc = seg.get_value('BHT02')
                        map_file_new = self.map_index_if.get_filename(icvn, \
                            vriic, fic, tspc)
                        if self.map_file != map_file_new:
                            #map_abbr = self.map_index_if.get_abbr(icvn, \
                            #    vriic, fic, tspc)
                            self.map_file = map_file_new
                            if self.map_file is None:
                                err_str = "Map not found.  icvn=%s, fic=%s, vriic=%s, tspc=%s" % \
                                    (icvn, fic, vriic, tspc)
                                raise pyx12.errors.EngineError, err_str
                            cur_map = map_if.load_map_file(self.map_file, \
                                self.param, self.xslt_files)
                            self._apply_loop_count(self.x12_map_node, cur_map)
                            tpath = '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BHT'
                            self.x12_map_node = cur_map.getnodebypath(tpath)

            node_path = self._get_path_list(self.x12_map_node.get_path())
            # If we are in the requested tree, wait until we have the whole thing
            if loop_id is not None and loop_id in node_path:
                #pdb.set_trace()
                # Are we at the start of the requested tree? 
                if node_path[-2] == loop_id and \
                        self.x12_map_node.is_first_seg_in_loop():
                    if cur_tree is not None:
                        # Found root loop repeat. Yield existing, create new tree
                        yield cur_tree
                    # Make new tree on parent loop
                    #pop_loops = get_pop_loops(cur_data_node.x12_map_node, self.x12_map_node)
                    #pop_loops = [x12_node for x12_node in pop_loops if x12_node.get_path().find(loop_id) == -1]
                    cur_tree = X12LoopDataNode(self.x12_map_node.parent, pop_loops)
                    cur_data_node = self._add_segment(cur_tree, self.x12_map_node, seg, pop_loops, push_loops)
                else:
                    if cur_data_node is None or self.x12_map_node is None:
                        raise errors.EngineError, 'Either cur_data_node or self.x12_map_node is None'
                    cur_data_node = self._add_segment(cur_data_node, self.x12_map_node, seg, pop_loops, push_loops)
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
                    cur_data_node = X12SegmentDataNode(self.x12_map_node, seg, None, push_loops, pop_loops)
                else:
                    cur_data_node = X12SegmentDataNode(self.x12_map_node, seg)
                # Get errors caught by x12Reader
                errh.handle_errors(self.src.pop_errors())
                # Handle errors captured in errh_list
                cur_data_node.handle_errh_errors(errh)
                yield cur_data_node
        
    def register_error_callback(self, callback, err_type):
        """
        Future:  Callbacks for X12 validation errors
        """
        pass

    #{ Property Accessors
    def _get_seg_term(self):
        """
        @return: Current X12 segment terminator
        @rtype: string
        """
        return self.src.seg_term

    seg_term = property(_get_seg_term, None, None)

    def _get_ele_term(self):
        """
        @return: Current X12 element terminator
        @rtype: string
        """
        return self.src.ele_term

    ele_term = property(_get_ele_term, None, None)

    def _get_subele_term(self):
        """
        @return: Current X12 sub-element terminator
        @rtype: string
        """
        return self.src.subele_term

    subele_term = property(_get_subele_term, None, None)

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
            raise errors.EngineError, 'Node must be a segment'
        # Get enclosing loop
        orig_data_node = cur_data_node
        parent_x12_node = pop_to_parent_loop(segment_x12_node) 
        cur_loop_node = cur_data_node
        if cur_loop_node.type == 'seg':
            cur_loop_node = cur_loop_node.parent
        # check path for new loops to be added
        new_path_list = self._get_path_list(parent_x12_node.get_path())
        last_path_list = self._get_path_list(cur_loop_node.cur_path)
        if last_path_list != new_path_list:
            for x12_loop in pop_loops:
            #for x12_loop in get_pop_loops(cur_data_node.x12_map_node, segment_x12_node):
                if cur_loop_node.id != x12_loop.id:
                    raise errors.EngineError, 'Loop pop: %s != %s' % (cur_loop_node.id, x12_loop.id)
                cur_loop_node = cur_loop_node.parent
            #for i in range(match_idx, len(new_path_list)):
            for x12_loop in push_loops:
            #for x12_loop in get_push_loops(cur_data_node.x12_map_node, \
            #        segment_x12_node):
                if cur_loop_node is None:
                    raise errors.EngineError, 'cur_loop_node is None. x12_loop: %s' % (x12_loop.id)
                # push new loop nodes, if needed
                cur_loop_node = cur_loop_node._add_loop_node(x12_loop)
        else:
            # handle loop repeat
            if cur_loop_node.parent is not None and segment_x12_node.is_first_seg_in_loop():
                cur_loop_node = cur_loop_node.parent._add_loop_node(segment_x12_node.parent)
        try:
            new_node = X12SegmentDataNode(self.x12_map_node, seg_data)
        except:
            raise errors.EngineError, 'X12SegmentDataNode failed: x12_path=%s, seg_date=%s ' % \
                (self.x12_map_node.get_path(), seg_data)
        try:
            cur_loop_node.children.append(new_node)
            new_node.parent = cur_loop_node
        except:
            err_str = 'X12SegmentDataNode child append failed:'
            err_str += ' seg_x12_path=%s' % (segment_x12_node.get_path())
            err_str += ', orig_datanode=%s' % (orig_data_node.cur_path)
            err_str += ', cur_datanode=%s' % (cur_data_node.cur_path)
            err_str += ', seg_data=%s' % (seg_data)
            raise errors.EngineError, err_str
        return new_node

    def _apply_loop_count(self, orig_node, new_map):
        """
        Apply loop counts to current map
        """
        ct_list = []
        orig_node.get_counts_list(ct_list)
        for (path, ct) in ct_list:
            curnode = new_map.getnodebypath(path)
            curnode.set_cur_count(ct)

    def _get_path_list(self, path_str):
        """
        Get list of path nodes from path string
        @rtype: list
        """
        return [x for x in path_str.split('/') if x!='']

#    def _get_path_match_idx(self, last_path, cur_path, seg_x12_node):
#        """
#        Get the index of the last matching path nodes
#        @param last_path: list of map ids
#        @type last_path: list of strings 
#        @param cur_path: list of map ids
#        @type cur_path: list of strings 
#        @param seg_x12_node: Segment Map Node
#        @type seg_x12_node: L{node<map_if.x12_node>}
#        """
#        match_idx = 0
#        for i in range(min(len(cur_path), len(last_path))):
#            if cur_path[i] != last_path[i]:
#                break
#            match_idx += 1
#        root_path = self._get_root_path(last_path, cur_path)
#        if seg_x12_node.is_first_seg_in_loop() \
#                and root_path == cur_path:
#            match_idx -= 1
#        return match_idx

#    def _get_parent_x12_loop(self, loop_id, start_x12_node):
#        """
#        From a segment X12 node, return the matching parent x12 loop node
#        """
#        x12_node = start_x12_node
#        while not x12_node.is_map_root():
#            if x12_node.id == loop_id:
#                return x12_node
#            else:
#                x12_node = x12_node.parent
#        return None

#    def _get_root_path(self, path_list1, path_list2):
#        """
#        @param path_list1: list of map ids
#        @type path_list1: list of strings 
#        @param path_list2: list of map ids
#        @type path_list2: list of strings 
#        @return: Common path prefix
#        @rtype: list of strings 
#        """
#        return self._get_path_list(os.path.commonprefix(
#            ['/'.join(path_list1), '/'.join(path_list2)]))

    #def _get_loop_pop_list(self, old_path_list, new_path_list):

    def _reset_isa_counts(self, cur_map):
        """
        Reset ISA instance counts
        """
        cur_map.getnodebypath('/ISA_LOOP').set_cur_count(1)
        cur_map.getnodebypath('/ISA_LOOP/ISA').set_cur_count(1)

    def _reset_gs_counts(self, cur_map):
        """
        Reset GS instance counts
        """
        cur_map.getnodebypath('/ISA_LOOP/GS_LOOP').reset_cur_count()
        cur_map.getnodebypath('/ISA_LOOP/GS_LOOP').set_cur_count(1)
        cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS').set_cur_count(1)

