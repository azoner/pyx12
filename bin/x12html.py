#! /usr/bin/env /usr/local/bin/python
######################################################################
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Parse a ANSI X12N data file.
Validate against a map and codeset values.
Create a html document based on the data file
"""

import os, os.path
import sys
import logging
from types import *
#import pdb
#import profile

# Intrapackage imports
#sys.path.append('/usr/home/sniper/src')
import pyx12
import pyx12.x12n_document
import pyx12.params

__author__  = pyx12.__author__
__status__  = pyx12.__status__
__version__ = pyx12.__version__
__date__    = pyx12.__date__

def usage():
    pgm_nme = os.path.basename(sys.argv[0])
    sys.stdout.write('usage: %s source_file\n' % (pgm_nme))
    
def main():
    """
    Set up environment for processing
    """
    import getopt
    param = pyx12.params.params()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'qv')
    except getopt.error, msg:
        usage()
        raise
        return False
    logger = logging.getLogger('pyx12')
    #hdlr = logging.FileHandler('./run.log')
    stderr_hdlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')
    #hdlr.setFormatter(formatter)
    stderr_hdlr.setFormatter(formatter)
    #logger.addHandler(hdlr) 
    logger.addHandler(stderr_hdlr)
    logger.setLevel(logging.INFO)

    fd_src = None
    fd_html = None

    target_html = ''
    #param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
    for o, a in opts:
        #if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-c': param.set('charset', a)
        #if o == '-H': target_html = a

    try:
        fd_html = sys.stdout
    except:
        logger.error('Could not open files')
        usage()
        return False

    try:
        if args:
            src_filename = args[0]
            pyx12.x12n_document.x12n_document(param, src_filename, None, fd_html)
    except KeyboardInterrupt:
        print "\n[interrupt]"
    return True

#profile.run('x12n_document(src_filename)', 'pyx12.prof')
if __name__ == '__main__':
    sys.exit(not main())

