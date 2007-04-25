#! /usr/bin/env /usr/local/bin/python

import os.path, sys, string
import unittest

import pyx12.map_index
import pyx12.params
from pyx12.tests.map_index import *

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetFilename))
    return suite

try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())
