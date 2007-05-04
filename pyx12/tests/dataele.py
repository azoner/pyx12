import unittest
import sys
from os.path import dirname, abspath, join, isdir, isfile

import pyx12.dataele 
from pyx12.errors import EngineError
import pyx12.params
from pyx12.tests.support import getMapPath

class BadDataElem(unittest.TestCase):
    def setUp(self):
        map_path = getMapPath()
        params = pyx12.params.params()
        if map_path is None:
            map_path = params.get('map_path')
        self.de = pyx12.dataele.DataElements(map_path)

    def testNone(self):
        self.failUnlessRaises(EngineError, self.de.get_by_elem_num, None)

    def testInvalid(self):
        self.failUnlessRaises(EngineError, self.de.get_by_elem_num, '28902')
        self.failUnlessRaises(EngineError, self.de.get_by_elem_num, '0')
        self.failUnlessRaises(EngineError, self.de.get_by_elem_num, '99991')

class LookupDataElem(unittest.TestCase):

    def setUp(self):
        map_path = getMapPath()
        params = pyx12.params.params()
        if map_path is None:
            map_path = params.get('map_path')
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
