#! /usr/bin/env /usr/local/bin/python

#import test_support
#from test_support import TestFailed, have_unicode
import unittest
import sys
import StringIO

import error_handler
from utils import *
from errors import *
import x12file

class pyx12LibraryTests(unittest.TestCase):

    def test_valid_codes_basic_N(self):
        self.failUnless(IsValidDataType('1', 'N', 'B'))
        self.failUnless(IsValidDataType('-1', 'N', 'B'))
        self.failUnless(IsValidDataType('10', 'N', 'B'))
        self.failUnless(IsValidDataType('-10', 'N', 'B'))
        self.failIf(IsValidDataType('+10', 'N', 'B'))
        self.failIf(IsValidDataType('1.', 'N', 'B'))
        self.failIf(IsValidDataType('-1.', 'N', 'B'))
        self.failUnless(IsValidDataType('0000500', 'N', 'B'))
        self.failUnless(IsValidDataType('1', 'R', 'B'))

    def test_valid_codes_basic_R(self):
        self.failUnless(IsValidDataType('-331232', 'R', 'B'))
        self.failIf(IsValidDataType('+331232', 'R', 'B'))
        self.failIf(IsValidDataType('123,456,789.123', 'R', 'B'))
        self.failIf(IsValidDataType('333.', 'R', 'B'))
        self.failUnless(IsValidDataType('1.325', 'R', 'B'))
        self.failUnless(IsValidDataType('.024', 'R', 'B'))
        self.failIf(IsValidDataType('a.603', 'R', 'B'))
        self.failIf(IsValidDataType('0.0b', 'R', 'B'))

    def test_valid_codes_basic_ID(self):
        self.failIf(IsValidDataType('abc', 'ID', 'B'))
        self.failUnless(IsValidDataType('10&3', 'ID', 'B'))
        self.failUnless(IsValidDataType('  XYZ', 'ID', 'B'))
        self.failIf(IsValidDataType('abc   ', 'ID', 'B'))

    def test_valid_codes_basic_AN(self):
        self.failUnless(IsValidDataType('LKJS\\', 'AN', 'B'))
        self.failIf(IsValidDataType('abd1P', 'AN', 'B'))
        self.failUnless(IsValidDataType('THIS IS A TEST ()', 'AN', 'B'))
        self.failUnless(IsValidDataType(r"""BASIC ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?=""", 'AN', 'B'))
        self.failIf(IsValidDataType(r'entended abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$', 'AN', 'B'))
        self.failIf(IsValidDataType(r"""Both ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?= abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$""", 'AN', 'B'))
        self.failIf(IsValidDataType('bad ^`', 'AN', 'B'))
        self.failIf(IsValidDataType('wharf', 'AN', 'B'))

    def test_valid_codes_basic_DT(self):
        self.failUnless(IsValidDataType('20010418', 'DT', 'B'))
        self.failIf(IsValidDataType('19992377', 'DT', 'B'))
        self.failIf(IsValidDataType('19991277', 'DT', 'B'))
        self.failIf(IsValidDataType('200204a', 'DT', 'B'))
        self.failIf(IsValidDataType('2002041a', 'DT', 'B'))
        self.failUnless(IsValidDataType('20030429', 'DT', 'B'))
        self.failIf(IsValidDataType('19000229', 'DT', 'B'))
        self.failUnless(IsValidDataType('19040229', 'DT', 'B'))
        self.failUnless(IsValidDataType('20000229', 'DT', 'B'))
        self.failUnless(IsValidDataType('20040229', 'DT', 'B'))
        self.failIf(IsValidDataType('20030229', 'DT', 'B'))
        self.failUnless(IsValidDataType('020414', 'DT', 'B'))
        self.failIf(IsValidDataType('990229', 'DT', 'B'))
        self.failUnless(IsValidDataType('960229', 'DT', 'B'))
        self.failIf(IsValidDataType('030732', 'DT', 'B'))

    def test_valid_codes_basic_TM(self):
        self.failUnless(IsValidDataType('0731', 'TM', 'B'))
        self.failIf(IsValidDataType('07315a', 'TM', 'B'))
        self.failUnless(IsValidDataType('000159', 'TM', 'B'))

    def test_valid_codes_extended_N(self):
        self.failUnless(IsValidDataType('1', 'N', 'E'))
        self.failUnless(IsValidDataType('-1', 'N', 'E'))
        self.failUnless(IsValidDataType('10', 'N', 'E'))
        self.failUnless(IsValidDataType('-10', 'N', 'E'))
        self.failIf(IsValidDataType('+10', 'N', 'E'))
        self.failIf(IsValidDataType('1.', 'N', 'E'))
        self.failIf(IsValidDataType('-1.', 'N', 'E'))
        self.failUnless(IsValidDataType('0000500', 'N', 'E'))

    def test_valid_codes_extended_R(self):
        self.failUnless(IsValidDataType('1', 'R', 'E'))
        self.failUnless(IsValidDataType('-331232', 'R', 'E'))
        self.failIf(IsValidDataType('+331232', 'R', 'E'))
        self.failIf(IsValidDataType('123,456,789.123', 'R', 'E'))
        self.failIf(IsValidDataType('333.', 'R', 'E'))
        self.failUnless(IsValidDataType('1.325', 'R', 'E'))
        self.failUnless(IsValidDataType('.024', 'R', 'E'))
        self.failIf(IsValidDataType('a.603', 'R', 'E'))
        self.failIf(IsValidDataType('0.0b', 'R', 'E'))

    def test_valid_codes_extended_ID(self):
        self.failUnless(IsValidDataType('abc', 'ID', 'E'))
        self.failUnless(IsValidDataType('10&3', 'ID', 'E'))
        self.failUnless(IsValidDataType('  XYZ', 'ID', 'E'))
        self.failUnless(IsValidDataType('abc   ', 'ID', 'E'))

    def test_valid_codes_extended_AN(self):
        self.failUnless(IsValidDataType('LKJS\\', 'AN', 'E'))
        self.failUnless(IsValidDataType('abd1P', 'AN', 'E'))
        self.failUnless(IsValidDataType('THIS IS A TEST ()', 'AN', 'E'))
        self.failUnless(IsValidDataType("""BASIC ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?=""", 'AN', 'E'))
        self.failUnless(IsValidDataType('entended abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$', 'AN', 'E'))
        self.failUnless(IsValidDataType("""Both ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?= abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$""", 'AN', 'E'))
        self.failIf(IsValidDataType('bad ^`', 'AN', 'E'))
        self.failUnless(IsValidDataType('wharf', 'AN', 'E'))

    def test_valid_codes_extended_DT(self):
        self.failUnless(IsValidDataType('20010418', 'DT', 'E'))
        self.failIf(IsValidDataType('19992377', 'DT', 'E'))
        self.failIf(IsValidDataType('19991277', 'DT', 'E'))
        self.failIf(IsValidDataType('200204a', 'DT', 'E'))
        self.failIf(IsValidDataType('2002041a', 'DT', 'E'))
        self.failUnless(IsValidDataType('20030429', 'DT', 'E'))
        self.failIf(IsValidDataType('19000229', 'DT', 'E'))
        self.failUnless(IsValidDataType('19040229', 'DT', 'E'))
        self.failUnless(IsValidDataType('20000229', 'DT', 'E'))
        self.failUnless(IsValidDataType('20040229', 'DT', 'E'))
        self.failIf(IsValidDataType('20030229', 'DT', 'E'))
        self.failUnless(IsValidDataType('020414', 'DT', 'E'))
        self.failIf(IsValidDataType('990229', 'DT', 'E'))
        self.failUnless(IsValidDataType('960229', 'DT', 'E'))
        self.failIf(IsValidDataType('030732', 'DT', 'E'))

    def test_valid_codes_extended_TM(self):
        self.failUnless(IsValidDataType('0731', 'TM', 'E'))
        self.failIf(IsValidDataType('07315a', 'TM', 'E'))
        self.failUnless(IsValidDataType('000159', 'TM', 'E'))


class x12fileTests(unittest.TestCase):

    def test_x12file_headers(self):
        fd = StringIO.StringIO(' ISA~')
        errh = error_handler.err_handler()
        self.assertRaises(x12Error, x12file.x12file(fd, errh))
        #self.failUnless(IsValidDataType('1', 'N', 'B'))
        #self.failIf(IsValidDataType('+10', 'N', 'B'))

#def test_main():
    #loader = unittest.TestLoader()
    #suite = unittest.TestSuite()
    #suite.addTest(loader.loadTestsFromTestCase(pyx12LibraryTests))
    #run_suite(suite)
    #suite = unittest.makeSuite(pyx12LibraryTests,'test')
    #suite.addTest(WidgetTestCase("pyx12LibraryTests"))
    #suite.addTest(loader.loadTestsFromTestCase(pyx12LibraryTests))
    #suite.run()
#    test_support.run_unittest(pyx12LibraryTests)


#if __name__ == "__main__":
#    test_main()
 
if __name__ == "__main__":
    unittest.main()   
