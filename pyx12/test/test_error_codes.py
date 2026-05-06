"""Invariants on the pyx12 error code registry."""

import unittest

from pyx12.error_codes import ERROR_CODES, ErrorCodeSpec, x12_code_for

# Mapping from a pyx12 code-name prefix to the level the code MUST
# carry in its ErrorCodeSpec. Composites surface as element-level
# errors in the err_handler tree (composite errors flow through
# err_ele.errors via apply_segment_errors / errh.ele_error), so
# COMP_-prefixed codes share the "ELE" level with ELE_ codes.
PREFIX_TO_LEVEL = {
    "ELE_": "ELE",
    "COMP_": "ELE",
    "SEG_": "SEG",
}


class TableConsistency(unittest.TestCase):
    """Every code in ERROR_CODES has a name prefix matching its
    declared ErrorCodeSpec.level. Catches typos like naming a code
    SEG_3_foo with level="ELE", or an entry whose key string disagrees
    with its spec.code field."""

    def test_every_code_has_a_known_prefix(self):
        for code in ERROR_CODES:
            self.assertTrue(
                any(code.startswith(p) for p in PREFIX_TO_LEVEL),
                f"Code {code!r} does not start with any of "
                f"{tuple(PREFIX_TO_LEVEL)} — extend PREFIX_TO_LEVEL or "
                f"rename the code.",
            )

    def test_prefix_matches_spec_level(self):
        for code, spec in ERROR_CODES.items():
            for prefix, level in PREFIX_TO_LEVEL.items():
                if code.startswith(prefix):
                    self.assertEqual(
                        spec.level,
                        level,
                        f"Code {code!r} has prefix {prefix!r} (level={level}) "
                        f"but ErrorCodeSpec.level={spec.level!r}",
                    )
                    break

    def test_key_matches_spec_code(self):
        for code, spec in ERROR_CODES.items():
            self.assertEqual(
                code,
                spec.code,
                f"ERROR_CODES key {code!r} disagrees with ErrorCodeSpec.code={spec.code!r}",
            )

    def test_ak_and_ik_codes_when_set_are_short_strings(self):
        # X12 spec codes are 1-3 characters (e.g. "1"-"10", "I4"-"I13").
        for code, spec in ERROR_CODES.items():
            for field, value in (("ak_code", spec.ak_code), ("ik_code", spec.ik_code)):
                if value is None:
                    continue
                self.assertIsInstance(value, str)
                self.assertTrue(
                    1 <= len(value) <= 3,
                    f"Code {code!r} {field}={value!r} is not a 1-3 char X12 ack code",
                )


class X12CodeForResolution(unittest.TestCase):
    """x12_code_for returns the dereferenced X12 code for pyx12 codes
    in ERROR_CODES, and falls through to err_cde unchanged for codes
    not in the table (envelope-level passthrough)."""

    def test_known_code_resolves_to_ik_code(self):
        self.assertEqual(x12_code_for("ELE_8_invalid_date"), "8")
        self.assertEqual(x12_code_for("SEG_5_segment_repeat_exceeded"), "5")

    def test_unknown_code_falls_through(self):
        # ISA-level codes like "025" aren't in ERROR_CODES but should
        # round-trip unchanged for JSON x12_code field rendering.
        self.assertEqual(x12_code_for("025"), "025")
        self.assertEqual(x12_code_for("010"), "010")

    def test_ak_preferred_when_ik_is_none(self):
        # Synthetic spec with ik_code=None -> should fall back to
        # ak_code in prefer_5010 mode (current implementation: first
        # consult ik_code, then ak_code).
        spec = ErrorCodeSpec(
            code="X_1_synthetic",
            level="SEG",
            description="synthetic",
            ak_code="1",
            ik_code=None,
        )
        # Patch ERROR_CODES temporarily.
        try:
            ERROR_CODES[spec.code] = spec
            self.assertEqual(x12_code_for(spec.code, prefer_5010=True), "1")
            self.assertEqual(x12_code_for(spec.code, prefer_5010=False), "1")
        finally:
            del ERROR_CODES[spec.code]


if __name__ == "__main__":
    unittest.main()
