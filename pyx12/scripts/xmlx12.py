#!/usr/bin/env python

######################################################################
# Copyright 
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Create an X12 document from a XML data file
"""

import os
import os.path
import sys
import logging
import codecs

# Intrapackage imports
libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if os.path.isdir(libpath):
    sys.path.insert(0, libpath)
import pyx12.segment
import pyx12.xmlx12_simple

#Global Variables
__author__ = pyx12.__author__
__status__ = pyx12.__status__
__version__ = pyx12.__version__
__date__ = pyx12.__date__


def main():
    """Script main program."""
    import argparse
    parser = argparse.ArgumentParser(description='XML to X12 conversion')
    parser.add_argument('--log-file', '-l', action='store', dest="logfile", default=None)
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--quiet', '-q', action='store_true')
    parser.add_argument('--outputfile', '-o', action='store', help="X12 target filename")
    parser.add_argument('--version', action='version', version='{prog} {version}'.format(prog=parser.prog, version=__version__))
    parser.add_argument('input_file')
    args = parser.parse_args()

    logger = logging.getLogger('pyx12')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.addHandler(stdout_hdlr)
    logger.setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)
    if args.verbose > 0:
        logger.setLevel(logging.DEBUG)
    if args.quiet:
        logger.setLevel(logging.ERROR)
    if args.logfile:
        try:
            hdlr = logging.FileHandler(args.logfile)
            hdlr.setFormatter(formatter)
            logger.addHandler(hdlr)
        except IOError:
            logger.exception('Could not open log file: %s' % (args.logfile))

    if args.input_file:
        try:
            fd_source = open(args.input_file)
        except:
            logger.error('Could not open file %s' % (args.input_file))
            return False
    else:
        fd_source = sys.stdin

    if args.outputfile:
        try:
            fd_x12 = codecs.open(args.outputfile, mode='w', encoding='ascii')
        except:
            logger.error('Could not open file %s' % (args.outputfile))
            return False
    else:
        fd_x12 = sys.stdout

    try:
        result = pyx12.xmlx12_simple.convert(fd_source, fd_x12)
        if not result:
            logger.error('Input file had errors.')
            return False
    except KeyboardInterrupt:
        print "\n[interrupt]"

    return True

if __name__ == '__main__':
    sys.exit(not main())
