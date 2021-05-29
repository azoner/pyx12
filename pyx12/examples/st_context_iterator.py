#! /usr/bin/env python
import sys
from itertools import groupby
import tempfile
import random

import pyx12
import pyx12.x12context
import pyx12.params


def st_generator():
    """
    """
    testfile = 'multiple_st_loops.txt'
    #wr = edifile.WriteFile(conn)
    with open(testfile, encoding='ascii') as fd_in:
        isa_seg = None
        gs_seg = None
        isa_id = 11
        gs_id = 21
        #for k, g in groupby(iterate_2000(fd_in), lambda x: x['st_id']):
        for k, g in groupby(iterate_2000(fd_in), lambda x: x[0]):
            #yield (k, g)
            print('-----------------------------------------------------------')
            print(k)
            for d in g:
                yield d
            print('-----------------------------------------------------------')
        #for d in iterate_2000(fd_in):
        #    yield d


def simple_reader():
    testfile = 'multiple_st_loops.txt'
    src = pyx12.x12file.X12Reader(testfile)
    #for d in get_headers_stream(src):
    #    print d
    for k, g in groupby(get_headers_stream(src), lambda x: x[0]):
        print('-----------------------------------------------------------')
        print(k)
        for d in g:
            #yield d
            print(d)
        print('-----------------------------------------------------------')


def x12_split_on_st(source_filename, isa_id=11, gs_id=21):
    src = pyx12.x12file.X12Reader(source_filename)
    idx = -1
    for k, g in groupby(get_headers_stream(src), lambda x: x[0]):
        idx += 1
        st_id = int(k['st_seg'].get_value('ST02'))
        fd_temp = tempfile.TemporaryFile(mode='w+', encoding='ascii')
        wr = pyx12.x12file.X12Writer(fd_temp, '~', '*', ':', '\n', '^')
        wr.Write(update_isa_id(k['isa_seg'], isa_id + idx))
        wr.Write(update_gs_id(k['gs_seg'], gs_id + idx))
        for seg in g:
            wr.Write(seg[1])
        wr.Close()
        yield (isa_id + idx, gs_id + idx, st_id, fd_temp)


def save_many(src_filename, targetformat=None):
    base_isa_id = random.randint(1000, 999999999)
    base_gs_id = random.randint(100, 999999999)
    for (isa_id, gs_id, st_id, fd_temp) in x12_split_on_st(src_filename, base_isa_id, base_gs_id):
        if targetformat is not None:
            newname = targetformat.format(isa_id=isa_id, gs_id=gs_id, st_id=st_id)
        else:
            newname = "newfile_{isa_id}.txt".format(isa_id=isa_id)
        with open(newname, 'w', encoding='ascii') as fd_out:
            fd_temp.seek(0)
            fd_out.write(fd_temp.read())
            print((newname, isa_id, gs_id, st_id))


def update_isa_id(seg_data, isa_id):
    seg_data.set('ISA13', "{0:0>9}".format(int(isa_id)))
    return seg_data


def update_gs_id(seg_data, gs_id):
    seg_data.set('GS06', "{0}".format(int(gs_id)))
    return seg_data


def get_headers_stream(segments):
    """
    passed a segment enumerable
    yields (isa_segment, gs_segment, st_segment, current_segment)
    """
    isa_seg = None
    gs_seg = None
    st_seg = None
    for seg_data in segments:
        seg_id = seg_data.get_seg_id()
        if seg_id == 'ISA':
            isa_seg = seg_data
        elif seg_id == 'GS':
            gs_seg = seg_data
        elif seg_id in ('IEA', 'GE'):
            pass
        else:
            if seg_id == 'ST':
                st_seg = seg_data
                #st_id = st_seg.get_value('ST02')
            k = {
                'isa_seg': isa_seg,
                'gs_seg': gs_seg,
                'st_seg': st_seg,
            }
            v = seg_data
            yield (k, v)


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
            for dt in datatree.iterate_segments():
                isa_seg = dt['segment']
                break
        elif datatree.id == 'GS':
            for dt in datatree.iterate_segments():
                gs_seg = dt['segment']
                break
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


def _get_unique_isa_id():
    """
    Generate a random, 4 to 9 character ISA ID
    """
    return "{0:0>9}".format(random.randint(1000, 999999999))


def _get_unique_gs_id():
    """
    Generate a random, 3 to 9 character GS ID
    """
    return "{0}".format(random.randint(100, 999999999))


def _get_unique_st_id():
    """
    Generate a random, 4 to 9 character ST ID
    """
    #return '%04i' % (random.randint(10, 999999999))
    return "{0:0>4}".format(random.randint(100, 999999999))


def main():
    #for s in st_generator():
    #    print '\t' + s[1].format()
    #simple_reader()
    testfile = 'multiple_st_loops.txt'
    testfile = '/home/mdch/download/5014.131020.2350.28i04i5m'
    targetformat = None
    save_many(testfile, targetformat)
    return True

if __name__ == '__main__':
    sys.exit(not main())
