#! /usr/bin/env /usr/local/bin/python

#    $Id$

import os.path
import unittest
import pdb

import pyx12.error_handler
#from error_handler import ErrorErrhNull
from pyx12.errors import *
from pyx12.map_walker import walk_tree
import pyx12.map_if
from pyx12.params import params
import pyx12.segment


class Find_Explicit_Loops(unittest.TestCase):

    def setUp(self):
        self.walker = walk_tree()
        param = params()
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)

    def test_ISA_to_GS(self):
        node = self.map.getnodebypath('/ISA/ISA')
        seg = pyx12.segment.segment('GS*HC', '~', '*', ':')
        path = self.walker.find_match(node, seg)
        self.assertEqual(path, '/ISA/GS/GS')

    def test_GS_to_ST(self):
        node = self.map.getnodebypath('/ISA/GS/GS')
        seg = pyx12.segment.segment('ST*837', '~', '*', ':')
        path = self.walker.find_match(node, seg)
        self.assertEqual(path, '/ISA/GS/ST/HEADER/ST')

    def test_SE_to_ST(self):
        node = self.map.getnodebypath('/ISA/GS/ST/FOOTER/SE')
        seg = pyx12.segment.segment('ST*837', '~', '*', ':')
        path = self.walker.find_match(node, seg)
        self.assertEqual(path, '/ISA/GS/ST/HEADER/ST')

    def test_SE_to_GE(self):
        node = self.map.getnodebypath('/ISA/GS/ST/FOOTER/SE')
        #node.cur_count = 1 # HACK
        seg = pyx12.segment.segment('GE*1', '~', '*', ':')
        path = self.walker.find_match(node, seg)
        self.assertEqual(path, '/ISA/GS/GE')

    def test_GE_to_GS(self):
        node = self.map.getnodebypath('/ISA/GS/GE')
        seg = pyx12.segment.segment('GS*HC', '~', '*', ':')
        path = self.walker.find_match(node, seg)
        self.assertEqual(path, '/ISA/GS/GS')

    def test_GE_to_IEA(self):
        node = self.map.getnodebypath('/ISA/GS/GE')
        self.assertEqual('GE', node.id)
        seg = pyx12.segment.segment('IEA*1', '~', '*', ':')
        path = self.walker.find_match(node, seg)
        self.assertEqual(path, '/ISA/IEA')

    def test_IEA_to_ISA(self):
        node = self.map.getnodebypath('/ISA/IEA')
        self.assertEqual('IEA', node.id)
        seg = pyx12.segment.segment('ISA*00', '~', '*', ':')
        path = self.walker.find_match(node, seg)
        self.assertEqual(path, '/ISA/ISA')

    def test_ST_to_BHT_fail(self):
        node = self.map.getnodebypath('/ISA/GS/ST/HEADER/ST')
        seg = pyx12.segment.segment('ZZZ*0019', '~', '*', ':')
        path = self.walker.find_match(node, seg)
        self.assertEqual(path, '')

    def tearDown(self):
        del self.map
        del self.walker
        

class Find_Implicit_Loops(unittest.TestCase):
    """
    TA1 segment

    child loop
    next sibling loop
    end loop - goto parent loop
    
    start at loop node
    start at segment node

    MATCH HL segment

    """

    def setUp(self):
        self.walker = walk_tree()
        param = params()
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)

    def test_ST_to_BHT(self):
        node = self.map.getnodebypath('/ISA/GS/ST/HEADER/ST')
        seg_data = pyx12.segment.segment('BHT*0019', '~', '*', ':')
        path = self.walker.find_match(node, seg_data)
        self.assertEqual(path, '/ISA/GS/ST/HEADER/BHT')

    def test_match_loop_by_hl_ok(self):
        """
        MATCH loop by HL segment
        """
        node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000A')
        seg_data = pyx12.segment.segment('HL*1**20*1~', '~', '*', ':')
        path = self.walker.find_match(node, seg_data)
        self.assertEqual(path, '/ISA/GS/ST/DETAIL/2000A/HL')
 
    def tearDown(self):
        del self.map
        del self.walker
        

