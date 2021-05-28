import unittest

import pyx12.error_handler
from pyx12.map_walker import walk_tree, get_id_list, traverse_path, pop_to_parent_loop
import pyx12.map_if
import pyx12.params
import pyx12.path
import pyx12.segment


class Explicit_Loops(unittest.TestCase):

    def setUp(self):

        self.walker = walk_tree()
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()
        #self.logger = logging.getLogger('pyx12')
        #self.logger.setLevel(logging.DEBUG)
        #formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        #hdlr = logging.FileHandler('debug.txt')
        #hdlr.setFormatter(formatter)
        #self.logger.addHandler(hdlr)

    def test_ISA_to_GS(self):
        self.errh.reset()
        node = self.map.getnodebypath('/ISA_LOOP/ISA')
        self.assertNotEqual(node, None, 'node not found')
        seg_data = pyx12.segment.Segment('GS*HC', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None, 'walker failed')
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), ['GS_LOOP'])

    def test_GS_to_ST(self):
        self.errh.reset()
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
        seg_data = pyx12.segment.Segment('ST*837', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), ['ST_LOOP'])

    def test_SE_to_ST(self):
        self.errh.reset()
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/SE')
        self.assertNotEqual(node, None)
        seg_data = pyx12.segment.Segment('ST*837', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), ['ST_LOOP'])
        self.assertEqual(get_id_list(push), ['ST_LOOP'])

    def test_SE_to_GE(self):
        self.errh.reset()
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/SE')
        seg_data = pyx12.segment.Segment('GE*1', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), ['ST_LOOP'])
        self.assertEqual(get_id_list(push), [])

    def test_GE_to_GS(self):
        self.errh.reset()
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/GE')
        seg_data = pyx12.segment.Segment('GS*HC', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), ['GS_LOOP'])
        self.assertEqual(get_id_list(push), ['GS_LOOP'])

    def test_GE_to_IEA(self):
        self.errh.reset()
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/GE')
        self.assertEqual('GE', node.id)
        seg_data = pyx12.segment.Segment('IEA*1', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), ['GS_LOOP'])
        self.assertEqual(get_id_list(push), [])

    def test_IEA_to_ISA(self):
        self.errh.reset()
        node = self.map.getnodebypath('/ISA_LOOP/IEA')
        self.assertEqual('IEA', node.id)
        seg_data = pyx12.segment.Segment('ISA*00', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), ['ISA_LOOP'])
        self.assertEqual(get_id_list(push), ['ISA_LOOP'])

    def test_ST_to_BHT_fail(self):
        self.errh.reset()
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/ST')
        seg_data = pyx12.segment.Segment('ZZZ*0019', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(node, None)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])

    def tearDown(self):
        del self.errh
        del self.map
        del self.walker

    def test_GS_to_ST_277(self):
        map_file = '277.5010.X214.xml'
        walker = walk_tree()
        param = pyx12.params.params()
        map = pyx12.map_if.load_map_file(map_file, param)
        errh = pyx12.error_handler.errh_null()
        errh.reset()
        node = map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
        seg_data = pyx12.segment.Segment('ST*277*0001*005010X214', '~', '*', ':')
        (node, pop, push) = walker.walk(
            node, seg_data, errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), ['ST_LOOP'])

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

        self.walker = walk_tree()
        self.param = pyx12.params.params()

        self.map = pyx12.map_if.load_map_file(
            '837.4010.X098.A1.xml', self.param)
        self.errh = pyx12.error_handler.errh_null()

    def test_ST_to_BHT(self):
        self.errh.reset()
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/ST')
        seg_data = pyx12.segment.Segment('BHT*0019', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), ['HEADER'])

    def xtest_repeat_loop_with_one_segment(self):
        cmap = pyx12.map_if.load_map_file('841.4010.XXXC.xml', self.param)
        node = cmap.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/SPI')
        self.assertNotEqual(node, None, 'Node not found')
        start_node = node
        #node.cur_count = 1
        self.walker.setCountState({node.x12path: 1})
        self.errh.reset()
        seg_data = pyx12.segment.Segment('SPI*00', '~', '*', ':')
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None, 'walker failed')
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), ['2100'])
        self.assertEqual(get_id_list(push), ['2100'])
        self.assertEqual(traverse_path(start_node, pop, push), pop_to_parent_loop(node).get_path())

    def test_repeat_loop_with_one_segment_EQ(self):
        #errh = pyx12.error_handler.errh_null()
        cmap = pyx12.map_if.load_map_file('270.4010.X092.A1.xml', self.param)
        node = cmap.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2000C/2100C/2110C/EQ')
        start_node = node
        self.assertNotEqual(node, None, 'Node not found')
        #node.cur_count = 1
        self.walker.setCountState({node.x12path: 1})
        seg_data = pyx12.segment.Segment('EQ*30**CHD', '~', '*', ':')
        self.errh.reset()
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None, 'walker failed')
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), ['2110C'])
        self.assertEqual(get_id_list(push), ['2110C'])
        self.assertEqual(traverse_path(start_node, pop, push),
                         pop_to_parent_loop(node).get_path())

    def test_loop_required_fail1(self):
        """
        Test for skipped /2000A/2010AA/NM1 segment - first segment of loop
        """
        self.errh.reset()
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/HL')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.Segment('HL*1**20*1~', '~', '*', ':')
        result = node.is_valid(seg_data, self.errh)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.walker.setCountState({node.x12path: 1})
        self.errh.reset()
        seg_data = pyx12.segment.Segment('HL*2*1*22*0~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        #result = node.is_valid(seg_data, self.errh)
        #self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '3', self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), ['2000B'])

    def test_match_loop_by_hl_ok(self):
        """
        MATCH loop by HL segment
        """
        self.errh.reset()
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'loop')
        seg_data = pyx12.segment.Segment('HL*1**20*1~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        result = node.is_valid(seg_data, self.errh)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), ['2000A'])
        self.assertEqual(get_id_list(push), ['2000A'])

    def test_loop_required_ok1(self):
        """
        MATCH loop by first segment
        Test for found /2000A/2010AA/NM1 segment
        """
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'loop')
        seg_data = pyx12.segment.Segment('HL*1**20*1~', '~', '*', ':')
        self.errh.reset()
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        result = node.is_valid(seg_data, self.errh)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), ['2000A'])
        self.assertEqual(get_id_list(push), ['2000A'])

        seg_data = pyx12.segment.Segment(
            'NM1*85*2*Provider Name*****XX*24423423~', '~', '*', ':')
        self.errh.reset()
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        result = node.is_valid(seg_data, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), ['2010AA'])

    def test_mult_matching_subloops_ok(self):
        """
        Test for match of 820 Individual Remittance Loop
        """
        cmap = pyx12.map_if.load_map_file('820.5010.X218.xml', self.param)
        node = cmap.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'loop')
        #node.cur_count = 1
        node = cmap.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'loop')
        #node.cur_count = 1
        node = cmap.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'loop')
        #node.cur_count = 1
        node = cmap.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N1')
        self.assertNotEqual(node, None)
        start_node = node
        self.assertEqual(node.base_name, 'segment')
        #node.cur_count = 1
        seg_data = pyx12.segment.Segment(
            'ENT*1*2J*EI*99998707~', '~', '*', ':')
        self.errh.reset()
        #print node.get_path()
        self.walker.setCountState({
            '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER': 1,
            '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A': 1,
            '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B': 1,
            '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N1': 1,
        })
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        #print node.get_path()
        self.assertEqual(get_id_list(pop), ['1000B', 'HEADER'])
        self.assertEqual(get_id_list(push), ['TABLE2AREA3', '2000B'])
        self.assertEqual(traverse_path(start_node, pop, push),
                         pop_to_parent_loop(node).get_path())

    def test_837i_2420a(self):

        walker = walk_tree()
        param = pyx12.params.params()

        cmap = pyx12.map_if.load_map_file(
            '837Q3.I.5010.X223.A1.xml', self.param)
        errh = pyx12.error_handler.errh_null()
        path = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/DTP'
        node = cmap.getnodebypath(path)
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.Segment(
            'NM1*72*1*TEST*BAR****XX*9999974756~', '~', '*', ':')
        (node, pop, push) = walker.walk(node, seg_data, errh, 5, 4, None)
        self.assertNotEqual(node, None, 'walker failed to find %s' % (seg_data))
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(errh.err_cde, None, errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), ['2420A'])

    def test_999_2110_IK4(self):
        walker = walk_tree()
        param = pyx12.params.params()

        cmap = pyx12.map_if.load_map_file('999.5010.xml', self.param)
        errh = pyx12.error_handler.errh_null()
        path = '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/2000/2100/IK3'
        node = cmap.getnodebypath(path)
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        #node.cur_count = 1
        walker.setCountState({node.parent.x12path: 1, node.x12path: 1})
        seg_data = pyx12.segment.Segment('IK4*3*116*7*88888-8888~', '~', '*', ':')
        errh.reset()
        (node, pop, push) = walker.walk(node, seg_data, errh, seg_count=8, cur_line=7, ls_id=None)
        self.assertNotEqual(node, None, 'walker failed to find %s' % (seg_data))
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(errh.err_cde, None, errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), ['2110'])

    def tearDown(self):
        del self.errh
        del self.map
        del self.walker


