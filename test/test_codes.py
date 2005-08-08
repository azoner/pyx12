#! /usr/bin/env /usr/local/bin/python

import os.path, sys, string
import unittest
#import pdb

import pyx12.codes
import pyx12.error_handler
#from error_handler import ErrorErrhNull
from pyx12.errors import *
import pyx12.map_if
import pyx12.params

map_path = os.path.join(string.join(os.path.abspath(
    sys.argv[0]).split('/')[:-2], '/'), 'map')
if not os.path.isdir(map_path):
    map_path = None

class TestExternal(unittest.TestCase):
    """
    """
    def setUp(self):
        self.param = pyx12.params.params('pyx12.conf.xml')
        if map_path:
            self.param.set('map_path', map_path)
        self.ext_codes = pyx12.codes.ExternalCodes(self.param.get('map_path'), \
            self.param.get('exclude_external_codes'))

    def test_valid_state1(self):
        self.failUnless(self.ext_codes.IsValid('states', 'MI', '20031001'))

    def test_valid_state2(self):
        self.failUnless(self.ext_codes.IsValid('states', 'NV'))

    def test_invalid_state1(self):
        self.failIf(self.ext_codes.IsValid('states', 'AN', '20031001'))

    def test_exclude_state_code(self):
        self.param.set('exclude_external_codes', 'states')
        ext_codes = pyx12.codes.ExternalCodes(self.param.get('map_path'), \
            self.param.get('exclude_external_codes'))
        self.failUnless(ext_codes.IsValid('states', 'ZZ'))

    def test_noexclude_state_code(self):
        ext_codes = pyx12.codes.ExternalCodes(self.param.get('map_path'), \
            self.param.get('exclude_external_codes'))
        self.failIf(ext_codes.IsValid('states', 'ZZ'))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestExternal))
    return suite

#if __name__ == "__main__":
#    unittest.main()
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())
