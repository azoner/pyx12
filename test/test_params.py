#! /usr/bin/env /usr/local/bin/python

import unittest
import sys

import pyx12.params
from pyx12.errors import *

class Default(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()

    def test_valid1(self):
        self.assertEqual(self.param.get_param('charset'), 'E')

    def test_valid2(self):
        self.assertEqual(self.param.get_param('skip_997'), False)

class SetParamOverride(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()

    def test_valid1(self):
        self.param.set_param('ignore_syntax', False)
        self.assertEqual(self.param.get_param('ignore_syntax'), False)
        self.param.set_param('ignore_syntax', True)
        self.assertEqual(self.param.get_param('ignore_syntax'), True)

    def test_valid2(self):
        self.param.set_param('exclude_external_codes', 'states,diagnosis')
        self.assertEqual(self.param.get_param('exclude_external_codes'), 'states,diagnosis')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Default))
    suite.addTest(unittest.makeSuite(SetParamOverride))
    return suite

#if __name__ == "__main__":
#    unittest.main()
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())
