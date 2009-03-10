import sys
from os.path import dirname, abspath, join, isdir, isfile
import unittest

import pyx12.codes
import pyx12.error_handler
from pyx12.errors import *
import pyx12.map_if
import pyx12.params
from pyx12.tests.support import getMapPath

class TestExternal(unittest.TestCase):
    """
    """
    def setUp(self):
        map_path = getMapPath()
        self.param = pyx12.params.params('pyx12.conf.xml')
        if map_path:
            self.param.set('map_path', map_path)
        self.map_path = self.param.get('map_path')
        self.ext_codes = pyx12.codes.ExternalCodes(self.map_path, \
            self.param.get('exclude_external_codes'))

    def test_valid_state1(self):
        self.failUnless(self.ext_codes.isValid('states', 'MI', '20031001'))

    def test_valid_state2(self):
        self.failUnless(self.ext_codes.isValid('states', 'NV'))

    def test_invalid_state1(self):
        self.failIf(self.ext_codes.isValid('states', 'AN', '20031001'))

    def test_exclude_state_code(self):
        self.param.set('exclude_external_codes', 'states')
        ext_codes = pyx12.codes.ExternalCodes(self.map_path, \
            self.param.get('exclude_external_codes'))
        self.failUnless(ext_codes.isValid('states', 'ZZ'))

    def test_noexclude_state_code(self):
        ext_codes = pyx12.codes.ExternalCodes(self.map_path, \
            self.param.get('exclude_external_codes'))
        self.failIf(ext_codes.isValid('states', 'ZZ'))

