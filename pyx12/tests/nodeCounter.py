import unittest

from pyx12.nodeCounter import NodeCounter
#from pyx12.path import X12Path


class Default(unittest.TestCase):
    def test_loop_repeat(self):
        initialCounts = {}
        counter = NodeCounter(initialCounts)
        counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/ST')
        counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BPR')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/TRN')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF[EV]')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/DTM')
        counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N1')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N3')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N4')
        counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N1')
        counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/LX')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/TS3')
        counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100')

        self.assertEqual(0, counter.get_count('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110'))
        counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110')
        self.assertEqual(0, counter.get_count('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110'))
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110')
        self.assertEqual(1, counter.get_count('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110'))
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/SVC')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/DTM')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/DTM')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/CAS')
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/LQ')

        self.assertEqual(1, counter.get_count('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110'))
        counter.reset_to_node('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110')
        self.assertEqual(1, counter.get_count('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110'))
        counter.increment('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110')
        self.assertEqual(2, counter.get_count('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110'))
