#! /usr/bin/env /usr/local/bin/python

#import test_support
#from test_support import TestFailed, have_unicode
import unittest
#import sys
import StringIO
import pdb

import error_handler
#from error_handler import ErrorErrhNull
from errors import *
import x12file

class ISA_header(unittest.TestCase):

    def setUp(self):
        self.fd = None
        self.errh = error_handler.errh_null()

    def test_starts_with_ISA(self):
        self.fd = StringIO.StringIO(' ISA~')
        #src = x12file.x12file(self.fd, self.errh)
        #self.assertEqual(self.errh.err_cde, 'ISA1', self.errh.err_str)
        self.failUnlessRaises(x12file.x12Error, x12file.x12file, self.fd, self.errh)

    def test_at_least_ISA_len(self):
        self.fd = StringIO.StringIO('ISA~')
        #src = x12file.x12file(self.fd, self.errh)
        #self.assertEqual(self.errh.err_cde, 'ISA4', self.errh.err_str)
        self.failUnlessRaises(x12file.x12Error, x12file.x12file, self.fd, self.errh)

    def tearDown(self):
        self.fd.close()


def suite():
    suite = unittest.makeSuite((ISA_header, IEA_Checks, GE_Checks, SE_Checks))
    return suite
                
if __name__ == "__main__":
    unittest.main()   
