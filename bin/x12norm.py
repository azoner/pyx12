#! /usr/bin/env /usr/local/bin/python

import pyx12.x12file
import pyx12.error_handler
import sys
import getopt


try:
    opts, args = getopt.getopt(sys.argv[1:], 'ef')
except getopt.error, msg:
    sys.exit(2)

eol = ''
fix = False
for o, a in opts:
    if o == '-e': eol = '\n'
    if o == '-f': fix = True

errh = pyx12.error_handler.errh_null()
for filename in args:
    src = pyx12.x12file.x12file(filename, errh)
    for c in src:
        if fix:
            if c[0] == 'IEA' and errh.err_cde == '021':
                c[1] = src.gs_count
            elif c[0] == 'GE' and errh.err_cde == '5':
                c[1] = src.st_count
            elif c[0] == 'SE' and errh.err_cde == '4':
                c[1] = src.seg_count
        sys.stdout.write(c.format() + eol)
