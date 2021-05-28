import unittest

from pyx12.validation import IsValidDataType


class BasicNumeric(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('1', 'N', 'B'))
        self.assertTrue(IsValidDataType('-1', 'N', 'B'))
        self.assertTrue(IsValidDataType('10', 'N', 'B'))
        self.assertTrue(IsValidDataType('-10', 'N', 'B'))
        self.assertTrue(IsValidDataType('0000500', 'N', 'B'))
        self.assertTrue(IsValidDataType('1', 'R', 'B'))

    def testInvalid(self):
        self.assertFalse(IsValidDataType('+10', 'N', 'B'))
        self.assertFalse(IsValidDataType('1.', 'N', 'B'))
        self.assertFalse(IsValidDataType('-1.', 'N', 'B'))


class BasicReal(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('-331232', 'R', 'B'))
        self.assertTrue(IsValidDataType('1.325', 'R', 'B'))
        self.assertTrue(IsValidDataType('.024', 'R', 'B'))

    def testInvalid(self):
        self.assertFalse(IsValidDataType('+331232', 'R', 'B'))
        self.assertFalse(IsValidDataType('123,456,789.123', 'R', 'B'))
        self.assertFalse(IsValidDataType('333.', 'R', 'B'))
        self.assertFalse(IsValidDataType('a.603', 'R', 'B'))
        self.assertFalse(IsValidDataType('0.0b', 'R', 'B'))


class BasicIdentifier(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('10&3', 'ID', 'B'))
        self.assertTrue(IsValidDataType('  XYZ', 'ID', 'B'))

    def testInvalid(self):
        self.assertFalse(IsValidDataType('abc', 'ID', 'B'))
        self.assertFalse(IsValidDataType('abc   ', 'ID', 'B'))


class BasicString(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('LKJS', 'AN', 'B'))
        self.assertTrue(IsValidDataType('THIS IS A TEST ()', 'AN', 'B'))
        self.assertTrue(IsValidDataType(r"""BASIC ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?=""", 'AN', 'B'))

    def testInvalid(self):
        self.assertFalse(IsValidDataType('abd1P', 'AN', 'B'))
        self.assertFalse(IsValidDataType(r'extended abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$', 'AN', 'B'))
        self.assertFalse(IsValidDataType(r"""Both ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?= abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$""", 'AN', 'B'))
        self.assertFalse(IsValidDataType('bad ^`', 'AN', 'B'))
        self.assertFalse(IsValidDataType('wharf', 'AN', 'B'))
        self.assertFalse(IsValidDataType('\\', 'AN', 'B'))


class BasicDate(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('20010418', 'DT', 'B'))
        self.assertTrue(IsValidDataType('20030429', 'DT', 'B'))
        self.assertTrue(IsValidDataType('19040229', 'DT', 'B'))
        self.assertTrue(IsValidDataType('20000229', 'DT', 'B'))
        self.assertTrue(IsValidDataType('20040229', 'DT', 'B'))
        self.assertTrue(IsValidDataType('020414', 'DT', 'B'))
        self.assertTrue(IsValidDataType('960229', 'DT', 'B'))
        self.assertTrue(IsValidDataType('200402020400', 'DT', 'B'))
        self.assertTrue(IsValidDataType('20040430', 'DT', 'B'))
        self.assertTrue(IsValidDataType('20040401-20040430', 'RD8', 'B'))

    def testInvalidLeapDate(self):
        self.assertFalse(IsValidDataType('990229', 'DT', 'B'))
        self.assertFalse(IsValidDataType('20030229', 'DT', 'B'))
        self.assertFalse(IsValidDataType('19000229', 'DT', 'B'))

    def testInvalidAlpha(self):
        self.assertFalse(IsValidDataType('200204a', 'DT', 'B'))
        self.assertFalse(IsValidDataType('2002041a', 'DT', 'B'))

    def testInvalidMonth(self):
        self.assertFalse(IsValidDataType('19991301', 'DT', 'B'))
        self.assertFalse(IsValidDataType('030732', 'DT', 'B'))

    def testInvalidDay(self):
        self.assertFalse(IsValidDataType('19992377', 'DT', 'B'))
        self.assertFalse(IsValidDataType('19991277', 'DT', 'B'))
        self.assertFalse(IsValidDataType('20040431', 'DT', 'B'))

    def testInvalidLength(self):
        self.assertFalse(IsValidDataType('200402024 00', 'DT', 'B'))
        self.assertFalse(IsValidDataType('200422024000', 'DT', 'B'))
        self.assertFalse(IsValidDataType('20040222040', 'DT', 'B'))
        self.assertFalse(IsValidDataType('2004022204', 'DT', 'B'))
        self.assertFalse(IsValidDataType('200402220', 'DT', 'B'))

    def testInvalidChar(self):
        self.assertFalse(IsValidDataType('-20040430', 'RD8', 'B'))
        self.assertFalse(IsValidDataType('20040430-', 'RD8', 'B'))

    def testInvalidAncient(self):
        self.assertFalse(IsValidDataType('17992301', 'DT', 'B'))
        self.assertFalse(IsValidDataType('09991202', 'DT', 'B'))