class Walk_Implicit_Loops(unittest.TestCase):
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
        self.walker = walk_tree()
        param = params()
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_ST_to_BHT(self):
        node = self.map.getnodebypath('/ISA/GS/ST/HEADER/ST')
        seg = pyx12.segment.segment('BHT*0019', '~', '*', ':')
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg.get_seg_id(), node.id)

    def test_repeat_loop_with_one_segment(self):
        param = params()
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        map = pyx12.map_if.load_map_file('841.4010.XXXC.xml', param)
        node = map.getnodebypath('/ISA/GS/ST/DETAIL/1000/2000/2100/SPI')
        seg = pyx12.segment.segment('SPI*00', '~', '*', ':')
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg.get_seg_id(), node.id)

    def test_loop_required_fail1(self):
        """
        Test for skipped /2000A/2010AA/NM1 segment - first segment of loop
        """
        node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000A/HL')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.segment('HL*1**20*1~', '~', '*', ':')
        result = node.is_valid(seg_data, self.errh)
        seg_data = pyx12.segment.segment('HL*2*1*22*0~', '~', '*', ':')
        errh = pyx12.error_handler.errh_null()
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        #result = node.is_valid(seg_data, self.errh)
        #self.failIf(result)
        self.assertEqual(errh.err_cde, '3', errh.err_str)
        
    def test_match_loop_by_hl_ok(self):
        """
        MATCH loop by HL segment
        """
        node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000A')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'loop')
        seg_data = pyx12.segment.segment('HL*1**20*1~', '~', '*', ':')
        errh = pyx12.error_handler.errh_null()
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        result = node.is_valid(seg_data, self.errh)
        self.assertEqual(errh.err_cde, None, errh.err_str)
 
    def test_loop_required_ok1(self):
        """
        MATCH loop by first segment
        Test for found /2000A/2010AA/NM1 segment
        """
        node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000A')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'loop')
        seg_data = pyx12.segment.segment('HL*1**20*1~', '~', '*', ':')
        errh = pyx12.error_handler.errh_null()
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        result = node.is_valid(seg_data, self.errh)
        self.assertEqual(errh.err_cde, None, errh.err_str)
        seg_data = pyx12.segment.segment('NM1*85*2*Provider Name*****XX*24423423~', '~', '*', ':')
        errh = pyx12.error_handler.errh_null()
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        self.assertEqual(errh.err_cde, None, errh.err_str)
        result = node.is_valid(seg_data, self.errh)
        self.failUnless(result)
        self.assertEqual(errh.err_cde, None, errh.err_str)

    def tearDown(self):
        del self.errh
        del self.map
        del self.walker
        

class SegmentWalk(unittest.TestCase):

    def setUp(self):
        self.walker = walk_tree()
        param = params()
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_match_regular_segment(self):
        node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000A/2010AB/NM1')
        seg = pyx12.segment.segment('N4*Billings*MT*56123', '~', '*', ':')
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg.get_seg_id(), node.id)
    
    def test_match_ID_segment1(self):
        node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000A/2000B/2300/CLM')
        seg = pyx12.segment.segment('DTP*454*D8*20040101', '~', '*', ':')
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg.get_seg_id(), node.id)
    
    def test_match_ID_segment2(self):
        node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000A/2000B/2300/CLM')
        seg = pyx12.segment.segment('DTP*454*D8*20040101', '~', '*', ':')
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg.get_seg_id(), node.id)
    
