#! /usr/bin/env /usr/local/bin/python

import unittest
import pdb

#import error_handler
from errors import *
import map_if

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
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', 'AAAA']
        syntax = ['R', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)
        
    def test_R_ok1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA']
        syntax = ['R', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_R_ok2(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '']
        syntax = ['R', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)

    def test_R_fail_blank(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '']
        syntax = ['R', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)


class IsValidSyntaxC(unittest.TestCase):
    """
    If the first is present, then all others are required
    """
    def test_C_ok(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', 'AAAA']
        syntax = ['C', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result, err_str)
        
    def test_C_fail1(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA']
        syntax = ['C', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failUnless(result) #, err_str)

    def test_C_fail2(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '']
        syntax = ['C', 8, 9]
        (result, err_str) = map_if.is_syntax_valid(seg, syntax)
        self.failIf(result, err_str)

    def test_C_ok_blank(self):
        seg = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '']
        syntax = ['C', 8, 9]
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

def suite():
    suite = unittest.makeSuite((IsValidSyntaxChecks))
    return suite
                
if __name__ == "__main__":
    unittest.main()   
