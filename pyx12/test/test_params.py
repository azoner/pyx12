#! /usr/bin/env /usr/local/bin/python

import unittest
import sys

import pyx12.params
from pyx12.errors import *
from pyx12.tests.params import *

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Default))
    suite.addTest(unittest.makeSuite(SetParamOverride))
    suite.addTest(unittest.makeSuite(ReadConfigFile))
    return suite

#if __name__ == "__main__":
#    unittest.main()
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())
