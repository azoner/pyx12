#! /usr/bin/env /usr/local/bin/python

import unittest
import pdb

#import error_handler
from errors import *
import map_if

class Test_getnodebypath(unittest.TestCase):
    """
    """
    def setUp(self):
        self.map = map_if.load_map_file('map/837.4010.X098.A1.xml')

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

class IsValidSyntax(unittest.TestCase):
    def test_fail_bad_syntax(self):
        seg = ['MEA', 'OG', 'HT', '', '', '', '', '', '']
        syntax = ['R', 3]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
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
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)
        
    def test_P_bad1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA']
        syntax = ['P', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_P_bad2(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '']
        syntax = ['P', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_P_ok_blank(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '']
        syntax = ['P', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

class IsValidSyntaxR(unittest.TestCase):
    """
    At least one element in list is required
    """

    def test_R_ok(self):
        seg = ['REF', '1A', 'AAA', '']
        syntax = ['R', 2, 3]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)
        
    def test_R_ok3(self):
        seg = ['REF', '1A', 'AAA']
        syntax = ['R', 2, 3]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)
        
    def test_R_fail1(self):
        #pdb.set_trace()
        seg = ['REF', '1A']
        syntax = ['R', 2, 3]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_R_fail2(self):
        seg = ['REF', '1A', '']
        syntax = ['R', 2, 3]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_R_ok1(self):
        seg = ['MEA', 'OG', 'HT', '3', '', '', '', '', '8']
        syntax = ['R', 3, 5, 6, 8]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_R_ok2(self):
        seg = ['MEA', 'OG', 'HT', '', '', '', '', '', '8']
        syntax = ['R', 3, 5, 6, 8]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_R_fail_blank(self):
        seg = ['MEA', 'OG', 'HT', '', '', '', '', '', '']
        syntax = ['R', 3, 5, 6, 8]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

class IsValidSyntaxC(unittest.TestCase):
    """
    If the first is present, then all others are required
    """
    def test_C_ok(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', 'AAAA']
        #seg = ['CUR', ]
        syntax = ['C', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)
        
    def test_C_fail1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '']
        syntax = ['C', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_C_ok1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA']
        syntax = ['C', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_C_ok2(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '']
        syntax = ['C', 7, 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_C_ok_blank(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '']
        syntax = ['C', 6, 7, 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_C_ok_null(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam']
        syntax = ['C', 6, 7, 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)


class IsValidSyntaxL(unittest.TestCase):
    """
    If the first is present, then at least one of others is required
    """
    def test_L_ok(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', 'AAAA', 'ZZZZ']
        syntax = ['L', 8, 9, 10]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)
        
    def test_L_ok1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA', '']
        syntax = ['L', 8, 9, 10]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_L_fail1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '', '']
        syntax = ['L', 8, 9, 10]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_L_ok_blank(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '', 'ZZZZ']
        syntax = ['L', 8, 9, 10]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

class IsValidSyntaxE(unittest.TestCase):
    """
    Not more than one of the elements may be present
    """
    def test_E_fail1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', 'AAAA', 'ZZZZ']
        syntax = ['E', 8, 9, 10]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)
        
    def test_E_ok1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA', '']
        syntax = ['E', 8, 9, 10]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_E_ok2(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '', '']
        syntax = ['E', 8, 9, 10]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_E_fail2(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'YY', 'ZZZZ']
        syntax = ['E', 8, 9, 10]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_E_ok_blank(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '', '']
        syntax = ['E', 8, 9, 10]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_E_ok_null(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam']
        syntax = ['E', 8, 9, 10]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

def suite():
    suite = unittest.makeSuite((Test_getnodebypath, IsValidSyntax, \
        IsValidSyntaxP, IsValidSyntaxR, IsValidSyntaxC, \
        IsValidSyntaxE, IsValidSyntaxL))
    return suite
                
#if __name__ == "__main__":
#    unittest.main()   
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(Test_getnodebypath))
suite.addTest(unittest.makeSuite(IsValidSyntax))
suite.addTest(unittest.makeSuite(IsValidSyntaxP))
suite.addTest(unittest.makeSuite(IsValidSyntaxR))
suite.addTest(unittest.makeSuite(IsValidSyntaxC))
suite.addTest(unittest.makeSuite(IsValidSyntaxE))
suite.addTest(unittest.makeSuite(IsValidSyntaxL))
unittest.TextTestRunner(verbosity=2).run(suite)
