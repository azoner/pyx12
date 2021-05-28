import unittest

import pyx12.path
from pyx12.errors import X12PathError


class AbsPath(unittest.TestCase):

    #def setUp(self):

    def testLoopOK1(self):
        path_str = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400'
        path = pyx12.path.X12Path(path_str)
        self.assertEqual(path_str, path.format())
        self.assertEqual(path.seg_id, None)
        self.assertEqual(path.loop_list[2], 'ST_LOOP')

    def testLoopSegOK1(self):
        path_str = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/SV2'
        path = pyx12.path.X12Path(path_str)
        self.assertEqual(path_str, path.format())
        self.assertEqual(path.seg_id, 'SV2')


class Format(unittest.TestCase):

    def test_Format1(self):
        path_str = '/2000A/2000B/2300/2400/SV2'
        path = pyx12.path.X12Path(path_str)
        self.assertEqual(path_str, path.format())

    def test_Format2(self):
        path_str = '/2000A/2000B/2300/2400/SV201'
        path = pyx12.path.X12Path(path_str)
        self.assertEqual(path_str, path.format())

    def test_Format3(self):
        path_str = '/2000A/2000B/2300/2400/SV2[421]01'
        path = pyx12.path.X12Path(path_str)
        self.assertEqual(path_str, path.format())


class RefDes(unittest.TestCase):
    def test_refdes(self):
        tests = [
            ('TST', 'TST', None, None, None),
            ('TST02', 'TST', None, 2, None),
            ('TST03-2', 'TST', None, 3, 2),
            ('TST[AA]02', 'TST', 'AA', 2, None),
            ('TST[1B5]03-1', 'TST', '1B5', 3, 1),
            ('03', None, None, 3, None),
            ('03-2', None, None, 3, 2),
            ('N102', 'N1', None, 2, None),
            ('N102-5', 'N1', None, 2, 5),
            ('N1[AZR]02', 'N1', 'AZR', 2, None),
            ('N1[372]02-5', 'N1', '372', 2, 5)
        ]
        for (spath, seg_id, qual, eleidx, subeleidx) in tests:
            rd = pyx12.path.X12Path(spath)
            self.assertEqual(rd.seg_id, seg_id,
                             '%s: %s != %s' % (spath, rd.seg_id, seg_id))
            self.assertEqual(rd.id_val, qual, '%s: %s != %s' %
                             (spath, rd.id_val, qual))
            self.assertEqual(rd.ele_idx, eleidx,
                             '%s: %s != %s' % (spath, rd.ele_idx, eleidx))
            self.assertEqual(rd.subele_idx, subeleidx, '%s: %s != %s' %
                             (spath, rd.subele_idx, subeleidx))
            self.assertEqual(rd.format(), spath,
                             '%s: %s != %s' % (spath, rd.format(), spath))
            self.assertEqual(rd.loop_list, [],
                             '%s: Loop list is not empty' % (spath))


class RelativePath(unittest.TestCase):
    def test_rel_paths(self):
        tests = [
            ('AAA/TST', 'TST', None, None, None, ['AAA']),
            ('B1000/TST02', 'TST', None, 2, None, ['B1000']),
            ('1000B/TST03-2', 'TST', None, 3, 2, ['1000B']),
            ('1000A/1000B/TST[AA]02', 'TST', 'AA', 2, None, [
                '1000A', '1000B']),
            ('AA/BB/CC/TST[1B5]03-1', 'TST', '1B5', 3, 1, ['AA', 'BB', 'CC']),
            ('DDD/E1000/N102', 'N1', None, 2, None, ['DDD', 'E1000']),
            ('E1000/D322/N102-5', 'N1', None, 2, 5, ['E1000', 'D322']),
            ('BB/CC/N1[AZR]02', 'N1', 'AZR', 2, None, ['BB', 'CC']),
            ('BB/CC/N1[372]02-5', 'N1', '372', 2, 5, ['BB', 'CC'])
        ]
        for (spath, seg_id, qual, eleidx, subeleidx, plist) in tests:
            rd = pyx12.path.X12Path(spath)
            self.assertEqual(rd.relative, True,
                             '%s: %s != %s' % (spath, rd.relative, True))
            self.assertEqual(rd.seg_id, seg_id,
                             '%s: %s != %s' % (spath, rd.seg_id, seg_id))
            self.assertEqual(rd.id_val, qual, '%s: %s != %s' %
                             (spath, rd.id_val, qual))
            self.assertEqual(rd.ele_idx, eleidx,
                             '%s: %s != %s' % (spath, rd.ele_idx, eleidx))
            self.assertEqual(rd.subele_idx, subeleidx, '%s: %s != %s' %
                             (spath, rd.subele_idx, subeleidx))
            self.assertEqual(rd.format(), spath,
                             '%s: %s != %s' % (spath, rd.format(), spath))
            self.assertEqual(rd.loop_list, plist,
                             '%s: %s != %s' % (spath, rd.loop_list, plist))

    def test_bad_rel_paths(self):
        bad_paths = [
            'AA/03',
            'BB/CC/03-2'
        ]
        for spath in bad_paths:
            self.assertRaises(X12PathError, pyx12.path.X12Path, spath)

    def test_plain_loops(self):
        paths = [
            'ISA_LOOP/GS_LOOP',
            'GS_LOOP',
            'ST_LOOP/DETAIL/2000',
            'GS_LOOP/ST_LOOP/DETAIL/2000A',
            'DETAIL/2000A/2000B',
            '2000A/2000B/2300',
            '2000B/2300/2400',
            'ST_LOOP/HEADER',
            'ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A',
            'GS_LOOP/ST_LOOP/HEADER/1000B'
        ]
        for spath in paths:
            plist = spath.split('/')
            rd = pyx12.path.X12Path(spath)
            self.assertEqual(rd.loop_list, plist,
                             '%s: %s != %s' % (spath, rd.loop_list, plist))


