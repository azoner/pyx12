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
Create a XML document based on the data file.
"""

import os, os.path
import sys
import logging
#import string
from types import *
#import StringIO
#import tempfile
#import pdb
#import profile

# Intrapackage imports
#import pyx12.x12xml_simple
#import pyx12.x12xml_idtag
import pyx12
import pyx12.x12n_document
import pyx12.params

#Global Variables
__author__  = pyx12.__author__
__status__  = pyx12.__status__
__version__ = pyx12.__version__
__date__    = pyx12.__date__

def usage():
    pgm_nme = os.path.basename(sys.argv[0])
    sys.stdout.write('%s %s (%s)\n' % (pgm_nme, __version__, __date__))
    sys.stdout.write('usage: %s [options] source_file\n' % (pgm_nme))
    sys.stdout.write('\noptions:\n')
    sys.stdout.write('  -c <b|e>   Specify X12 character set: b=basic, e=extended\n')
    sys.stdout.write('  -f         Force map load.  Do not use the map pickle file\n')
    sys.stdout.write('  -H         Create HTML output file\n')
    sys.stdout.write('  -l <file>  Output log\n')
    sys.stdout.write('  -m <path>  Path to map files\n')
    sys.stdout.write('  -o <file>  Output file\n')
    sys.stdout.write('  -p <path>  Path to to pickle files\n')
    sys.stdout.write('  -q         Quiet output\n')
    sys.stdout.write('  -v         Verbose output\n')
    sys.stdout.write('  -x <tag>   Exclude external code\n')

def main():
    """Script main program."""
    import getopt
    param = pyx12.params.params()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:fl:m:o:p:qvx:Hh')
    except getopt.error, msg:
        usage()
        raise
        return False
    logger = logging.getLogger('pyx12')
    hdlr = logging.FileHandler('./run.log')
    stderr_hdlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')
    hdlr.setFormatter(formatter)
    stderr_hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.addHandler(stderr_hdlr)
    logger.setLevel(logging.INFO)
    target_xml = None
    #param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
    for o, a in opts:
        if o == '-h':
            usage()
            return True
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-c': param.set('charset', a)
        if o == '-x': param.set('exclude_external_codes', a)
        if o == '-f': param.set('force_map_load', True)
        if o == '-m': param.set('map_path', a)
        if o == '-o': target_xml = a
        if o == '-p': param.set('pickle_path', a)
        if o == '-H': flag_html = True
        if o == '-l':
            try:
                hdlr = logging.FileHandler(a)
                hdlr.setFormatter(formatter)
                logger.addHandler(hdlr)
            except IOError:
                logger.error('Could not open log file: %s' % (a))
                return False

    if len(args) > 0:
        src_filename = args[0]
        logger.debug('src=%s    xml=%s' % (src_filename, target_xml))
    else:
        src_filename = '-'
    if target_xml:
        try:
            fd_xml = open(target_xml, 'w')
        except:
            logger.error('Could not open file %s' % (target_xml))
            return False
        #target_xml = os.path.splitext(src_filename)[0] + '.xml'
    else:
        fd_xml = sys.stdout

    try:
        result = pyx12.x12n_document.x12n_document(param, src_filename, None, None, fd_xml)
        fd_xml.close()
        if not result:
            logger.error('File %s had errors.  XML file was not created.' \
                % (src_filename))
            os.remove(target_xml)
            return False
    except KeyboardInterrupt:
        print "\n[interrupt]"
        
    return True

#profile.run('x12n_document(src_filename)', 'pyx12.prof')
if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    sys.exit(not main())
