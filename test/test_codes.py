#! /usr/bin/env /usr/local/bin/python

import os.path
import unittest
#import pdb

import pyx12.codes
import pyx12.error_handler
#from error_handler import ErrorErrhNull
from pyx12.errors import *
import pyx12.map_if
from pyx12.params import params


class TestExternal(unittest.TestCase):
    """
    FAIL - no end tag for explicit loop
    """
    def setUp(self):
        param = params()
        param.set_param('map_path', os.path.expanduser('~/src/pyx12/map/'))
        self.ext_codes = pyx12.codes.ExternalCodes(param.get_param('map_path'), \
            param.get_param('exclude_external_codes'))

    def test_valid_state1(self):
        self.failUnless(self.ext_codes.IsValid('states', 'MI', '20031001'))

    def test_valid_state2(self):
        self.failUnless(self.ext_codes.IsValid('states', 'NV'))

    def test_invalid_state1(self):
        self.failIf(self.ext_codes.IsValid('states', 'AN', '20031001'))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestExternal))
    return suite

#if __name__ == "__main__":
#    unittest.main()
unittest.TextTestRunner(verbosity=2).run(suite())

