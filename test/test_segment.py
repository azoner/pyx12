#! /usr/bin/env /usr/local/bin/python

import unittest

import pyx12.segment
from pyx12.errors import *
from pyx12.tests.segment import *

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ArbitraryDelimiters))
    suite.addTest(unittest.makeSuite(Identity))
    suite.addTest(unittest.makeSuite(Alter))
    suite.addTest(unittest.makeSuite(Composite))
    suite.addTest(unittest.makeSuite(Simple))
    suite.addTest(unittest.makeSuite(RefDes))
    suite.addTest(unittest.makeSuite(Indexing))
    suite.addTest(unittest.makeSuite(IsEmpty))
    suite.addTest(unittest.makeSuite(IsValidSegID))
    return suite

#if __name__ == "__main__":
#    unittest.main()
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())


