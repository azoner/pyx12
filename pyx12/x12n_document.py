# script to validate a X12N batch transaction set  and convert it into an XML document
#
#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#                John Holland <jholland@kazoocmh.org> <john@zoner.org>
#
#    All rights reserved.
#
#        Redistribution and use in source and binary forms, with or without modification, 
#        are permitted provided that the following conditions are met:
#
#        1. Redistributions of source code must retain the above copyright notice, this list 
#           of conditions and the following disclaimer. 
#        
#        2. Redistributions in binary form must reproduce the above copyright notice, this 
#           list of conditions and the following disclaimer in the documentation and/or other 
#           materials provided with the distribution. 
#        
#        3. The name of the author may not be used to endorse or promote products derived 
#           from this software without specific prior written permission. 
#
#        THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED 
#        WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
#        MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
#        EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#        EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
#        OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
#        INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
#        CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
#        ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
#        THE POSSIBILITY OF SUCH DAMAGE.

"""
Parse a ANSI X12N data file.
Validate against a map and codeset values.
Create a XML document based on the data file
"""

#import time
import os, os.path
#import stat
import sys
import logging
#import string
from types import *
#import StringIO
#import tempfile
import pdb
#import profile

# Intrapackage imports
import pyx12
import error_handler
import error_997
import error_debug
import error_html
from errors import *
#import codes
import map_index
import map_if
import x12file
from map_walker import walk_tree
from utils import *
import x12xml_simple
import x12xml_idtag
from params import params

#Global Variables
#logger = None

def x12n_document(param, fd_src, fd_997, fd_html, fd_xmldoc=None):
    map_path = param.get_param('map_path')
    logger = logging.getLogger('pyx12')
    errh = error_handler.err_handler()
    #errh.register()
    #param.set_param('checkdate', None)
    
    # Get X12 DATA file
    try:
        src = x12file.x12file(fd_src, errh) 
    except x12Error:
        logger.error('This does not look like a X12 data file')
        sys.exit(2)

    #Get Map of Control Segments
    control_map = map_if.map_if(os.path.join(map_path, 'x12.control.00401.xml'), param)
    
    walker = walk_tree()
    #Determine which map to use for this transaction
    for seg in src:
        if seg[0] == 'ISA':
            #map_node = walker.walk(control_map, seg)
            map_node = control_map.getnodebypath('/ISA')
            errh.add_isa_loop(seg, src)
            map_node.is_valid(seg, errh)
            #map_node = control_map
            icvn = map_node.get_elemval_by_id(seg, 'ISA12')
        elif seg[0] == 'GS':
            #map_node = walker.walk(map_node, seg)
            map_node = control_map.getnodebypath('/GS')
            errh.add_gs_loop(seg, src)
            map_node.is_valid(seg, errh)
            fic = map_node.get_elemval_by_id(seg, 'GS01')
            vriic = map_node.get_elemval_by_id(seg, 'GS08')
            
            #Get map for this GS loop
            #logger.debug('icvn=%s fic=%s vriic=%s' % (icvn, fic, vriic))
            map_index_if = map_index.map_index(os.path.join(map_path, 'maps.xml'))
            map_file = map_index_if.get_filename(icvn, vriic, fic)
        else:
            break        

    #XXX Generate TA1 if needed.
    del errh
    errh = error_handler.err_handler()

    #Determine which map to use for this transaction
    if map_file is None:
        raise EngineError, "Map not found.  icvn=%s, fic=%s, vriic=%s" % \
            (icvn, fic, vriic)
    #map = map_if.map_if(os.path.join('map', map_file), param)
    map = map_if.load_map_file(map_file, param)
    logger.debug('Map file: %s' % (map_file))
    node = map.getnodebypath('/ISA')
    logger.debug('Map file loaded')

    fd_src.seek(0)
    src = x12file.x12file(fd_src, errh) 
    if fd_html:
        html = error_html.error_html(errh, fd_html, src.get_term())
        html.header()
        err_iter = error_handler.err_iter(errh)
    if fd_xmldoc:
        #xmldoc = x12xml_simple.x12xml_simple(fd_xmldoc)
        xmldoc = x12xml_idtag.x12xml_idtag(fd_xmldoc)

    for seg in src:
        #logger.debug(seg)
        #find node
        orig_node = node
        try:
            (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = src.get_id()
            node = walker.walk(node, seg, errh, seg_count, cur_line, ls_id)
        except EngineError:
            logger.error('Source file line %i' % (src.cur_line))
            raise
            node = orig_node
            continue

        if node is None:
            #raise EngineError, 'Node is None (%s)' % (seg[0])
            node = orig_node
        else:

            if seg[0] == 'ISA':
                errh.add_isa_loop(seg, src)
            elif seg[0] == 'IEA':
                errh.close_isa_loop(node, seg, src)
                #errh.update_node({'id': 'IEA', 'seg': seg, 'src_id': src.get_id()})
                # Generate 997
                #XXX Generate TA1 if needed.
            elif seg[0] == 'GS':
                fic = map_node.get_elemval_by_id(seg, 'GS01')
                vriic = map_node.get_elemval_by_id(seg, 'GS08')
                #map_node = control_map.getnodebypath('/GS')
                #map_node.is_valid(seg, errh)
                map_file_new = map_index_if.get_filename(icvn, vriic, fic)
                if map_file != map_file_new:
                    map_file = map_file_new
                    if map_file is None:
                        raise EngineError, "Map not found.  icvn=%s, fic=%s, vriic=%s" % \
                            (icvn, fic, vriic)
                    #map = map_if.map_if(os.path.join('map', map_file), param)
                    map = map_if.load_map_file(map_file, param)
                    logger.debug('Map file: %s' % (map_file))
                    node = map.getnodebypath('/GS')
                    node.cur_count = 1
                errh.add_gs_loop(seg, src)
            elif seg[0] == 'GE':
                errh.close_gs_loop(node, seg, src)
            elif seg[0] == 'ST':
                    errh.add_st_loop(seg, src)
            elif seg[0] == 'SE':
                errh.close_st_loop(node, seg, src)
            else:
                (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = src.get_id()
                errh.add_seg(node, seg, seg_count, cur_line, ls_id)

            node.is_valid(seg, errh)

        if fd_html:
            if node is not None and node.is_first_seg_in_loop():
                html.gen_info('Loop %s: %s' % (node.get_parent().id, node.get_parent().name))
            err_node_list = []
            #cur_line = src.cur_line
            while 1:
                try:
                    err_iter.next()
                    err_node = err_iter.get_cur_node()
                    err_node_list.append(err_node)
                except IterOutOfBounds:
                    break
            html.gen_seg(seg, src, err_node_list)

        if fd_xmldoc:
            xmldoc.seg(node, seg)

    src.cleanup()

    if fd_html:
        html.footer()

    if fd_xmldoc:
        del xmldoc

    #If this transaction is not a 997, generate one.
    if not (vriic=='004010' and fic=='FA'):
        #fd_997 = open(filename_997, 'w')
        #fd_997 = sys.stdout
        if fd_997:
            visit_997 = error_997.error_997_visitor(fd_997, src.get_term())
            errh.accept(visit_997)
    try:
        if errh.get_error_count() > 0:
            return False
        else:
            return True
    except:
        print errh
        return False
