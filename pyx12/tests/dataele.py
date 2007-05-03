import unittest
import sys
import os.path

#from pyx12.dataele import *
import pyx12.dataele 
from pyx12.errors import EngineError
import pyx12.params


class BadDataElem(unittest.TestCase):
    def setUp(self):
        params = pyx12.params.params()
        map_path = params.get('map_path')
        #map_path = os.path.join('/'.join( \
        #    os.path.abspath(sys.argv[0]).split('/')[:-2]), \
        #    'map')
        if not os.path.isdir(map_path):
            map_path = None
        self.de = pyx12.dataele.DataElements(map_path)

    def testNone(self):
        self.failUnlessRaises(EngineError, self.de.get_by_elem_num, None)

    def testInvalid(self):
        self.failUnlessRaises(EngineError, self.de.get_by_elem_num, '28902')
        self.failUnlessRaises(EngineError, self.de.get_by_elem_num, '0')
        self.failUnlessRaises(EngineError, self.de.get_by_elem_num, '99991')

class LookupDataElem(unittest.TestCase):

    def setUp(self):
        params = pyx12.params.params()
        map_path = params.get('map_path')
        if not os.path.isdir(map_path):
            map_path = None
        self.de = pyx12.dataele.DataElements(map_path)
    
    def testOK_AN(self):
        self.assertEqual(self.de.get_by_elem_num('1204')[:3], ('AN', 1, 50))

    def testOK_ID(self):
        self.assertEqual(self.de.get_by_elem_num('116')[:3], ('ID', 3, 15))

    def testOK_N(self):
        self.assertEqual(self.de.get_by_elem_num('554')[:3], ('N0', 1, 6))

    def testOK_DT(self):
        self.assertEqual(self.de.get_by_elem_num('373')[:3], ('DT', 8, 8))

    def testOK_TM(self):
        self.assertEqual(self.de.get_by_elem_num('337')[:3], ('TM', 4, 8))
