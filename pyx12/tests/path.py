#! /usr/bin/env /usr/local/bin/python
import unittest
import sys, os.path

import pyx12.path
from pyx12.errors import *

"""
Absolute paths:
    parse path to loop
    parse path to segment
    parse path to element
    parse path to sub-element

Relative path:
    parse path to loop
    parse path to segment
    parse path to element
    parse path to sub-element

Get list of loops

Get seg ID

Get seg pos

get sub-ele pos

Convert path obj to path string

Get string repr of seg id, pos, ... : SEG03-1

2400/REF[6R]02
2400/AMT[AAE]02
AMT[AAE]02
2430/AMT[AAE]02
DTP[096]
DTP[434]
"""

class AbsPath(unittest.TestCase):

    #def setUp(self):

    def testLoopOK1(self):
        path_str = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400'
        path = pyx12.path.path(path_str)
        self.assertEqual(path_str, path.format())
        self.assertEqual(path.seg_id, None)
        self.assertEqual(path.loop_list[2], 'ST_LOOP')

    def testLoopSegOK1(self):
        path_str = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/SV2'
        path = pyx12.path.path(path_str)
        self.assertEqual(path_str, path.format())
        self.assertEqual(path.seg_id, 'SV2')

        
class Format(unittest.TestCase):

    def test_Format1(self):
        path_str = '/2000A/2000B/2300/2400/SV2'
        path = pyx12.path.path(path_str)
        self.assertEqual(path_str, path.format())
    
    def test_Format2(self):
        path_str = '/2000A/2000B/2300/2400/SV201'
        path = pyx12.path.path(path_str)
        self.assertEqual(path_str, path.format())
    
    def test_Format3(self):
        path_str = '/2000A/2000B/2300/2400/SV2[421]01'
        path = pyx12.path.path(path_str)
        self.assertEqual(path_str, path.format())


class RefDes(unittest.TestCase):
    def test_refdes(self):
        tests = [
            ('TST', 'TST', None, None, None),
            ('TST02', 'TST', None, 2, None),
            ('TST03-2', 'TST', None, 3, 2),
            ('TST[AA]02', 'TST', 'AA', 2, None),
            ('TST[1B5]03-1', 'TST', '1B5', 3, 1),
            ('03', None, None, 3, None),
            ('03-2', None, None, 3, 2),
            ('N102', 'N1', None, 2, None),
            ('N102-5', 'N1', None, 2, 5),
            ('N1[AZR]02', 'N1', 'AZR', 2, None),
            ('N1[372]02-5', 'N1', '372', 2, 5)
        ]
        for (spath, seg_id, qual, eleidx, subeleidx) in tests:
            rd = pyx12.path.path(spath)
            self.assertEqual(rd.seg_id, seg_id, '%s: %s != %s' % (spath, rd.seg_id, seg_id))
            self.assertEqual(rd.id_val, qual, '%s: %s != %s' % (spath, rd.id_val, qual))
            self.assertEqual(rd.ele_idx, eleidx, '%s: %s != %s' % (spath, rd.ele_idx, eleidx))
            self.assertEqual(rd.subele_idx, subeleidx, '%s: %s != %s' % (spath, rd.subele_idx, subeleidx))
            self.assertEqual(rd.format(), spath, '%s: %s != %s' % (spath, rd.format(), spath))
            self.assertEqual(rd.loop_list, [], '%s: Loop list is not empty' % (spath))


