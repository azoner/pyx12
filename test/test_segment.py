#! /usr/bin/env /usr/local/bin/python

import unittest

import pyx12.segment

class ArbitraryDelimiters(unittest.TestCase):

    def setUp(self):
        self.seg_str = 'TST&AA!1!1&BB!5&ZZ'
        self.seg = pyx12.segment.segment(self.seg_str, '+', '&', '!')

    def test_identity(self):
        self.assertEqual(self.seg_str+'+', self.seg.__repr__())

    def test_get_seg_id(self):
        self.assertEqual(self.seg.get_seg_id(), 'TST')

    def test_len(self):
        self.assertEqual(len(self.seg), 3)

    def test_getitem3(self):
        self.assertEqual(self.seg[3].__repr__(), 'ZZ')
                    
    def test_getitem_0(self):
        self.failUnlessRaises(IndexError, self.seg.__getitem__, 0)
                    
    def test_getitem1(self):
        self.assertEqual(self.seg[1].__repr__(), 'AA!1!1')
                    
    def test_getitem_minus_1(self):
        self.assertEqual(self.seg[-1].__repr__(), 'ZZ')
                    
    def test_other_terms(self):
        self.assertEqual(self.seg.format('~', '*', ':', ''), 'TST*AA:1:1*BB:5*ZZ~')

class Identity(unittest.TestCase):

    def setUp(self):
        pass

    def test_identity(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.assertEqual(seg.__repr__(), seg_str+'~')

    def test_identity1(self):
        seg_str = 'ISA*00*          *00*          *ZZ*ZZ000          *'
        seg_str += 'ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:\n'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.assertEqual(seg.__repr__(), seg_str+'~')

    def test_identity3(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ~'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.assertEqual(seg.__repr__(), seg_str)


class Alter(unittest.TestCase):

    def test_alter_element(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        seg[3] = 'YY'
        self.assertEqual(seg.__repr__(), 'TST*AA:1:1*BB:5*YY~')

class Composite(unittest.TestCase):

    def setUp(self):
        seg_str = 'TST*AA:1:Y*BB:5*ZZ'
        self.seg = pyx12.segment.segment(seg_str, '~', '*', ':')

    def test_composite_is_a(self):
        self.failUnless(self.seg[1].is_composite())
        
    def test_composite_len(self):
        self.assertEqual(len(self.seg[1]), 3)

    def test_composite_indexing(self):
        self.assertEqual(self.seg[1][0], 'AA')
        self.assertEqual(self.seg[1][2], 'Y')
        self.assertEqual(self.seg[1][-1], 'Y')
        self.failUnlessRaises(IndexError, lambda x: self.seg[1][x], 3)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ArbitraryDelimiters))
    suite.addTest(unittest.makeSuite(Identity))
    suite.addTest(unittest.makeSuite(Alter))
    suite.addTest(unittest.makeSuite(Composite))
    return suite

#if __name__ == "__main__":
#    unittest.main()
unittest.TextTestRunner(verbosity=2).run(suite())


