#####################################################################
# Copyright (c) 2008-2009 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#
#    $Id: x12n_document.py 1312 2008-10-05 02:54:39Z johnholland $

"""
Parse a ANSI X12 data file.

Maintain context state
Start saving context and segments
Interface to read and alter segments
Should have multiple contexts ??
Able to save and release independantly ??
Notify if an expected segment instance does not exist ??

"""

import os, os.path
#import pdb

# Intrapackage imports
import pyx12
#import error_handler
import errors
import map_index
import map_if
import x12file
from map_walker import walk_tree, pop_to_parent_loop

class X12DataNode(object):
    """
    Capture the segment data and X12 definition for a loop subtree
    Alter relational data
    Iterate over contents
    """
    def __init__(self, x12_node, seg_data, type='seg'):
        """
        """
        self.x12_map_node = x12_node
        self.cur_path = self.x12_map_node.get_path().split('/')[1:]
        self.type = type
        self.seg_data = seg_data
        self.parent = None
        self.children = []
        self.errors = []

    def AddChild(self, x12_node, seg_data):
        new_seg = X12DataNode(x12_node, seg_data)
        match_path = x12_node.get_path()
# Create a new node
# Find the correct parent
# If needed, create the loop node
# Append the node, set parent property

    def _isChildPath(self, root_path, child_path):
        """
        Is the child path really a child of the root path?
        @type root_path: string
        @type child_path: string
        """
        root = root_path.split('/')
        child = child_path.split('/')
        if len(root) >= len(child):
            return False
        for i in range(len(root)):
            if root[i] != child[i]:
                return False
        return True

    def _addLoop(self, x12_node):
        new_loop = X12DataNode(x12_node, None, 'loop')
# Append the node, set parent property

    #def _findParentNode(self, find_path):

def IterateSegments(tree):
    if tree.type == 'seg':
        yield {'type': 'seg', 'id': tree.x12_map_node.id, 'segment': tree.seg_data}
    for child in tree.children:
        IterateSegments(child)

def IterateLoopSegments(tree):
    if tree.type == 'loop':
        yield {'type': 'loop_start', 'id': tree.x12_map_node.id, 'node': tree.x12_map_node}
    elif tree.type == 'seg':
        yield {'type': 'seg', 'id': tree.x12_map_node.id, 'segment': tree.seg_data}
    for child in tree.children:
        IterateLoopSegments(child)
    if tree.type == 'loop':
        yield {'type': 'loop_end', 'id': tree.x12_map_node.id, 'node': tree.x12_map_node}


