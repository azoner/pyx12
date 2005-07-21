#! /usr/bin/env /usr/local/bin/python

import os, os.path, sys
import string
import unittest
#import pdb

import pyx12.error_handler
from pyx12.errors import *
import pyx12.map_if
import pyx12.params 
import pyx12.segment

class ElementIsValidDate(unittest.TestCase):
    """
    """
    def setUp(self):
        param = pyx12.params.params('pyx12.conf.xml')
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X096.A1.xml', param)
        self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300')
        # 1 096 TM, 2 434 RD8 & D8
        self.errh = pyx12.error_handler.errh_null()

    def test_date_bad1(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.segment('DTP*434*D8*20041340~', '~', '*', ':')
        #node = self.node.get_child_node_by_idx(2) 
        node = self.node.getnodebypath('DTP[434]')
        result = node.is_valid(seg_data, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '8')

    def test_date_ok1(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.segment('DTP*434*D8*20040110~', '~', '*', ':')
        #node = self.node.get_child_node_by_idx(2) 
        node = self.node.getnodebypath('DTP[434]')
        result = node.is_valid(seg_data, self.errh)
        self.failUnless(result, '%s should be valid' % (seg_data.format()))
        self.assertEqual(self.errh.err_cde, None)

    def test_time_bad1(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.segment('DTP*096*TM*2577~', '~', '*', ':')
        #node = self.node.get_child_node_by_idx(1) 
        node = self.node.getnodebypath('DTP[096]')
        result = node.is_valid(seg_data, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '9')

    def test_time_ok1(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.segment('DTP*096*TM*1215~', '~', '*', ':')
        #node = self.node.get_child_node_by_idx(1) 
        node = self.node.getnodebypath('DTP[096]')
        result = node.is_valid(seg_data, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_date_1251_ok1(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.segment('DMG*D8*20040110*M~', '~', '*', ':')
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2010BA/DMG')
        self.assertNotEqual(node, None)
        result = node.is_valid(seg_data, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_date_1251_bad1(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.segment('DMG*D8*20042110*M~', '~', '*', ':')
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2010BA/DMG')
        self.assertNotEqual(node, None)
        result = node.is_valid(seg_data, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '8')

    def test_date_1251_bad2(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.segment('DMG*D8*20040109-20040110*M~', '~', '*', ':')
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2010BA/DMG')
        self.assertNotEqual(node, None)
        result = node.is_valid(seg_data, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '8')

    def test_date_1251_ok2(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.segment('CR6*4*20050204*RD8*20050101-20050220*20050104*N*N*I*********D~', '~', '*', ':')
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CR6')
        self.assertNotEqual(node, None)
        result = node.is_valid(seg_data, self.errh)
        self.failUnless(result, self.errh.err_str)
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)


class SegmentIsValid(unittest.TestCase):
    """
    """
    def setUp(self):
        param = pyx12.params.params('pyx12.conf.xml')
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X096.A1.xml', param)
        self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300')
        self.errh = pyx12.error_handler.errh_null()

    def test_segment_length(self):
        self.errh.err_cde = None
        seg_data = pyx12.segment.segment('DTP*434*D8*20040101*R~', '~', '*', ':')
        #node = self.node.get_child_node_by_idx(2) 
        node = self.node.getnodebypath('DTP[434]')
        result = node.is_valid(seg_data, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '3', self.errh.err_str)


class ElementIsValid(unittest.TestCase):
    """
    """
    def setUp(self):
        param = pyx12.params.params('pyx12.conf.xml')
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        self.errh = pyx12.error_handler.errh_null()

    def test_len_ID(self):
        node = self.node.get_child_node_by_idx(11)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM12')
        self.assertEqual(node.base_name, 'element')

        #elem = pyx12.segment.element('1')
        #result = node.is_valid(elem, self.errh)
        #self.failIf(result)
        #self.assertEqual(self.errh.err_cde, '4')

        self.errh.err_cde = None
        elem = pyx12.segment.element('01')
        result = node.is_valid(elem, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

        #self.errh.err_cde = None
        #elem = pyx12.segment.element('01010')
        #result = node.is_valid(elem, self.errh)
        #self.failIf(result)
        #self.assertEqual(self.errh.err_cde, '5')

    def test_len_R(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(1)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM02')
        self.assertEqual(node.base_name, 'element')

        self.errh.err_cde = None
        elem = pyx12.segment.element('-5.2344')
        result = node.is_valid(elem, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

        self.errh.err_cde = None
        elem = pyx12.segment.element('-5.23442673245673345')
        result = node.is_valid(elem, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

        self.errh.err_cde = None
        elem = pyx12.segment.element('-5.234426732456733454')
        result = node.is_valid(elem, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '5')

    def test_bad_char_R(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(1)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM02')
        self.assertEqual(node.base_name, 'element')

        self.errh.err_cde = None
        elem = pyx12.segment.element('-5.AB4')
        result = node.is_valid(elem, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '6')
        
    #def test_bad_char_DT(self):
    #    node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/2000A/2000B/2300/DTP')
    #    node = self.node.get_child_node_by_idx(2)
    #    self.assertNotEqual(node, None)
    #    self.assertEqual(node.id, 'DTP03')
    #    self.assertEqual(node.base_name, 'element')

    #    result = node.is_valid('2003010Z', self.errh)
    #    self.failIf(result)
    #    self.assertEqual(self.errh.err_cde, '6')

    def test_valid_codes_ok1(self):
        #CLM05-01   02 bad, 11 good, no external
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(4) #CLM05
        node = node.get_child_node_by_idx(0) #CLM05-1
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM05-01')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.element('11')
        result = node.is_valid(elem, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)
        
    def test_valid_codes_bad1(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(4) #CLM05
        node = node.get_child_node_by_idx(0) #CLM05-1
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM05-01')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.element('02')
        result = node.is_valid(elem, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '7')

    def test_valid_codes_bad_spaces(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/SV1')
        node = node.get_child_node_by_idx(0) #SV101
        node = node.get_child_node_by_idx(0) # SV101-1
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'SV101-01')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.element('  ')
        result = node.is_valid(elem, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '7')

    def test_external_codes_ok1(self):
        self.errh.err_cde = None
        #CLM11-04 external states, no valid_codes
        node = self.node.get_child_node_by_idx(10) #CLM11
        node = node.get_child_node_by_idx(3) #CLM11-4
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM11-04')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.element('MI')
        result = node.is_valid(elem, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)
        
    def test_external_codes_bad1(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(10) #CLM11
        node = node.get_child_node_by_idx(3) #CLM11-4
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM11-04')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.element('NA')
        result = node.is_valid(elem, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '7')

    def test_bad_passed_comp_to_ele_node(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        comp = pyx12.segment.composite('NA::1', ':')
        result = node.is_valid(comp, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '6')

    def test_null_N(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(2)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM03')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid(None, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)
        
    def test_blank_N(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(2)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM03')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.element('')
        result = node.is_valid(elem, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)
        
    def test_null_S(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(9)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM10')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid(None, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)
        
    def test_blank_S(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(9)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM10')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.element('')
        result = node.is_valid(elem, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)
         
    def test_null_R(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid(None, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '1')
        
    def test_blank_R(self):
        self.errh.err_cde = None
        node = self.node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.element('')
        result = node.is_valid(elem, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '1')
        

class GetNodeByPath(unittest.TestCase):
    """
    """
    def setUp(self):
        param = pyx12.params.params('pyx12.conf.xml')
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)

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

#    def test_get_by_id(self):
#        path = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/DTP[435]'
#        node = self.map.getnodebypath(path)
#        self.assertNotEqual(node, None)
#        self.assertEqual(node.id, 'DTP')
#        self.assertEqual(node.get_path(), path)
#        self.assertEqual(node.base_name, 'segment')

    def test_get_TST(self):
        path = '/TST'
        param = pyx12.params.params('pyx12.conf.xml')
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        map = pyx12.map_if.load_map_file('comp_test.xml', param)
        node = map.getnodebypath(path)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'TST')
        self.assertEqual(node.get_path(), path)

    def tearDown(self):
        del self.map
        

class CompositeRequirement(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params('pyx12.conf.xml')
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_comp_required_ok1(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(4)
        self.assertNotEqual(node, None)
        #self.assertEqual(node.id, 'CLM05', node.id)
        self.assertEqual(node.base_name, 'composite')
        comp = pyx12.segment.composite('03::1', ':')
        result = node.is_valid(comp, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_comp_required_ok2(self):
        self.errh.err_cde = None
        param = pyx12.params.params('pyx12.conf.xml')
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        map = pyx12.map_if.load_map_file('comp_test.xml', param)
        node = map.getnodebypath('/TST')
        self.assertNotEqual(node, None)
        node = node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'composite')
        comp = pyx12.segment.composite('::1', ':')
        result = node.is_valid(comp, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_comp_S_sub_R_ok3(self):
        self.errh.err_cde = None
        param = pyx12.params.params('pyx12.conf.xml')
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        map = pyx12.map_if.load_map_file('837.4010.X096.xml', param)
        node = map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/SV2')
        node = node.get_child_node_by_idx(1) #SV202
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'composite')
        #self.assertEqual(node.id, 'SV202')
        comp = pyx12.segment.composite('', ':')
        result = node.is_valid(comp, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_comp_required_fail1(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(4)
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'composite')
        comp = pyx12.segment.composite('', ':')
        result = node.is_valid(comp, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '2')

#    def test_comp_not_used_ok1(self):

    def test_comp_not_used_fail1(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'REF')
        self.assertEqual(node.get_path(), '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF')
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.segment('REF*87*004010X098A1**:1~', '~', '*', ':')
        result = node.is_valid(seg_data, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '5')


class TrailingSpaces(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params('pyx12.conf.xml')
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_trailing_ID_ok(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/ISA')
        node = node.get_child_node_by_idx(5)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'ISA06')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.element('TEST           ')
        result = node.is_valid(elem, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_no_trailing_AN_ok(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.element('TEST')
        result = node.is_valid(elem, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_trailing_AN_bad(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        elem = pyx12.segment.element('TEST     ')
        result = node.is_valid(elem, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '6', self.errh.err_str)


class ElementRequirement(unittest.TestCase):
    def setUp(self):
        param = pyx12.params.params('pyx12.conf.xml')
        param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
        param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_ele_not_used_fail1(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'REF')
        self.assertEqual(node.get_path(), '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF')
        self.assertEqual(node.base_name, 'segment')
        seg_data = pyx12.segment.segment('REF*87*004010X098A1*Description*~', '~', '*', ':')
        result = node.is_valid(seg_data, self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '5')

    def test_ele_required_ok1(self):
        self.errh.err_cde = None
        node = self.map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(1)
        self.assertNotEqual(node, None)
        #self.assertEqual(node.id, 'CLM05', node.id)
        self.assertEqual(node.base_name, 'element')
        ele_data = pyx12.segment.element('0398090')
        result = node.is_valid(ele_data, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)


def suite(args):
    suite = unittest.TestSuite()
    if args:
        for arg in args:
            if arg == 'GetNodeByPath':
                suite.addTest(unittest.makeSuite(GetNodeByPath))
            elif arg == 'TrailingSpaces':
                suite.addTest(unittest.makeSuite(TrailingSpaces))
            elif arg == 'CompositeRequirement':
                suite.addTest(unittest.makeSuite(CompositeRequirement))
            elif arg == 'ElementRequirement':
                suite.addTest(unittest.makeSuite(ElementRequirement))
            elif arg == 'ElementIsValid':
                suite.addTest(unittest.makeSuite(ElementIsValid))
            elif arg == 'ElementIsValidDate':
                suite.addTest(unittest.makeSuite(ElementIsValidDate))
            elif arg == 'SegmentIsValid':
                suite.addTest(unittest.makeSuite(SegmentIsValid))
    else:
        suite.addTest(unittest.makeSuite(GetNodeByPath))
        suite.addTest(unittest.makeSuite(TrailingSpaces))
        suite.addTest(unittest.makeSuite(CompositeRequirement))
        suite.addTest(unittest.makeSuite(ElementRequirement))
        suite.addTest(unittest.makeSuite(ElementIsValid))
        suite.addTest(unittest.makeSuite(ElementIsValidDate))
        suite.addTest(unittest.makeSuite(SegmentIsValid))
    return suite
                
#if __name__ == "__main__":
#    unittest.main()   
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite(sys.argv[1:]))