class BasicTime(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('0731', 'TM', 'B'))
        self.assertTrue(IsValidDataType('000159', 'TM', 'B'))

    def testInvalid(self):
        self.assertFalse(IsValidDataType('07315a', 'TM', 'B'))
        self.assertFalse(IsValidDataType('7 31', 'TM', 'B'))
        self.assertFalse(IsValidDataType('7:31', 'TM', 'B'))


class ExtendedNumeric(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('1', 'N', 'E'))
        self.assertTrue(IsValidDataType('-1', 'N', 'E'))
        self.assertTrue(IsValidDataType('10', 'N', 'E'))
        self.assertTrue(IsValidDataType('-10', 'N', 'E'))
        self.assertTrue(IsValidDataType('0000500', 'N', 'E'))

    def testInvalid(self):
        self.assertFalse(IsValidDataType('+10', 'N', 'E'))
        self.assertFalse(IsValidDataType('1.', 'N', 'E'))
        self.assertFalse(IsValidDataType('-1.', 'N', 'E'))


class ExtendedReal(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('1', 'R', 'E'))
        self.assertTrue(IsValidDataType('-331232', 'R', 'E'))
        self.assertTrue(IsValidDataType('1.325', 'R', 'E'))
        self.assertTrue(IsValidDataType('.024', 'R', 'E'))

    def testInvalid(self):
        self.assertFalse(IsValidDataType('a.603', 'R', 'E'))
        self.assertFalse(IsValidDataType('0.0b', 'R', 'E'))
        self.assertFalse(IsValidDataType('+331232', 'R', 'E'))
        self.assertFalse(IsValidDataType('123,456,789.123', 'R', 'E'))
        self.assertFalse(IsValidDataType('333.', 'R', 'E'))


class ExtendedIdentifier(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('abc', 'ID', 'E'))
        self.assertTrue(IsValidDataType('10&3', 'ID', 'E'))
        self.assertTrue(IsValidDataType('  XYZ', 'ID', 'E'))
        self.assertTrue(IsValidDataType('abc   ', 'ID', 'E'))


class ExtendedString(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('LKJS\\', 'AN', 'E'))
        self.assertTrue(IsValidDataType('abd1P', 'AN', 'E'))
        self.assertTrue(IsValidDataType('THIS IS A TEST ()', 'AN', 'E'))
        self.assertTrue(IsValidDataType("""BASIC ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?=""", 'AN', 'E'))
        self.assertTrue(IsValidDataType('extended abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$', 'AN', 'E'))
        self.assertTrue(IsValidDataType("""Both ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?= abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$""", 'AN', 'E'))
        self.assertTrue(IsValidDataType('wharf', 'AN', 'E'))

    def testInvalid(self):
        self.assertFalse(IsValidDataType('bad ^`', 'AN', 'E'))


class ExtendedDate(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('20010418', 'DT', 'E'))
        self.assertTrue(IsValidDataType('20030429', 'DT', 'E'))
        self.assertTrue(IsValidDataType('19040229', 'DT', 'E'))
        self.assertTrue(IsValidDataType('20000229', 'DT', 'E'))
        self.assertTrue(IsValidDataType('20040229', 'DT', 'E'))
        self.assertTrue(IsValidDataType('020414', 'DT', 'E'))
        self.assertTrue(IsValidDataType('960229', 'DT', 'E'))
        self.assertTrue(IsValidDataType('200402020400', 'DT', 'B'))
        self.assertTrue(IsValidDataType('20010418', 'D8', 'E'))
        self.assertTrue(IsValidDataType('20030429', 'D8', 'E'))
        self.assertTrue(IsValidDataType('19040229', 'D8', 'E'))
        self.assertTrue(IsValidDataType('20000229', 'D8', 'E'))
        self.assertTrue(IsValidDataType('20040229', 'D8', 'E'))
        self.assertTrue(IsValidDataType('020414', 'D6', 'E'))
        self.assertTrue(IsValidDataType('960229', 'D6', 'E'))
        self.assertTrue(IsValidDataType('20040401-20040430', 'RD8', 'E'))

    def testInvalid(self):
        self.assertFalse(IsValidDataType('990229', 'DT', 'E'))
        self.assertFalse(IsValidDataType('030732', 'DT', 'E'))
        self.assertFalse(IsValidDataType('19992377', 'DT', 'E'))
        self.assertFalse(IsValidDataType('19991277', 'DT', 'E'))
        self.assertFalse(IsValidDataType('200204a', 'DT', 'E'))
        self.assertFalse(IsValidDataType('2002041a', 'DT', 'E'))
        self.assertFalse(IsValidDataType('19000229', 'DT', 'E'))
        self.assertFalse(IsValidDataType('20030229', 'DT', 'E'))
        self.assertFalse(IsValidDataType('200402024 00', 'DT', 'B'))

        self.assertFalse(IsValidDataType('990229', 'D6', 'E'))
        self.assertFalse(IsValidDataType('030732', 'D6', 'E'))
        self.assertFalse(IsValidDataType('19992377', 'D8', 'E'))
        self.assertFalse(IsValidDataType('19991277', 'D8', 'E'))
        self.assertFalse(IsValidDataType('200204a', 'D8', 'E'))
        self.assertFalse(IsValidDataType('2002041a', 'D8', 'E'))
        self.assertFalse(IsValidDataType('19000229', 'D8', 'E'))
        self.assertFalse(IsValidDataType('20030229', 'D8', 'E'))
        self.assertFalse(IsValidDataType('55555555', 'D8', 'E'))
        self.assertFalse(IsValidDataType('55555555', 'D8', 'B'))
        self.assertFalse(IsValidDataType('200402024 00', 'D8', 'B'))
        self.assertFalse(IsValidDataType('020414', 'D8', 'E'))
        self.assertFalse(IsValidDataType('20020414', 'D6', 'E'))
        self.assertFalse(IsValidDataType('-20040430', 'RD8', 'E'))
        self.assertFalse(IsValidDataType('20040430-', 'RD8', 'E'))

    def testInvalidAncient(self):
        self.assertFalse(IsValidDataType('17992301', 'DT', 'E'))
        self.assertFalse(IsValidDataType('09991202', 'DT', 'E'))
        self.assertFalse(IsValidDataType('17992301', 'D8', 'E'))
        self.assertFalse(IsValidDataType('09991202', 'D8', 'E'))


