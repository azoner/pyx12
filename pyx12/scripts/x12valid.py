#!/usr/bin/env python

######################################################################
# Copyright (c) 
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
"""

import os
import os.path
from os.path import abspath, join, dirname, isdir, isfile
import sys
import logging
import tempfile
import codecs
import argparse

# Intrapackage imports
libpath = abspath(join(dirname(__file__), '../..'))
if isdir(libpath):
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
    parser = argparse.ArgumentParser(description='X12 Validation')
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
    parser.add_argument('--profile', action='store_true', help='Profile the code with plop')
    parser.add_argument('--version', action='version',
                        version='{prog} {version}'.format(prog=parser.prog, version=__version__))
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
    fd_997 = None
    fd_html = None
    flag_997 = True
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
            #fd_src = open(src_filename, 'U')
            if flag_997:
                fd_997 = tempfile.TemporaryFile()
            if args.html:
                if os.path.splitext(src_filename)[1] == '.txt':
                    target_html = os.path.splitext(src_filename)[0] + '.html'
                else:
                    target_html = src_filename + '.html'
                fd_html = open(target_html, 'w')

            if args.profile:
                from plop.collector import Collector
                p = Collector()
                p.start()
                if pyx12.x12n_document.x12n_document(param=param, src_file=src_filename,
                        fd_997=fd_997, fd_html=fd_html, fd_xmldoc=None, map_path=args.map_path):
                    sys.stderr.write('%s: OK\n' % (src_filename))
                else:
                    sys.stderr.write('%s: Failure\n' % (src_filename))
                #import profile
                #prof_str = 'pyx12.x12n_document.x12n_document(param, src_filename, ' \
                #        + 'fd_997, fd_html, None, None)'
                #print prof_str
                #print param
                #profile.run(prof_str, 'pyx12.prof')
                p.stop()
                try:
                    pfile = os.path.splitext(os.path.basename(
                        src_filename))[0] + '.plop.out'
                    pfull = os.path.join(os.path.expanduser(
                        '~/.plop.profiles'), pfile)
                    print(pfull)
                    with open(pfull, 'w') as fdp:
                        fdp.write(repr(dict(p.stack_counts)))
                except Exception:
                    logger.exception('Failed to write profile data')
                    sys.stderr.write('%s: bad profile save\n' % (src_filename))
            else:
                if pyx12.x12n_document.x12n_document(param=param, src_file=src_filename,
                        fd_997=fd_997, fd_html=fd_html, fd_xmldoc=None, map_path=args.map_path):
                    sys.stderr.write('%s: OK\n' % (src_filename))
                else:
                    sys.stderr.write('%s: Failure\n' % (src_filename))
            if flag_997 and fd_997.tell() != 0:
                fd_997.seek(0)
                if os.path.splitext(src_filename)[1] == '.txt':
                    target_997 = os.path.splitext(src_filename)[0] + '.997'
                else:
                    target_997 = src_filename + '.997'
                codecs.open(target_997, mode='w',
                            encoding='ascii').write(fd_997.read())

            if fd_997:
                fd_997.close()
            if fd_html:
                fd_html.close()
        except IOError:
            logger.exception('Could not open files')
            return False
        except KeyboardInterrupt:
            print("\n[interrupt]")

    return True

if __name__ == '__main__':
    sys.exit(not main())
