#! /usr/bin/env /usr/local/bin/python

import x12file
import error_handler
import sys

errh = error_handler.err_handler()
fd = sys.stdin
src = x12file.x12file(fd, errh)
for c in src:
    src.print_seg(c)
