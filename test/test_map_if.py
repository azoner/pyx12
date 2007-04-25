#! /usr/bin/env /usr/local/bin/python

import os, os.path, sys
import string
import unittest
#import pdb

import pyx12.error_handler
from pyx12.errors import *
import pyx12.map_if
import pyx12.params 
import pyx12.segment

from pyx12.tests.map_if import *

def suite(args):
    suite = unittest.TestSuite()
    if args:
        for arg in args:
            if arg == 'GetNodeByPath':
                suite.addTest(unittest.makeSuite(GetNodeByPath))
            elif arg == 'TrailingSpaces':
                suite.addTest(unittest.makeSuite(TrailingSpaces))
            elif arg == 'CompositeRequirement':
                suite.addTest(unittest.makeSuite(CompositeRequirement))
            elif arg == 'ElementRequirement':
                suite.addTest(unittest.makeSuite(ElementRequirement))
            elif arg == 'ElementIsValid':
                suite.addTest(unittest.makeSuite(ElementIsValid))
            elif arg == 'ElementIsValidDate':
                suite.addTest(unittest.makeSuite(ElementIsValidDate))
            elif arg == 'SegmentIsValid':
                suite.addTest(unittest.makeSuite(SegmentIsValid))
            elif arg == 'MapTransform':
                suite.addTest(unittest.makeSuite(MapTransform))
    else:
        suite.addTest(unittest.makeSuite(GetNodeByPath))
        suite.addTest(unittest.makeSuite(TrailingSpaces))
        suite.addTest(unittest.makeSuite(CompositeRequirement))
        suite.addTest(unittest.makeSuite(ElementRequirement))
        suite.addTest(unittest.makeSuite(ElementIsValid))
        suite.addTest(unittest.makeSuite(ElementIsValidDate))
        suite.addTest(unittest.makeSuite(SegmentIsValid))
        suite.addTest(unittest.makeSuite(MapTransform))
    return suite
                
#if __name__ == "__main__":
#    unittest.main()   
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite(sys.argv[1:]))
