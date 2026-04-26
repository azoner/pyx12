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

import argparse
import glob
import logging
import os
import os.path
import sys

import pyx12
import pyx12.x12n_document
import pyx12.params

__author__ = pyx12.__author__
__status__ = pyx12.__status__
__version__ = pyx12.__version__
__date__ = pyx12.__date__

def check_map_path_arg(map_path):
    if not os.path.isdir(map_path):
        raise argparse.ArgumentTypeError(f"MAP_PATH '{map_path}' is not a valid directory")
    index_file = 'maps.xml'
    if not os.path.isfile(os.path.join(map_path, index_file)):
        raise argparse.ArgumentTypeError(
            f"MAP_PATH '{map_path}' does not contain the map index file '{index_file}'"
        )
    return map_path

def main():
    """
    Set up environment for processing
    """
    parser = argparse.ArgumentParser(description='Format an X12 file as HTML')
    parser.add_argument('--config-file', '-c', action='store', dest="configfile", default=None)
    parser.add_argument('--log-file', '-l', action='store', dest="logfile", default=None)
    parser.add_argument('--map-path', '-m', action='store', dest="map_path", default=None, type=check_map_path_arg)
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--quiet', '-q', action='store_true')
    parser.add_argument('--html', '-H', action='store_true',
                        help='Write HTML to a file instead of stdout')
    parser.add_argument('--exclude-external-codes', '-x', action='append', dest="exclude_external",
                        default=[], help='External Code Names to ignore')
    parser.add_argument('--charset', '-s', choices=('b', 'e'),
                        help='Specify X12 character set: b=basic, e=extended')
    parser.add_argument('--version', action='version',
                        version=f'{parser.prog} {__version__}')
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
        except OSError:
            logger.exception(f'Could not open log file: {args.logfile}')

    for fn in args.input_files:
        for src_filename in glob.iglob(fn):
            try:
                if not os.path.isfile(src_filename):
                    logger.error(f'Could not open file "{src_filename}"')
                    continue
                if args.html:
                    base = os.path.splitext(src_filename)[0] if src_filename.endswith('.txt') else src_filename
                    target_html = base + '.html'
                    with open(target_html, 'w', encoding='utf-8') as fd_html:
                        pyx12.x12n_document.x12n_document(param=param, src_file=src_filename,
                            fd_997=None, fd_html=fd_html, fd_xmldoc=None, map_path=args.map_path)
                else:
                    pyx12.x12n_document.x12n_document(param=param, src_file=src_filename,
                        fd_997=None, fd_html=sys.stdout, fd_xmldoc=None, map_path=args.map_path)
            except OSError:
                logger.error('Could not open files')
                return False
            except KeyboardInterrupt:
                print("\n[interrupt]")
    return True

if __name__ == '__main__':
    sys.exit(not main())
