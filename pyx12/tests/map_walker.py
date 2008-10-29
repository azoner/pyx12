#! /usr/bin/env /usr/local/bin/python

#    $Id$

import sys
from os.path import dirname, abspath, join, isdir, isfile
import unittest

import pyx12.error_handler
from pyx12.errors import *
from pyx12.map_walker import walk_tree, get_pop_loops, get_push_loops, common_root_node
import pyx12.map_if
import pyx12.params 
import pyx12.segment
from pyx12.tests.support import getMapPath

class Explicit_Loops(unittest.TestCase):

    def setUp(self):
        map_path = getMapPath()
        self.walker = walk_tree()
        param = pyx12.params.params('pyx12.conf.xml')
        if map_path:
            param.set('map_path', map_path)
            param.set('pickle_path', map_path)
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()
        #self.logger = logging.getLogger('pyx12')
        #self.logger.setLevel(logging.DEBUG)
        #formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        #hdlr = logging.FileHandler('debug.txt')
        #hdlr.setFormatter(formatter)
        #self.logger.addHandler(hdlr)

    def test_ISA_to_GS(self):
        node = self.map.getnodebypath('/ISA_LOOP/ISA')
        self.assertNotEqual(node, None, 'node not found')
        seg_data = pyx12.segment.Segment('GS*HC', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None, 'walker failed')
        self.assertEqual(seg_data.get_seg_id(), node.id)

    def test_GS_to_ST(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
        seg_data = pyx12.segment.Segment('ST*837', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)

    def test_SE_to_ST(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/SE')
        self.assertNotEqual(node, None)
        seg_data = pyx12.segment.Segment('ST*837', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)

    def test_SE_to_GE(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/SE')
        #node.cur_count = 1 # HACK
        seg_data = pyx12.segment.Segment('GE*1', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)

    def test_GE_to_GS(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/GE')
        seg_data = pyx12.segment.Segment('GS*HC', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)

    def test_GE_to_IEA(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/GE')
        self.assertEqual('GE', node.id)
        seg_data = pyx12.segment.Segment('IEA*1', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)

    def test_IEA_to_ISA(self):
        node = self.map.getnodebypath('/ISA_LOOP/IEA')
        self.assertEqual('IEA', node.id)
        seg_data = pyx12.segment.Segment('ISA*00', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)

    def test_ST_to_BHT_fail(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/ST')
        seg_data = pyx12.segment.Segment('ZZZ*0019', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(node, None)

    def tearDown(self):
        del self.errh
        del self.map
        del self.walker
        

class Implicit_Loops(unittest.TestCase):
    """
    TA1 segment

    child loop
    next sibling loop
    end loop - goto parent loop
    
    start at loop node
    start at segment node
    start at element/composite node?

    MATCH HL segment

    FAIL - loop repeat exceeds max count
    OK - loop repeat does not exceed max count
    """

    def setUp(self):
        map_path = getMapPath()
        self.walker = walk_tree()
        self.param = pyx12.params.params('pyx12.conf.xml')
        if map_path:
            self.param.set('map_path', map_path)
            self.param.set('pickle_path', map_path)
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', self.param)
        self.errh = pyx12.error_handler.errh_null()

    def test_ST_to_BHT(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/ST')
        seg_data = pyx12.segment.Segment('BHT*0019', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)

    def test_repeat_loop_with_one_segment(self):
        map = pyx12.map_if.load_map_file('841.4010.XXXC.xml', self.param)
        node = map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/SPI')
        self.assertNotEqual(node, None, 'Node not found')
        node.cur_count = 1
        seg_data = pyx12.segment.Segment('SPI*00', '~', '*', ':')
        errh = pyx12.error_handler.errh_null()
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        self.assertNotEqual(node, None, 'walker failed')
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(errh.err_cde, None, errh.err_str)

    def test_repeat_loop_with_one_segment_EQ(self):
        errh = pyx12.error_handler.errh_null()
        map = pyx12.map_if.load_map_file('270.4010.X092.A1.xml', self.param)
        node = map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2000C/2100C/2110C/EQ')
        self.assertNotEqual(node, None, 'Node not found')
        node.cur_count = 1
        seg_data = pyx12.segment.Segment('EQ*30**CHD', '~', '*', ':')
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        self.assertNotEqual(node, None, 'walker failed')
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(errh.err_cde, None, errh.err_str)

    def test_loop_required_fail1(self):
        """
        Test for skipped /2000A/2010AA/NM1 segment - first segment of loop
        """
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/HL')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.Segment('HL*1**20*1~', '~', '*', ':')
        result = node.is_valid(seg_data, self.errh)
        seg_data = pyx12.segment.Segment('HL*2*1*22*0~', '~', '*', ':')
        errh = pyx12.error_handler.errh_null()
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        #result = node.is_valid(seg_data, self.errh)
        #self.failIf(result)
        self.assertEqual(errh.err_cde, '3', errh.err_str)
        
    def test_match_loop_by_hl_ok(self):
        """
        MATCH loop by HL segment
        """
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'loop')
        seg_data = pyx12.segment.Segment('HL*1**20*1~', '~', '*', ':')
        errh = pyx12.error_handler.errh_null()
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        result = node.is_valid(seg_data, self.errh)
        self.assertEqual(errh.err_cde, None, errh.err_str)
 
    def test_loop_required_ok1(self):
        """
        MATCH loop by first segment
        Test for found /2000A/2010AA/NM1 segment
        """
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'loop')
        seg_data = pyx12.segment.Segment('HL*1**20*1~', '~', '*', ':')
        errh = pyx12.error_handler.errh_null()
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        result = node.is_valid(seg_data, self.errh)
        self.assertEqual(errh.err_cde, None, errh.err_str)
        seg_data = pyx12.segment.Segment('NM1*85*2*Provider Name*****XX*24423423~', '~', '*', ':')
        errh = pyx12.error_handler.errh_null()
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        self.assertEqual(errh.err_cde, None, errh.err_str)
        result = node.is_valid(seg_data, self.errh)
        self.failUnless(result)
        self.assertEqual(errh.err_cde, None, errh.err_str)

    def test_mult_matching_subloops_ok(self):
        """
        Test for match of 820 Individual Remittance Loop
        """
        errh = pyx12.error_handler.errh_null()
        map = pyx12.map_if.load_map_file('820.4010.X061.A1.xml', self.param)
        node = map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'loop')
        node.cur_count = 1
        node = map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'loop')
        node.cur_count = 1
        node = map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'loop')
        node.cur_count = 1
        node = map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N1')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        node.cur_count = 1
        seg_data = pyx12.segment.Segment('ENT*1*2J*EI*99998707~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        self.assertEqual(errh.err_cde, None, errh.err_str)
        
    def tearDown(self):
        del self.errh
        del self.map
        del self.walker
        

class SegmentWalk(unittest.TestCase):

    def setUp(self):
        map_path = getMapPath()
        self.walker = walk_tree()
        self.param = pyx12.params.params('pyx12.conf.xml')
        if map_path:
            self.param.set('map_path', map_path)
            self.param.set('pickle_path', map_path)
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', self.param)
        self.errh = pyx12.error_handler.errh_null()

    def test_match_regular_segment(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2010AB/NM1')
        seg_data = pyx12.segment.Segment('N4*Billings*MT*56123', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
    
    def test_match_ID_segment1(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        seg_data = pyx12.segment.Segment('DTP*454*D8*20040101', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
    
    def test_segment_required_fail1(self):
        """
        Skipped required segment
        """
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2010AA/NM1')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.Segment('N4*NOWHERE*MA*30001~', '~', '*', ':')
        errh = pyx12.error_handler.errh_null()
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        self.assertEqual(errh.err_cde, '3', errh.err_str)
   
    def test_found_unused_segment1(self):
        map = pyx12.map_if.load_map_file('comp_test.xml', self.param)
        node = map.getnodebypath('/TST')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        node.cur_count = 1
        seg_data = pyx12.segment.Segment('UNU*AA*B~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        #result = node.is_valid(comp, self.errh)
        #self.failUnless(result)
        self.assertEqual(self.errh.err_cde, '2', self.errh.err_str)

    def tearDown(self):
        del self.errh
        del self.map
        del self.walker
        

class Segment_ID_Checks(unittest.TestCase):

    def setUp(self):
        map_path = getMapPath()
        self.walker = walk_tree()
        param = pyx12.params.params('pyx12.conf.xml')
        if map_path:
            param.set('map_path', map_path)
            param.set('pickle_path', map_path)
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()
        self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/ST')

    def test_segment_id_short(self):
        node = self.node
        seg_data = pyx12.segment.Segment('Z*0019', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(node, None)
        self.assertEqual(self.errh.err_cde, '1', self.errh.err_str)

    def test_segment_id_long(self):
        node = self.node
        seg_data = pyx12.segment.Segment('ZZZZ*0019', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(node, None)
        self.assertEqual(self.errh.err_cde, '1', self.errh.err_str)


class Counting(unittest.TestCase):

    def setUp(self):
        map_path = getMapPath()
        self.walker = walk_tree()
        param = pyx12.params.params('pyx12.conf.xml')
        if map_path:
            param.set('map_path', map_path)
            param.set('pickle_path', map_path)
        self.map = pyx12.map_if.load_map_file('270.4010.X092.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()
        #self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2100B/N4')
        self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2100B/NM1')
        self.node.parent.cur_count = 1 # Loop 2100B
        self.node.cur_count = 1
        self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2100B/PER')
        self.assertNotEqual(self.node, None)

    def test_count_ok1(self):
        node = self.node
        node.cur_count = 1
        seg_data = pyx12.segment.Segment('PER*IC*Name1*EM*dev@null.com~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_count_ok2(self):
        node = self.node
        node.cur_count = 2 
        seg_data = pyx12.segment.Segment('PER*IC*Name1*EM*dev@null.com~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_count_fail1(self):
        node = self.node
        node.cur_count = 3 
        seg_data = pyx12.segment.Segment('PER*IC*Name1*EM*dev@null.com~', '~', '*', ':')
        self.assertNotEqual(node, None, 'Node not found')
        self.errh.err_cde = None
        self.errh.err_str = None
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, '5', self.errh.err_str)


class LoopCounting(unittest.TestCase):

    def setUp(self):
        map_path = getMapPath()
        self.walker = walk_tree()
        param = pyx12.params.params('pyx12.conf.xml')
        if map_path:
            param.set('map_path', map_path)
            param.set('pickle_path', map_path)
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_max_loop_count_ok1(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400')
        self.assertNotEqual(node, None, 'Node not found')
        node.cur_count = 48 
        seg_data = pyx12.segment.Segment('LX*51~', '~', '*', ':')
        self.errh.err_cde = None
        self.errh.err_str = None
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_max_loop_count_fail1(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400')
        self.assertNotEqual(node, None, 'Node not found')
        node.cur_count = 50
        seg_data = pyx12.segment.Segment('LX*51~', '~', '*', ':')
        self.errh.err_cde = None
        self.errh.err_str = None
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, '4', self.errh.err_str)


class CountOrdinal(unittest.TestCase):

    def setUp(self):
        map_path = getMapPath()
        self.walker = walk_tree()
        param = pyx12.params.params('pyx12.conf.xml')
        if map_path:
            param.set('map_path', map_path)
            param.set('pickle_path', map_path)
        self.map = pyx12.map_if.load_map_file('834.4010.X095.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()
        #self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2100B/N4')
        self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
        self.assertNotEqual(self.node, None)
        self.node.parent.cur_count = 1 # Loop 2000
        self.node.cur_count = 1 # INS

    def test_ord_ok1(self):
        node = self.node
        seg_data = pyx12.segment.Segment('REF*0F*1234~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        seg_data = pyx12.segment.Segment('REF*1L*91234~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_ord_ok2(self):
        node = self.node
        seg_data = pyx12.segment.Segment('REF*0F*1234~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        seg_data = pyx12.segment.Segment('REF*17*A232~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_ord_ok3(self):
        node = self.node
        seg_data = pyx12.segment.Segment('REF*17*1234~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        seg_data = pyx12.segment.Segment('REF*0F*A232~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_ord_bad1(self):
        node = self.node
        seg_data = pyx12.segment.Segment('REF*0F*1234~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        seg_data = pyx12.segment.Segment('DTP*297*D8*20040101~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        seg_data = pyx12.segment.Segment('REF*17*A232~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, '1', self.errh.err_str)

    def test_lui_ok(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100A/NM1')
        node.parent.cur_count = 1 # Loop 2100A
        node.cur_count = 1 # NM1
        self.assertNotEqual(node, None)
        seg_data = pyx12.segment.Segment('LUI***ES~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

class LoopPathPopPush(unittest.TestCase):

    def setUp(self):
        map_path = getMapPath()
        self.walker = walk_tree()
        param = pyx12.params.params('pyx12.conf.xml')
        if map_path:
            param.set('map_path', map_path)
            param.set('pickle_path', map_path)
        self.map = pyx12.map_if.load_map_file('834.4010.X095.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()
        self.map837P = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)

    def test_path_same_repeat(self):
        start = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
        end =   self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
        #self.assertNotEqual(node, None)
        base = common_root_node(start, end)
        self.assertEqual(base.get_path(), '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL')
        self.assertEqual([l.id for l in get_pop_loops(start, end)], ['2000'])
        self.assertEqual([l.id for l in get_push_loops(start, end)], ['2000'])

    def test_path_in(self):
        start = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
        end = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/DTP')
        #self.assertNotEqual(node, None)
        base = common_root_node(start, end)
        self.assertEqual(base.get_path(), '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000')
        self.assertEqual([l.id for l in get_pop_loops(start, end)], [])
        self.assertEqual([l.id for l in get_push_loops(start, end)], [])

    def test_path_repeat(self):
        start = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/DTP')
        end = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
        #self.assertNotEqual(node, None)
        base = common_root_node(start, end)
        self.assertEqual(base.get_path(), '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL')
        self.assertEqual([l.id for l in get_pop_loops(start, end)], ['2000'])
        self.assertEqual([l.id for l in get_push_loops(start, end)], ['2000'])

    def test_path_up(self):
        start = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
        end = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N1')
        #self.assertNotEqual(node, None)
        base = common_root_node(start, end)
        desc = '%s => %s' % (start.get_path(), end.get_path())
        self.assertEqual(base.get_path(), '/ISA_LOOP/GS_LOOP')
        self.assertEqual([l.id for l in get_pop_loops(start, end)], ['2000', 'DETAIL', 'ST_LOOP'])
        self.assertEqual([l.id for l in get_push_loops(start, end)], ['ST_LOOP', 'HEADER', '1000B'])

    def test_path_up2(self):
        start = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
        end = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
        desc = '%s => %s' % (start.get_path(), end.get_path())
        #self.assertNotEqual(node, None)
        base = common_root_node(start, end)
        self.assertEqual(base.get_path(), '/ISA_LOOP')
        self.assertEqual([l.id for l in get_pop_loops(start, end)], ['2000', 'DETAIL', 'ST_LOOP', 'GS_LOOP'])
        self.assertEqual([l.id for l in get_push_loops(start, end)], ['GS_LOOP'])

    def test_path_up3(self):
        start = self.map837P.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/2430/SVD')
        end = self.map837P.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/LX')
        desc = '%s => %s' % (start.get_path(), end.get_path())
        self.assertNotEqual(start, None)
        self.assertNotEqual(end, None)
        base = common_root_node(start, end)
        self.assertEqual(base.get_path(), '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300')
        self.assertEqual([l.id for l in get_pop_loops(start, end)], ['2430', '2400'])
        self.assertEqual([l.id for l in get_push_loops(start, end)], ['2400'])

    def test_path_sub_loop(self):
        start = self.map837P.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/HI')
        end =   self.map837P.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2310B/NM1')
        desc = '%s => %s' % (start.get_path(), end.get_path())
        self.assertNotEqual(start, None)
        self.assertNotEqual(end, None)
        base = common_root_node(start, end)
        self.assertEqual(base.get_path(), '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300')
        self.assertEqual([l.id for l in get_pop_loops(start, end)], [])
        self.assertEqual([l.id for l in get_push_loops(start, end)], ['2310B'])