class SegmentWalk(unittest.TestCase):

    def setUp(self):

        self.walker = walk_tree()
        self.param = pyx12.params.params()

        self.map = pyx12.map_if.load_map_file(
            '837.4010.X098.A1.xml', self.param)
        self.errh = pyx12.error_handler.errh_null()

    def test_match_regular_segment(self):
        self.errh.reset()
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2010AB/NM1')
        seg_data = pyx12.segment.Segment('N4*Billings*MT*56123', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])

    def test_match_ID_segment1(self):
        self.errh.reset()
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        seg_data = pyx12.segment.Segment('DTP*454*D8*20040101', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])

    def test_segment_required_fail1(self):
        """
        Skipped required segment
        """
        self.errh.reset()
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2010AA/NM1')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.Segment('N4*NOWHERE*MA*30001~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, '3', self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])

    def test_found_unused_segment1(self):
        self.errh.reset()
        cmap = pyx12.map_if.load_map_file('comp_test.xml', self.param)
        node = cmap.getnodebypath('/TST')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        #node.cur_count = 1
        self.walker.setCountState({node.x12path: 1})
        seg_data = pyx12.segment.Segment('UNU*AA*B~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        #result = node.is_valid(comp, self.errh)
        #self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, '2', self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])

    def tearDown(self):
        del self.errh
        del self.map
        del self.walker


class SegmentWalk278(unittest.TestCase):

    def setUp(self):

        self.walker = walk_tree()
        self.param = pyx12.params.params()

        self.map = pyx12.map_if.load_map_file(
            '278.4010.X094.A1.xml', self.param)
        self.errh = pyx12.error_handler.errh_null()

    def test_match_regular_segment(self):
        self.errh.reset()
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2000C/2000E/2000F/DTP')
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.Segment('HI*BO:T1017::::382', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(
            node, None, 'Segment not found: %s' % (seg_data.format()))
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])


