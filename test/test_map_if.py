#! /usr/bin/env /usr/local/bin/python

import os, os.path
import unittest
import pdb

import pyx12.error_handler
from pyx12.errors import *
import pyx12.map_if
from pyx12.params import params

class Element_is_valid(unittest.TestCase):
    """
    """
    def setUp(self):
        param = params()
        param.set_param('map_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.node = self.map.getnodebypath('/2000A/2000B/2300/CLM')
        self.errh = pyx12.error_handler.errh_null()

    def test_valid_codes_ok1(self):
        #CLM05-01   02 bad, 11 good, no external
        node = self.node.get_child_node_by_idx(4) #CLM05
        node = node.get_child_node_by_idx(0) #CLM05-1
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM05-01')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid('11', self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)
        
    def test_valid_codes_bad1(self):
        node = self.node.get_child_node_by_idx(4) #CLM05
        node = node.get_child_node_by_idx(0) #CLM05-1
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM05-01')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid('02', self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '7')

    def test_external_codes_ok1(self):
        "CLM11-04 external states, no valid_codes"
        node = self.node.get_child_node_by_idx(10) #CLM11
        node = node.get_child_node_by_idx(3) #CLM11-4
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM11-04')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid('MI', self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)
        
    def test_external_codes_bad1(self):
        node = self.node.get_child_node_by_idx(10) #CLM11
        node = node.get_child_node_by_idx(3) #CLM11-4
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM11-04')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid('NA', self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '7')

    def test_passed_list_bad(self):
        node = self.node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid(['NA', '', '1'], self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '6')

    def test_null_N(self):
        node = self.node.get_child_node_by_idx(2)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM03')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid(None, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)
        
    def test_blank_N(self):
        node = self.node.get_child_node_by_idx(2)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM03')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid('', self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)
        
    def test_null_S(self):
        node = self.node.get_child_node_by_idx(9)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM10')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid(None, self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)
        
    def test_blank_S(self):
        node = self.node.get_child_node_by_idx(9)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM10')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid('', self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)
        


class Test_getnodebypath(unittest.TestCase):
    """
    """
    def setUp(self):
        param = params()
        param.set_param('map_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)

    def test_get_ISA(self):
        node = self.map.getnodebypath('/ISA')
        self.assertEqual(node.id, 'ISA')
        self.assertEqual(node.base_name, 'segment')

    def test_get_GS(self):
        node = self.map.getnodebypath('/GS')
        self.assertEqual(node.id, 'GS')
        self.assertEqual(node.base_name, 'segment')

    def test_get_ST(self):
        node = self.map.getnodebypath('/ST')
        self.assertEqual(node.id, 'ST')
        self.assertEqual(node.base_name, 'segment')

    def test_get_1000A(self):
        node = self.map.getnodebypath('/1000A')
        self.assertEqual(node.id, '1000A')
        self.assertEqual(node.base_name, 'loop')

    def test_get_2000A(self):
        node = self.map.getnodebypath('/2000A')
        self.assertEqual(node.id, '2000A')
        self.assertEqual(node.base_name, 'loop')

    def test_get_2000B(self):
        #pdb.set_trace()
        node = self.map.getnodebypath('/2000A/2000B')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, '2000B')
        self.assertEqual(node.base_name, 'loop')

    def test_get_2300(self):
        node = self.map.getnodebypath('/2000A/2000B/2300')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, '2300')
        self.assertEqual(node.base_name, 'loop')

    def test_get_2300_CLM(self):
        node = self.map.getnodebypath('/2000A/2000B/2300/CLM')
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM')
        self.assertEqual(node.base_name, 'segment')

    def tearDown(self):
        del self.map
        

