import unittest
import sys
import os.path

import pyx12.params
#from pyx12.errors import EngineError


class Default(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()

    def test_valid1(self):
        self.assertEqual(self.param.get('charset'), 'E')

    def test_valid2(self):
        self.assertEqual(self.param.get('skip_997'), False)


class ClearParam(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()

    def test_valid1(self):
        self.param.set('simple_dtd', '')
        self.assertEqual(self.param.get('simple_dtd'), None)
        self.param.set('simple_dtd', 'aaa')
        self.assertEqual(self.param.get('simple_dtd'), 'aaa')

    def test_valid2(self):
        self.param.set('exclude_external_codes', '')
        self.assertEqual(self.param.get('exclude_external_codes'), None)


class SetParamOverride(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()

    def test_valid1(self):
        self.param.set('ignore_syntax', False)
        self.assertEqual(self.param.get('ignore_syntax'), False)
        self.param.set('ignore_syntax', True)
        self.assertEqual(self.param.get('ignore_syntax'), True)

    def test_valid2(self):
        self.param.set('exclude_external_codes', 'states,diagnosis')
        self.assertEqual(self.param.get(
            'exclude_external_codes'), 'states,diagnosis')


class ReadConfigFile(unittest.TestCase):
    def setUp(self):
        test_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.param = pyx12.params.params(
            os.path.join(test_path, 'pyx12test.conf.xml'))

    def test_changed(self):
        self.assertEqual(self.param.get(
            'exclude_external_codes'), 'taxonomy,states')
        self.assertEqual(self.param.get('ignore_syntax'), True)
        self.assertEqual(self.param.get('charset'), 'B')

    def test_unchanged(self):
        #self.assertEqual(self.param.get('pickle_path'), '/usr/local/share/pyx12/map')
        self.assertEqual(self.param.get('ignore_codes'), False)
        self.assertEqual(self.param.get('skip_html'), False)

    def test_invalid_file(self):
        self.assertRaises(pyx12.errors.EngineError,
                          pyx12.params.params, 'nonexistant_file.xml')