class AbsolutePath(unittest.TestCase):
    def test_paths_with_refdes(self):
        tests = [
            ('/AAA/TST', 'TST', None, None, None, ['AAA']),
            ('/B1000/TST02', 'TST', None, 2, None, ['B1000']),
            ('/1000B/TST03-2', 'TST', None, 3, 2, ['1000B']),
            ('/1000A/1000B/TST[AA]02', 'TST', 'AA', 2, None, [
                '1000A', '1000B']),
            ('/AA/BB/CC/TST[1B5]03-1', 'TST', '1B5', 3, 1, ['AA', 'BB', 'CC']),
            ('/DDD/E1000/N102', 'N1', None, 2, None, ['DDD', 'E1000']),
            ('/E1000/D322/N102-5', 'N1', None, 2, 5, ['E1000', 'D322']),
            ('/BB/CC/N1[AZR]02', 'N1', 'AZR', 2, None, ['BB', 'CC']),
            ('/BB/CC/N1[372]02-5', 'N1', '372', 2, 5, ['BB', 'CC'])
        ]
        for (spath, seg_id, qual, eleidx, subeleidx, plist) in tests:
            rd = pyx12.path.X12Path(spath)
            self.assertEqual(rd.relative, False,
                             '%s: %s != %s' % (spath, rd.relative, False))
            self.assertEqual(rd.seg_id, seg_id,
                             '%s: %s != %s' % (spath, rd.seg_id, seg_id))
            self.assertEqual(rd.id_val, qual, '%s: %s != %s' %
                             (spath, rd.id_val, qual))
            self.assertEqual(rd.ele_idx, eleidx,
                             '%s: %s != %s' % (spath, rd.ele_idx, eleidx))
            self.assertEqual(rd.subele_idx, subeleidx, '%s: %s != %s' %
                             (spath, rd.subele_idx, subeleidx))
            self.assertEqual(rd.format(), spath,
                             '%s: %s != %s' % (spath, rd.format(), spath))
            self.assertEqual(rd.loop_list, plist,
                             '%s: %s != %s' % (spath, rd.loop_list, plist))

    def test_bad_paths(self):
        bad_paths = [
            '/AA/03',
            '/BB/CC/03-2'
        ]
        for spath in bad_paths:
            self.assertRaises(X12PathError, pyx12.path.X12Path, spath)

    def test_plain_loops(self):
        paths = [
            '/ISA_LOOP/GS_LOOP',
            '/ISA_LOOP/GS_LOOP',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A',
            '/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B'
        ]
        for spath in paths:
            plist = spath.split('/')[1:]
            rd = pyx12.path.X12Path(spath)
            self.assertEqual(rd.loop_list, plist,
                             '%s: %s != %s' % (spath, rd.loop_list, plist))


