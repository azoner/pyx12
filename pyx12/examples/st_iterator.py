#! /usr/bin/env python
import sys
import logging

import pyx12
import pyx12.x12context
import pyx12.params

__author__ = 'John Holland'
__version__ = '1.0'
__date__ = '2011-01-22'

"""
Populate tables with 999 data
"""

VERBOSE = 0

logger = logging.getLogger()
sub_idx = 0


def st_generator():
    """
    """
    testfile = 'multiple_st_loops.txt'
    #wr = edifile.WriteFile(conn)
    fd_in = open(testfile)
    isa_id = 11
    gs_id = 21
    for seg in iterate_2000(fd_in):
        seg_id = seg.get_seg_id()
        if seg_id == 'ISA':
# get ISA
            isa_seg = seg
        elif seg_id == 'GS':
            gs_seg = seg
        elif seg_id == 'ST':
            yield (isa_seg, gs_seg, seg)
        #print seg.get_seg_id()


def iterate_2000(fd_in):
    param = pyx12.params.params()
    errh = pyx12.error_handler.errh_null()
    src = pyx12.x12context.X12ContextReader(param, errh, fd_in)
    for datatree in src.iter_segments('2000'):
        for seg_node in datatree.iterate_segments():
# do something with loop 2000
            yield seg_node['segment']


def main():
    for s in st_generator():
        print s
    return True

if __name__ == '__main__':
    sys.exit(not main())
