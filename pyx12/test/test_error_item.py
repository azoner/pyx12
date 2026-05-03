import unittest

from pyx12.error_item import EleError, ErrorItem, ISAError, SegError
from pyx12.errors import EngineError


class TestErrorItem(unittest.TestCase):
    def test_basic_creation(self):
        e = ErrorItem("001", "some error")
        self.assertEqual(e.err_cde, "001")
        self.assertEqual(e.err_str, "some error")


class TestISAError(unittest.TestCase):
    def test_valid_code(self):
        e = ISAError("001", "ISA segment error")
        self.assertEqual(e.err_cde, "001")
        self.assertEqual(e.err_str, "ISA segment error")

    def test_valid_code_000(self):
        e = ISAError("000", "no error")
        self.assertEqual(e.err_cde, "000")

    def test_valid_code_031(self):
        e = ISAError("031", "last valid code")
        self.assertEqual(e.err_cde, "031")

    def test_invalid_code_raises(self):
        with self.assertRaises(EngineError):
            ISAError("999", "bad code")

    def test_invalid_code_empty(self):
        with self.assertRaises(EngineError):
            ISAError("", "bad code")


class TestSegError(unittest.TestCase):
    def test_valid_code(self):
        e = SegError("1", "segment error")
        self.assertEqual(e.err_cde, "1")
        self.assertEqual(e.err_str, "segment error")

    def test_valid_code_8(self):
        e = SegError("8", "seg error")
        self.assertEqual(e.err_cde, "8")

    def test_err_val_default_none(self):
        e = SegError("1", "seg error")
        self.assertIsNone(e.err_val)

    def test_err_val_set(self):
        e = SegError("2", "seg error", err_val="BAD*SEG")
        self.assertEqual(e.err_val, "BAD*SEG")

    def test_invalid_code_raises(self):
        with self.assertRaises(EngineError):
            SegError("99", "bad code")

    def test_invalid_code_zero(self):
        with self.assertRaises(EngineError):
            SegError("0", "bad code")


class TestEleError(unittest.TestCase):
    def test_valid_code(self):
        e = EleError("1", "element error")
        self.assertEqual(e.err_cde, "1")
        self.assertEqual(e.err_str, "element error")

    def test_valid_code_10(self):
        e = EleError("10", "element error")
        self.assertEqual(e.err_cde, "10")

    def test_refdes_default_none(self):
        e = EleError("1", "element error")
        self.assertIsNone(e.refdes)

    def test_refdes_set(self):
        e = EleError("1", "element error", refdes="03")
        self.assertEqual(e.refdes, "03")

    def test_err_val_default_none(self):
        e = EleError("1", "element error")
        self.assertIsNone(e.err_val)

    def test_err_val_set(self):
        e = EleError("2", "element error", err_val="BADVAL")
        self.assertEqual(e.err_val, "BADVAL")

    def test_invalid_code_raises(self):
        with self.assertRaises(EngineError):
            EleError("11", "bad code")

    def test_invalid_code_zero(self):
        with self.assertRaises(EngineError):
            EleError("0", "bad code")


if __name__ == "__main__":
    unittest.main()
