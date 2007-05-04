#! /usr/bin/env /usr/local/bin/python

import sys
import unittest
from os.path import dirname, abspath, join, isdir, isfile

import pyx12.map_index
import pyx12.params
from pyx12.tests.support import getMapPath

class GetFilename(unittest.TestCase):
    """
    """
    def setUp(self):
        map_path = getMapPath()
        param = pyx12.params.params('pyx12.conf.xml')
        if not map_path:
            map_path = param.get('map_path')
        self.idx = pyx12.map_index.map_index(join(map_path, 'maps.xml'))

    def test_get_837p(self):
        self.assertEqual(self.idx.get_filename('00401', '004010X098A1', 'HC'), '837.4010.X098.A1.xml')

    def test_get_278_initial(self):
        self.assertEqual(self.idx.get_filename('00401', '004010X094A1', 'HI'), '278.4010.X094.27.A1.xml')
        
    def test_get_278(self):
        self.assertEqual(self.idx.get_filename('00401', '004010X094A1', 'HI', '11'), '278.4010.X094.27.A1.xml')
        self.assertEqual(self.idx.get_filename('00401', '004010X094A1', 'HI', '13'), '278.4010.X094.A1.xml')
