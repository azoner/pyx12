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

class Delimiters(unittest.TestCase):

    def setUp(self):
        self.errh = pyx12.error_handler.errh_null()

    def test_arbitrary_delimiters(self):
        str = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&004010X098+\n'
        str += 'ST&837&11280001+\n'
        str += 'TST&AA!1!1&BB!5+\n'
        str += 'SE&3&11280001+\n'
        str += 'GE&1&17+\n'
        str += 'IEA&1&000010121+\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, None)
        self.assertEqual(src.subele_term, '!')
        self.assertEqual(src.ele_term, '&')
        self.assertEqual(src.seg_term, '+')

    def test_binary_delimiters(self):
        str = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&004010X098+\n'
        str += 'ST&837&11280001+\n'
        str += 'TST&AA!1!1&BB!5+\n'
        str += 'SE&3&11280001+\n'
        str += 'GE&1&17+\n'
        str += 'IEA&1&000010121+\n'
        str = str.replace('&', chr(0x1C))
        str = str.replace('+', chr(0x1D))
        str = str.replace('!', chr(0x1E))
        #print str
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, None)
        self.assertEqual(src.subele_term, chr(0x1E))
        self.assertEqual(src.ele_term, chr(0x1C))
        self.assertEqual(src.seg_term, chr(0x1D))

    def test_trailing_ele_delim(self):
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'ZZ****~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            if seg.get_seg_id() == 'ZZ':
                self.assertEqual(self.errh.err_cde, 'SEG1', self.errh.err_str)

                    
class ISA_header(unittest.TestCase):

    def setUp(self):
        self.errh = pyx12.error_handler.errh_null()

    def test_starts_with_ISA(self):
        fd = tempfile.NamedTemporaryFile()
        fd.write(' ISA~')
        fd.seek(0)
        self.failUnlessRaises(pyx12.x12file.x12Error, pyx12.x12file.x12file, fd.name, self.errh)

    def test_at_least_ISA_len(self):
        fd = tempfile.NamedTemporaryFile()
        fd.write('ISA~')
        fd.seek(0)
        self.failUnlessRaises(pyx12.x12file.x12Error, pyx12.x12file.x12file, fd.name, self.errh)

    def test_repeat_ISA_loops(self):
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'IEA*0*000010121~\n'
        str += 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010122*0*T*:~\n'
        str += 'IEA*0*000010122~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, None)

    def test_Unique_Interchange_ID(self):
        seg = None
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'IEA*0*000010121~\n'
        str += 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'IEA*0*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, '025', self.errh.err_str)

    def tearDown(self):
        pass

class IEA_Checks(unittest.TestCase):

    def setUp(self):
        self.errh = pyx12.error_handler.errh_null()

    def test_IEA_id_match_ISA_id(self):
        seg = None
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'GE*0*17~\n'
        str += 'IEA*1*000010555~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, '001', self.errh.err_str)

    def test_IEA_count(self):
        seg = None
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'GE*0*17~\n'
        str += 'IEA*2*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, '021', self.errh.err_str)

    def test_missing_IEA(self):
        seg = None
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'GE*0*17~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        src.cleanup()
        self.assertEqual(self.errh.err_cde, '023', self.errh.err_str)

    def tearDown(self):
        pass


class GE_Checks(unittest.TestCase):
    def setUp(self):
        self.errh = pyx12.error_handler.errh_null()

    def test_GE_id_match_GS_id(self):
        seg = None
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'GE*0*555~\n'
        str += 'IEA*1*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, '4', self.errh.err_str)

    def test_GE_count(self):
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'GE*999*17~\n'
        str += 'IEA*1*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, '5', self.errh.err_str)

    def test_Unique_Functional_Group_ID(self):
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'GE*0*17~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'GE*0*17~\n'
        str += 'IEA*2*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, '6', self.errh.err_str)

    def test_missing_GE(self):
        seg = None
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'IEA*1*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, '024', self.errh.err_str)

    def tearDown(self):
        pass

class SE_Checks(unittest.TestCase):
    def setUp(self):
        self.errh = pyx12.error_handler.errh_null()

    def test_SE_id_match_ST_id(self):
        seg = None
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'ST*837*11280001~\n'
        str += 'SE*2*11280999~\n'
        str += 'GE*1*17~\n'
        str += 'IEA*1*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, '3', self.errh.err_str)

    def test_SE_count(self):
        seg = None
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'ST*837*11280001~\n'
        str += 'SE*0*11280001~\n'
        str += 'GE*1*17~\n'
        str += 'IEA*1*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, '4', self.errh.err_str)

    def test_Unique_Transaction_Set_ID(self):
        seg = None
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'ST*837*11280001~\n'
        str += 'SE*2*11280001~\n'
        str += 'ST*837*11280001~\n'
        str += 'SE*2*11280001~\n'
        str += 'GE*2*17~\n'
        str += 'IEA*1*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, '23', self.errh.err_str)

    def test_missing_SE(self):
        seg = None
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'ST*837*11280001~\n'
        str += 'GE*1*17~\n'
        str += 'IEA*1*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, '3', self.errh.err_str)

    def tearDown(self):
        pass

class HL_Checks(unittest.TestCase):
    def setUp(self):
        self.errh = pyx12.error_handler.errh_null()

    def test_HL_increment_good(self):
        seg = None
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'ST*837*11280001~\n'
        str += 'HL*1**20*1~\n'
        str += 'HL*2*1*22*1~\n'
        str += 'HL*3*2*23*1~\n'
        str += 'HL*4*1*22*1~\n'
        str += 'SE*6*11280001~\n'
        str += 'GE*1*17~\n'
        str += 'IEA*1*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, None, self.errh.err_str)

    def test_HL_increment_bad(self):
        seg = None
        str = 'ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        str += 'GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098~\n'
        str += 'ST*837*11280001~\n'
        str += 'HL*1**20*1~\n'
        str += 'HL*2*1*22*1~\n'
        str += 'HL*3*2*23*1~\n'
        str += 'HL*5*1*22*1~\n'
        str += 'SE*6*11280001~\n'
        str += 'GE*1*17~\n'
        str += 'IEA*1*000010121~\n'
        fd = tempfile.NamedTemporaryFile()
        fd.write(str)
        fd.seek(0)
        src = pyx12.x12file.x12file(fd.name, self.errh)
        for seg in src:
            pass
        self.assertEqual(self.errh.err_cde, 'HL1', self.errh.err_str)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Delimiters))
    suite.addTest(unittest.makeSuite(ISA_header))
    suite.addTest(unittest.makeSuite(IEA_Checks))
    suite.addTest(unittest.makeSuite(GE_Checks))
    suite.addTest(unittest.makeSuite(SE_Checks))
    suite.addTest(unittest.makeSuite(HL_Checks))
    return suite

#if __name__ == "__main__":
#    unittest.main()
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())