class Segment_ID_Checks(unittest.TestCase):

    def setUp(self):

        self.walker = walk_tree()
        param = pyx12.params.params()

        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()
        self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/ST')

    def test_segment_id_short(self):
        self.errh.reset()
        node = self.node
        seg_data = pyx12.segment.Segment('Z*0019', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(node, None)
        self.assertEqual(self.errh.err_cde, '1', self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])

    def test_segment_id_long(self):
        self.errh.reset()
        node = self.node
        seg_data = pyx12.segment.Segment('ZZZZ*0019', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(node, None)
        self.assertEqual(self.errh.err_cde, '1', self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])


class Counting(unittest.TestCase):

    def setUp(self):

        self.walker = walk_tree()
        param = pyx12.params.params()

        self.map = pyx12.map_if.load_map_file('270.4010.X092.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()
        #self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2100B/N4')
        self.node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2100B/NM1')
        #self.node.parent.cur_count = 1  # Loop 2100B
        self.countState = {
            self.node.parent.x12path: 1,
            self.node.x12path: 1,
        }
        #self.node.cur_count = 1
        self.node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2100B/PER')
        self.assertNotEqual(self.node, None)
        self.countState[self.node.x12path] = 1

    def test_count_ok1(self):
        self.errh.reset()
        node = self.node
        #node.cur_count = 1
        self.walker.setCountState(self.countState)
        seg_data = pyx12.segment.Segment('PER*IC*Name1*EM*dev@null.com~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_count_ok2(self):
        self.errh.reset()
        node = self.node
        #node.cur_count = 2
        countState = {
            self.node.parent.x12path: 1,
            self.node.x12path: 2,
        }
        self.walker.setCountState(countState)
        seg_data = pyx12.segment.Segment('PER*IC*Name1*EM*dev@null.com~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_count_fail1(self):
        self.errh.reset()
        node = self.node
        #node.cur_count = 3
        self.walker.setCountState(self.countState)
        #self.walker.counter.increment(node.x12path)
        #self.walker.counter.increment(node.x12path)
        self.walker.counter.setCount(node.x12path, 3)
        seg_data = pyx12.segment.Segment('PER*IC*Name1*EM*dev@null.com~', '~', '*', ':')
        self.assertNotEqual(node, None, 'Node not found')
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, '5', self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])


class LoopCounting(unittest.TestCase):

    def setUp(self):
        initialCounts = {}
        self.walker = walk_tree(initialCounts)
        param = pyx12.params.params()

        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_max_loop_count_ok1(self):
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400')
        self.assertNotEqual(node, None, 'Node not found')
        self.walker.setCountState({
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400': 48,
        })
        #node.cur_count = 48
        self.errh.reset()
        seg_data = pyx12.segment.Segment('LX*51~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), ['2400'])
        self.assertEqual(get_id_list(push), ['2400'])

    def test_max_loop_count_fail1(self):
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400')
        self.assertNotEqual(node, None, 'Node not found')
        self.walker.setCountState({
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400': 50,
        })
        #node.cur_count = 50
        seg_data = pyx12.segment.Segment('LX*51~', '~', '*', ':')
        self.errh.reset()
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, '4', self.errh.err_str)
        self.assertEqual(get_id_list(pop), ['2400'])
        self.assertEqual(get_id_list(push), ['2400'])


class CountOrdinal(unittest.TestCase):

    def setUp(self):
        initialCounts = {
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000': 1,
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS': 1,
        }
        self.walker = walk_tree(initialCounts)
        param = pyx12.params.params()

        self.map = pyx12.map_if.load_map_file('834.5010.X220.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()
        #self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2100B/N4')
        self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
        self.assertNotEqual(self.node, None)
        #self.node.parent.cur_count = 1  # Loop 2000
        #self.node.cur_count = 1  # INS

    def test_ord_ok1(self):
        self.errh.reset()
        node = self.node
        seg_data = pyx12.segment.Segment('REF*0F*1234~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])
        self.errh.reset()
        seg_data = pyx12.segment.Segment('REF*1L*91234~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])

    def test_ord_ok2(self):
        self.errh.reset()
        node = self.node
        seg_data = pyx12.segment.Segment('REF*0F*1234~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])
        self.errh.reset()
        seg_data = pyx12.segment.Segment('REF*17*A232~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])

    def test_ord_ok3(self):
        self.errh.reset()
        node = self.node
        seg_data = pyx12.segment.Segment('REF*17*1234~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])
        self.errh.reset()
        seg_data = pyx12.segment.Segment('REF*0F*A232~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])

    def test_ord_bad1(self):
        self.errh.reset()
        node = self.node
        seg_data = pyx12.segment.Segment('REF*0F*1234~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])
        self.errh.reset()
        seg_data = pyx12.segment.Segment('DTP*297*D8*20040101~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])
        self.errh.reset()
        seg_data = pyx12.segment.Segment('REF*17*A232~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertEqual(self.errh.err_cde, '1', self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])

    def test_lui_ok(self):
        self.errh.reset()
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100A/NM1')
        #node.parent.cur_count = 1  # Loop 2100A
        #node.cur_count = 1  # NM1
        self.walker.setCountState({
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100A': 1,
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100A/NM1': 1,
        })
        self.assertNotEqual(node, None)
        seg_data = pyx12.segment.Segment('LUI***ES~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])


class LoopPathPopPush837(unittest.TestCase):

    def setUp(self):

        self.walker = walk_tree()
        param = pyx12.params.params()

        self.errh = pyx12.error_handler.errh_null()
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)

    def test_path_sub_loop(self):
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/HI')
        seg_data = pyx12.segment.Segment(
            'NM1*82*2*Provider Name*****XX*24423423~', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), ['2310B'])

    def test_path_up3(self):
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/2430/SVD')
        seg_data = pyx12.segment.Segment('LX*2', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), ['2430', '2400'])
        self.assertEqual(get_id_list(push), ['2400'])


class LoopPathPopPush834(unittest.TestCase):

    def setUp(self):

        self.walker = walk_tree()
        param = pyx12.params.params()

        self.map = pyx12.map_if.load_map_file('834.5010.X220.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_path_same_repeat(self):
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
        seg_data = pyx12.segment.Segment('INS*Y*18*030*20*A', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), ['2000'])
        self.assertEqual(get_id_list(push), ['2000'])

    def test_path_in(self):
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
        seg_data = pyx12.segment.Segment('DTP*356*D8*20080101', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])

    def test_path_repeat(self):
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/DTP')
        seg_data = pyx12.segment.Segment('INS*Y*18*030*20*A', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), ['2000'])
        self.assertEqual(get_id_list(push), ['2000'])

    def test_path_up(self):
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100A/NM1')
        seg_data = pyx12.segment.Segment('ST*834*11', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(
            get_id_list(pop), ['2100A', '2000', 'DETAIL', 'ST_LOOP'])
        self.assertEqual(get_id_list(push), ['ST_LOOP'])

    def test_path_up2(self):
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
        seg_data = pyx12.segment.Segment('GS*BE*AAA*BBB*20081116*2044*328190001*X*004010X095A1', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(
            pop), ['2000', 'DETAIL', 'ST_LOOP', 'GS_LOOP'])
        self.assertEqual(get_id_list(push), ['GS_LOOP'])

    def test_path_in2(self):
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/INS')
        seg_data = pyx12.segment.Segment('DTP*356*D8*20080203', '~', '*', ':')
        (node, pop, push) = self.walker.walk(
            node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), [])


class Bug837i(unittest.TestCase):
    def setUp(self):
        self.walker = walk_tree()
        self.param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file('837Q3.I.5010.X223.A1.xml', self.param)
        self.errh = pyx12.error_handler.errh_null()

    def testWalk2420A(self):
        mpath = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400'
        node = self.map.getnodebypath(mpath)
        self.assertNotEqual(node, None, 'Path %s not found' % (mpath))
        #start_node = node
        self.assertEqual(node.base_name, 'loop')
        #node.cur_count = 1
        self.walker.setCountState({node.x12path: 1})
        seg_data = pyx12.segment.Segment('NM1*72*1*TEST*USER****XX*9107999999~', '~', '*', ':')
        #self.errh.reset()
        (node, pop, push) = self.walker.walk(node, seg_data, self.errh, 5, 4, None)
        self.assertNotEqual(node, None)
        self.assertEqual(seg_data.get_seg_id(), node.id)
        #self.assertEqual(self.errh.err_cde, None, self.errh.err_str)
        self.assertEqual(get_id_list(pop), [])
        self.assertEqual(get_id_list(push), ['2420A'])
        #self.assertEqual(traverse_path(start_node, pop, push), pop_to_parent_loop(node).get_path())

    def tearDown(self):
        del self.errh
        del self.map
        del self.walker
