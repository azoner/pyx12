#! /usr/bin/env /usr/local/bin/python
# script to validate a X12N batch transaction set  and convert it into an XML document
#
#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
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

# THIS IS PRE-ALPHA CODE.  IT DOES NOT WORK. 

"""
Parse a ANSI X12N data file.
Validate against a map and codeset values.
Create a XML document based on the data file
"""

import time
import os, os.path
#import stat
import sys
import logging
#import string
from types import *
#import StringIO
#import tempfile
#import time
import pdb
#import xml.dom.minidom

# Intrapackage imports
import err_997
from errors import *
import codes
import map_index
import map_if
import x12file
from map_walker import walk_tree
from utils import *

#Global Variables
__author__  = "John Holland <jholland@kazoocmh.org> <john@zoner.org>"
__status__  = "beta"
__version__ = "0.3.0.0"
__date__    = "10/1/2003"

#logger = None

def x12n_document(fd):

    logger = logging.getLogger('pyx12')
    check_dte = '20030930'
    
    # Get X12 DATA file
    try:
        src = x12file.x12file(fd) 
    except x12Error:
        logger.error('This does not look like a X12 data file')
        sys.exit(2)

    #Get Map of Control Segments
    control_map = map_if.map_if('map/map.x12.control.00401.xml')
    
    logger.info('Start')
    walker = walk_tree()
    now = time.localtime()
    #Determine which map to use for this transaction
    for seg in src:
        if seg[0] == 'ISA':
            #map_node = walker.walk(control_map, seg)
            map_node = control_map.getnodebypath('/ISA')
            map_node.is_valid(seg, [])
            #map_node = control_map
            icvn = map_node.get_elemval_by_id(seg, 'ISA12')
            #ISA*00*          *00*          *ZZ*ENCOUNTER      *ZZ*00GR           *030425*1501*U*00401*000065350*0*T*:~
            isa_seg = [seg[0],seg[3],seg[4],seg[1],seg[7],seg[8],seg[5],seg[6]]
            isa_seg.append(now.strftime('%y%m%d')) # Date
            isa_seg.append(now.strftime('%H%M')) # Time
            isa_seg.extend([seg[11],seg[12]]
            isa_control_num = ('%s%s'%(now.strftime('%y%m%d'), now.strftime('%H%M')))[-1:]
            isa_seg.append(isa_control_num) # ISA Interchange Control Number
            isa_seg.extend([seg[14],seg[15]]
        elif seg[0] == 'GS':
            #map_node = walker.walk(map_node, seg)
            map_node = control_map.getnodebypath('/GS')
            map_node.is_valid(seg, [])
            fic = map_node.get_elemval_by_id(seg, 'GS01')
            vriic = map_node.get_elemval_by_id(seg, 'GS08')
            # GS*FA*ENCOUNTER*00GR*20030425*150153*653500001*X*004010
            gs_seg = [seg[0], 'FA', seg[2], seg[1], now.strftime('%Y%m%d'), now.strftime('%H%M%s')]
            gs_seg.extend([seg[6], seg[7], '004010'])
            
            #Get map for this GS loop
            #logger.debug('icvn=%s fic=%s vriic=%s' % (icvn, fic, vriic))
            map_index_if = map_index.map_index('map/maps.xml')
            map_file = map_index_if.get_filename(icvn, vriic, fic)
            gs_997_count = 0
        else:
            break        

    #Determine which map to use for this transaction
    if map_file is None:
        raise EngineError, "Map not found.  icvn=%s, fic=%s, vriic=%s" % \
            (icvn, fic, vriic)
    map = map_if.map_if(os.path.join('map', map_file))
    logger.info('Map file: %s' % (map_file))
    node = map.getnodebypath('/ISA')
    #logger.info('Map file loaded')

    fd.seek(0)
    src = x12file.x12file(fd) 

    fd_997 = open('data/997.txt', 'w')
    errors_997 = err_997.if_997(src)
    # Create 997 ISA segment
    isa_seg.append(src.subele_term)
    fd_997.write(src.seg_str(isa_seg, '\n')
    fd_997.write(src.seg_str(gs_seg, '\n') # 997 GS segment
                     
    for seg in src:
        logger.debug(seg)
        #find node
        seg_err_codes = []
        ele_err_list = []
        #e997 = err_997.err_997()
        node = walker.walk(node, seg, seg_err_codes)

        if seg[0] == 'GS':
            # Write 997 file
            fic = map_node.get_elemval_by_id(seg, 'GS01')
            vriic = map_node.get_elemval_by_id(seg, 'GS08')
            #map_node = control_map.getnodebypath('/GS')
            #map_node.is_valid(seg, [])
            map_file_new = map_index_if.get_filename(icvn, vriic, fic)
            if map_file != map_file_new:
                map_file = map_file_new
                if map_file is None:
                    raise EngineError, "Map not found.  icvn=%s, fic=%s, vriic=%s" % \
                        (icvn, fic, vriic)
                map = map_if.map_if(os.path.join('map', map_file))
                logger.info('Map file: %s' % (map_file))
                node = map.getnodebypath('/GS')
        elif seg[0] == 'ST':
            pass
        node.is_valid(seg, ele_err_list) 

        #get special values
        #generate xml
        
    # Create 997 IEA segment
    isa_seg.append(src.subele_term)
    fd_997.write(src.seg_str(['GE', '%i'%errors_997.st_loop_count, gs_seg[6]], '\n')
    gs_loop_count = 1
    fd_997.write(src.seg_str(['IEA', '%i'%gs_loop_count, isa_seg[13]], '\n')

    logger.info('End')

   
def main():
    """Script main program."""
    import getopt
    #global logger
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'qv:')
#        opts, args = getopt.getopt(sys.argv[1:], 'lfd:')
    except getopt.error, msg:
    #    sys.stderr.write(msg + '\n')
        sys.stdout.write('usage: pyx12.py file\n')
        raise
        sys.exit(2)
    logger = logging.getLogger('pyx12')
    hdlr = logging.FileHandler('./run.log')
    stderr_hdlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')
    hdlr.setFormatter(formatter)
    stderr_hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.addHandler(stderr_hdlr)
    logger.setLevel(logging.INFO)

    for o, a in opts:
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)

    try:
        if args:
            fd = open(args[0], 'r')
        else:
            fd = sys.stdin
    except:
        logger.error('Could not open file')
        sys.exit(2)

    try:
        x12n_document(fd)
    except KeyboardInterrupt:
        print "\n[interrupt]"
    return True

codes = codes.ExternalCodes()
tab = Indent()

if __name__ == '__main__':
    sys.exit(not main())

