#!/usr/bin/env python

import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../..')
import os
import os.path
import logging
import logging.handlers
#import tempfile

import pyx12.error_handler
import pyx12.x12file
import pyx12.rawx12file
import pyx12.x12n_fastparse
import pyx12.params


def read_x12(filename):
    with open(filename) as fd:
        src = pyx12.x12file.X12Reader(fd)
        for seg in src:
            pass
            #x = seg.seg_id


def read_rawx12(filename):
    with open(filename) as fd:
        src = pyx12.rawx12file.RawX12File(fd)
        for seg in src:
            #print seg
            pass


def read_fastx12(filename):
    param = pyx12.params.params('../../test/pyx12.conf.xml')
    with open(filename) as fd:
        pyx12.x12n_fastparse.x12n_fastparser(param, fd)


def main():
    """Script main program."""
    import argparse
    parser = argparse.ArgumentParser(description='Test line parser')
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--background', '-b', action='store_true')
    parser.add_argument('--test', '-t', action='store_true')
    #parser.add_argument('--version', action='version', version='{prog} {version}'.format(prog=parser.prog, version=__version__))
    parser.add_argument('--profile', action='store_true', help='Profile the code with plop')
    parser.add_argument('input_files', nargs='*')
    args = parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')

    stderr_hdlr = logging.StreamHandler()
    stderr_hdlr.setFormatter(formatter)
    logger.addHandler(stderr_hdlr)

    if args.debug or args.verbose > 0:
        logger.setLevel(logging.DEBUG)

    if len(args.input_files) > 0:
        for file1 in args.input_files:
            #read_x12(file1)
            read_rawx12(file1)
            #read_fastx12(file1)


if __name__ == '__main__':
    sys.exit(not main())
