#! /usr/bin/env python

######################################################################
# Copyright (c) 2001-2008 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Parse a ANSI X12N data file.
Validate against a map and codeset values.
Create a html document based on the data file
Write to the standard output stream
"""

import os, os.path
import sys
import logging
from types import *

# Intrapackage imports
libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if os.path.isdir(libpath):
    sys.path.insert(0, libpath)
import pyx12
import pyx12.x12n_document
import pyx12.params

__author__  = pyx12.__author__
__status__  = pyx12.__status__
__version__ = pyx12.__version__
__date__    = pyx12.__date__

def usage():
    pgm_nme = os.path.basename(sys.argv[0])
    sys.stdout.write('%s %s (%s)\n' % (pgm_nme, __version__, __date__))
    sys.stdout.write('usage: %s [options] source_files\n' % (pgm_nme))
    sys.stdout.write('\noptions:\n')
    sys.stdout.write('  -c <file>  XML configuration file\n')
    sys.stdout.write('  -d         Debug Mode.  Implies verbose output\n')
    sys.stdout.write('  -f         Force map load.  Do not use the map pickle file\n')
    sys.stdout.write('  -l <file>  Output log\n')
    sys.stdout.write('  -m <path>  Path to map files\n')
    sys.stdout.write('  -p <path>  Path to to pickle files\n')
    sys.stdout.write('  -P         Profile script\n')
    sys.stdout.write('  -q         Quiet output\n')
    sys.stdout.write('  -s <b|e>   Specify X12 character set: b=basic, e=extended\n')
    sys.stderr.write('  -t <file>  XSL Transform, applied to the map.  May be used multiple times.\n')
    sys.stdout.write('  -v         Verbose output\n')
    sys.stdout.write('  -x <tag>   Exclude external code\n')
    
def main():
    """
    Set up environment for processing
    """
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:dfl:m:p:qs:t:vx:P')
    except getopt.error, msg:
        usage()
        return False
    logger = logging.getLogger('pyx12')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    stderr_hdlr = logging.StreamHandler()
    stderr_hdlr.setFormatter(formatter)
    logger.addHandler(stderr_hdlr)
    logger.setLevel(logging.INFO)

    fd_src = None
    fd_html = None

    profile = False
    debug = False
    configfile = None
    xslt_files = []
    for o, a in opts:
        if o == '-c':
            configfile = a
    param = pyx12.params.params(configfile)

    for xslt_file in param.get('xslt_files'):
        if os.path.isfile(xslt_file):
            xslt_files.append(xslt_file)
        else:
            logger.debug("XSL Transform '%s' not found" % (xslt_file))

    for o, a in opts:
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-d': 
            param.set('debug', True)
            debug = True
            logger.setLevel(logging.DEBUG)
        if o == '-x': param.set('exclude_external_codes', a)
        if o == '-f': param.set('force_map_load', True)
        if o == '-m': param.set('map_path', a)
        if o == '-p': param.set('pickle_path', a)
        if o == '-P': profile = True
        if o == '-s': param.set('charset', a)
        if o == '-t':
            if os.path.isfile(a):
                xslt_files.append(a)
            else:
                logger.debug("XSL Transform '%s' not found" % (a))
        if o == '-l':
            try:
                hdlr = logging.FileHandler(a)
                hdlr.setFormatter(formatter)
                logger.addHandler(hdlr) 
            except IOError:
                logger.error('Could not open log file: %s' % (a))

    for src_filename in args:
        try:
            #fd_src = open(src_filename, 'U')
            fd_html = sys.stdout
            if profile:
                import profile
                profile.run('pyx12.x12n_document.x12n_document(param, src_filename, None, fd_html, None, xslt_files)', 
                    'pyx12.prof')
            else:
                pyx12.x12n_document.x12n_document(param=param, src_file=src_filename,
                    fd_997=None, fd_html=fd_html, fd_xmldoc=None, xslt_files=xslt_files)

        except IOError:
            logger.error('Could not open files')
            usage()
            return False
        except KeyboardInterrupt:
            print "\n[interrupt]"

    return True

if __name__ == '__main__':
    sys.exit(not main())

