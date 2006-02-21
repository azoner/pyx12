#! /usr/bin/env /usr/local/bin/python

#    $Id$

import sys, string
import os.path
import unittest

import pyx12.error_handler
from pyx12.errors import *
from pyx12.map_walker import walk_tree
import pyx12.map_if
import pyx12.params 
import pyx12.segment
from pyx12.tests.map_walker import *

def suite(args):
    suite = unittest.TestSuite()
    if args:
        for arg in args:
            if arg == 'Explicit_Loops':
                suite.addTest(unittest.makeSuite(Explicit_Loops))
            elif arg == 'Implicit_Loops':
                suite.addTest(unittest.makeSuite(Implicit_Loops))
            elif arg == 'SegmentWalk':
                suite.addTest(unittest.makeSuite(SegmentWalk))
            elif arg == 'Segment_ID_Checks':
                suite.addTest(unittest.makeSuite(Segment_ID_Checks))
            elif arg == 'Counting':
                suite.addTest(unittest.makeSuite(Counting))
            elif arg == 'LoopCounting':
                suite.addTest(unittest.makeSuite(LoopCounting))
            elif arg == 'CountOrdinal':
                suite.addTest(unittest.makeSuite(CountOrdinal))
    else:
        suite.addTest(unittest.makeSuite(Explicit_Loops))
        suite.addTest(unittest.makeSuite(Implicit_Loops))
        suite.addTest(unittest.makeSuite(SegmentWalk))
        suite.addTest(unittest.makeSuite(Segment_ID_Checks))
        suite.addTest(unittest.makeSuite(Counting))
        suite.addTest(unittest.makeSuite(LoopCounting))
        suite.addTest(unittest.makeSuite(CountOrdinal))
    return suite

try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite(sys.argv[1:]))

