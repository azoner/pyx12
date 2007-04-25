#! /usr/bin/env /usr/local/bin/python

import unittest
#import sys
#import StringIO
import pdb
import tempfile

import pyx12.error_handler
#from error_handler import ErrorErrhNull
from pyx12.errors import *
import pyx12.x12file

class X12fileTestCase(unittest.TestCase):

    def _get_first_error(self, x12str):
        fd = tempfile.NamedTemporaryFile()
        fd.write(x12str)
        fd.seek(0)
        errors = []
        err_cde = None
        err_str = None
        src = pyx12.x12file.X12file(fd.name)
        for seg in src:
            errors.extend(src.pop_errors())
        errors.extend(src.pop_errors())
        src.cleanup()
        errors.extend(src.pop_errors())
        if len(errors) > 0:
            err_cde = errors[0][1]
            err_str = errors[0][2]
        return (err_cde, err_str)
    
class Delimiters(unittest.TestCase):

    def test_arbitrary_delimiters(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str1 += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&004010X098+\n'
        str1 += 'ST&837&11280001+\n'
        str1 += 'TST&AA!1!1&BB!5+\n'
        str1 += 'SE&3&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str1)
        fd.seek(0)
        errors = []
        src = pyx12.x12file.X12file(fd.name)
        for seg in src:
            errors.extend(src.pop_errors())
        err_cde = None
        if len(errors) > 0: err_cde = errors[0][1]
        self.assertEqual(err_cde, None)
        self.assertEqual(src.subele_term, '!')
        self.assertEqual(src.ele_term, '&')
        self.assertEqual(src.seg_term, '+')

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
        #print str1
        fd = tempfile.NamedTemporaryFile()
        fd.write(str1)
        fd.seek(0)
        errors = []
        src = pyx12.x12file.X12file(fd.name)
        for seg in src:
            errors.extend(src.pop_errors())
        err_cde = None
        if len(errors) > 0: err_cde = errors[0][1]
        self.assertEqual(err_cde, None)
        self.assertEqual(src.subele_term, chr(0x1E))
        self.assertEqual(src.ele_term, chr(0x1C))
        self.assertEqual(src.seg_term, chr(0x1D))

    def test_trailing_ele_delim(self):
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'ZZ*1***~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str1)
        fd.seek(0)
        src = pyx12.x12file.X12file(fd.name)
        err_cde = None
        err_str = None
        for seg in src:
            if seg.get_seg_id() == 'ZZ':
                errors = src.pop_errors()
                if len(errors) > 0:
                    err_cde = errors[0][1]
                    err_str = errors[0][2]
        self.assertEqual(err_cde, 'SEG1', err_str)

                    
class ISA_header(X12fileTestCase):

    def test_starts_with_ISA(self):
        fd = tempfile.NamedTemporaryFile()
        fd.write(' ISA~')
        fd.seek(0)
        self.failUnlessRaises(pyx12.errors.X12Error, pyx12.x12file.X12file, fd.name)

    def test_at_least_ISA_len(self):
        fd = tempfile.NamedTemporaryFile()
        fd.write('ISA~')
        fd.seek(0)
        self.failUnlessRaises(pyx12.errors.X12Error, pyx12.x12file.X12file, fd.name)

    def test_repeat_ISA_loops(self):
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'IEA*0*000010121~\n'
        str1 += 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010122*0*T*:~\n'
        str1 += 'IEA*0*000010122~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, None, err_str)

    def test_Unique_Interchange_ID(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'IEA*0*000010121~\n'
        str1 += 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'IEA*0*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '025', err_str)


class IEA_Checks(X12fileTestCase):

    def test_IEA_id_match_ISA_id(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'GE*0*17~\n'
        str1 += 'IEA*1*000010555~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '001', err_str)

    def test_IEA_count(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'GE*0*17~\n'
        str1 += 'IEA*2*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '021', err_str)

    def test_missing_IEA(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'GE*0*17~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '023', err_str)


class GE_Checks(X12fileTestCase):

    def test_GE_id_match_GS_id(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'GE*0*555~\n'
        str1 += 'IEA*1*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '4', err_str)

    def test_GE_count(self):
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'GE*999*17~\n'
        str1 += 'IEA*1*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '5', err_str)

    def test_Unique_Functional_Group_ID(self):
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'GE*0*17~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'GE*0*17~\n'
        str1 += 'IEA*2*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '6', err_str)

    def test_missing_GE(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'IEA*1*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '024', err_str)


class SE_Checks(X12fileTestCase):

    def test_SE_id_match_ST_id(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'ST*837*11280001~\n'
        str1 += 'SE*2*11280999~\n'
        str1 += 'GE*1*17~\n'
        str1 += 'IEA*1*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '3', err_str)

    def test_SE_count(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'ST*837*11280001~\n'
        str1 += 'SE*0*11280001~\n'
        str1 += 'GE*1*17~\n'
        str1 += 'IEA*1*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '4', err_str)

    def test_Unique_Transaction_Set_ID(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'ST*837*11280001~\n'
        str1 += 'SE*2*11280001~\n'
        str1 += 'ST*837*11280001~\n'
        str1 += 'SE*2*11280001~\n'
        str1 += 'GE*2*17~\n'
        str1 += 'IEA*1*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '23', err_str)

    def test_missing_SE(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'ST*837*11280001~\n'
        str1 += 'GE*1*17~\n'
        str1 += 'IEA*1*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '3', err_str)


class HL_Checks(X12fileTestCase):
    """
    We can do minimal HL parent checks here
    """
    def test_HL_increment_good(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'ST*837*11280001~\n'
        str1 += 'HL*1**20*1~\n'
        str1 += 'HL*2*1*22*1~\n'
        str1 += 'HL*3*2*23*1~\n'
        str1 += 'HL*4*1*22*1~\n'
        str1 += 'SE*6*11280001~\n'
        str1 += 'GE*1*17~\n'
        str1 += 'IEA*1*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, None, err_str)

    def test_HL_increment_bad(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'ST*837*11280001~\n'
        str1 += 'HL*1**20*1~\n'
        str1 += 'HL*2*1*22*1~\n'
        str1 += 'HL*3*2*23*1~\n'
        str1 += 'HL*5*1*22*1~\n'
        str1 += 'SE*6*11280001~\n'
        str1 += 'GE*1*17~\n'
        str1 += 'IEA*1*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, 'HL1', err_str)

    def test_HL_parent_good(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'ST*837*11280001~\n'
        str1 += 'HL*1**20*1~\n'
        str1 += 'HL*2*1*22*1~\n'
        str1 += 'HL*3*2*23*1~\n'
        str1 += 'HL*4*1*22*1~\n'
        str1 += 'SE*6*11280001~\n'
        str1 += 'GE*1*17~\n'
        str1 += 'IEA*1*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, None, err_str)

    def test_HL_parent_bad_invalid(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'ST*837*11280001~\n'
        str1 += 'HL*1**20*1~\n'
        str1 += 'HL*2*1*22*1~\n'
        str1 += 'HL*3*5*23*1~\n'
        str1 += 'HL*4*2*22*1~\n'
        str1 += 'SE*6*11280001~\n'
        str1 += 'GE*1*17~\n'
        str1 += 'IEA*1*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, 'HL2', err_str)

    def xtest_HL_parent_bad_blank(self):
        seg = None
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str1 += 'ST*837*11280001~\n'
        str1 += 'HL*1**20*1~\n'
        str1 += 'HL*2*1*22*1~\n'
        str1 += 'HL*3**23*1~\n'
        str1 += 'HL*4*2*22*1~\n'
        str1 += 'SE*6*11280001~\n'
        str1 += 'GE*1*17~\n'
        str1 += 'IEA*1*000010121~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, 'HL2', err_str)


class Formatting(unittest.TestCase):

    def test_identity(self):
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
#        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
#        str1 += 'ST*837*11280001~\n'
#        str1 += 'HL*1**20*1~\n'
#        str1 += 'HL*2*1*22*1~\n'
#        str1 += 'HL*3*2*23*1~\n'
#        str1 += 'HL*4*1*22*1~\n'
#        str1 += 'SE*6*11280001~\n'
#        str1 += 'GE*1*17~\n'
        str1 += 'IEA*1*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str1)
        fd.seek(0)
        src = pyx12.x12file.X12file(fd.name)
        str_out = ''
        for seg in src:
            str_out += seg.format() + '\n'
        self.assertEqual(str1, str_out)

    def test_strip_eol(self):
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
#        str1 += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
#        str1 += 'ST*837*11280001~\n'
#        str1 += 'HL*1**20*1~\n'
#        str1 += 'HL*2*1*22*1~\n'
#        str1 += 'HL*3*2*23*1~\n'
#        str1 += 'HL*4*1*22*1~\n'
#        str1 += 'SE*6*11280001~\n'
#        str1 += 'GE*1*17~\n'
        str1 += 'IEA*1*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str1)
        fd.seek(0)
        src = pyx12.x12file.X12file(fd.name)
        str_out = ''
        for seg in src:
            str_out += seg.format()
        str1 = str1.replace('\n', '')
        self.assertEqual(str1, str_out)
 

class Segment_ID_Checks(X12fileTestCase):

    def test_segment_id_short(self):
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'Z*0019~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '1', err_str)

    def test_segment_last_space(self):
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'ZZ*0019 ~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str1)
        fd.seek(0)
        val = None
        src = pyx12.x12file.X12file(fd.name)
        for seg in src:
            if seg.get_seg_id() == 'ZZ':
                val = seg.get('ZZ01').format()
        self.assertEqual(val, '0019 ')

    def test_segment_id_long(self):
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'ZZZZ*0019~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '1', err_str)

    def test_segment_id_empty(self):
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += '*1~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '1', err_str)
        
    def test_segment_empty(self):
        errh = pyx12.error_handler.errh_null()
        str1 = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str1 += 'TST~\n'
        (err_cde, err_str) = self._get_first_error(str1)        
        self.assertEqual(err_cde, '8', err_str)
