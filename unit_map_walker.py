#! /usr/bin/env /usr/local/bin/python

#import test_support
#from test_support import TestFailed, have_unicode
import unittest
#import pdb

import error_handler
#from error_handler import ErrorErrhNull
from errors import *
from map_walker import walk_tree
import map_if


class Explicit_Loops(unittest.TestCase):
    """
    FAIL - no end tag for explicit loop
    """
    def setUp(self):
        self.walker = walk_tree()
        #self.map = map_if.map_if('map/837.4010.X098.A1.xml')
        self.map = map_if.load_map_file('map/837.4010.X098.A1.xml')
        self.errh = error_handler.errh_null()

    def test_ISA_to_GS(self):
        node = self.map.getnodebypath('/ISA')
        seg = ['GS', 'HC']
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg[0], node.id)

    def test_GS_to_ST(self):
        node = self.map.getnodebypath('/GS')
        seg = ['ST', '837']
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg[0], node.id)

    def test_SE_to_ST(self):
        node = self.map.getnodebypath('/SE')
        seg = ['ST', '837']
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg[0], node.id)

    def test_SE_to_GE(self):
        node = self.map.getnodebypath('/SE')
        seg = ['GE', '1']
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg[0], node.id)

    def test_GE_to_GS(self):
        node = self.map.getnodebypath('/GE')
        seg = ['GS', '1']
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg[0], node.id)

    def test_GE_to_IEA(self):
        node = self.map.getnodebypath('/GE')
        seg = ['IEA', '1']
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg[0], node.id)

    def test_IEA_to_ISA(self):
        node = self.map.getnodebypath('/IEA')
        seg = ['ISA', '1']
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg[0], node.id)

#    def test_ST_to_BHT_fail(self):
#        node = self.map.getnodebypath('/ST')
#        seg = ['ZZZ', '0019']
#        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
#        self.assertNotEqual(seg[0], node.id)

class Implicit_Loops(unittest.TestCase):
    """
    FAIL - Mandatory segment skipped
    FAIL - Mandatory loop skipped

    TA1 segment

    child loop
    next sibling loop
    end loop - goto parent loop
    
    start at loop node
    start at segment node
    start at element/composite node?

    MATCH loop by first segment
    MATCH HL segment

    FAIL - loop repeat exceeds max count
    OK - loop repeat does not exceed max count
    

    """

    def setUp(self):
        self.walker = walk_tree()
        #self.map = map_if.map_if('map/837.4010.X098.A1.xml')
        self.map = map_if.load_map_file('map/837.4010.X098.A1.xml')
        self.errh = error_handler.errh_null()

    def test_ST_to_BHT(self):
        node = self.map.getnodebypath('/ST')
        seg = ['BHT', '0019']
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg[0], node.id)

class SegmentWalk(unittest.TestCase):
    """
    FAIL - segment repeat exceeds max count
    OK - segment repeat does not exceed max count
    FAIL - found not used segment
    FAIL - segment was not found
    """

    def setUp(self):
        self.walker = walk_tree()
        self.map = map_if.load_map_file('map/837.4010.X098.A1.xml')
        self.errh = error_handler.errh_null()

    def test_match_regular_segment(self):
        node = self.map.getnodebypath('/2000A/2010AB/NM1')
        seg = ['N4', 'Billings', 'MT', '56123']
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg[0], node.id)
    
    def test_match_ID_segment1(self):
        node = self.map.getnodebypath('/2000A/2000B/2300/CLM')
        seg = ['DTP', '454', 'D8', '20040101']
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg[0], node.id)
    
    def test_match_ID_segment2(self):
        node = self.map.getnodebypath('/2000A/2000B/2300/CLM')
        seg = ['DTP', '304', 'D8', '20040201']
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg[0], node.id)
    
    def test_fail_ID_segment(self):
        node = self.map.getnodebypath('/2000A/2000B/2300/CLM')
        seg = ['DTP', '999', 'D8', '20040201']
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertNotEqual(seg[0], node.id)
    
def suite():
    suite = unittest.makeSuite((Explicit_Loops))
    return suite
                
if __name__ == "__main__":
    unittest.main()   
