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
from errors import *
import codes
import map_index
import map_if
import x12file
from map_walker import walk_tree
from utils import *

#Global Variables
__version__ = "0.1.0"
#logger = None

def x12n_document(fd):

    logger = logging.getLogger('pyx12')
    check_dte = '20030930'
    # Get X12 DATA file
    src = x12file.x12file(fd) 

    #Get Map of Control Segments
    control_map = map_if.map_if('map/map.x12.control.00401.xml')
    
    logger.info('Start')
    walker = walk_tree()
    #Determine which map to use for this transaction
    for seg in src:
        if seg[0] == 'ISA':
            #map_node = walker.walk(control_map, seg)
            map_node = control_map.getnodebypath('/ISA')
            map_node.is_valid(seg)
            #map_node = control_map
            icvn = map_node.get_elemval_by_id(seg, 'ISA12')
            #isa_seg = segment(control_map.getnodebypath('/ISA'), seg)
            #isa_seg.validate()
            #icvn = isa_seg.GetElementValue('ISA12')
        elif seg[0] == 'GS':
            #map_node = walker.walk(map_node, seg)
            map_node = control_map.getnodebypath('/GS')
            map_node.is_valid(seg)
            fic = map_node.get_elemval_by_id(seg, 'GS01')
            vriic = map_node.get_elemval_by_id(seg, 'GS08')
            
            #gs_seg = segment(control_map.getnodebypath('/GS'), seg)
            #gs_seg.validate()
            #fic = gs_seg.GetElementValue('GS01')
            #vriic = gs_seg.GetElementValue('GS08')

            #Get map for this GS loop
            #logger.debug('icvn=%s fic=%s vriic=%s' % (icvn, fic, vriic))
            map_index_if = map_index.map_index('map/maps.xml')
            map_file = map_index_if.get_filename(icvn, vriic, fic)
        else:
            break        

    #Determine which map to use for this transaction
    if map_file is None:
        raise x12Error, "Map not found.  icvn=%s, fic=%s, vriic=%s" % \
            (icvn, fic, vriic)
    map = map_if.map_if(os.path.join('map', map_file))
    logger.info('Map file: %s' % (map_file))
    node = map.getnodebypath('/ISA')
    #logger.info('Map file loaded')

    fd.seek(0)
    src = x12file.x12file(fd) 
    for seg in src:
        logger.debug(seg)
        #find node
        node = walker.walk(node, seg)

        #validate intra-element dependancies

        if (len(seg) - 1) > node.get_child_count(): 
            #pdb.set_trace()
            raise x12Error, 'Too many elements in segment %s. Counted %i, should be %i' \
                % (seg[0], len(seg)-1, node.get_child_count())
        for i in xrange(node.get_child_count()):
            child_node = node.get_child_node_by_idx(i)
            # Validate Elements
            if i < len(seg)-1:
                #logger.debug('i=%i, elem=%s, id=%s' % (i, seg[i+1], child_node.id))
                #if type(seg[i+1]) is ListType: # composite
                if child_node.is_composite():
                    # Validate composite
                    comp = seg[i+1]
                    if len(comp) > child_node.get_child_count():
                        raise x12Error, 'Too many elements in segment %s' % (seg[0])
                    child_node.is_valid(seg[i+1], check_dte)
                elif child_node.is_element():
                    child_node.is_valid(seg[i+1], check_dte)
            else: #missing required elements
                #logger.debug('id=%s, name=%s' % (child_node.id, child_node.base_name))
                child_node.is_valid(None)
            
        #get special values
        #generate xml
    logger.info('End')

   
def main():
    """Script main program."""
    import getopt
    #global logger
    try:
        opts, args = getopt.getopt(sys.argv[1:], ':')
#        opts, args = getopt.getopt(sys.argv[1:], 'lfd:')
    except getopt.error, msg:
        sys.stderr.write(msg + '\n')
        sys.stdout.write('usage: pyx12.py file\n')
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

#    try:
    if 1:
        if args:
            for file in args:
                fd = open(file, 'r')
                a = x12n_document(fd)
        else:
            a = x12n_document(sys.stdin)

#    except KeyboardInterrupt:
#        print "\n[interrupt]"
#        success = 0
#    return success

codes = codes.ExternalCodes()
tab = Indent()

if __name__ == '__main__':
    sys.exit(not main())

