#! /usr/bin/env /usr/local/bin/python

import unittest
import sys, string
import StringIO
import os.path

import pyx12.x12xml_idtag
import pyx12.map_if
import pyx12.params
import pyx12.segment
from pyx12.errors import *
from pyx12.tests.x12xml_idtag import *

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ConvertToXML))
    return suite

#if __name__ == "__main__":
#    unittest.main()
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())
