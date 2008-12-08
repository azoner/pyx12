#    $Id$

import sys
from os.path import dirname, abspath, join, isdir, isfile
import unittest

import pyx12.params 
from pyx12.tests.support import getMapPath

class MapPath(unittest.TestCase):

    def test_get_map_path(self):
        map_path = getMapPath()
        param = pyx12.params.params('pyx12.conf.xml')
        self.assertNotEqual(map_path, '/usr/local/share/pyx12/map')
        self.assertNotEqual(param.get('map_path'), '/usr/local/share/pyx12/map')
        file837 = join(map_path, '837.4010.X098.A1.xml')
        self.failUnless(isfile(file837))
