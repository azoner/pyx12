import unittest

import pyx12.map_index
import pyx12.params


class GetFilename(unittest.TestCase):
    """
    """
    def setUp(self):
        param = pyx12.params.params()
        self.idx = pyx12.map_index.map_index()

    def test_get_837p(self):
        self.assertEqual(self.idx.get_filename(
            '00401', '004010X098A1', 'HC'), '837.4010.X098.A1.xml')
        self.assertEqual(
            self.idx.get_abbr('00401', '004010X098A1', 'HC'), '837P')

    def test_get_278_initial(self):
        self.assertEqual(self.idx.get_filename(
            '00401', '004010X094A1', 'HI'), '278.4010.X094.27.A1.xml')
        self.assertEqual(
            self.idx.get_abbr('00401', '004010X094A1', 'HI'), '278a')

    def test_get_278(self):
        self.assertEqual(self.idx.get_filename('00401',
                                               '004010X094A1', 'HI', '11'), '278.4010.X094.27.A1.xml')
        self.assertEqual(self.idx.get_abbr(
            '00401', '004010X094A1', 'HI', '11'), '278a')
        self.assertEqual(self.idx.get_filename('00401',
                                               '004010X094A1', 'HI', '13'), '278.4010.X094.A1.xml')
        self.assertEqual(self.idx.get_abbr(
            '00401', '004010X094A1', 'HI', '13'), '278b')


class GetFilenameMapPath(unittest.TestCase):
    """
    """
    def setUp(self):
        import os.path
        map_path = os.path.join(os.path.dirname(pyx12.map_index.__file__), 'map')
        param = pyx12.params.params()
        self.idx = pyx12.map_index.map_index(map_path)

    def test_get_837p(self):
        self.assertEqual(self.idx.get_filename(
            '00401', '004010X098A1', 'HC'), '837.4010.X098.A1.xml')
        self.assertEqual(
            self.idx.get_abbr('00401', '004010X098A1', 'HC'), '837P')

    def test_get_278_initial(self):
        self.assertEqual(self.idx.get_filename(
            '00401', '004010X094A1', 'HI'), '278.4010.X094.27.A1.xml')
        self.assertEqual(
            self.idx.get_abbr('00401', '004010X094A1', 'HI'), '278a')

    def test_get_278(self):
        self.assertEqual(self.idx.get_filename('00401',
                                               '004010X094A1', 'HI', '11'), '278.4010.X094.27.A1.xml')
        self.assertEqual(self.idx.get_abbr(
            '00401', '004010X094A1', 'HI', '11'), '278a')
        self.assertEqual(self.idx.get_filename('00401',
                                               '004010X094A1', 'HI', '13'), '278.4010.X094.A1.xml')
        self.assertEqual(self.idx.get_abbr(
            '00401', '004010X094A1', 'HI', '13'), '278b')
