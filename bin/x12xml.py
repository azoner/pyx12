#! /usr/bin/env /usr/local/bin/python
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
#import error_handler
#import error_997
#import error_debug
#import error_html
#from errors import *
#import codes
#import map_index
#import map_if
#import x12file
#from map_walker import walk_tree
#from utils import *
#import pyx12.x12xml_simple
#import pyx12.x12xml_idtag
import pyx12.x12n_document
import pyx12.params

#Global Variables
__author__  = "John Holland <jholland@kazoocmh.org> <john@zoner.org>"
__status__  = "beta"
__version__ = "0.3.0.0"
__date__    = "10/1/2003"

def usage():
    sys.stdout.write('usage: x12xml source_files\n')

def main():
    """Script main program."""
    import getopt
    param = pyx12.params.params()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'qvc:')
    except getopt.error, msg:
        usage()
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

    param.set_param('map_path', os.path.expanduser('~/src/pyx12/map/'))
    for o, a in opts:
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-c': param.set_param('charset', a)

    for src_filename in args:
        target_xml = os.path.splitext(src_filename)[0] + '.xml'
        logger.debug('src=%s    xml=%s' % (src_filename, target_xml))
        try:
            fd_src = open(src_filename, 'r')
            fd_xml = open(target_xml, 'w')
        except:
            logger.error('Could not open files')
            usage()
            sys.exit(2)

        try:
            result = pyx12.x12n_document.x12n_document(param, fd_src, None, None, fd_xml)
            fd_src.close()
            fd_xml.close()
            if not result:
                logger.error('File %s had errors.  XML file was not created.' \
                    % (src_filename))
                os.remove(target_xml)
        except KeyboardInterrupt:
            print "\n[interrupt]"
        
    return True

#profile.run('x12n_document(src_filename)', 'pyx12.prof')
if __name__ == '__main__':
    sys.exit(not main())
