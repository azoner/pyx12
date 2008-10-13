#! /usr/bin/env /usr/local/bin/python


import unittest

def suite():
    modules_to_test = ('test_x12file', 'test_utils', 'test_map_if', \
        'test_map_walker', 'test_codes', 'test_segment', 'test_syntax', \
        'test_path', 'test_x12xml_idtag', 'test_map_index', 'test_dataele', \
        'text_x12context')
    alltests = unittest.TestSuite()
    for module in map(__import__, modules_to_test):
        alltests.addTest(unittest.findTestCases(module))
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
