#! /usr/bin/env python

import sys
sys.path.insert(0, '..')
import unittest

#from pyx12.tests.xmlwriter import *
import pyx12.tests.xmlwriter
from helper import get_testcases, print_testcases, get_suite

ns = pyx12.tests.xmlwriter
if len(sys.argv) > 1 and sys.argv[1] == '-h':
    print_testcases(ns)
else:
    unittest.TextTestRunner(verbosity=2).run(get_suite(ns, sys.argv[1:]))
