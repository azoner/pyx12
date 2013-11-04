#! /usr/bin/env python
import sys
import logging
from itertools import groupby

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
    isa_seg = None
    gs_seg = None
    isa_id = 11
    gs_id = 21
    #for k, g in groupby(iterate_2000(fd_in), lambda x: x['st_id']):
    for k, g in groupby(iterate_2000(fd_in), lambda x: x[0]):
        #yield (k, g)
        print '-----------------------------------------------------------'
        print k
        for d in g:
            yield d
        print '-----------------------------------------------------------'
    #for d in iterate_2000(fd_in):
    #    yield d


def iterate_2000(fd_in):
    param = pyx12.params.params()
    errh = pyx12.error_handler.errh_null()
    src = pyx12.x12context.X12ContextReader(param, errh, fd_in)
    #isa_id = None
    #gs_id = None
    isa_seg = None
    gs_seg = None
    st_id = None
    for datatree in src.iter_segments('2000'):
        if datatree.id == 'ISA':
# get_first_segment(xpath)
            isa_seg = list(datatree.iterate_segments())[0]['segment']
            #isa_id = datatree.get_value('ISA13')
        elif datatree.id == 'GS':
            gs_seg = list(datatree.iterate_segments())[0]['segment']
            #gs_id = datatree.get_value('GS06')
        elif datatree.id in ('IEA', 'GE'):
            pass
        else:
            if datatree.id == 'ST':
                st_id = datatree.get_value('ST02')
            for seg_node in datatree.iterate_segments():
# do something with loop 2000
                k = {
                    'isa_seg': isa_seg,
                    'gs_seg': gs_seg,
                    'st_id': st_id,
                }
                v = seg_node['segment']
                yield (k, v)


def main():
    for s in st_generator():
        print '\t' + s[1].format()
    return True

if __name__ == '__main__':
    sys.exit(not main())
