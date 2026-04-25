import unittest
from io import StringIO

import pyx12.error_handler
from pyx12.errors import *
import pyx12.rawx12file


class X12fileTestCase(unittest.TestCase):

    def _makeFd(self, x12str=None):
        try:
            if x12str:
                fd = StringIO(x12str)
            else:
                fd = StringIO()
        except:
            if x12str:
                fd = StringIO(x12str, encoding='ascii')
            else:
                fd = StringIO(encoding='ascii')
        fd.seek(0)
        return fd


class RawDelimiters(X12fileTestCase):

    def test_arbitrary_delimiters(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str1 += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&004010X098+\n'
        str1 += 'ST&837&11280001+\n'
        str1 += 'TST&AA!1!1&BB!5+\n'
        str1 += 'SE&3&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        fd = self._makeFd(str1)
        src = pyx12.rawx12file.RawX12File(fd)
        ct = 0
        for seg in src:
            ct += 1
        (seg_term, ele_term, subele_term, eol,
            repetition_term) = src.get_term()
        self.assertEqual(subele_term, '!')
        self.assertEqual(ele_term, '&')
        self.assertEqual(seg_term, '+')
        self.assertEqual(repetition_term, None)
        self.assertEqual(ct, 7)

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
        fd = self._makeFd(str1)
        src = pyx12.rawx12file.RawX12File(fd)
        ct = 0
        for seg in src:
            ct += 1
        (seg_term, ele_term, subele_term, eol,
            repetition_term) = src.get_term()
        self.assertEqual(subele_term, chr(0x1E))
        self.assertEqual(ele_term, chr(0x1C))
        self.assertEqual(seg_term, chr(0x1D))
        self.assertEqual(repetition_term, None)
        self.assertEqual(ct, 7)

    def test_arbitrary_delimiters_5010(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&^&00501&000010121&0&T&!+\n'
        str1 += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&005010X218+\n'
        str1 += 'ST&837&11280001+\n'
        str1 += 'TST&AA!1!1&BB!5+\n'
        str1 += 'SE&3&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        fd = self._makeFd(str1)
        src = pyx12.rawx12file.RawX12File(fd)
        ct = 0
        for seg in src:
            ct += 1
        (seg_term, ele_term, subele_term, eol,
            repetition_term) = src.get_term()
        self.assertEqual(subele_term, '!')
        self.assertEqual(ele_term, '&')
        self.assertEqual(seg_term, '+')
        self.assertEqual(repetition_term, '^')
        self.assertEqual(ct, 7)

    def test_binary_delimiters_5010(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&^&00501&000010121&0&T&!+\n'
        str1 += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&005010X218+\n'
        str1 += 'ST&837&11280001+\n'
        str1 += 'TST&AA!1!1&BB!5+\n'
        str1 += 'SE&3&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        str1 = str1.replace('&', chr(0x1C))
        str1 = str1.replace('+', chr(0x1D))
        str1 = str1.replace('!', chr(0x1E))
        str1 = str1.replace('^', chr(0x1F))
        fd = self._makeFd(str1)
        src = pyx12.rawx12file.RawX12File(fd)
        ct = 0
        for seg in src:
            ct += 1
        (seg_term, ele_term, subele_term, eol,
            repetition_term) = src.get_term()
        self.assertEqual(subele_term, chr(0x1E))
        self.assertEqual(ele_term, chr(0x1C))
        self.assertEqual(seg_term, chr(0x1D))
        self.assertEqual(repetition_term, chr(0x1F))
        self.assertEqual(ct, 7)


class X12InterchangeControlVersion(X12fileTestCase):

    def test_4010(self):
        fd = self._makeFd('ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n')
        src = pyx12.rawx12file.RawX12File(fd)
        self.assertEqual(src.icvn, '00401')

    def test_5010(self):
        fd = self._makeFd('ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&^&00501&000010121&0&T&!+\n')
        src = pyx12.rawx12file.RawX12File(fd)
        self.assertEqual(src.icvn, '00501')

    def test_unknown(self):
        fd = self._makeFd('ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&^&00101&000010121&0&T&!+\n')
        self.assertRaises(
            pyx12.errors.X12Error, pyx12.rawx12file.RawX12File, fd)


class RawISA_header(X12fileTestCase):

    def test_starts_with_ISA(self):
        fd = self._makeFd(' ISA~')
        self.assertRaises(
            pyx12.errors.X12Error, pyx12.rawx12file.RawX12File, fd)

    def test_at_least_ISA_len(self):
        fd = self._makeFd('ISA~')
        self.assertRaises(
            pyx12.errors.X12Error, pyx12.rawx12file.RawX12File, fd)


#class Formatting(unittest.TestCase):
#    def test_identity(self):
#        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
#        str1 += 'IEA*1*000010121~\n'
#        fd = StringIO(str1, encoding='ascii')
#        fd.seek(0)
#        src = pyx12.rawx12file.RawX12File(fd)
#        str_out = ''
#        for seg in src:
#            str_out += seg.format() + '\n'
#        self.assertEqual(str1, str_out)
