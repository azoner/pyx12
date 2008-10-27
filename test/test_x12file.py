#! /usr/bin/env /usr/local/bin/python

import sys
import unittest

from pyx12.tests.x12file import *
from helper import get_testcases, print_testcases, get_suite

try:
    import psyco
    psyco.full()
except ImportError:
    pass
ns = pyx12.tests.x12file
if len(sys.argv) > 1 and sys.argv[1] == '-h':
    print_testcases(ns)
else:
    unittest.TextTestRunner(verbosity=2).run(get_suite(ns, sys.argv[1:]))
