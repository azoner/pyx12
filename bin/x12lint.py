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

import os, os.path
import sys
import logging
from types import *
import pdb
#import profile

# Intrapackage imports
#sys.path.append('/usr/home/sniper/src')
import pyx12.x12n_document
import pyx12.params

__author__  = "John Holland <jholland@kazoocmh.org> <john@zoner.org>"
__status__  = "beta"
__version__ = "0.3.0.0"
__date__    = "10/1/2003"

def usage():
    sys.stdout.write('usage: x12lint source_files\n')
    
def main():
    """
    Set up environment for processing
    """
    import getopt
    param = pyx12.params.params()
    try:
        opts, args = getopt.getopt(sys.argv[1:], '9c:qvHl:')
    except getopt.error, msg:
        usage()
        raise
        sys.exit(2)
    logger = logging.getLogger('pyx12')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')

    hdlr = logging.FileHandler('./run.log')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    
    stderr_hdlr = logging.StreamHandler()
    stderr_hdlr.setFormatter(formatter)
    logger.addHandler(stderr_hdlr)

    fd_src = None
    fd_997 = None
    fd_html = None

    flag_html = False
    flag_997 = True
    param.set_param('map_path', os.path.expanduser('~/src/pyx12/map/'))
    for o, a in opts:
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-c': param.set_param('charset', a)
        if o == '-H': flag_html = True
        #if o == '-9': target_997 = os.path.splitext(src_filename)[0] + '.997'

    for src_filename in args:
        try:
            fd_src = open(src_filename, 'U')
            if flag_997:
                target_997 = os.path.splitext(src_filename)[0] + '.997'
                fd_997 = open(target_997, 'w')
            if flag_html:
                target_html = os.path.splitext(src_filename)[0] + '.html'
                fd_html = open(target_html, 'w')
            if pyx12.x12n_document.x12n_document(param, fd_src, fd_997, fd_html):
                sys.stderr.write('OK\n')
            else:
                sys.stderr.write('Failure\n')
        except IOError:
            logger.error('Could not open files')
            usage()
            sys.exit(2)
        except KeyboardInterrupt:
            print "\n[interrupt]"

    return True

#profile.run('x12n_document(src_filename)', 'pyx12.prof')
if __name__ == '__main__':
    sys.exit(not main())

