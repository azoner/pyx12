#! /usr/bin/env /usr/local/bin/python

#import test_support
#from test_support import TestFailed, have_unicode
import unittest
#import pdb

import error_handler
#from error_handler import ErrorErrhNull
from errors import *
from map_walker import walk_tree
import map_if


class Explicit_Loops(unittest.TestCase):

    def setUp(self):
        self.walker = walk_tree()
        self.map = map_if.map_if('map/837.4010.X098.A1.xml')
        self.errh = error_handler.errh_null()

    def test_ISA_to_GS(self):
        node = self.map.getnodebypath('/ISA')
        seg = ['GS', 'HC']
        #(isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = src.get_id()
        node = self.walker.walk(node, seg, self.errh, 5, 4, None)
        self.assertEqual(seg[0], node.id)

def suite():
    suite = unittest.makeSuite((Explicit_Loops))
    return suite
                
if __name__ == "__main__":
    unittest.main()   
