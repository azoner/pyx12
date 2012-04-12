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

"""
Create an X12 document from a XML data file
"""

import os, os.path
import sys
import logging
import codecs

# Intrapackage imports
libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if os.path.isdir(libpath):
    sys.path.insert(0, libpath)
import pyx12.segment
import pyx12.xmlx12_simple

#Global Variables
__author__  = pyx12.__author__
__status__  = pyx12.__status__
__version__ = pyx12.__version__
__date__    = pyx12.__date__

NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3,
    'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8,
    'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12, 'CData2': 14}

def usage():
    pgm_nme = os.path.basename(sys.argv[0])
    sys.stdout.write('%s %s (%s)\n' % (pgm_nme, __version__, __date__))
    sys.stdout.write('usage: %s [options] source_file\n' % (pgm_nme))
    sys.stdout.write('\noptions:\n')
    sys.stdout.write('  -l <file>  Output log\n')
    sys.stdout.write('  -o <file>  Output file\n')
    sys.stdout.write('  -q         Quiet output\n')
    sys.stdout.write('  -v         Verbose output\n')

def main():
    """Script main program."""
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l:o:qvh')
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
    target_x12 = None
    for o, a in opts:
        if o == '-h':
            usage()
            return True
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-o': target_x12 = a
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
        logger.debug('src=%s    xml=%s' % (src_filename, target_x12))
    else:
        src_filename = '-'
    if target_x12:
        try:
            fd_x12 = codecs.open(target_x12, mode='w', encoding='ascii')
        except:
            logger.error('Could not open file %s' % (target_x12))
            return False
    else:
        fd_x12 = sys.stdout

    try:
        result = pyx12.xmlx12_simple.convert(src_filename, fd_x12)
        fd_x12.close()
        if not result:
            logger.error('File %s had errors.' % (src_filename))
            return False
    except KeyboardInterrupt:
        print "\n[interrupt]"
        
    return True

#profile.run('x12n_document(src_filename)', 'pyx12.prof')
if __name__ == '__main__':
    sys.exit(not main())
