#! /usr/bin/env /usr/local/bin/python

#import test_support
#from test_support import TestFailed, have_unicode
import unittest
#import sys
import StringIO

import error_handler
#from error_handler import ErrorErrhNull
from errors import *
import x12file

class x12fileTests(unittest.TestCase):

    def test_x12file_headers(self):
        fd = StringIO.StringIO(' ISA~')
        errh = error_handler.errh_null()
        self.failUnlessRaises(error_handler.ErrorErrhNull, x12file.x12file, fd, errh)

def suite():
    suite = unittest.makeSuite(x12fileTests)
    return suite
                
if __name__ == "__main__":
    unittest.main()   
