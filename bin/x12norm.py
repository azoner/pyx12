#! /usr/bin/env /usr/local/bin/python

import pyx12.x12file
import pyx12.error_handler
import sys

errh = pyx12.error_handler.err_handler()
src = pyx12.x12file.x12file('', errh)
for c in src:
    src.print_seg(c)
