#####################################################################
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#
#    $Id$

"""
Parse a ANSI X12N data file.  Validate against a map and codeset values.
Create XML, HTML, and 997 documents based on the data file.
"""

#import time
import os, os.path
#import stat
#import sys
import logging
#import string
from types import *
#import StringIO
#import tempfile
#import pdb
#import profile

# Intrapackage imports
import pyx12
#import error_handler
#import error_997
#import error_debug
#import error_html
import errh_xml
from errors import *
#import codes
import map_index
import map_if
import x12file
from map_walker import walk_tree
import x12xml_simple
import x12xml_idtag
import x12xml_idtagqual
#from params import params

#Global Variables
#logger = None

def x12n_document(param, src_file, fd_997, fd_html, fd_xmldoc=None):
    """
    Primary X12 validation function
    @param param: pyx12.param instance
    @param src_file: Source document
    @type src_file: string
    @param fd_997: 997 output document
    @type fd_997: file descriptor
    @param fd_html: HTML output document
    @type fd_html: file descriptor
    @param fd_xmldoc: XML output document
    @type fd_xmldoc: file descriptor
    @rtype: boolean
    """
    map_path = param.get('map_path')
    logger = logging.getLogger('pyx12')
    logger.debug('MAP PATH: %s' % (map_path))
    #errh = error_handler.err_handler()
    errh = errh_xml.errh_list()
    #errh.register()
    #param.set('checkdate', None)
    
    # Get X12 DATA file
    try:
        src = x12file.X12file(src_file) 
    except pyx12.errors.x12Error:
        logger.error('"%s" does not look like an X12 data file' % (src_file))
        return False

    #Get Map of Control Segments
    map_file = 'x12.control.00401.xml'
    control_map = map_if.map_if(os.path.join(map_path, map_file), param)
    map_index_if = map_index.map_index(os.path.join(map_path, 'maps.xml'))
    #cur_map = control_map # XXX
    node = control_map.getnodebypath('/ISA_LOOP/ISA')
    #logger.debug('Map file loaded')
    walker = walk_tree()
    icvn = fic = vriic = tspc = None
    #XXX Generate TA1 if needed.

    #if fd_html:
    #    html = error_html.error_html(errh, fd_html, src.get_term())
    #    html.header()
    #    err_iter = error_handler.err_iter(errh)
    if fd_xmldoc:
        logger.debug('xmlout: %s' % (param.get('xmlout')))
        if param.get('xmlout') == 'simple':
            xmldoc = x12xml_simple.x12xml_simple(fd_xmldoc, param.get('simple_dtd'))
        elif param.get('xmlout') == 'idtag':
            xmldoc = x12xml_idtag.x12xml_idtag(fd_xmldoc, param.get('idtag_dtd'))
        elif param.get('xmlout') == 'idtagqual':
            xmldoc = x12xml_idtagqual.x12xml_idtagqual(fd_xmldoc, param.get('idtagqual_dtd'))
        else:
            xmldoc = x12xml_simple.x12xml_simple(fd_xmldoc, param.get('simple_dtd'))

    erx = errh_xml.err_handler('errors.xml')

    valid = True
    for seg in src:
        #find node
        orig_node = node
        
        if seg.get_seg_id() == 'ISA':
            node = control_map.getnodebypath('/ISA_LOOP/ISA')
        elif seg.get_seg_id() == 'GS':
            node = control_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
        else:
            try:
                node = walker.walk(node, seg, errh, src.get_seg_count(), \
                    src.get_cur_line(), src.get_ls_id())
            except EngineError:
                logger.error('Source file line %i' % (src.get_cur_line()))
                raise
                #node = orig_node
                #continue
        #logger.debug('Node %s' % (node.__repr__()))
        if node is None:
            node = orig_node
        else:
            if seg.get_seg_id() == 'ISA':
                errh.add_isa_loop(seg, src)
                icvn = seg.get_value('ISA12')
                #cur_map.getnodebypath('/ISA_LOOP').set_cur_count(1)
                #cur_map.getnodebypath('/ISA_LOOP/ISA').set_cur_count(1)
            elif seg.get_seg_id() == 'IEA':
                errh.close_isa_loop(node, seg, src)
                # Generate 997
                #XXX Generate TA1 if needed.
            elif seg.get_seg_id() == 'GS':
                fic = seg.get_value('GS01')
                vriic = seg.get_value('GS08')
                map_file_new = map_index_if.get_filename(icvn, vriic, fic)
                if map_file != map_file_new:
                    #if vriic not in ('004010X094', '004010X094A1'):
                    #    map_file = map_index_if.get_filename(icvn, vriic, fic)
                    ct_list = []
                    orig_node.get_counts_list(ct_list)
                    map_file = map_file_new
                    if map_file is None:
                        raise EngineError, "Map not found.  icvn=%s, fic=%s, vriic=%s" % \
                            (icvn, fic, vriic)
                    #map = map_if.map_if(os.path.join('map', map_file), param)
                    cur_map = map_if.load_map_file(map_file, param)
                    logger.debug('Map file: %s' % (map_file))
                    for (path, ct) in ct_list:
                        cur_map.getnodebypath(path).set_cur_count(ct)
                    cur_map.getnodebypath('/ISA_LOOP').set_cur_count(1)
                    cur_map.getnodebypath('/ISA_LOOP/ISA').set_cur_count(1)
                    cur_map.getnodebypath('/ISA_LOOP/GS_LOOP').reset_cur_count()
                    cur_map.getnodebypath('/ISA_LOOP/GS_LOOP').set_cur_count(1)
                    cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS').set_cur_count(1)
                    node = cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
                    #node.reset_cur_count()
                    #node.incr_cur_count()
                else:
                    node = cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
                    node.reset_cur_count()
                    node.incr_cur_count()
                errh.add_gs_loop(seg, src)
            elif seg.get_seg_id() == 'BHT':
                if vriic in ('004010X094', '004010X094A1'):
                    tspc = seg.get_value('BHT02')
                    logger.debug('icvn=%s, fic=%s, vriic=%s, tspc=%s' % (icvn, fic, vriic, tspc))
                    map_file_new = map_index_if.get_filename(icvn, vriic, fic, tspc)
                    logger.debug('New map file: %s' % (map_file_new))
                    if map_file != map_file_new:
                        ct_list = []
                        node.get_counts_list(ct_list)
                        map_file = map_file_new
                        if map_file is None:
                            raise EngineError, "Map not found.  icvn=%s, fic=%s, vriic=%s, tspc=%s" % \
                                (icvn, fic, vriic, tspc)
                        cur_map = map_if.load_map_file(map_file, param)
                        logger.debug('Map file: %s' % (map_file))
                        for (path, ct) in ct_list:
                            cur_map.getnodebypath(path).set_cur_count(ct)
                        node = cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BHT')
                        #node.reset_cur_count()
                        #node.incr_cur_count()
                errh.add_seg(node, seg, src.get_seg_count(), src.get_cur_line(), src.get_ls_id())
            elif seg.get_seg_id() == 'GE':
                errh.close_gs_loop(node, seg, src)
            elif seg.get_seg_id() == 'ST':
                errh.add_st_loop(seg, src)
            elif seg.get_seg_id() == 'SE':
                errh.close_st_loop(node, seg, src)
            else:
                errh.add_seg(node, seg, src.get_seg_count(), src.get_cur_line(), src.get_ls_id())

            errh.set_cur_line(src.get_cur_line())
            valid &= node.is_valid(seg, errh)
            #errh.handle_errors(src.pop_errors())
            erx.handleErrors(src.pop_errors())
            erx.handleErrors(errh.get_errors())
            errh.reset()

        #if fd_html:
        #    if node is not None and node.is_first_seg_in_loop():
        #        html.loop(node.get_parent())
        #    err_node_list = []
            #cur_line = src.cur_line
        #    while 1:
        #        try:
        #            err_iter.next()
        #            err_node = err_iter.get_cur_node()
        #            err_node_list.append(err_node)
        #        except IterOutOfBounds:
        #            break
        #    html.gen_seg(seg, src, err_node_list)

        if fd_xmldoc:
            xmldoc.seg(node, seg)

        erx.Write(src.cur_line)

    erx.handleErrors(src.pop_errors())
    src.cleanup() #Catch any skipped loop trailers
    #errh.handle_errors(src.pop_errors())
    erx.handleErrors(src.pop_errors())
    erx.handleErrors(errh.get_errors())
    
    #if fd_html:
    #    html.footer()
    #    del html

    if fd_xmldoc:
        del xmldoc

    #visit_debug = error_debug.error_debug_visitor(sys.stdout)
    #errh.accept(visit_debug)

    #If this transaction is not a 997, generate one.
    #if not (vriic=='004010' and fic=='FA'):
        #fd_997 = open(filename_997, 'w')
        #fd_997 = sys.stdout
    #    if fd_997:
    #        visit_997 = error_997.error_997_visitor(fd_997, src.get_term())
    #        errh.accept(visit_997)
    #        del visit_997
    del node
    del src
    del control_map
    del cur_map
    try:
        if not valid or errh.get_error_count() > 0:
            return False
        else:
            return True
    except:
        print errh
        return False
