#! /usr/bin/env /usr/local/bin/python

import pyx12.x12file
import pyx12.error_handler
import sys
import getopt


try:
    opts, args = getopt.getopt(sys.argv[1:], 'e')
except getopt.error, msg:
    sys.exit(2)

eol = ''
for o, a in opts:
    if o == '-e': eol = '\n'

errh = pyx12.error_handler.err_handler()
for filename in args:
    src = pyx12.x12file.x12file(filename, errh)
    for c in src:
        sys.stdout.write(src.format_seg(c, eol))
