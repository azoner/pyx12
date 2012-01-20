#    $Id: map_walker.py 1484 2011-10-22 02:06:12Z johnholland $

import sys
from os.path import dirname, abspath, join, isdir, isfile
import unittest

import pyx12.error_handler
from pyx12.errors import *
from pyx12.map_walker import walk_tree, get_id_list, traverse_path, pop_to_parent_loop
import pyx12.map_if
import pyx12.params 
import pyx12.segment
from pyx12.tests.support import getMapPath

class UniqueNodePath(unittest.TestCase):

    def setUp(self):
        map_path = getMapPath()
        self.walker = walk_tree()
        self.param = pyx12.params.params('pyx12.conf.xml')
        if map_path:
            self.param.set('map_path', map_path)
            self.param.set('pickle_path', map_path)
        self.errh = pyx12.error_handler.errh_null()

    def test_all_unique(self):
        self.errh.reset()
        paths = set()
        map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', self.param)
        for x in map.loop_segment_iterator():
            p = x.get_path()
            self.assertTrue(p not in paths, 'Duplicate path %s' % (p))
            paths.add(p)
