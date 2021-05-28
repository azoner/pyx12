import unittest

import pyx12.dataele
from pyx12.errors import EngineError


class BadDataElem(unittest.TestCase):
    def setUp(self):
        self.de = pyx12.dataele.DataElements()

    def testNone(self):
        self.assertRaises(EngineError, self.de.get_by_elem_num, None)

    def testInvalid(self):
        self.assertRaises(EngineError, self.de.get_by_elem_num, '28902')
        self.assertRaises(EngineError, self.de.get_by_elem_num, '0')
        self.assertRaises(EngineError, self.de.get_by_elem_num, '99991')


class LookupDataElem(unittest.TestCase):

    def setUp(self):
        self.de = pyx12.dataele.DataElements()

    def testOK_AN(self):
        self.assertEqual(self.de.get_by_elem_num('1204'), {'max_len': 50, 'name': 'Plan Coverage Description', 'data_type': 'AN', 'min_len': 1})

    def testOK_ID(self):
        self.assertEqual(self.de.get_by_elem_num('116'), {'max_len': 15,
                                                          'name': 'Postal Code', 'data_type': 'ID', 'min_len': 3})

    def testOK_N(self):
        self.assertEqual(self.de.get_by_elem_num('554'), {'max_len': 6, 'name':
                                                          'Assigned Number', 'data_type': 'N0', 'min_len': 1})

    def testOK_DT(self):
        self.assertEqual(self.de.get_by_elem_num('373'),
                         {'max_len': 8, 'name': 'Date', 'data_type': 'DT', 'min_len': 8})

    def testOK_TM(self):
        self.assertEqual(self.de.get_by_elem_num('337'), {'max_len':
                                                          8, 'name': 'Time', 'data_type': 'TM', 'min_len': 4})


class LookupDataElemMapPath(unittest.TestCase):

    def setUp(self):
        import os.path
        map_path = os.path.join(os.path.dirname(pyx12.dataele.__file__), 'map')
        self.de = pyx12.dataele.DataElements(map_path)

    def testOK_AN(self):
        self.assertEqual(self.de.get_by_elem_num('1204'), {'max_len': 50, 'name': 'Plan Coverage Description', 'data_type': 'AN', 'min_len': 1})

    def testOK_ID(self):
        self.assertEqual(self.de.get_by_elem_num('116'), {'max_len': 15,
                                                          'name': 'Postal Code', 'data_type': 'ID', 'min_len': 3})

    def testOK_N(self):
        self.assertEqual(self.de.get_by_elem_num('554'), {'max_len': 6, 'name':
                                                          'Assigned Number', 'data_type': 'N0', 'min_len': 1})

    def testOK_DT(self):
        self.assertEqual(self.de.get_by_elem_num('373'),
                         {'max_len': 8, 'name': 'Date', 'data_type': 'DT', 'min_len': 8})

    def testOK_TM(self):
        self.assertEqual(self.de.get_by_elem_num('337'), {'max_len':
                                                          8, 'name': 'Time', 'data_type': 'TM', 'min_len': 4})
