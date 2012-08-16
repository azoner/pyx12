#import sys
#from os.path import dirname, abspath, join, isdir, isfile
import unittest

import pyx12.codes
import pyx12.error_handler
#from pyx12.errors import *
import pyx12.map_if
import pyx12.params


class TestExternal(unittest.TestCase):
    """
    Load Codes interface
    """
    def setUp(self):
        self.param = pyx12.params.params('pyx12.conf.xml')
        self.ext_codes = pyx12.codes.ExternalCodes(None,
                                                   self.param.get('exclude_external_codes'))

    def test_valid_state1(self):
        self.assertTrue(self.ext_codes.isValid('states', 'MI', '20031001'))

    def test_valid_state2(self):
        self.assertTrue(self.ext_codes.isValid('states', 'NV'))

    def test_invalid_state1(self):
        self.assertFalse(self.ext_codes.isValid('states', 'AN', '20031001'))

    def test_exclude_state_code(self):
        self.param.set('exclude_external_codes', 'states')
        ext_codes = pyx12.codes.ExternalCodes(None,
                                              self.param.get('exclude_external_codes'))
        self.assertTrue(ext_codes.isValid('states', 'ZZ'))

    def test_noexclude_state_code(self):
        ext_codes = pyx12.codes.ExternalCodes(None,
                                              self.param.get('exclude_external_codes'))
        self.assertFalse(ext_codes.isValid('states', 'ZZ'))
