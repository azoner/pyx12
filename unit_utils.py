#! /usr/bin/env /usr/local/bin/python

#import test_support
#from test_support import TestFailed, have_unicode
import unittest
import sys

from utils import *
from errors import *

class BasicNumeric(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('1', 'N', 'B'))
        self.failUnless(IsValidDataType('-1', 'N', 'B'))
        self.failUnless(IsValidDataType('10', 'N', 'B'))
        self.failUnless(IsValidDataType('-10', 'N', 'B'))
        self.failUnless(IsValidDataType('0000500', 'N', 'B'))
        self.failUnless(IsValidDataType('1', 'R', 'B'))

    def testInvalid(self):
        self.failIf(IsValidDataType('+10', 'N', 'B'))
        self.failIf(IsValidDataType('1.', 'N', 'B'))
        self.failIf(IsValidDataType('-1.', 'N', 'B'))

class BasicReal(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('-331232', 'R', 'B'))
        self.failUnless(IsValidDataType('1.325', 'R', 'B'))
        self.failUnless(IsValidDataType('.024', 'R', 'B'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('+331232', 'R', 'B'))
        self.failIf(IsValidDataType('123,456,789.123', 'R', 'B'))
        self.failIf(IsValidDataType('333.', 'R', 'B'))
        self.failIf(IsValidDataType('a.603', 'R', 'B'))
        self.failIf(IsValidDataType('0.0b', 'R', 'B'))

class BasicIdentifier(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('10&3', 'ID', 'B'))
        self.failUnless(IsValidDataType('  XYZ', 'ID', 'B'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('abc', 'ID', 'B'))
        self.failIf(IsValidDataType('abc   ', 'ID', 'B'))

class BasicString(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('LKJS\\', 'AN', 'B'))
        self.failUnless(IsValidDataType('THIS IS A TEST ()', 'AN', 'B'))
        self.failUnless(IsValidDataType(r"""BASIC ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?=""", 'AN', 'B'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('abd1P', 'AN', 'B'))
        self.failIf(IsValidDataType(r'extended abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$', 'AN', 'B'))
        self.failIf(IsValidDataType(r"""Both ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?= abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$""", 'AN', 'B'))
        self.failIf(IsValidDataType('bad ^`', 'AN', 'B'))
        self.failIf(IsValidDataType('wharf', 'AN', 'B'))

class BasicDate(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('20010418', 'DT', 'B'))
        self.failUnless(IsValidDataType('20030429', 'DT', 'B'))
        self.failUnless(IsValidDataType('19040229', 'DT', 'B'))
        self.failUnless(IsValidDataType('20000229', 'DT', 'B'))
        self.failUnless(IsValidDataType('20040229', 'DT', 'B'))
        self.failUnless(IsValidDataType('020414', 'DT', 'B'))
        self.failUnless(IsValidDataType('960229', 'DT', 'B'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('990229', 'DT', 'B'))
        self.failIf(IsValidDataType('20030229', 'DT', 'B'))
        self.failIf(IsValidDataType('19000229', 'DT', 'B'))
        self.failIf(IsValidDataType('19992377', 'DT', 'B'))
        self.failIf(IsValidDataType('19991277', 'DT', 'B'))
        self.failIf(IsValidDataType('200204a', 'DT', 'B'))
        self.failIf(IsValidDataType('2002041a', 'DT', 'B'))
        self.failIf(IsValidDataType('030732', 'DT', 'B'))

class BasicTime(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('0731', 'TM', 'B'))
        self.failUnless(IsValidDataType('000159', 'TM', 'B'))

    def testInvalid(self):
        self.failIf(IsValidDataType('07315a', 'TM', 'B'))
        self.failIf(IsValidDataType('7 31', 'TM', 'B'))
        self.failIf(IsValidDataType('7:31', 'TM', 'B'))

class ExtendedNumeric(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('1', 'N', 'E'))
        self.failUnless(IsValidDataType('-1', 'N', 'E'))
        self.failUnless(IsValidDataType('10', 'N', 'E'))
        self.failUnless(IsValidDataType('-10', 'N', 'E'))
        self.failUnless(IsValidDataType('0000500', 'N', 'E'))

    def testInvalid(self):
        self.failIf(IsValidDataType('+10', 'N', 'E'))
        self.failIf(IsValidDataType('1.', 'N', 'E'))
        self.failIf(IsValidDataType('-1.', 'N', 'E'))

class ExtendedReal(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('1', 'R', 'E'))
        self.failUnless(IsValidDataType('-331232', 'R', 'E'))
        self.failUnless(IsValidDataType('1.325', 'R', 'E'))
        self.failUnless(IsValidDataType('.024', 'R', 'E'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('a.603', 'R', 'E'))
        self.failIf(IsValidDataType('0.0b', 'R', 'E'))
        self.failIf(IsValidDataType('+331232', 'R', 'E'))
        self.failIf(IsValidDataType('123,456,789.123', 'R', 'E'))
        self.failIf(IsValidDataType('333.', 'R', 'E'))

class ExtendedIdentifier(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('abc', 'ID', 'E'))
        self.failUnless(IsValidDataType('10&3', 'ID', 'E'))
        self.failUnless(IsValidDataType('  XYZ', 'ID', 'E'))
        self.failUnless(IsValidDataType('abc   ', 'ID', 'E'))

class ExtendedString(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('LKJS\\', 'AN', 'E'))
        self.failUnless(IsValidDataType('abd1P', 'AN', 'E'))
        self.failUnless(IsValidDataType('THIS IS A TEST ()', 'AN', 'E'))
        self.failUnless(IsValidDataType("""BASIC ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?=""", 'AN', 'E'))
        self.failUnless(IsValidDataType('extended abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$', 'AN', 'E'))
        self.failUnless(IsValidDataType("""Both ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?= abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$""", 'AN', 'E'))
        self.failUnless(IsValidDataType('wharf', 'AN', 'E'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('bad ^`', 'AN', 'E'))

class ExtendedDate(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('20010418', 'DT', 'E'))
        self.failUnless(IsValidDataType('20030429', 'DT', 'E'))
        self.failUnless(IsValidDataType('19040229', 'DT', 'E'))
        self.failUnless(IsValidDataType('20000229', 'DT', 'E'))
        self.failUnless(IsValidDataType('20040229', 'DT', 'E'))
        self.failUnless(IsValidDataType('020414', 'DT', 'E'))
        self.failUnless(IsValidDataType('960229', 'DT', 'E'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('990229', 'DT', 'E'))
        self.failIf(IsValidDataType('030732', 'DT', 'E'))
        self.failIf(IsValidDataType('19992377', 'DT', 'E'))
        self.failIf(IsValidDataType('19991277', 'DT', 'E'))
        self.failIf(IsValidDataType('200204a', 'DT', 'E'))
        self.failIf(IsValidDataType('2002041a', 'DT', 'E'))
        self.failIf(IsValidDataType('19000229', 'DT', 'E'))
        self.failIf(IsValidDataType('20030229', 'DT', 'E'))

class ExtendedTime(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('0731', 'TM', 'E'))
        self.failUnless(IsValidDataType('000159', 'TM', 'E'))

    def testInvalid(self):
        self.failIf(IsValidDataType('07315a', 'TM', 'E'))
        self.failIf(IsValidDataType('7 31', 'TM', 'B'))
        self.failIf(IsValidDataType('7:31', 'TM', 'B'))
    

def suite():
    suite1 = unittest.makeSuite(BasicNumeric)
    suite2 = unittest.makeSuite(BasicReal)
    suite3 = unittest.makeSuite(BasicIdentifier)
    suite4 = unittest.makeSuite(BasicString)
    suite5 = unittest.makeSuite(BasicDate)
    suite6 = unittest.makeSuite(BasicTime)
    suite7 = unittest.makeSuite(ExtendedNumeric)
    suite8 = unittest.makeSuite(ExtendedReal)
    suite9 = unittest.makeSuite(ExtendedIdentifier)
    suite10 = unittest.makeSuite(ExtendedString)
    suite11 = unittest.makeSuite(ExtendedDate)
    suite12 = unittest.makeSuite(ExtendedTime)
    return unittest.TestSuite((suite1, suite2, suite3, suite4, suite5, \
        suite6, suite7, suite8, suite9, suite10, suite11, suite12))


#    suite = unittest.TestSuite()

#    suite.addTests((\
#        unittest.makeSuite(x12fileTests, 'test_x12file_headers'), \
#    ))
#    return suite

if __name__ == "__main__":
    unittest.main()   

