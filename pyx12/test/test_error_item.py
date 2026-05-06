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
    # PR 5 (#TBD) tightens SegError validation to require pyx12 codes
    # from pyx12.error_codes.ERROR_CODES. Raw X12 codes like "1" / "8"
    # are no longer accepted.
    def test_valid_code(self):
        e = SegError("SEG_1_segment_not_found", "segment error")
        self.assertEqual(e.err_cde, "SEG_1_segment_not_found")
        self.assertEqual(e.err_str, "segment error")

    def test_valid_code_8(self):
        e = SegError("SEG_8_trailing_terminators", "seg error")
        self.assertEqual(e.err_cde, "SEG_8_trailing_terminators")

    def test_err_val_default_none(self):
        e = SegError("SEG_1_segment_not_found", "seg error")
        self.assertIsNone(e.err_val)

    def test_err_val_set(self):
        e = SegError("SEG_2_segment_not_used", "seg error", err_val="BAD*SEG")
        self.assertEqual(e.err_val, "BAD*SEG")

    def test_invalid_code_raises(self):
        with self.assertRaises(EngineError):
            SegError("99", "bad code")

    def test_invalid_code_legacy_raw_X12_rejected(self):
        # Raw X12 codes were accepted pre-PR-5. Now rejected.
        with self.assertRaises(EngineError):
            SegError("1", "bad code")

    def test_invalid_code_zero(self):
        with self.assertRaises(EngineError):
            SegError("0", "bad code")


class TestEleError(unittest.TestCase):
    # PR 5 (#TBD) tightens EleError validation to require pyx12 codes
    # from pyx12.error_codes.ERROR_CODES. Raw X12 codes like "1" / "10"
    # are no longer accepted.
    def test_valid_code(self):
        e = EleError("ELE_1_mandatory_missing", "element error")
        self.assertEqual(e.err_cde, "ELE_1_mandatory_missing")
        self.assertEqual(e.err_str, "element error")

    def test_valid_code_10(self):
        e = EleError("ELE_10_not_used", "element error")
        self.assertEqual(e.err_cde, "ELE_10_not_used")

    def test_refdes_default_none(self):
        e = EleError("ELE_1_mandatory_missing", "element error")
        self.assertIsNone(e.refdes)

    def test_refdes_set(self):
        e = EleError("ELE_1_mandatory_missing", "element error", refdes="03")
        self.assertEqual(e.refdes, "03")

    def test_err_val_default_none(self):
        e = EleError("ELE_1_mandatory_missing", "element error")
        self.assertIsNone(e.err_val)

    def test_err_val_set(self):
        e = EleError("ELE_4_too_short", "element error", err_val="BADVAL")
        self.assertEqual(e.err_val, "BADVAL")

    def test_invalid_code_raises(self):
        with self.assertRaises(EngineError):
            EleError("11", "bad code")

    def test_invalid_code_legacy_raw_X12_rejected(self):
        # Raw X12 codes were accepted pre-PR-5. Now rejected.
        with self.assertRaises(EngineError):
            EleError("1", "bad code")

    def test_invalid_code_zero(self):
        with self.assertRaises(EngineError):
            EleError("0", "bad code")


if __name__ == "__main__":
    unittest.main()