class CompositeRequirement(unittest.TestCase):
    def setUp(self):
        param = params()
        param.set_param('map_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_comp_required_ok1(self):
        node = self.map.getnodebypath('/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(4)
        self.assertNotEqual(node, None)
        #self.assertEqual(node.id, 'CLM05', node.id)
        self.assertEqual(node.base_name, 'composite')
        result = node.is_valid(['03', '', '1'], self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_comp_required_ok2(self):
        param = params()
        param.set_param('map_path', os.path.expanduser('~/src/pyx12/map/'))
        map = pyx12.map_if.load_map_file('comp_test.xml', param)
        node = map.getnodebypath('/TST')
        node = node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'composite')
        result = node.is_valid([None, '', '1'], self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_comp_required_fail1(self):
        node = self.map.getnodebypath('/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(4)
        self.assertNotEqual(node, None)
        self.assertEqual(node.base_name, 'composite')
        result = node.is_valid([None, '', ''], self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '2')

class TrailingSpaces(unittest.TestCase):
    def setUp(self):
        param = params()
        param.set_param('map_path', os.path.expanduser('~/src/pyx12/map/'))
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.errh = pyx12.error_handler.errh_null()

    def test_trailing_ID_ok(self):
        node = self.map.getnodebypath('/ISA')
        node = node.get_child_node_by_idx(5)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'ISA06')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid('TEST           ', self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_no_trailing_AN_ok(self):
        node = self.map.getnodebypath('/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid('TEST', self.errh)
        self.failUnless(result)
        self.assertEqual(self.errh.err_cde, None)

    def test_trailing_AN_bad(self):
        node = self.map.getnodebypath('/2000A/2000B/2300/CLM')
        node = node.get_child_node_by_idx(0)
        self.assertNotEqual(node, None)
        self.assertEqual(node.id, 'CLM01')
        self.assertEqual(node.base_name, 'element')
        result = node.is_valid('TEST     ', self.errh)
        self.failIf(result)
        self.assertEqual(self.errh.err_cde, '6', self.errh.err_str)


class IsValidSyntax(unittest.TestCase):
    def test_fail_bad_syntax(self):
        seg = ['MEA', 'OG', 'HT', '', '', '', '', '', '']
        syntax = ['R', 3]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        #self.failUnlessRaises(EngineError, map_if.is_syntax_valid, seg, syntax)
        self.failIf(result, err_str)


class IsValidSyntaxP(unittest.TestCase):
    """
    If has one, must have all
    """
    #def setUp(self):
    #    self.errh = error_handler.errh_null()

    def test_P_ok(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', 'AAAA']
        syntax = ['P', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)
        
    def test_P_bad1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA']
        syntax = ['P', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_P_bad2(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '']
        syntax = ['P', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_P_ok_blank(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '']
        syntax = ['P', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)


class IsValidSyntaxR(unittest.TestCase):
    """
    At least one element in list is required
    """

    def test_R_ok(self):
        seg = ['REF', '1A', 'AAA', '']
        syntax = ['R', 2, 3]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)
        
    def test_R_ok3(self):
        seg = ['REF', '1A', 'AAA']
        syntax = ['R', 2, 3]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)
        
    def test_R_fail1(self):
        #pdb.set_trace()
        seg = ['REF', '1A']
        syntax = ['R', 2, 3]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_R_fail2(self):
        seg = ['REF', '1A', '']
        syntax = ['R', 2, 3]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_R_ok1(self):
        seg = ['MEA', 'OG', 'HT', '3', '', '', '', '', '8']
        syntax = ['R', 3, 5, 6, 8]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_R_ok2(self):
        seg = ['MEA', 'OG', 'HT', '', '', '', '', '', '8']
        syntax = ['R', 3, 5, 6, 8]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_R_fail_blank(self):
        seg = ['MEA', 'OG', 'HT', '', '', '', '', '', '']
        syntax = ['R', 3, 5, 6, 8]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)


class IsValidSyntaxC(unittest.TestCase):
    """
    If the first is present, then all others are required
    """
    def test_C_ok(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', 'AAAA']
        #seg = ['CUR', ]
        syntax = ['C', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)
        
    def test_C_fail1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '']
        syntax = ['C', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_C_ok1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA']
        syntax = ['C', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_C_ok2(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '']
        syntax = ['C', 7, 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_C_ok_blank(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '']
        syntax = ['C', 6, 7, 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_C_ok_null(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam']
        syntax = ['C', 6, 7, 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)


class IsValidSyntaxL(unittest.TestCase):
    """
    If the first is present, then at least one of others is required
    """
    def test_L_ok(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', 'AAAA', 'ZZZZ']
        syntax = ['L', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)
        
    def test_L_ok1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA', '']
        syntax = ['L', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_L_fail1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '', '']
        syntax = ['L', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_L_ok_blank(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '', 'ZZZZ']
        syntax = ['L', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)


class IsValidSyntaxE(unittest.TestCase):
    """
    Not more than one of the elements may be present
    """
    def test_E_fail1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', 'AAAA', 'ZZZZ']
        syntax = ['E', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)
        
    def test_E_ok1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA', '']
        syntax = ['E', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_E_ok2(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '', '']
        syntax = ['E', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_E_fail2(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'YY', 'ZZZZ']
        syntax = ['E', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_E_ok_blank(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '', '']
        syntax = ['E', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_E_ok_null(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam']
        syntax = ['E', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)


def suite():
    #suite = unittest.makeSuite((Test_getnodebypath, IsValidSyntax, \
    #    IsValidSyntaxP, IsValidSyntaxR, IsValidSyntaxC, \
    #    IsValidSyntaxE, IsValidSyntaxL))
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_getnodebypath))
    suite.addTest(unittest.makeSuite(TrailingSpaces))
    suite.addTest(unittest.makeSuite(CompositeRequirement))
    suite.addTest(unittest.makeSuite(IsValidSyntax))
    suite.addTest(unittest.makeSuite(IsValidSyntaxP))
    suite.addTest(unittest.makeSuite(IsValidSyntaxR))
    suite.addTest(unittest.makeSuite(IsValidSyntaxC))
    suite.addTest(unittest.makeSuite(IsValidSyntaxE))
    suite.addTest(unittest.makeSuite(IsValidSyntaxL))
    suite.addTest(unittest.makeSuite(Element_is_valid))
    return suite
                
#if __name__ == "__main__":
#    unittest.main()   
unittest.TextTestRunner(verbosity=2).run(suite())
