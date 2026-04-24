#!/usr/bin/env python

"""
Format a X12 document.  If the option -e is used, it adds newlines.
If no source file is given, read from stdin.
If no output filename is given with -o, write to stdout.
"""

import argparse
import glob
import io
import logging
import os
import os.path
import sys

# Intrapackage imports
libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if os.path.isdir(libpath):
    sys.path.insert(0, libpath)
import pyx12
import pyx12.x12file

__author__ = pyx12.__author__
__status__ = pyx12.__status__
__version__ = pyx12.__version__
__date__ = pyx12.__date__

def main():
    parser = argparse.ArgumentParser(description='Format an X12 document')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--quiet', '-q', action='store_true')
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--eol', '-e', action='store_true', help='Add eol to each segment line')
    parser.add_argument('--inplace', '-i', action='store_true', help='Make changes to files in place')
    parser.add_argument('--fixcounting', '-f', action='store_true', help='Try to fix counting errors')
    parser.add_argument('--output', '-o', action='store', dest='outputfile', default=None,
                        help='Output filename. Defaults to stdout')
    parser.add_argument('--version', action='version', version=f'{parser.prog} {__version__}')
    parser.add_argument('input_files', nargs='*')
    args = parser.parse_args()

    logger = logging.getLogger()
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

    eol = '\n' if args.eol else ''
    for fn in args.input_files:
        for file_in in glob.iglob(fn):
            if not os.path.isfile(file_in):
                logger.error(f'Could not open file "{file_in}"')
                continue

            buf = io.StringIO()
            src = pyx12.x12file.X12Reader(file_in)
            for seg_data in src:
                if args.fixcounting:
                    err_codes = [x[1] for x in src.pop_errors()]
                    if seg_data.get_seg_id() == 'IEA' and '021' in err_codes:
                        seg_data.set('IEA01', str(src.gs_count))
                    elif seg_data.get_seg_id() == 'GE' and '5' in err_codes:
                        seg_data.set('GE01', str(src.st_count))
                    elif seg_data.get_seg_id() == 'SE' and '4' in err_codes:
                        seg_data.set('SE01', str(src.seg_count + 1))
                    elif seg_data.get_seg_id() == 'HL' and 'HL1' in err_codes:
                        seg_data.set('HL01', str(src.hl_count))
                buf.write(seg_data.format() + eol)
            if not eol:
                buf.write('\n')

            content = buf.getvalue()
            if args.outputfile:
                with open(args.outputfile, 'w', encoding='ascii') as fd_out:
                    fd_out.write(content)
            elif args.inplace:
                with open(file_in, 'w', encoding='ascii') as fd_orig:
                    fd_orig.write(content)
            else:
                sys.stdout.write(content)
    return True

if __name__ == '__main__':
    sys.exit(not main())
