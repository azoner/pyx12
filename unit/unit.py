#! /usr/bin/env /usr/local/bin/python


import unittest

def suite():
    modules_to_test = ('unit_x12file', 'unit_utils', 'unit_map_if', \
        'unit_map_walker') # and so on
    alltests = unittest.TestSuite()
    for module in map(__import__, modules_to_test):
        alltests.addTest(unittest.findTestCases(module))
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
