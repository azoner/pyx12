import os
import os.path
import unittest

import pyx12.map_if
import pyx12.syntax
import pyx12.segment
from pyx12.errors import *


class IsValidSyntax(unittest.TestCase):

    def test_fail_bad_syntax(self):
        seg1 = ['MEA', 'OG', 'HT', '', '', '', '', '', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['R', 3]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        #self.assertRaises(EngineError, map_if.is_syntax_valid, seg, syntax)
        self.assertFalse(result, err_str)


class IsValidSyntaxP(unittest.TestCase):
    """
    If has one, must have all
    """

    def test_P_ok(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', 'AAAA']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['P', 8, 9]
        #pdb.set_trace()
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_P_bad1(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['P', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertFalse(result, err_str)

    def test_P_bad2(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['P', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertFalse(result, err_str)

    def test_P_ok_blank(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['P', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_P_ok_len(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['P', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_P_bad_len(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['P', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertFalse(result, err_str)


class IsValidSyntaxR(unittest.TestCase):
    """
    At least one element in list is required
    """

    def test_R_ok(self):
        seg1 = ['REF', '1A', 'AAA', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['R', 2, 3]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_R_ok3(self):
        seg1 = ['REF', '1A', 'AAA']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['R', 2, 3]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_R_fail1(self):
        #pdb.set_trace()
        seg1 = ['REF', '1A']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['R', 2, 3]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertFalse(result, err_str)

    def test_R_fail2(self):
        seg1 = ['REF', '1A', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['R', 2, 3]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertFalse(result, err_str)

    def test_R_ok1(self):
        seg1 = ['MEA', 'OG', 'HT', '3', '', '', '', '', '8']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['R', 3, 5, 6, 8]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_R_ok2(self):
        seg1 = ['MEA', 'OG', 'HT', '', '', '', '', '', '8']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['R', 3, 5, 6, 8]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_R_fail_blank(self):
        seg1 = ['MEA', 'OG', 'HT', '', '', '', '', '', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['R', 3, 5, 6, 8]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertFalse(result, err_str)


class IsValidSyntaxC(unittest.TestCase):
    """
    If the first is present, then all others are required
    """
    def test_C_ok(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', 'AAAA']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        #seg = ['CUR', ]
        syntax = ['C', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_C_fail1(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['C', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertFalse(result, err_str)

    def test_C_fail2(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['C', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)

    def test_C_ok1(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['C', 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_C_ok2(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['C', 7, 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_C_ok_blank(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['C', 6, 7, 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_C_ok_null(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['C', 6, 7, 8, 9]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)


class IsValidSyntaxL(unittest.TestCase):
    """
    If the first is present, then at least one of others is required
    """
    def test_L_ok(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46',
                'AAAA', 'ZZZZ']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['L', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_L_ok1(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['L', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_L_ok2(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['L', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_L_fail1(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['L', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertFalse(result, err_str)

    def test_L_fail2(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['L', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertFalse(result, err_str)

    def test_L_missing_element_ok(self):
        seg = pyx12.segment.Segment(
            'CAS*PR*42*75.00**1*25.00**2*75.00~', '~', '*', ':')
        syntax = ['L', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_L_ok_blank(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '', 'ZZZZ']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['L', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_L_ok_len(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['L', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)


class IsValidSyntaxE(unittest.TestCase):
    """
    Not more than one of the elements may be present
    """
    def test_E_fail1(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46',
                'AAAA', 'ZZZZ']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['E', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertFalse(result, err_str)

    def test_E_ok1(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'AAAA', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['E', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_E_ok2(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '46', '', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['E', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_E_fail2(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', 'YY', 'ZZZZ']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['E', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertFalse(result, err_str)

    def test_E_ok_blank(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam', '', '', '', '', '', '']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['E', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)

    def test_E_ok_null(self):
        seg1 = ['NM1', '41', '1', 'Smith', 'Sam']
        seg = pyx12.segment.Segment('*'.join(seg1), '~', '*', ':')
        syntax = ['E', 8, 9, 10]
        (result, err_str) = pyx12.map_if.is_syntax_valid(seg, syntax)
        self.assertTrue(result, err_str)