class ExtendedTime(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('0731', 'TM', 'E'))
        self.assertTrue(IsValidDataType('000159', 'TM', 'E'))

    def testInvalid(self):
        self.assertFalse(IsValidDataType('07315a', 'TM', 'E'))
        self.assertFalse(IsValidDataType('7 31', 'TM', 'B'))
        self.assertFalse(IsValidDataType('7:31', 'TM', 'B'))


class Extendedi5010Identifier(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('abc', 'ID', 'E', '00501'))
        self.assertTrue(IsValidDataType('10&3', 'ID', 'E', '00501'))
        self.assertTrue(IsValidDataType('  XYZ', 'ID', 'E', '00501'))
        self.assertTrue(IsValidDataType('abc   ', 'ID', 'E', '00501'))

    def testInvalid(self):
        self.assertFalse(
            IsValidDataType('%s' % (chr(0x1D)), 'ID', 'E', '00501'))


class Extended5010String(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType('LKJS\\', 'AN', 'E', '00501'))
        self.assertTrue(IsValidDataType('abd1P', 'AN', 'E', '00501'))
        self.assertTrue(
            IsValidDataType('THIS IS A TEST ()', 'AN', 'E', '00501'))
        self.assertTrue(IsValidDataType("""BASIC ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?=""", 'AN', 'E', '00501'))
        self.assertTrue(IsValidDataType('extended abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$', 'AN', 'E', '00501'))
        self.assertTrue(IsValidDataType("""Both ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?= abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$""", 'AN', 'E', '00501'))
        self.assertTrue(IsValidDataType('wharf', 'AN', 'E', '00501'))
        self.assertTrue(IsValidDataType('_good ^`', 'AN', 'E', '00501'))

    def testInvalid(self):
        self.assertFalse(
            IsValidDataType('%s' % (chr(0x1D)), 'AN', 'E', '00501'))

class BadWhitespace(unittest.TestCase):
    def testValid(self):
        self.assertTrue(IsValidDataType(' ', 'AN', 'E', '00501'))
        self.assertTrue(IsValidDataType('  ', 'AN', 'E', '00501'))
        self.assertTrue(IsValidDataType(' ', 'AN', 'B', '00501'))
        self.assertTrue(IsValidDataType('  ', 'AN', 'B', '00501'))
        self.assertTrue(IsValidDataType(' ', 'AN', 'B'))
        self.assertTrue(IsValidDataType('  ', 'AN', 'B'))
        self.assertTrue(IsValidDataType('%s' % (chr(0x68)), 'AN', 'E', '00501'))

    def testInvalid(self):
        self.assertFalse(IsValidDataType(chr(0x09), 'AN', 'E', '00501'))
        self.assertFalse(IsValidDataType(chr(0x11), 'AN', 'E', '00501'))
        self.assertFalse(IsValidDataType('\t', 'AN', 'E', '00501'))
        self.assertFalse(IsValidDataType('\n', 'AN', 'E', '00501'))
        self.assertFalse(IsValidDataType('\r', 'AN', 'E', '00501'))
        self.assertFalse(IsValidDataType('\b', 'AN', 'E', '00501'))
        self.assertFalse(IsValidDataType(chr(0x0A), 'AN', 'E', '00501'))
        self.assertFalse(IsValidDataType(chr(0x0D), 'AN', 'E', '00501'))
