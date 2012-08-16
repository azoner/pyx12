#! /usr/bin/env python

import unittest


def suite():
    modules_to_test = (
        'test_codes',
        'test_dataele',
        'test_map_if',
        'test_map_index',
        'test_map_unique',
        'test_map_walker',
        'test_params',
        'test_path',
        'test_rawx12file',
        'test_segment',
        'test_syntax',
        'test_validation',
        'test_x12context',
        'test_x12file',
        'test_x12n_document',
        'test_xmlwriter',
        'test_x12n_document',
        'test_xmlx12_simple',
    )
    alltests = unittest.TestSuite()
    for module in map(__import__, modules_to_test):
        alltests.addTest(unittest.findTestCases(module))
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
