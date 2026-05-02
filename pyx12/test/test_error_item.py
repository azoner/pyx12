import unittest

from pyx12.error_item import EleError, ErrorItem, ISAError, SegError
from pyx12.errors import EngineError


class TestErrorItem(unittest.TestCase):
    def test_basic_creation(self):
        e = ErrorItem("isa", "001", "some error")
        self.assertEqual(e.getErrCde(), "001")
        self.assertEqual(e.getErrStr(), "some error")


class TestISAError(unittest.TestCase):
    def test_valid_code(self):
        e = ISAError("001", "ISA segment error")
        self.assertEqual(e.getErrCde(), "001")
        self.assertEqual(e.getErrStr(), "ISA segment error")

    def test_valid_code_000(self):
        e = ISAError("000", "no error")
        self.assertEqual(e.getErrCde(), "000")

    def test_valid_code_031(self):
        e = ISAError("031", "last valid code")
        self.assertEqual(e.getErrCde(), "031")

    def test_invalid_code_raises(self):
        with self.assertRaises(EngineError):
            ISAError("999", "bad code")

    def test_invalid_code_empty(self):
        with self.assertRaises(EngineError):
            ISAError("", "bad code")


class TestSegError(unittest.TestCase):
    def test_valid_code(self):
        e = SegError("1", "segment error")
        self.assertEqual(e.getErrCde(), "1")
        self.assertEqual(e.getErrStr(), "segment error")

    def test_valid_code_8(self):
        e = SegError("8", "seg error")
        self.assertEqual(e.getErrCde(), "8")

    def test_err_val_default_none(self):
        e = SegError("1", "seg error")
        self.assertIsNone(e.getErrVal())

    def test_err_val_set(self):
        e = SegError("2", "seg error", err_val="BAD*SEG")
        self.assertEqual(e.getErrVal(), "BAD*SEG")

    def test_invalid_code_raises(self):
        with self.assertRaises(EngineError):
            SegError("99", "bad code")

    def test_invalid_code_zero(self):
        with self.assertRaises(EngineError):
            SegError("0", "bad code")


class TestEleError(unittest.TestCase):
    def test_valid_code(self):
        e = EleError("1", "element error", ele_idx=1)
        self.assertEqual(e.getErrCde(), "1")
        self.assertEqual(e.getErrStr(), "element error")

    def test_valid_code_10(self):
        e = EleError("10", "element error", ele_idx=5)
        self.assertEqual(e.getErrCde(), "10")

    def test_ele_idx(self):
        e = EleError("1", "element error", ele_idx=3)
        self.assertEqual(e.getEleIdx(), 3)

    def test_subele_idx_default_none(self):
        e = EleError("1", "element error", ele_idx=1)
        self.assertIsNone(e.getSubeleIdx())

    def test_subele_idx_set(self):
        e = EleError("1", "element error", ele_idx=2, subele_idx=1)
        self.assertEqual(e.getSubeleIdx(), 1)

    def test_err_val_default_none(self):
        e = EleError("1", "element error", ele_idx=1)
        self.assertIsNone(e.getErrVal())

    def test_err_val_set(self):
        e = EleError("2", "element error", ele_idx=1, err_val="BADVAL")
        self.assertEqual(e.getErrVal(), "BADVAL")

    def test_invalid_code_raises(self):
        with self.assertRaises(EngineError):
            EleError("11", "bad code", ele_idx=1)

    def test_invalid_code_zero(self):
        with self.assertRaises(EngineError):
            EleError("0", "bad code", ele_idx=1)


if __name__ == "__main__":
    unittest.main()
