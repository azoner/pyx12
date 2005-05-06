#! /usr/bin/env /usr/local/bin/python

import unittest

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
"""

class AbsPath(unittest.TestCase):

    def setUp(self):

    def testLoopOK1(self):
        path_str = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400'
        path = pyx12.path(path_str)
        self.assertEqual(path_str, path.format())
        self.assertEqual(path.seg_id(), None)
        self.assertEqual(path.loops()[2], 'ST_LOOP')

    def testLoopSegOK1(self):
        path_str = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/SV2'
        path = pyx12.path(path_str)
        self.assertEqual(path_str, path.format())
        self.assertEqual(path.seg_id(), 'SV2')

        
class RefDes(unittest.TestCase):

    def test_simple1(self):
        self.assertEqual(self.seg.get_value('TST01'), 'AA')
        self.assertEqual(self.seg.get_value('01'), 'AA')

        self.assertEqual(self.seg.get_value('TST02'), '1')
        self.assertEqual(self.seg.get_value('02'), '1')

    def test_composite1(self):
        self.assertEqual(self.seg.get_value('TST04-2'), '5')
        self.assertEqual(self.seg.get_value('04-2'), '5')

    def test_composite2(self):
        self.assertEqual(self.seg.get_value('TST04-1'), 'BB')
        self.assertEqual(self.seg.get_value('04-1'), 'BB')

    def test_composite3(self):
        self.assertEqual(self.seg.get_value('TST04'), 'BB:5')
        self.assertEqual(self.seg.get_value('04'), 'BB:5')

    def test_none(self):
        self.assertEqual(self.seg.get_value('TST15'), None)
        self.assertEqual(self.seg.get_value('15'), None)
        self.assertEqual(self.seg.get_value('TST15-2'), None)
        self.assertEqual(self.seg.get_value('15-2'), None)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ArbitraryDelimiters))
    return suite

#if __name__ == "__main__":
#    unittest.main()
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())


'/ISA_LOOP/GS_LOOP/GE')
'/ISA_LOOP/GS_LOOP/GS')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/SPI')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2010BA/DMG')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2100B/N4')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2100B/N4')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2100B/NM1')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2100B/PER')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CR6')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2010AA/NM1')
'/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/HL')
'/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER')
'/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A')
'/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B')
'/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N1')
'/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF')
'/ISA_LOOP/GS_LOOP/ST_LOOP/ST')
'/ISA_LOOP/IEA')
'/ISA_LOOP/ISA')
'/TST')
'DTP[096]')
'DTP[096]')
'DTP[434]')
'DTP[434]')
'DTP[434]')
