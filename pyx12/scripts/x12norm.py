#!/usr/bin/env python

"""
Format a X12 document.  If the option -e is used, it adds newlines.
If no source file is given, read from stdin.
If no ouput filename is given with -o,  write to stdout.
"""

import sys
import os.path
import codecs
import tempfile
import logging

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
    import argparse
    parser = argparse.ArgumentParser(description='X12 Validation')
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--quiet', '-q', action='store_true')
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--eol', '-e', action='store_true', help="Add eol to each segment line")
    parser.add_argument('--inplace', '-i', action='store_true', help="Make changes to files in place")
    parser.add_argument('--fixcounting', '-f', action='store_true', help="Try to fix counting errors")
    #parser.add_argument('--fixwhitespace', '-w', action='store_true', help="Try to fix extra whitespace errors.")
    parser.add_argument('--output', '-o', action='store', dest="outputfile", default=None, help="Output filename.  Defaults to stdout")
    parser.add_argument('--version', action='version', version='{prog} {version}'.format(prog=parser.prog, version=__version__))
    parser.add_argument('input_files', nargs='*')
    args = parser.parse_args()

    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.addHandler(stdout_hdlr)
    logger.setLevel(logging.INFO)

    eol = '\n' if args.eol else ''
    for file_in in args.input_files:
        if not os.path.isfile(file_in):
            logger.error('Could not open file "%s"' % (file_in))

        fd_out = tempfile.TemporaryFile()
        src = pyx12.x12file.X12Reader(file_in)
        for seg_data in src:
            if args.fixcounting:
                err_codes = [(x[1]) for x in src.pop_errors()]
                if seg_data.get_seg_id() == 'IEA' and '021' in err_codes:
                    seg_data.set('IEA01', '%i' % (src.gs_count))
                elif seg_data.get_seg_id() == 'GE' and '5' in err_codes:
                    seg_data.set('GE01', '%i' % (src.st_count))
                elif seg_data.get_seg_id() == 'SE' and '4' in err_codes:
                    seg_data.set('SE01', '%i' % (src.seg_count + 1))
                elif seg_data.get_seg_id() == 'HL' and 'HL1' in err_codes:
                    seg_data.set('HL01', '%i' % (src.hl_count))
            #if args.fixwhitespace:
            #    err_codes = [(x[1]) for x in src.pop_errors()]
            #    if 'SEG1' in err_codes:
            fd_out.write(seg_data.format() + eol)
        if eol == '':
            fd_out.write('\n')

        fd_out.seek(0)
        if args.outputfile:
            fd_out = codecs.open(args.outputfile, mode='w', encoding='ascii')
        else:
            if args.inplace:
                with codecs.open(file_in, mode='w', encoding='ascii') as fd_orig:
                    fd_orig.write(fd_out.read())
            else:
                sys.stdout.write(fd_out.read())
    return True

if __name__ == '__main__':
    sys.exit(not main())
