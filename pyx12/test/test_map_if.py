import unittest

import pyx12.error_handler
import pyx12.map_if
import pyx12.params
import pyx12.path
import pyx12.segment


class ElementIsValidDate(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file('837Q3.I.5010.X223.A1.xml', param)
        self.node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300')
        # 1 096 TM, 2 434 RD8 & D8
        self.errh = pyx12.error_handler.errh_null()

    def test_date_bad1(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.Segment('DTP*434*D8*20041340~', '~', '*', ':')
        #node = self.node.get_child_node_by_idx(2)
        node = self.node.getnodebypath('DTP[434]')
        result = node.is_valid(seg_data, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '8')

    def test_date_ok1(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.Segment('DTP*435*D8*20040110~', '~', '*', ':')
        #node = self.node.get_child_node_by_idx(2)
        node = self.node.getnodebypath('DTP[435]')
        result = node.is_valid(seg_data, self.errh)
        self.assertTrue(result, '%s should be valid' % (seg_data.format()))
        self.assertEqual(self.errh.err_cde, None)

    def test_time_bad1(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.Segment('DTP*096*TM*2577~', '~', '*', ':')
        #node = self.node.get_child_node_by_idx(1)
        node = self.node.getnodebypath('DTP[096]')
        result = node.is_valid(seg_data, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '9')

    def test_time_ok1(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.Segment('DTP*096*TM*1215~', '~', '*', ':')
        #node = self.node.get_child_node_by_idx(1)
        node = self.node.getnodebypath('DTP[096]')
        result = node.is_valid(seg_data, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_date_1251_ok1(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.Segment('DMG*D8*20040110*M~', '~', '*', ':')
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2010BA/DMG')
        self.assertNotEqual(node, None)
        (is_match, qual_code, matched_ele_idx, matched_subele_idx) = node.is_match_qual(seg_data, 'DMG', None)
        self.assertTrue(is_match)
        result = node.is_valid(seg_data, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_date_1251_bad1(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.Segment('DMG*D8*20042110*M~', '~', '*', ':')
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2010BA/DMG')
        self.assertNotEqual(node, None)
        result = node.is_valid(seg_data, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '8')

    def test_date_1251_bad2(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.Segment(
            'DMG*D8*20040109-20040110*M~', '~', '*', ':')
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2010BA/DMG')
        self.assertNotEqual(node, None)
        result = node.is_valid(seg_data, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '8')

    def test_date_1251_ok2(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.Segment(
            'DTP*434*RD8*20110101-20110220~', '~', '*', ':')
        seg_path = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/DTP[434]'
        node = self.map.getnodebypath(seg_path)
        self.assertNotEqual(node, None)
        result = node.is_valid(seg_data, self.errh)
        self.assertTrue(result, self.errh.err_str)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)


class SegmentIsValid(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file(
            '837Q3.I.5010.X223.A1.xml', param)
        self.node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300')
        self.errh = pyx12.error_handler.errh_null()

    def test_segment_length(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.Segment(
            'DTP*435*D8*20040101*R~', '~', '*', ':')
        #node = self.node.get_child_node_by_idx(2)
        node = self.node.getnodebypath('DTP[435]')
        result = node.is_valid(seg_data, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '3', self.errh.err_str)


class ElementIsValid(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file('837.5010.X222.A1.xml', param)
        self.node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        self.errh = pyx12.error_handler.errh_null()

    def test_len_ID(self):
        node = self.node.get_child_node_by_idx(11)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM12')
        self.assertEqual(node.base_name, 'element')

        #elem = pyx12.segment.Element('1')
        #result = node.is_valid(elem, self.errh)
        #self.assertFalse(result)
        #self.assertEqual(self.errh.err_cde, '4')

        self.errh.err_cde = None
        elem = pyx12.segment.Element('02')
        result = node.is_valid(elem, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

        #self.errh.err_cde = None
        #elem = pyx12.segment.Element('01010')
        #result = node.is_valid(elem, self.errh)
        #self.assertFalse(result)
        #self.assertEqual(self.errh.err_cde, '5')

    def test_len_R(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(1)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM02')
        self.assertEqual(node.base_name, 'element')

        self.errh.err_cde = None
        elem = pyx12.segment.Element('-5.2344')
        result = node.is_valid(elem, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

        self.errh.err_cde = None
        elem = pyx12.segment.Element('-5.23442673245673345')
        result = node.is_valid(elem, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

        self.errh.err_cde = None
        elem = pyx12.segment.Element('-5.234426732456733454')
        result = node.is_valid(elem, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '5')

    def test_bad_char_R(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(1)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM02')
        self.assertEqual(node.base_name, 'element')

        self.errh.err_cde = None
        elem = pyx12.segment.Element('-5.AB4')
        result = node.is_valid(elem, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '6')

    #def test_bad_char_DT(self):
    #    node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/2000A/2000B/2300/DTP')
    #    node = self.node.get_child_node_by_idx(2)
    #    self.assertNotEqual(node, None)
    #    self.assertEqual(node.id, 'DTP03')
    #    self.assertEqual(node.base_name, 'element')

    #    result = node.is_valid('2003010Z', self.errh)
    #    self.assertFalse(result)
    #    self.assertEqual(self.errh.err_cde, '6')

    def test_valid_codes_ok1(self):
        #CLM05-01   02 bad, 11 good, no external
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(4)  # CLM05
        node = node.get_child_node_by_idx(0)  # CLM05-1
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM05-01')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.Element('11')
        result = node.is_valid(elem, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_valid_codes_bad1(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(4)  # CLM05
        node = node.get_child_node_by_idx(0)  # CLM05-1
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM05-01')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.Element('AA')
        self.assertFalse(node.is_valid(elem, self.errh))
        self.assertEqual(self.errh.err_cde, '7')

    def test_valid_codes_bad_spaces(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/SV1')
        node = node.get_child_node_by_idx(0)  # SV101
        node = node.get_child_node_by_idx(0)  # SV101-1
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'SV101-01')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.Element('  ')
        result = node.is_valid(elem, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '7')

    def test_external_codes_ok1(self):
        self.errh.err_cde = None
        #CLM11-04 external states, no valid_codes
        node = self.node.get_child_node_by_idx(10)  # CLM11
        node = node.get_child_node_by_idx(3)  # CLM11-4
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM11-04')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.Element('MI')
        self.assertTrue(node.is_valid(
            elem, self.errh), 'Error Code: %s' % (self.errh.err_cde))
        self.assertEqual(self.errh.err_cde, None)

    def test_external_codes_bad1(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(10)  # CLM11
        node = node.get_child_node_by_idx(3)  # CLM11-4
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM11-04')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.Element('NA')
        self.assertFalse(node.is_valid(elem, self.errh))
        self.assertEqual(self.errh.err_cde, '7')

    def test_bad_passed_comp_to_ele_node(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        comp = pyx12.segment.Composite('NA::1', ':')
        result = node.is_valid(comp, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '6')

    def test_null_N(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(2)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM03')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid(None, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_blank_N(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(2)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM03')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.Element('')
        result = node.is_valid(elem, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_null_S(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(9)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM10')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid(None, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_blank_S(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(9)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM10')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.Element('')
        result = node.is_valid(elem, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_null_R(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid(None, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '1')

    def test_blank_R(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.Element('')
        result = node.is_valid(elem, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '1')


class GetNodeByPath(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file(
            '837.4010.X098.A1.xml', self.param)

    def test_get_ISA(self):
        path = '/ISA_LOOP/ISA'
        node = self.map.getnodebypath(path)
        self.assertEqual(node.id, 'ISA')
        self.assertEqual(node.get_path(), path)
        self.assertEqual(node.base_name, 'segment')

    def test_get_GS(self):
        path = '/ISA_LOOP/GS_LOOP/GS'
        node = self.map.getnodebypath(path)
        self.assertEqual(node.id, 'GS')
        self.assertEqual(node.get_path(), path)
        self.assertEqual(node.base_name, 'segment')

    def test_get_ST(self):
        path = '/ISA_LOOP/GS_LOOP/ST_LOOP/ST'
        node = self.map.getnodebypath(path)
        self.assertEqual(node.id, 'ST')
        self.assertEqual(node.get_path(), path)
        self.assertEqual(node.base_name, 'segment')

    def test_get_1000A(self):
        path = '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A'
        node = self.map.getnodebypath(path)
        self.assertEqual(node.id, '1000A')
        self.assertEqual(node.get_path(), path)
        self.assertEqual(node.base_name, 'loop')

    def test_get_2000A(self):
        path = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A'
        node = self.map.getnodebypath(path)
        self.assertEqual(node.id, '2000A')
        self.assertEqual(node.get_path(), path)
        self.assertEqual(node.base_name, 'loop')

    def test_get_2000B(self):
        #pdb.set_trace()
        path = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B'
        node = self.map.getnodebypath(path)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, '2000B')
        self.assertEqual(node.get_path(), path)
        self.assertEqual(node.base_name, 'loop')

    def test_get_2300(self):
        path = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300'
        node = self.map.getnodebypath(path)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, '2300')
        self.assertEqual(node.get_path(), path)
        self.assertEqual(node.base_name, 'loop')

    def test_get_2300_CLM(self):
        path = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM'
        node = self.map.getnodebypath(path)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM')
        self.assertEqual(node.get_path(), path)
        self.assertEqual(node.base_name, 'segment')

    def test_get_TST(self):
        path = '/TST'
        map = pyx12.map_if.load_map_file('comp_test.xml', self.param)
        node = map.getnodebypath(path)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'TST')
        self.assertEqual(node.get_path(), path)

    def tearDown(self):
        del self.map


class CompositeRequirement(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file(
            '837.4010.X098.A1.xml', self.param)
        self.errh = pyx12.error_handler.errh_null()

    def test_comp_required_ok1(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(4)
        self.assertNotEqual(node, None)
        #self.assertEqual(node.id, 'CLM05', node.id)
        self.assertEqual(node.base_name, 'composite')
        comp = pyx12.segment.Composite('03::1', ':')
        result = node.is_valid(comp, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_comp_required_ok2(self):
        self.errh.err_cde = None
        map = pyx12.map_if.load_map_file('comp_test.xml', self.param)
        node = map.getnodebypath('/TST')
        self.assertNotEqual(node, None)
        node = node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'composite')
        comp = pyx12.segment.Composite('::1', ':')
        result = node.is_valid(comp, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_comp_S_sub_R_ok3(self):
        self.errh.err_cde = None
        map = pyx12.map_if.load_map_file(
            '837Q3.I.5010.X223.A1.xml', self.param)
        node = map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/SV2')
        node = node.get_child_node_by_idx(1)  # SV202
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'composite')
        #self.assertEqual(node.id, 'SV202')
        comp = pyx12.segment.Composite('', ':')
        result = node.is_valid(comp, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_comp_required_fail1(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(4)
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'composite')
        comp = pyx12.segment.Composite('', ':')
        result = node.is_valid(comp, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '2')

    def test_comp_not_used_fail1(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'REF')
        self.assertEqual(
            node.get_path(), '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF')
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.Segment(
            'REF*87*004010X098A1**:1~', '~', '*', ':')
        result = node.is_valid(seg_data, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '5')


class TrailingSpaces(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_trailing_ID_ok(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/ISA')
        node = node.get_child_node_by_idx(5)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'ISA06')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.Element('TEST           ')
        result = node.is_valid(elem, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_no_trailing_AN_ok(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.Element('TEST')
        result = node.is_valid(elem, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_trailing_AN_bad(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.Element('TEST     ')
        result = node.is_valid(elem, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '6', self.errh.err_str)


class ElementRequirement(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_ele_not_used_fail1(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'REF')
        self.assertEqual(
            node.get_path(), '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF')
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.Segment(
            'REF*87*004010X098A1*Description*~', '~', '*', ':')
        result = node.is_valid(seg_data, self.errh)
        self.assertFalse(result)
        self.assertEqual(self.errh.err_cde, '10')

    def test_ele_required_ok1(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(1)
        self.assertNotEqual(node, None)
        #self.assertEqual(node.id, 'CLM05', node.id)
        self.assertEqual(node.base_name, 'element')
        ele_data = pyx12.segment.Element('0398090')
        result = node.is_valid(ele_data, self.errh)
        self.assertTrue(result)
        self.assertEqual(self.errh.err_cde, None)


class NodeEquality(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_eq_1(self):
        self.errh.err_cde = None
        node1 = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300')
        self.assertNotEqual(node1, None)
        node2 = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300')
        self.assertNotEqual(node2, None)
        self.assertTrue(node1 == node2)

    def test_neq_1(self):
        self.errh.err_cde = None
        node1 = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300')
        self.assertNotEqual(node1, None)
        node2 = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400')
        self.assertNotEqual(node2, None)
        self.assertFalse(node1 == node2)


class LoopIsMatch(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file(
            '837Q3.I.5010.X223.A1.xml', param)
        self.node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300')
        self.errh = pyx12.error_handler.errh_null()

    def test_match_self(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.Segment('CLM*657657*AA**5::1~', '~', '*', ':')
        self.assertTrue(self.node.is_match(seg_data))


class GetNodeBySegment(unittest.TestCase):
    """
    Find matching child nodes matching a segment
    """
    def setUp(self):
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file('834.5010.X220.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_get_seg_node(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, '2000')
        seg_data = pyx12.segment.Segment('INS*Y*18*030*20*A', '~', '*', ':')
        seg_node = node.get_child_seg_node(seg_data)
        (is_match, qual_code, matched_ele_idx, matched_subele_idx) = seg_node.is_match_qual(seg_data, 'INS', None)
        self.assertTrue(is_match)
        self.assertNotEqual(seg_node, None)
        self.assertEqual(seg_node.id, 'INS')

    def test_get_loop_node(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, '2000')
        seg_data = pyx12.segment.Segment(
            'NM1*IL*1*User*Test****ZZ*XX1234', '~', '*', ':')
        loop_node = node.get_child_loop_node(seg_data)
        self.assertNotEqual(loop_node, None)
        self.assertEqual(loop_node.id, '2100A')

    def test_get_seg_node_fail(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, '2000')
        seg_data = pyx12.segment.Segment('CLM*657657*AA**5::1~', '~', '*', ':')
        seg_node = node.get_child_seg_node(seg_data)
        self.assertEqual(seg_node, None)

    def test_get_loop_node_fail(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, '2000')
        seg_data = pyx12.segment.Segment('INS*Y*18*030*20*A', '~', '*', ':')
        loop_node = node.get_child_loop_node(seg_data)
        self.assertEqual(loop_node, None)


class MatchSegmentQual(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file(
            '837Q3.I.5010.X223.A1.xml', param)
        self.node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300')
        self.errh = pyx12.error_handler.errh_null()

    def test_match_plain_ok1(self):
        self.errh.err_cde = None
        node = self.node.getnodebypath('CLM')
        seg_data = pyx12.segment.Segment('CLM*Y', '~', '*', ':')
        (is_match, qual_code, matched_ele_idx, matched_subele_idx) = node.is_match_qual(seg_data, 'CLM', None)
        self.assertTrue(is_match)

    def test_match_qual_ok1(self):
        self.errh.err_cde = None
        node = self.node.getnodebypath('DTP[435]')
        seg_data = pyx12.segment.Segment('DTP*435*D8*20090101~', '~', '*', ':')
        (is_match, qual_code, matched_ele_idx, matched_subele_idx) = node.is_match_qual(seg_data, 'DTP', '435')
        self.assertTrue(is_match)

    def test_match_qual_ok2(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath(
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2010AA/REF')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'REF')
        self.assertEqual(node.get_path(
        ), '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2010AA/REF')
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.Segment('REF*EI*5555~', '~', '*', ':')
        (is_match, qual_code, matched_ele_idx, matched_subele_idx) = node.is_match_qual(seg_data, 'REF', 'EI')
        self.assertTrue(is_match)


class X12Path(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)

    def test_837_paths(self):
        paths = [
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/REF[4N]',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/SV1'
        ]
        for p1 in paths:
            node = self.map.getnodebypath(p1)
            self.assertEqual(p1, node.get_path())
            self.assertEqual(pyx12.path.X12Path(p1), node.x12path)


class X12Version(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()

    def test_4010(self):
        map = pyx12.map_if.load_map_file('834.4010.X095.A1.xml', self.param)
        self.assertEqual(map.icvn, '00401')

    def test_5010(self):
        map = pyx12.map_if.load_map_file('834.5010.X220.A1.xml', self.param)
        self.assertEqual(map.icvn, '00501')


class SegmentChildrenOrdinal(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file('999.5010.xml', param)

    def test_check_ord_ok(self):
        mypath = '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/2000/2100/CTX'
        self.node = self.map.getnodebypath(mypath)
        #errh = pyx12.error_handler.errh_null()
        i = 1
        for c in self.node.children:
            self.assertEqual(i, c.seq)
            i += 1

    def test_check_ord_ok2(self):
        mypath = '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/2000/2100/IK3'
        self.node = self.map.getnodebypath(mypath)
        i = 1
        for c in self.node.children:
            self.assertEqual(i, c.seq)
            i += 1


class SegmentChildrenOrdinalMapPath(unittest.TestCase):
    def setUp(self):
        import os.path
        param = pyx12.params.params()
        map_path = os.path.join(os.path.dirname(pyx12.codes.__file__), 'map')
        self.map = pyx12.map_if.load_map_file('999.5010.xml', param, map_path)

    def test_check_ord_ok(self):
        mypath = '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/2000/2100/CTX'
        self.node = self.map.getnodebypath(mypath)
        #errh = pyx12.error_handler.errh_null()
        i = 1
        for c in self.node.children:
            self.assertEqual(i, c.seq)
            i += 1

    def test_check_ord_ok2(self):
        mypath = '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/2000/2100/IK3'
        self.node = self.map.getnodebypath(mypath)
        i = 1
        for c in self.node.children:
            self.assertEqual(i, c.seq)
            i += 1


class GetCompositeNodeByPath(unittest.TestCase):
    """
    Find matching child nodes matching a segment
    """
    def setUp(self):
        param = pyx12.params.params()
        self.map = pyx12.map_if.load_map_file('277.5010.X214.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_get_segment_node_absolute(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath2('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2200B/STC02')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'STC02')

    def test_get_composite_node_absolute(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath2('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2200B/STC01-01')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'STC01-01')

    def test_get_segment_node_relative(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath2('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2200B')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, '2200B')
        node2 = node.getnodebypath2('STC02')
        self.assertNotEqual(node2, None)
        self.assertEqual(node2.id, 'STC02')

    def test_get_composite_node(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath2('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2200B/STC02')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'STC02')

    def test_get_node_path_refdes(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath2('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2200B/STC02')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'STC02')
        refdes = 'STC02'
        newnode = node.parent.getnodebypath2(refdes)
        self.assertEqual(newnode.get_path(), '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2200B/STC02')

    def test_get_composite_node_path_refdes(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath2('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2200B/STC01-01')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'STC01-01')
        refdes = 'STC01-01'
        newnode = node.parent.parent.getnodebypath2(refdes)
        self.assertEqual(newnode.get_path(), '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2200B/STC01-01')
