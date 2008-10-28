#! /usr/bin/env /usr/local/bin/python

import unittest
#import sys
import tempfile
import StringIO

import pyx12.error_handler
#from error_handler import ErrorErrhNull
from pyx12.errors import *
import pyx12.x12context
import pyx12.params

class Delimiters(unittest.TestCase):

    def test_arbitrary_delimiters(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str1 += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&004010X098A1+\n'
        str1 += 'ST&837&11280001+\n'
        str1 += 'REF&87&004010X098A1+\n'
        str1 += 'SE&3&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        fd = StringIO.StringIO(str1)
        fd.seek(0)
        param = pyx12.params.params('pyx12.conf.xml')
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(param, errh, fd, xslt_files = [])
        for datatree in src.iter_segments():
            pass
        self.assertEqual(src.subele_term, '!')
        self.assertEqual(src.ele_term, '&')
        self.assertEqual(src.seg_term, '+')

    def test_binary_delimiters(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str1 += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&004010X098A1+\n'
        str1 += 'ST&837&11280001+\n'
        str1 += 'REF&87&004010X098A1+\n'
        str1 += 'SE&3&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        str1 = str1.replace('&', chr(0x1C))
        str1 = str1.replace('+', chr(0x1D))
        str1 = str1.replace('!', chr(0x1E))
        fd = StringIO.StringIO(str1)
        fd.seek(0)
        errors = []
        param = pyx12.params.params('pyx12.conf.xml')
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(param, errh, fd, xslt_files = [])
        for datatree in src.iter_segments():
            pass
        self.assertEqual(src.subele_term, chr(0x1E))
        self.assertEqual(src.ele_term, chr(0x1C))
        self.assertEqual(src.seg_term, chr(0x1D))
