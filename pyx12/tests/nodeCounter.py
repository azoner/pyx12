"""
Node counter test
"""

import sys
import os.path
import logging
import unittest
from pdb import set_trace

from pyx12.nodeCounter import NodeCounter
#from pyx12.path import X12Path
from .test_config import TestCase


class NodeCounterTest(TestCase):
    def setUp(self):
        super().setUp()
        self.initialCounts = {}
        self.counter = NodeCounter(self.initialCounts)
        self.logger.debug("Setting up test case")

    def test_loop_repeat(self):
        self.logger.debug("Starting loop repeat test")
        self.counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/ST')
        self.counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BPR')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/TRN')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF[EV]')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/DTM')
        self.counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N1')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N3')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N4')
        self.counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N1')
        self.counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/LX')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/TS3')
        self.counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100')

        self.assertEqual(0, self.counter.get_count('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110'))
        self.counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110')
        self.assertEqual(0, self.counter.get_count('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110'))
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110')
        self.assertEqual(1, self.counter.get_count('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110'))
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/SVC')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/DTM')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/DTM')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/CAS')
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/LQ')

        self.assertEqual(1, self.counter.get_count('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110'))
        self.counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110')
        self.assertEqual(1, self.counter.get_count('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110'))
        self.counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110')
        self.assertEqual(2, self.counter.get_count('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110'))
        self.logger.debug("Loop repeat test completed")

if __name__ == '__main__':
    unittest.main()
