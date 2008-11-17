#! /usr/bin/env /usr/local/bin/python

import unittest
#import sys
import tempfile
import StringIO

import pyx12.error_handler
#from error_handler import ErrorErrhNull
from pyx12.errors import *
import pyx12.x12context
import pyx12.params

class Delimiters(unittest.TestCase):

    def test_arbitrary_delimiters(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str1 += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&004010X098A1+\n'
        str1 += 'ST&837&11280001+\n'
        str1 += 'REF&87&004010X098A1+\n'
        str1 += 'SE&3&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        fd = StringIO.StringIO(str1)
        fd.seek(0)
        param = pyx12.params.params('pyx12.conf.xml')
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(param, errh, fd, xslt_files = [])
        for datatree in src.iter_segments():
            pass
        self.assertEqual(src.subele_term, '!')
        self.assertEqual(src.ele_term, '&')
        self.assertEqual(src.seg_term, '+')

    def test_binary_delimiters(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str1 += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&004010X098A1+\n'
        str1 += 'ST&837&11280001+\n'
        str1 += 'REF&87&004010X098A1+\n'
        str1 += 'SE&3&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        str1 = str1.replace('&', chr(0x1C))
        str1 = str1.replace('+', chr(0x1D))
        str1 = str1.replace('!', chr(0x1E))
        fd = StringIO.StringIO(str1)
        fd.seek(0)
        errors = []
        param = pyx12.params.params('pyx12.conf.xml')
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(param, errh, fd, xslt_files = [])
        for datatree in src.iter_segments():
            pass
        self.assertEqual(src.subele_term, chr(0x1E))
        self.assertEqual(src.ele_term, chr(0x1C))
        self.assertEqual(src.seg_term, chr(0x1D))


class TreeGetValue(unittest.TestCase):

    def setUp(self):
        fd = open('files/simple_837p.txt')
        param = pyx12.params.params('pyx12.conf.xml')
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd, xslt_files = [])
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_get_seg_value(self):
        self.assertEqual(self.loop2300.get_value('CLM02'), '21')
        self.assertEqual(self.loop2300.get_value('CLM99'), None)

    def test_get_first_value(self):
        self.assertEqual(self.loop2300.get_value('2400/SV101'), 'HC:H2015:TT')
        self.assertEqual(self.loop2300.get_value('2400/SV101-2'), 'H2015')
        self.assertEqual(self.loop2300.get_value('2400/REF[6R]02'), '1057296')
        self.assertEqual(self.loop2300.get_value('2400/2430/SVD02'), '21')

    def test_get_no_value(self):
        self.assertEqual(self.loop2300.get_value('2400/SV199'), None)
        self.assertEqual(self.loop2300.get_value('2400'), None)


class TreeSelect(unittest.TestCase):

    def setUp(self):
        fd = open('files/simple_837p.txt')
        param = pyx12.params.params('pyx12.conf.xml')
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(param, errh, fd, xslt_files = [])
        for datatree in src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_select_loops(self):
        ct = 0
        for newtree in self.loop2300.select('2400'):
            self.assertEqual(newtree.id, '2400')
            ct += 1
        self.assertEqual(ct, 2)

    def test_select_seg(self):
        ct = 0
        for newtree in self.loop2300.select('2400/SV1'):
            self.assertEqual(newtree.id, 'SV1')
            self.assertEqual(newtree.get_value('SV102'), '21')
            ct += 1
        self.assertEqual(ct, 2)

class ParseRefDes(unittest.TestCase):

    def test_plain(self):
        self.assertEqual(pyx12.x12context.X12SegmentDataNode.get_seg_id('TST01'), ('TST01', None))
        self.assertEqual(pyx12.x12context.X12SegmentDataNode.get_seg_id('TST05-1'), ('TST05-1', None))
        self.assertEqual(pyx12.x12context.X12SegmentDataNode.get_seg_id('TST02-4'), ('TST02-4', None))

    def test_qual(self):
        self.assertEqual(pyx12.x12context.X12SegmentDataNode.get_seg_id('TST01[6R]'), ('TST01', '6R'))
        self.assertEqual(pyx12.x12context.X12SegmentDataNode.get_seg_id('TST05-1[DD]'), ('TST05-1', 'DD'))
        self.assertEqual(pyx12.x12context.X12SegmentDataNode.get_seg_id('TST02-4[EB]'), ('TST02-4', 'EB'))
        self.assertEqual(pyx12.x12context.X12SegmentDataNode.get_seg_id('TST[6R]01'), ('TST01', '6R'))
        self.assertEqual(pyx12.x12context.X12SegmentDataNode.get_seg_id('TST[DD]05-1'), ('TST05-1', 'DD'))
        self.assertEqual(pyx12.x12context.X12SegmentDataNode.get_seg_id('TST[EB]02-4'), ('TST02-4', 'EB'))


class TreeAddSegment(unittest.TestCase):

    def setUp(self):
        fd = open('files/simple_837p.txt')
        param = pyx12.params.params('pyx12.conf.xml')
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd, xslt_files = [])
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_add_new_plain(self):
        seg_data = pyx12.segment.Segment('HCP*00*7.11~', '~', '*', ':')
        new_node = self.loop2300.add_segment(seg_data)
        self.assertNotEqual(new_node, None)

    def test_add_new_id(self):
        seg_data = pyx12.segment.Segment('REF*F5*6.11~', '~', '*', ':')
        new_node = self.loop2300.add_segment(seg_data)
        self.assertNotEqual(new_node, None)

    def test_add_new_not_exists(self):
        seg_data = pyx12.segment.Segment('ZZZ*00~', '~', '*', ':')
        self.failUnlessRaises(pyx12.errors.X12PathError, self.loop2300.add_segment, seg_data)


class TreeAddSegmentString(unittest.TestCase):

    def setUp(self):
        fd = open('files/simple_837p.txt')
        param = pyx12.params.params('pyx12.conf.xml')
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd, xslt_files = [])
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_add_new_plain(self):
        new_node = self.loop2300.add_segment('HCP*00*7.11~')
        self.assertNotEqual(new_node, None)

    def test_add_new_id(self):
        new_node = self.loop2300.add_segment('REF*F5*6.11')
        self.assertNotEqual(new_node, None)

    def test_add_new_not_exists(self):
        self.failUnlessRaises(pyx12.errors.X12PathError, self.loop2300.add_segment, 'ZZZ*00~')


class TreeAddLoop(unittest.TestCase):

    def setUp(self):
        fd = open('files/simple_837p.txt')
        param = pyx12.params.params('pyx12.conf.xml')
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd, xslt_files = [])
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_add_new_plain(self):
        seg_data = pyx12.segment.Segment('NM1*82*2*Provider 1*****ZZ*9898798~', '~', '*', ':')
        new_node = self.loop2300.add_loop(seg_data)
        self.assertNotEqual(new_node, None)


class CountRepeatingLoop(unittest.TestCase):

    def setUp(self):
        fd = open('files/simple_837p.txt')
        param = pyx12.params.params('pyx12.conf.xml')
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd, xslt_files = [])
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300' and datatree.get_value('CLM01') == '5555':
                self.loop2300 = datatree
                break

    def test_repeat_2400(self):
        ct = 0
        for loop_2400 in self.loop2300.select('2400'):
            ct += 1
        self.assertEqual(ct, 3, 'Found %i 2400 loops.  Should have %i' % (ct, 3))