#    def test_fail_ID_segment(self):
#        node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000A/2000B/2300/CLM')
#        seg = ['DTP', '999', 'D8', '20040201']
#        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
#        self.assertNotEqual(seg.get_seg_id(), node.id)

    def test_segment_required_fail1(self):
        """
        Skipped required segment
        """
        node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000A/2010AA/NM1')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.segment('N4*NOWHERE*MA*30001~', '~', '*', ':')
        errh = pyx12.error_handler.errh_null()
        node = self.walker.walk(node, seg_data, errh, 5, 4, None)
        self.assertEqual(errh.err_cde, '3', errh.err_str)
   
    def test_found_unused_segment1(self):
        param = params()
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        map = pyx12.map_if.load_map_file('comp_test.xml', param)
        node = map.getnodebypath('/TST')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        node.cur_count = 1
        seg_data = pyx12.segment.segment('UNU*AA*B~', '~', '*', ':')
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
        self.walker = walk_tree()
        param = params()
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()
        self.node = self.map.getnodebypath('/ISA/GS/ST/HEADER/ST')

    def test_segment_id_short(self):
        node = self.node
        seg = pyx12.segment.segment('Z*0019', '~', '*', ':')
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(node, None)
        self.assertEqual(self.errh.err_cde, '1', self.errh.err_str)

    def test_segment_id_long(self):
        node = self.node
        seg = pyx12.segment.segment('ZZZZ*0019', '~', '*', ':')
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(node, None)
        self.assertEqual(self.errh.err_cde, '1', self.errh.err_str)

    def test_segment_empty(self):
        node = self.node
        seg = pyx12.segment.segment('', '~', '*', ':')
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(node, None)
        self.assertEqual(self.errh.err_cde, '1', self.errh.err_str)


class Counting(unittest.TestCase):

    def setUp(self):
        self.walker = walk_tree()
        param = params()
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('270.4010.X092.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()
        #self.node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000A/2000B/2100B/N4')
        self.node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000A/2000B/2100B/PER')
        self.assertNotEqual(self.node, None)

    def test_count_ok1(self):
        node = self.node
        seg_data = pyx12.segment.segment('PER*IC*Name1*EM*dev@null.com~', '~', '*', ':')
        node.cur_count = 1
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_count_ok2(self):
        node = self.node
        seg_data = pyx12.segment.segment('PER*IC*Name1*EM*dev@null.com~', '~', '*', ':')
        node.cur_count = 2 
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_count_fail1(self):
        node = self.node
        seg_data = pyx12.segment.segment('PER*IC*Name1*EM*dev@null.com~', '~', '*', ':')
        self.assertNotEqual(node, None)
        node.cur_count = 3 
        self.errh.err_cde = None
        self.errh.err_str = None
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, '5', self.errh.err_str)


class CountOrdinal(unittest.TestCase):

    def setUp(self):
        self.walker = walk_tree()
        param = params()
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('834.4010.X095.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()
        #self.node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000A/2000B/2100B/N4')
        self.node = self.map.getnodebypath('/ISA/GS/ST/DETAIL/2000/INS')
        self.assertNotEqual(self.node, None)
        self.node.cur_count = 1

    def test_ord_ok1(self):
        node = self.node
        seg_data = pyx12.segment.segment('REF*0F*1234~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        seg_data = pyx12.segment.segment('REF*1L*91234~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_ord_ok2(self):
        node = self.node
        seg_data = pyx12.segment.segment('REF*0F*1234~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        seg_data = pyx12.segment.segment('REF*17*A232~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_ord_ok3(self):
        node = self.node
        seg_data = pyx12.segment.segment('REF*17*1234~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        seg_data = pyx12.segment.segment('REF*0F*A232~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_ord_bad1(self):
        node = self.node
        seg_data = pyx12.segment.segment('REF*0F*1234~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        seg_data = pyx12.segment.segment('DTP*297*D8*20040101~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        seg_data = pyx12.segment.segment('REF*17*A232~', '~', '*', ':')
        node = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, '1', self.errh.err_str)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Find_Explicit_Loops))
    suite.addTest(unittest.makeSuite(Find_Implicit_Loops))
    #suite.addTest(unittest.makeSuite(SegmentWalk))
    #suite.addTest(unittest.makeSuite(Segment_ID_Checks))
    #suite.addTest(unittest.makeSuite(Counting))
    #suite.addTest(unittest.makeSuite(CountOrdinal))
    return suite

#if __name__ == "__main__":
#    unittest.main()
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())

