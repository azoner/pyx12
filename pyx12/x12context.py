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
Should have multiple contexts
Able to save and release independantly
Notify if an expected segment instance does not exist

"""

import os, os.path

# Intrapackage imports
import pyx12
#import error_handler
import errors
import map_index
import map_if
import x12file
from map_walker import walk_tree


class X12ContextReader(object):

    def __init__(self, param, errh, src_file, xslt_files = []):
        """
        Read an X12 input stream
        Keep context when needed

        @param param: pyx12.param instance
        @param errh: Error Handler object
        @param src_file: Source document
        @type src_file: string
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
        self.src = x12file.X12Reader(src_file) 

        #Get Map of Control Segments
        self.map_file = 'x12.control.00401.xml'
        self.control_map = map_if.load_map_file(os.path.join(map_path, self.map_file), param)
        self.map_index_if = map_index.map_index(os.path.join(map_path, 'maps.xml'))
        self.node = self.control_map.getnodebypath('/ISA_LOOP/ISA')
        self.walker = walk_tree()

    def IterSegments(self):
        for seg in self.src:
            #find node
            orig_node = self.node
            
            if seg.get_seg_id() == 'ISA':
                self.node = self.control_map.getnodebypath('/ISA_LOOP/ISA')
            elif seg.get_seg_id() == 'GS':
                self.node = self.control_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
            else:
                try:
                    self.node = self.walker.walk(self.node, seg, self.errh, self.src.get_seg_count(), \
                        self.src.get_cur_line(), self.src.get_ls_id())
                except errors.EngineError:
                    raise
            if self.node is None:
                self.node = orig_node
            else:
                if seg.get_seg_id() == 'ISA':
                    self. errh.add_isa_loop(seg, self.src)
                    icvn = seg.get_value('ISA12')
                    self.errh.handle_errors(self.src.pop_errors())
                elif seg.get_seg_id() == 'IEA':
                    self.errh.handle_errors(self.src.pop_errors())
                    self.errh.close_isa_loop(self.node, seg, self.src)
                elif seg.get_seg_id() == 'GS':
                    fic = seg.get_value('GS01')
                    vriic = seg.get_value('GS08')
                    map_file_new = self.map_index_if.get_filename(icvn, vriic, fic)
                    if self.map_file != map_file_new:
                        self.map_file = map_file_new
                        if self.map_file is None:
                            raise pyx12.errors.EngineError, "Map not found.  icvn=%s, fic=%s, vriic=%s" % \
                                (icvn, fic, vriic)
                        self.cur_map = map_if.load_map_file(self.map_file, self.param, self.xslt_files)
                        self._apply_loop_count(orig_node, self.cur_map)
                        self._reset_isa_counts(self.cur_map)
                    self._reset_gs_counts(self.cur_map)
                    self.node = self.cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
                    self.errh.add_gs_loop(seg, self.src)
                    self.errh.handle_errors(self.src.pop_errors())
                elif seg.get_seg_id() == 'BHT':
                    if vriic in ('004010X094', '004010X094A1'):
                        tspc = seg.get_value('BHT02')
                        map_file_new = self.map_index_if.get_filename(icvn, vriic, fic, tspc)
                        if self.map_file != map_file_new:
                            map_file = map_file_new
                            if self.map_file is None:
                                raise pyx12.errors.EngineError, "Map not found.  icvn=%s, fic=%s, vriic=%s, tspc=%s" % \
                                    (icvn, fic, vriic, tspc)
                            self.cur_map = map_if.load_map_file(self.map_file, self.param, self.xslt_files)
                            self._apply_loop_count(self.node, self.cur_map)
                            self.node = self.cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BHT')
                    self.errh.add_seg(self.node, seg, self.src.get_seg_count(), \
                        self.src.get_cur_line(), self.src.get_ls_id())
                    self.errh.handle_errors(self.src.pop_errors())
                elif seg.get_seg_id() == 'GE':
                    self.errh.handle_errors(self.src.pop_errors())
                    self.errh.close_gs_loop(self.node, seg, self.src)
                elif seg.get_seg_id() == 'ST':
                    self.errh.add_st_loop(seg, self.src)
                    self.errh.handle_errors(self.src.pop_errors())
                elif seg.get_seg_id() == 'SE':
                    self.errh.handle_errors(self.src.pop_errors())
                    self.errh.close_st_loop(self.node, seg, self.src)
                else:
                    self.errh.add_seg(self.node, seg, self.src.get_seg_count(), \
                        self.src.get_cur_line(), self.src.get_ls_id())
                    self.errh.handle_errors(self.src.pop_errors())

            node_path = self.node.get_path().split('/')[1:]
            yield (node_path, seg)
        
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