class Equality(unittest.TestCase):
    def test_equal1(self):
        p1 = pyx12.path.X12Path('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A')
        p2 = pyx12.path.X12Path('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A')
        self.assertEqual(p1, p2)
        self.assertEqual(p1.format(), p2.format())
        self.assertEqual(p1.__hash__(), p2.__hash__())

    def test_equal2(self):
        p1 = pyx12.path.X12Path('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A')
        p2 = pyx12.path.X12Path('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/')
        p2.loop_list.append('2000A')
        self.assertEqual(p1, p2)
        self.assertEqual(p1.format(), p2.format())
        self.assertEqual(p1.__hash__(), p2.__hash__())

    def test_equal3(self):
        p1 = pyx12.path.X12Path('/AA/BB/CC/TST[1B5]03-1')
        p2 = pyx12.path.X12Path('/AA/BB/CC/AAA[1B5]03-1')
        p2.seg_id = 'TST'
        self.assertEqual(p1, p2)
        self.assertEqual(p1.format(), p2.format())
        self.assertEqual(p1.__hash__(), p2.__hash__())

    def test_equal4(self):
        p1 = pyx12.path.X12Path('1000B/TST03-2')
        p2 = pyx12.path.X12Path('1000B/TST04-2')
        p2.ele_idx = 3
        self.assertEqual(p1, p2)
        self.assertEqual(p1.format(), p2.format())
        self.assertEqual(p1.__hash__(), p2.__hash__())
        
    def test_equal5(self):
        x12path = pyx12.path.X12Path('/1000A/SD01')
        self.assertEqual(len(x12path.loop_list), 1)
        del x12path.loop_list[0]
        self.assertEqual(len(x12path.loop_list), 0)
        self.assertEqual(x12path.format(), '/SD01')
        self.assertEqual(x12path.seg_id, 'SD')
        self.assertEqual(x12path.ele_idx, 1)
        self.assertEqual(x12path.subele_idx, None)

    def test_equal6(self):
        x12path = pyx12.path.X12Path('/1000A/SD01')
        self.assertEqual(len(x12path.loop_list), 1)
        del x12path.loop_list[0]
        self.assertEqual(len(x12path.loop_list), 0)
        self.assertEqual(x12path.format(), '/SD01')
        self.assertEqual(x12path.seg_id, 'SD')
        self.assertEqual(x12path.ele_idx, 1)
        self.assertEqual(x12path.subele_idx, None)


class NonEquality(unittest.TestCase):
    def test_nequal1(self):
        p1 = pyx12.path.X12Path('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A')
        p2 = pyx12.path.X12Path('ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A')
        self.assertNotEqual(p1, p2)
        self.assertNotEqual(p1.format(), p2.format())
        self.assertNotEqual(p1.__hash__(), p2.__hash__())

    def test_nequal2(self):
        p1 = pyx12.path.X12Path('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A')
        p2 = pyx12.path.X12Path('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/')
        self.assertNotEqual(p1, p2)
        self.assertNotEqual(p1.format(), p2.format())
        self.assertNotEqual(p1.__hash__(), p2.__hash__())

    def test_nequal3(self):
        p1 = pyx12.path.X12Path('/AA/BB/CC/TST[1B5]03-1')
        p2 = pyx12.path.X12Path('/AA/BB/CC/AAA[1B5]03-1')
        self.assertNotEqual(p1, p2)
        self.assertNotEqual(p1.format(), p2.format())
        self.assertNotEqual(p1.__hash__(), p2.__hash__())

    def test_nequal4(self):
        p1 = pyx12.path.X12Path('1000B/TST03-2')
        p2 = pyx12.path.X12Path('1000B/TST04-2')
        self.assertNotEqual(p1, p2)
        self.assertNotEqual(p1.format(), p2.format())
        self.assertNotEqual(p1.__hash__(), p2.__hash__())


class Empty(unittest.TestCase):
    def test_not_empty_1(self):
        p1 = '1000B/TST03-2'
        self.assertFalse(pyx12.path.X12Path(
            p1).empty(), 'Path "%s" is not empty' % (p1))

    def test_not_empty_2(self):
        p1 = '/AA/BB/CC/AAA[1B5]03'
        self.assertFalse(pyx12.path.X12Path(
            p1).empty(), 'Path "%s" is not empty' % (p1))

    def test_not_empty_3(self):
        p1 = 'GS_LOOP/ST_LOOP/DETAIL/2000A'
        self.assertFalse(pyx12.path.X12Path(
            p1).empty(), 'Path "%s" is not empty' % (p1))

    def test_not_empty_4(self):
        p1 = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A'
        self.assertFalse(pyx12.path.X12Path(
            p1).empty(), 'Path "%s" is not empty' % (p1))

    def test_not_empty_5(self):
        p1 = '/'
        self.assertFalse(pyx12.path.X12Path(
            p1).empty(), 'Path "%s" is not empty' % (p1))

    def test_not_empty_6(self):
        p1 = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/'
        self.assertFalse(pyx12.path.X12Path(
            p1).empty(), 'Path "%s" is not empty' % (p1))

    def test_empty_1(self):
        p1 = ''
        a = pyx12.path.X12Path(p1)
        self.assertTrue(pyx12.path.X12Path(
            p1).empty(), 'Path "%s" is empty' % (p1))


class IsChild(unittest.TestCase):

    def testChildLoopOK1(self):
        path_str = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400'
        parent = pyx12.path.X12Path(path_str)
        self.assertTrue(parent.is_child_path('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/SV2'))

    def testChildLoopOK2(self):
        path_str = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400'
        parent = pyx12.path.X12Path(path_str)
        self.assertTrue(parent.is_child_path('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/2500/ASD'))

    def testLoopSegSame1(self):
        path_str = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400'
        parent = pyx12.path.X12Path(path_str)
        self.assertFalse(parent.is_child_path('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400'))

    #def testLoopSegSame2(self):
    #    path_str = '/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400'
    #    parent = pyx12.path.X12Path(path_str)
    #    self.assertFalse(parent.is_child_path('/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/2400/'))
