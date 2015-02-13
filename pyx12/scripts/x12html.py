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
Parse a ANSI X12N data file.
Validate against a map and codeset values.
Create a html document based on the data file
Write to the standard output stream
"""

import os
import os.path
import sys
import logging
#from types import *

# Intrapackage imports
libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if os.path.isdir(libpath):
    sys.path.insert(0, libpath)
import pyx12
import pyx12.x12n_document
import pyx12.params

__author__ = pyx12.__author__
__status__ = pyx12.__status__
__version__ = pyx12.__version__
__date__ = pyx12.__date__


def check_map_path_arg(map_path):
    if not isdir(map_path):
        raise argparse.ArgumentError(None, "The MAP_PATH '{}' is not a valid directory".format(map_path))
    index_file = 'maps.xml'
    if not isfile(os.path.join(map_path, index_file)):
        raise argparse.ArgumentError(None,
                    "The MAP_PATH '{}' does not contain the map index file '{}'".format(map_path, index_file))
    return map_path


def main():
    """
    Set up environment for processing
    """
    import argparse
    parser = argparse.ArgumentParser(description='Format an X12 file as HTML')
    parser.add_argument('--config-file', '-c', action='store',
                        dest="configfile", default=None)
    parser.add_argument(
        '--log-file', '-l', action='store', dest="logfile", default=None)
    parser.add_argument('--map-path', '-m', action='store', dest="map_path", default=None, type=check_map_path_arg)
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--quiet', '-q', action='store_true')
    parser.add_argument('--html', '-H', action='store_true')
    parser.add_argument('--exclude-external-codes', '-x', action='append', dest="exclude_external",
                        default=[], help='External Code Names to ignore')
    parser.add_argument('--charset', '-s', choices=(
        'b', 'e'), help='Specify X12 character set: b=basic, e=extended')
    #parser.add_argument('--background', '-b', action='store_true')
    #parser.add_argument('--test', '-t', action='store_true')
    parser.add_argument('--profile', action='store_true',
                        help='Profile the code with plop')
    parser.add_argument('--version', action='version', version='{prog} {version}'.format(prog=parser.prog, version=__version__))
    parser.add_argument('input_files', nargs='*')
    args = parser.parse_args()

    logger = logging.getLogger('pyx12')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.addHandler(stdout_hdlr)
    logger.setLevel(logging.INFO)

    param = pyx12.params.params(args.configfile)
    if args.debug:
        logger.setLevel(logging.DEBUG)
        param.set('debug', True)
    if args.verbose > 0:
        logger.setLevel(logging.DEBUG)
    if args.quiet:
        logger.setLevel(logging.ERROR)
    param.set('exclude_external_codes', ','.join(args.exclude_external))
    if args.map_path:
        param.set('map_path', args.map_path)

    if args.logfile:
        try:
            hdlr = logging.FileHandler(args.logfile)
            hdlr.setFormatter(formatter)
            logger.addHandler(hdlr)
        except IOError:
            logger.exception('Could not open log file: %s' % (args.logfile))

    for src_filename in args.input_files:
        try:
            if not os.path.isfile(src_filename):
                logger.error('Could not open file "%s"' % (src_filename))
                continue
            fd_html = None
            if args.html:
                if os.path.splitext(src_filename)[1] == '.txt':
                    target_html = os.path.splitext(src_filename)[0] + '.html'
                else:
                    target_html = src_filename + '.html'
                fd_html = open(target_html, 'w')
            else:
                fd_html = sys.stdout

            pyx12.x12n_document.x12n_document(param=param, src_file=src_filename,
                fd_997=None, fd_html=fd_html, fd_xmldoc=None, map_path=args.map_path)

        except IOError:
            logger.error('Could not open files')
            return False
        except KeyboardInterrupt:
            print("\n[interrupt]")
    return True

if __name__ == '__main__':
    sys.exit(not main())