class RelativePath(unittest.TestCase):
    def test_rel_paths(self):
        tests = [
            ('AAA/TST', 'TST', None, None, None, ['AAA']),
            ('B1000/TST02', 'TST', None, 2, None, ['B1000']),
            ('1000B/TST03-2', 'TST', None, 3, 2, ['1000B']),
            ('1000A/1000B/TST[AA]02', 'TST', 'AA', 2, None, ['1000A', '1000B']),
            ('AA/BB/CC/TST[1B5]03-1', 'TST', '1B5', 3, 1, ['AA', 'BB', 'CC']),
            ('DDD/E1000/N102', 'N1', None, 2, None, ['DDD', 'E1000']),
            ('E1000/D322/N102-5', 'N1', None, 2, 5, ['E1000', 'D322']),
            ('BB/CC/N1[AZR]02', 'N1', 'AZR', 2, None, ['BB', 'CC']),
            ('BB/CC/N1[372]02-5', 'N1', '372', 2, 5, ['BB', 'CC'])
        ]
        for (spath, seg_id, qual, eleidx, subeleidx, plist) in tests:
            rd = pyx12.path.path(spath)
            self.assertEqual(rd.relative, True, '%s: %s != %s' % (spath, rd.relative, True))
            self.assertEqual(rd.seg_id, seg_id, '%s: %s != %s' % (spath, rd.seg_id, seg_id))
            self.assertEqual(rd.id_val, qual, '%s: %s != %s' % (spath, rd.id_val, qual))
            self.assertEqual(rd.ele_idx, eleidx, '%s: %s != %s' % (spath, rd.ele_idx, eleidx))
            self.assertEqual(rd.subele_idx, subeleidx, '%s: %s != %s' % (spath, rd.subele_idx, subeleidx))
            self.assertEqual(rd.format(), spath, '%s: %s != %s' % (spath, rd.format(), spath))
            self.assertEqual(rd.loop_list, plist, '%s: %s != %s' % (spath, rd.loop_list, plist))

    def test_bad_rel_paths(self):
        bad_paths = [
            'AA/03',
            'BB/CC/03-2'
        ]
        for spath in bad_paths:
            self.failUnlessRaises(pyx12.errors.X12PathError, pyx12.path.path, spath)

    def test_plain_loops(self):
        paths = [
            'ISA_LOOP/GS_LOOP',
            'GS_LOOP',
            'ST_LOOP/DETAIL/2000',
            'GS_LOOP/ST_LOOP/DETAIL/2000A',
            'DETAIL/2000A/2000B',
            '2000A/2000B/2300',
            '2000B/2300/2400',
            'ST_LOOP/HEADER',
            'ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A',
            'GS_LOOP/ST_LOOP/HEADER/1000B'
        ]
        for spath in paths:
            plist = spath.split('/')
            rd = pyx12.path.path(spath)
            self.assertEqual(rd.loop_list, plist, '%s: %s != %s' % (spath, rd.loop_list, plist))


class AbsolutePath(unittest.TestCase):
    def test_paths_with_refdes(self):
        tests = [
            ('/AAA/TST', 'TST', None, None, None, ['AAA']),
            ('/B1000/TST02', 'TST', None, 2, None, ['B1000']),
            ('/1000B/TST03-2', 'TST', None, 3, 2, ['1000B']),
            ('/1000A/1000B/TST[AA]02', 'TST', 'AA', 2, None, ['1000A', '1000B']),
            ('/AA/BB/CC/TST[1B5]03-1', 'TST', '1B5', 3, 1, ['AA', 'BB', 'CC']),
            ('/DDD/E1000/N102', 'N1', None, 2, None, ['DDD', 'E1000']),
            ('/E1000/D322/N102-5', 'N1', None, 2, 5, ['E1000', 'D322']),
            ('/BB/CC/N1[AZR]02', 'N1', 'AZR', 2, None, ['BB', 'CC']),
            ('/BB/CC/N1[372]02-5', 'N1', '372', 2, 5, ['BB', 'CC'])
        ]
        for (spath, seg_id, qual, eleidx, subeleidx, plist) in tests:
            rd = pyx12.path.path(spath)
            self.assertEqual(rd.relative, False, '%s: %s != %s' % (spath, rd.relative, False))
            self.assertEqual(rd.seg_id, seg_id, '%s: %s != %s' % (spath, rd.seg_id, seg_id))
            self.assertEqual(rd.id_val, qual, '%s: %s != %s' % (spath, rd.id_val, qual))
            self.assertEqual(rd.ele_idx, eleidx, '%s: %s != %s' % (spath, rd.ele_idx, eleidx))
            self.assertEqual(rd.subele_idx, subeleidx, '%s: %s != %s' % (spath, rd.subele_idx, subeleidx))
            self.assertEqual(rd.format(), spath, '%s: %s != %s' % (spath, rd.format(), spath))
            self.assertEqual(rd.loop_list, plist, '%s: %s != %s' % (spath, rd.loop_list, plist))

    def test_bad_paths(self):
        bad_paths = [
            '/AA/03',
            '/BB/CC/03-2'
        ]
        for spath in bad_paths:
            self.failUnlessRaises(pyx12.errors.X12PathError, pyx12.path.path, spath)

    def test_plain_loops(self):
        paths = [
            '/ISA_LOOP/GS_LOOP',
            '/ISA_LOOP/GS_LOOP',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B'
        ]
        for spath in paths:
            plist = spath.split('/')[1:]
            rd = pyx12.path.path(spath)
            self.assertEqual(rd.loop_list, plist, '%s: %s != %s' % (spath, rd.loop_list, plist))
