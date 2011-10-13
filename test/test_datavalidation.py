#! /usr/bin/env /usr/local/bin/python

#import test_support
#from test_support import TestFailed, have_unicode
import unittest
import sys

from pyx12.datavalidation import IsValidDataType
from pyx12.errors import *
from pyx12.tests.test_datavalidation import *

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicNumeric))
    suite.addTest(unittest.makeSuite(BasicReal))
    suite.addTest(unittest.makeSuite(BasicIdentifier))
    suite.addTest(unittest.makeSuite(BasicString))
    suite.addTest(unittest.makeSuite(BasicDate))
    suite.addTest(unittest.makeSuite(BasicTime))
    suite.addTest(unittest.makeSuite(ExtendedNumeric))
    suite.addTest(unittest.makeSuite(ExtendedReal))
    suite.addTest(unittest.makeSuite(ExtendedIdentifier))
    suite.addTest(unittest.makeSuite(ExtendedString))
    suite.addTest(unittest.makeSuite(ExtendedDate))
    suite.addTest(unittest.makeSuite(ExtendedTime))
    return suite

#if __name__ == "__main__":
#    unittest.main()
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())
