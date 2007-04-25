#! /usr/bin/env /usr/local/bin/python

import os, os.path
import string
import unittest
#import pdb

import pyx12.error_handler
from pyx12.errors import *
import pyx12.map_if
from pyx12.params import params
import pyx12.segment
from pyx12.tests.syntax import *

def suite():
    #suite = unittest.makeSuite((Test_getnodebypath, IsValidSyntax, \
    #    IsValidSyntaxP, IsValidSyntaxR, IsValidSyntaxC, \
    #    IsValidSyntaxE, IsValidSyntaxL))
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IsValidSyntax))
    suite.addTest(unittest.makeSuite(IsValidSyntaxP))
    suite.addTest(unittest.makeSuite(IsValidSyntaxR))
    suite.addTest(unittest.makeSuite(IsValidSyntaxC))
    suite.addTest(unittest.makeSuite(IsValidSyntaxE))
    suite.addTest(unittest.makeSuite(IsValidSyntaxL))
    return suite
                
#if __name__ == "__main__":
#    unittest.main()   
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())
