#! /usr/bin/env /usr/local/bin/python

import unittest
import StringIO

import pyx12.error_handler
from pyx12.errors import *
import pyx12.rawx12file

class Delimiters(unittest.TestCase):

    def test_arbitrary_delimiters(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str1 += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&004010X098+\n'
        str1 += 'ST&837&11280001+\n'
        str1 += 'TST&AA!1!1&BB!5+\n'
        str1 += 'SE&3&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        fd = StringIO.StringIO(str1)
        fd.seek(0)
        src = pyx12.x12file.RawX12file(fd)
        for seg in src:
            pass
        (seg_term, ele_term, subele_term, eol) = src.get_term()
        self.assertEqual(subele_term, '!')
        self.assertEqual(ele_term, '&')
        self.assertEqual(seg_term, '+')

    def test_binary_delimiters(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str1 += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&004010X098+\n'
        str1 += 'ST&837&11280001+\n'
        str1 += 'TST&AA!1!1&BB!5+\n'
        str1 += 'SE&3&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        str1 = str1.replace('&', chr(0x1C))
        str1 = str1.replace('+', chr(0x1D))
        str1 = str1.replace('!', chr(0x1E))
        fd = StringIO.StringIO(str1)
        fd.seek(0)
        src = pyx12.x12file.RawX12file(fd)
        for seg in src:
            pass
        (seg_term, ele_term, subele_term, eol) = src.get_term()
        self.assertEqual(subele_term, chr(0x1E))
        self.assertEqual(ele_term, chr(0x1C))
        self.assertEqual(seg_term, chr(0x1D))


class ISA_header(X12fileTestCase):

    def test_starts_with_ISA(self):
        fd = StringIO.StringIO(' ISA~')
        fd.seek(0)
        self.failUnlessRaises(pyx12.errors.X12Error, pyx12.rawx12file.RawX12file, fd)

    def test_at_least_ISA_len(self):
        fd = StringIO.StringIO('ISA~')
        fd.seek(0)
        self.failUnlessRaises(pyx12.errors.X12Error, pyx12.rawx12file.RawX12file, fd)


#class Formatting(unittest.TestCase):
#    def test_identity(self):
#        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
#        str1 += 'IEA*1*000010121~\n'
#        fd = StringIO.StringIO(str1)
#        fd.seek(0)
#        src = pyx12.rawx12file.RawX12file(fd)
#        str_out = ''
#        for seg in src:
#            str_out += seg.format() + '\n'
#        self.assertEqual(str1, str_out)
