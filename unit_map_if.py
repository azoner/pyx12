#! /usr/bin/env /usr/local/bin/python

import unittest
import pdb

import error_handler
from errors import *
import map_if

class IsValidSyntaxP(unittest.TestCase):

    def setUp(self):
        self.errh = error_handler.errh_null()

    def test_P_ok(self):
        seg = ['NM1', '41']
        syntax = ['P', 5, 4]
        map_if._is_syntax_valid(seg, self.errh, syntax)
        self.assertEqual(self.errh.err_cde, '2', self.errh.err_str)

def suite():
    suite = unittest.makeSuite((IsValidSyntaxChecks)
    return suite
                
if __name__ == "__main__":
    unittest.main()   
