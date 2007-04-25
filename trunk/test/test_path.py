#! /usr/bin/env /usr/local/bin/python

import unittest

import pyx12.path
from pyx12.errors import *
from pyx12.tests.path import *

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AbsPath))
    suite.addTest(unittest.makeSuite(Format))
    return suite

#if __name__ == "__main__":
#    unittest.main()
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())

