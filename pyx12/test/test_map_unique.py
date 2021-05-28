import unittest

import pyx12.error_handler
import pyx12.map_if
import pyx12.params


class UniqueNodePath(unittest.TestCase):

    def setUp(self):
        self.param = pyx12.params.params()
        self.errh = pyx12.error_handler.errh_null()

    def _get_paths(self, map_file):
        self.errh.reset()
        paths = set()
        map1 = pyx12.map_if.load_map_file(map_file, self.param)
        for x in [a for a in map1.loop_segment_iterator() if a.is_loop()]:
            p = x.get_path()
            self.assertTrue(p not in paths, 'Duplicate path %s' % (p))
            paths.add(p)
        return paths

    def test_all_unique(self):
        self.errh.reset()
        paths = set()
        map1 = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', self.param)
        for x in map1.loop_segment_iterator():
            p = x.get_path()
            self.assertTrue(p not in paths, 'Duplicate path %s' % (p))
            paths.add(p)

    def xtest_835(self):
        self.maxDiff = None
        (f1, f2) = ('835.4010.X091.A1.xml', '835.5010.X221.A1.xml')
        old = self._get_paths(f1)
        new = self._get_paths(f2)
        self.assertSequenceEqual(old, new)

    def xtest_834(self):
        self.maxDiff = None
        (f1, f2) = ('834.4010.X095.A1.xml', '834.5010.X220.A1.xml')
        old = self._get_paths(f1)
        new = self._get_paths(f2)
        self.assertSequenceEqual(old, new)

    def xtest_820(self):
        self.maxDiff = None
        (f1, f2) = ('820.4010.X061.A1.xml', '820.5010.X218.xml')
        old = self._get_paths(f1)
        new = self._get_paths(f2)
        self.assertSequenceEqual(old, new)

    def xtest_837p(self):
        self.maxDiff = None
        (f1, f2) = ('837.4010.X098.A1.xml', '837.5010.X222.A1.xml')
        old = self._get_paths(f1)
        new = self._get_paths(f2)
        self.assertSequenceEqual(old, new)

    def xtest_837i(self):
        self.maxDiff = None
        (f1, f2) = ('837.4010.X096.A1.xml', '837Q3.I.5010.X223.A1.xml')
        old = self._get_paths(f1)
        new = self._get_paths(f2)
        self.assertSequenceEqual(old, new)
