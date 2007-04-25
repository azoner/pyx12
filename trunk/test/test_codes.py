#! /usr/bin/env /usr/local/bin/python

import os.path, sys, string
import unittest
#import pdb

import pyx12.codes
import pyx12.error_handler
#from error_handler import ErrorErrhNull
from pyx12.errors import *
import pyx12.map_if
import pyx12.params

from pyx12.tests.codes import *

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestExternal))
    return suite

#if __name__ == "__main__":
#    unittest.main()
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())
