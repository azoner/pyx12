#! /usr/bin/env python

######################################################################
# Copyright (c) Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id: x12xml.py 1288 2008-06-12 22:05:54Z johnholland $

"""
Parse a ANSI X12N data file.
Validate against a map and codeset values.
Create an XML document based on the data file.
"""

import os, os.path
import sys
import logging
from types import *

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
    sys.stderr.write('%s %s (%s)\n' % (pgm_nme, __version__, __date__))
    sys.stderr.write('usage: %s [options] source_file\n' % (pgm_nme))
    sys.stderr.write('\noptions:\n')
    sys.stderr.write('  -c <file>  XML configuration file\n')
    sys.stderr.write('  -d         Debug mode\n')
    sys.stderr.write('  -f         Force map load.  Do not use the map pickle file\n')
    sys.stderr.write('  -l <file>  Output log\n')
    sys.stderr.write('  -m <path>  Path to map files\n')
    sys.stderr.write('  -o <file>  Output file\n')
    sys.stderr.write('  -p <path>  Path to to pickle files\n')
    sys.stderr.write('  -q         Quiet output\n')
    sys.stderr.write('  -s <b|e>   Specify X12 character set: b=basic, e=extended\n')
    sys.stderr.write('  -t <file>  XSL Transform, applied to the map.  May be used multiple times.\n')
    sys.stderr.write('  -v         Verbose output\n')
    sys.stderr.write('  -x <tag>   Exclude external code\n')
    sys.stderr.write('  -X <simple|idtag|idtagqual>   XML output format\n')

def main():
    """Script main program."""
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:dfl:m:o:p:qs:vx:X:h')
    except getopt.error, msg:
        usage()
        raise
        return False
    logger = logging.getLogger('pyx12')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')
    #try:
    #    hdlr = logging.FileHandler('./run.log')
    #    hdlr.setFormatter(formatter)
    #    logger.addHandler(hdlr) 
    #except:
    #    pass
    stderr_hdlr = logging.StreamHandler()
    stderr_hdlr.setFormatter(formatter)
    logger.addHandler(stderr_hdlr)
    logger.setLevel(logging.INFO)
    target_xml = None
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

    #param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
    debug = False
    for o, a in opts:
        if o == '-h':
            usage()
            return True
        if o == '-d':
            logger.setLevel(logging.DEBUG)
            debug = True
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-x': param.set('exclude_external_codes', a)
        if o == '-X': 
            if a not in ('simple','idtag', 'idtagqual'):
                logger.error('Unknown parameter for -X')
                usage()
                return False
            else:
                param.set('xmlout', a)
        if o == '-f': param.set('force_map_load', True)
        if o == '-m': param.set('map_path', a)
        if o == '-o': target_xml = a
        if o == '-p': param.set('pickle_path', a)
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
        result = pyx12.x12n_document.x12n_document(param=param, src_file=src_filename,
            fd_997=None, fd_html=None, fd_xmldoc=fd_xml, xslt_files=xslt_files)
        fd_xml.close()
        if not result:
            logger.error('File %s had errors.' % (src_filename))
            #if target_xml:
            #    os.remove(target_xml)
            return False
    except KeyboardInterrupt:
        print "\n[interrupt]"
        
    return True

#profile.run('x12n_document(src_filename)', 'pyx12.prof')
if __name__ == '__main__':
    sys.exit(not main())