class X12ContextReader(object):

    def __init__(self, param, errh, src_file_obj, xslt_files = []):
        """
        Read an X12 input stream
        Keep context when needed

        @param param: pyx12.param instance
        @param errh: Error Handler object
        @param src_file_obj: Source document
        @type src_file_obj: string
        @rtype: boolean
        """
        map_path = param.get('map_path')
        self.param = param
        self.errh = errh
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

    def IterSegments(self, loop_id=None):
        map_abbr = 'x12'
        cur_tree = None
        cur_data_node = None
        for seg in self.src:
            #find node
            orig_node = self.x12_map_node
            
            if seg.get_seg_id() == 'ISA':
                self.x12_map_node = self.control_map.getnodebypath('/ISA_LOOP/ISA')
            elif seg.get_seg_id() == 'GS':
                self.x12_map_node = self.control_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
            else:
                try:
                    self.x12_map_node = self.walker.walk(self.x12_map_node, seg, self.errh, self.src.get_seg_count(), \
                        self.src.get_cur_line(), self.src.get_ls_id())
                except errors.EngineError:
                    raise
            if self.x12_map_node is None:
                self.x12_map_node = orig_node
            else:
                if seg.get_seg_id() == 'ISA':
                    self. errh.add_isa_loop(seg, self.src)
                    icvn = seg.get_value('ISA12')
                    self.errh.handle_errors(self.src.pop_errors())
                elif seg.get_seg_id() == 'IEA':
                    self.errh.handle_errors(self.src.pop_errors())
                    self.errh.close_isa_loop(self.x12_map_node, seg, self.src)
                elif seg.get_seg_id() == 'GS':
                    fic = seg.get_value('GS01')
                    vriic = seg.get_value('GS08')
                    map_file_new = self.map_index_if.get_filename(icvn, vriic, fic)
                    if self.map_file != map_file_new:
                        map_abbr = self.map_index_if.get_abbr(icvn, vriic, fic)
                        self.map_file = map_file_new
                        if self.map_file is None:
                            raise pyx12.errors.EngineError, "Map not found.  icvn=%s, fic=%s, vriic=%s" % \
                                (icvn, fic, vriic)
                        self.cur_map = map_if.load_map_file(self.map_file, self.param, self.xslt_files)
                        self._apply_loop_count(orig_node, self.cur_map)
                        self._reset_isa_counts(self.cur_map)
                    self._reset_gs_counts(self.cur_map)
                    self.x12_map_node = self.cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
                    self.errh.add_gs_loop(seg, self.src)
                    self.errh.handle_errors(self.src.pop_errors())
                elif seg.get_seg_id() == 'BHT':
                    if vriic in ('004010X094', '004010X094A1'):
                        tspc = seg.get_value('BHT02')
                        map_file_new = self.map_index_if.get_filename(icvn, vriic, fic, tspc)
                        if self.map_file != map_file_new:
                            map_abbr = self.map_index_if.get_abbr(icvn, vriic, fic, tspc)
                            self.map_file = map_file_new
                            if self.map_file is None:
                                raise pyx12.errors.EngineError, "Map not found.  icvn=%s, fic=%s, vriic=%s, tspc=%s" % \
                                    (icvn, fic, vriic, tspc)
                            self.cur_map = map_if.load_map_file(self.map_file, self.param, self.xslt_files)
                            self._apply_loop_count(self.x12_map_node, self.cur_map)
                            self.x12_map_node = self.cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BHT')
                    self.errh.add_seg(self.x12_map_node, seg, self.src.get_seg_count(), \
                        self.src.get_cur_line(), self.src.get_ls_id())
                    self.errh.handle_errors(self.src.pop_errors())
                elif seg.get_seg_id() == 'GE':
                    self.errh.handle_errors(self.src.pop_errors())
                    self.errh.close_gs_loop(self.x12_map_node, seg, self.src)
                elif seg.get_seg_id() == 'ST':
                    self.errh.add_st_loop(seg, self.src)
                    self.errh.handle_errors(self.src.pop_errors())
                elif seg.get_seg_id() == 'SE':
                    self.errh.handle_errors(self.src.pop_errors())
                    self.errh.close_st_loop(self.x12_map_node, seg, self.src)
                else:
                    self.errh.add_seg(self.x12_map_node, seg, self.src.get_seg_count(), \
                        self.src.get_cur_line(), self.src.get_ls_id())
                    self.errh.handle_errors(self.src.pop_errors())

            node_path = self.x12_map_node.get_path().split('/')[1:]
            # If we are in the requested tree, wait until we have the whole thing
            if loop_id is not None and loop_id in node_path:
                # Are we at the start of the requested tree? 
                if node_path == loop_id and self.x12_map_node.is_first_seg_in_loop():
                    # Found loop repeat. Close existing, create new tree
                    yield cur_tree
                    # Make new tree on parent loop
                    cur_tree = X12DataNode(self.x12_map_node.parent, None, 'loop')
                    cur_data_node = cur_tree
                    cur_data_node = self._addSegment(cur_data_node, self.x12_map_node)
                else:
                    #cur_tree.AddSegment(self.x12_map_node, seg)
                    cur_data_node = self._addSegment(cur_data_node, self.x12_map_node)
            else:
                cur_data_node = X12DataNode(self.x12_map_node, seg)
                yield cur_data_node
        
    def _addSegment(self, cur_data_node, segment_x12_node): #, seg_data):
        """
        From the last position in the X12 Data Node Tree, find the correct
        position for the new segment.  Move up or down the tree as appropriate.
        Do not need to deal with loop repeats

        @param cur_data_node: Current X12 Data Node
        @type cur_data_node: L{node<x12context.X12DataNode>}
        @param segment_x12_node: Segment Map Node
        @type segment_x12_node: L{node<map_if.x12_node>}
        @return: New X12 Data Node
        @rtype: L{node<x12context.X12DataNode>}
        """
        # Logic copied from x12xml
        if not segment_x12_node.is_segment():
            raise errors.EngineError, 'Node must be a segment'
        parent_x12_node = pop_to_parent_loop(segment_x12_node) # Get enclosing loop
        # check path for new loops to be added
        new_path_list = self._path_list(parent_x12_node.get_path())
        last_path_list = self._path_list(cur_data_node.cur_path)
        if last_path_list != new_path_list:
            match_idx = self._get_path_match_idx(last_path_list, new_path_list)
            root_path = self._path_list(os.path.commonprefix(
                ['/'.join(new_path_list), '/'.join(last_path_list)]))
            if segment_x12_node.is_first_seg_in_loop() and root_path == new_path_list:
                match_idx -= 1
            for i in range(len(last_path_list)-1, match_idx-1, -1):
                # pop loop
                cur_data_node = cur_data_node.parent
            for i in range(match_idx, len(new_path_list)):
                # push new loop nodes, if needed
                self._get_parent_x12_loop(new_path_list[i], segment_x12_node)
                new_node = X12DataNode(parent_x12_node, None, 'loop')
                cur_data_node.children.append(new_node)
                new_node.parent = cur_data_node
                cur_data_node = new_node
        return cur_data_node

    def _apply_loop_count(self, orig_node, new_map):
        """
        Apply loop counts to current map
        """
        ct_list = []
        orig_node.get_counts_list(ct_list)
        for (path, ct) in ct_list:
            curnode = new_map.getnodebypath(path)
            curnode.set_cur_count(ct)

    def _reset_isa_counts(self, cur_map):
        cur_map.getnodebypath('/ISA_LOOP').set_cur_count(1)
        cur_map.getnodebypath('/ISA_LOOP/ISA').set_cur_count(1)

    def _reset_gs_counts(self, cur_map):
        cur_map.getnodebypath('/ISA_LOOP/GS_LOOP').reset_cur_count()
        cur_map.getnodebypath('/ISA_LOOP/GS_LOOP').set_cur_count(1)
        cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS').set_cur_count(1)

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

    def _get_parent_x12_loop(self, loop_id, start_x12_node):
        """
        From a segment X12 node, return the matching parent x12 loop node
        """
        x12_node = start_x12_node
        while not x12_node.is_map_root():
            if x12_node.id == loop_id:
                return x12_node
            else:
                x12_node = x12_node.parent
        return None
