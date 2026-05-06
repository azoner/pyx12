import json
import os
import tempfile
import unittest
from io import StringIO
from typing import Any

import pyx12.error_handler
import pyx12.params
import pyx12.x12context
import pyx12.x12n_document
from pyx12.test.x12testdata import datafiles


class X12DocumentTestCase(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()

    def _makeFd(self, x12str=None):
        try:
            if x12str:
                fd = StringIO(x12str)
            else:
                fd = StringIO()
        except Exception:
            if x12str:
                fd = StringIO(x12str, encoding="ascii")
            else:
                fd = StringIO(encoding="ascii")
        fd.seek(0)
        return fd

    def _isX12Diff(self, fd1, fd2):
        """
        Just want to know if the important bits of the x12 docs are different
        """
        src1 = pyx12.x12file.X12Reader(fd1)
        src2 = pyx12.x12file.X12Reader(fd2)
        segs1 = [
            x.format() for x in src1 if x.get_seg_id() not in ("ISA", "GS", "ST", "SE", "GE", "IEA")
        ]
        segs2 = [
            x.format() for x in src2 if x.get_seg_id() not in ("ISA", "GS", "ST", "SE", "GE", "IEA")
        ]
        self.assertListEqual(segs1, segs2)

    def _test_997(self, datakey):
        self.assertIn(datakey, datafiles)
        self.assertIn("source", datafiles[datakey])
        self.assertIn("res997", datafiles[datakey])
        fd_source = self._makeFd(datafiles[datakey]["source"])
        fd_997_base = self._makeFd(datafiles[datakey]["res997"])
        fd_997 = StringIO()
        fd_html = StringIO()
        import logging

        logger = logging.getLogger("pyx12")
        # logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        hdlr = logging.NullHandler()
        # hdlr = logging.StreamHandler()
        # hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        pyx12.x12n_document.x12n_document(self.param, fd_source, fd_997, fd_html, None)
        fd_997.seek(0)
        self._isX12Diff(fd_997_base, fd_997)

    def _test_999(self, datakey):
        self.assertIn(datakey, datafiles)
        self.assertIn("source", datafiles[datakey])
        self.assertIn("resAck", datafiles[datakey])
        fd_source = self._makeFd(datafiles[datakey]["source"])
        fd_997_base = self._makeFd(datafiles[datakey]["resAck"])
        fd_997 = StringIO()
        fd_html = StringIO()
        import logging

        logger = logging.getLogger("pyx12")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        hdlr = logging.NullHandler()
        logger.addHandler(hdlr)
        pyx12.x12n_document.x12n_document(self.param, fd_source, fd_997, fd_html, None)
        fd_997.seek(0)
        self._isX12Diff(fd_997_base, fd_997)

    def _test_json(self, datakey):
        self.assertIn(datakey, datafiles)
        self.assertIn("source", datafiles[datakey])
        self.assertIn("resJson", datafiles[datakey])
        fd_source = self._makeFd(datafiles[datakey]["source"])
        fd_997 = StringIO()
        fd_json = StringIO()
        pyx12.x12n_document.x12n_document(
            self.param, fd_source, fd_997, None, None, fd_json=fd_json
        )
        fd_json.seek(0)
        actual = json.loads(fd_json.read())
        self.assertEqual(actual, datafiles[datakey]["resJson"])


class Test834(X12DocumentTestCase):
    def test_834_lui_id(self):
        self._test_997("834_lui_id")

    def test_834_lui_id_json(self):
        self._test_json("834_lui_id")

    def test_834_ls_le_ls(self):
        self._test_999("834_ls_le_ls")

    def test_834_ls_le_ls_json(self):
        self._test_json("834_ls_le_ls")


class Test835(X12DocumentTestCase):
    def test_835id(self):
        self._test_997("835id")

    def test_835id_json(self):
        self._test_json("835id")


class ExplicitMissing(X12DocumentTestCase):
    def test_837miss(self):
        self._test_997("837miss")

    def test_837miss_json(self):
        self._test_json("837miss")


class X12Structure(X12DocumentTestCase):
    def test_mult_isa(self):
        self._test_997("mult_isa")

    def test_mult_isa_json(self):
        self._test_json("mult_isa")

    def test_trailer_errors(self):
        self._test_997("trailer_errors")

    def test_trailer_errors_json(self):
        self._test_json("trailer_errors")

    def test_trailing_terms(self):
        self._test_997("trailing_terms")

    def test_trailing_terms_json(self):
        self._test_json("trailing_terms")

    def test_bad_2010AA_bug(self):
        self._test_997("bad_2010AA_bug")

    def test_bad_2010AA_bug_json(self):
        self._test_json("bad_2010AA_bug")

    def test_elements(self):
        self._test_997("elements")

    def test_elements_json(self):
        self._test_json("elements")

    def test_bad_header_looping(self):
        self._test_997("bad_header_looping")

    def test_bad_header_looping_json(self):
        self._test_json("bad_header_looping")

    def test_blank1(self):
        self._test_997("blank1")

    def test_blank1_json(self):
        self._test_json("blank1")

    def test_ele(self):
        self._test_997("ele")

    def test_ele_json(self):
        self._test_json("ele")

    def test_fail_no_IEA(self):
        self._test_997("fail_no_IEA")

    def test_fail_no_IEA_json(self):
        self._test_json("fail_no_IEA")

    def test_loop_counting(self):
        self._test_997("loop_counting")

    def test_loop_counting_json(self):
        self._test_json("loop_counting")

    def test_loop_counting2(self):
        self._test_997("loop_counting2")

    def test_loop_counting2_json(self):
        self._test_json("loop_counting2")

    def test_multiple_trn(self):
        self._test_997("multiple_trn")

    def test_multiple_trn_json(self):
        self._test_json("multiple_trn")

    def test_ordinal(self):
        self._test_997("ordinal")

    def test_ordinal_json(self):
        self._test_json("ordinal")

    def test_per_segment_repeat(self):
        self._test_997("per_segment_repeat")

    def test_per_segment_repeat_json(self):
        self._test_json("per_segment_repeat")

    def test_repeat_init_segment(self):
        self._test_997("repeat_init_segment")

    def test_repeat_init_segment_json(self):
        self._test_json("repeat_init_segment")

    def test_simple1(self):
        self._test_997("simple1")

    def test_simple1_json(self):
        self._test_json("simple1")

    def test_simple_837p(self):
        self._test_997("simple_837p")

    def test_simple_837p_json(self):
        self._test_json("simple_837p")


class Test5010(X12DocumentTestCase):
    def test_834_lui_id_5010(self):
        self._test_999("834_lui_id_5010")

    def test_834_lui_id_5010_json(self):
        self._test_json("834_lui_id_5010")

    def test_834_lui_id_5010_non_ascii(self):
        # Non-ASCII char in REF02 → 999 ack must:
        # - emit IK4*2*127*6 (invalid character at element 2, ref-num 127)
        # - sanitize bad_value to ASCII (0x3F `?` substitutes the 0xE9 `é`)
        self._test_999("834_lui_id_5010_non_ascii")

    def test_834_lui_id_5010_non_ascii_json(self):
        # Same source, JSON output preserves the original codepoint in
        # err_str / err_val (unicode-safe channel, full fidelity).
        self._test_json("834_lui_id_5010_non_ascii")

    def test_834_eol_in_element(self):
        self._test_999("834_eol_in_element")

    def test_834_eol_in_element_json(self):
        self._test_json("834_eol_in_element")


class TestTemp(X12DocumentTestCase):
    def test_999_temp(self):
        datakey = "834_lui_id"
        fd_source = self._makeFd(datafiles[datakey]["source"])
        fd_997 = tempfile.TemporaryFile(mode="w+", encoding="ascii")
        fd_html = None
        import logging

        logger = logging.getLogger("pyx12")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        hdlr = logging.NullHandler()
        logger.addHandler(hdlr)
        param = pyx12.params.params()
        pyx12.x12n_document.x12n_document(param, fd_source, fd_997, fd_html, None)
        fd_997.seek(0)
        # self._isX12Diff(fd_997_base, fd_997)


class UnicodeInput(X12DocumentTestCase):
    """Regression for #157: non-ASCII bytes in the input file must
    surface as validation errors, not a UnicodeDecodeError that crashes
    the parser. Historically `open(..., encoding='ascii')` raised on
    the first non-ASCII byte; the file is now opened with latin-1 (a
    never-fail single-byte codec), so non-ASCII codepoints are passed
    through to the validator where rec_ID_B / rec_ID_E reject them via
    normal error paths."""

    def test_non_ascii_byte_does_not_raise(self):
        # Embed `é` (0xE9 in latin-1) inside a REF02 value of a real fixture.
        source = datafiles["834_lui_id"]["source"].replace("REF*0F*00389999", "REF*0F*00389\xe9999")
        # Write the source to a tempfile so x12n_document opens it via the
        # filename path (i.e. exercises the encoding choice in X12Reader).
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".x12", delete=False) as f:
            f.write(source.encode("latin-1"))
            temppath = f.name
        try:
            fd_997 = StringIO()
            # Must not raise UnicodeDecodeError. Return value can be either
            # — what matters is that the parser ran end-to-end.
            pyx12.x12n_document.x12n_document(self.param, temppath, fd_997, None, None)
        finally:
            os.unlink(temppath)


class ErrorCodePrefixPlacement(X12DocumentTestCase):
    """The pyx12 code prefix must match the X12 node type in the
    err_handler tree:

    * Codes stored on err_seg.errors must start with ``SEG_``.
    * Codes stored on err_ele.errors must start with ``ELE_`` or
      ``COMP_`` (composites surface as element-level errors).

    Verified by running representative fixtures through x12n_document
    and walking the resulting err_handler tree."""

    def _walk_tree(self, datakey: str) -> pyx12.error_handler.err_handler:
        errh = pyx12.error_handler.err_handler()
        fd_source = self._makeFd(datafiles[datakey]["source"])
        fd_997 = StringIO()
        fd_html = StringIO()
        # x12n_document creates its own err_handler internally, so we
        # can't pass ours. Drive X12ContextReader instead — it accepts
        # a caller-provided errh and threads it through (PR #166).
        src = pyx12.x12context.X12ContextReader(self.param, errh, fd_source)
        for _ in src.iter_segments():
            pass
        return errh

    def _collect(self, errh: pyx12.error_handler.err_handler) -> tuple[list[str], list[str]]:
        seg_codes: list[str] = []
        ele_codes: list[str] = []
        for isa in errh.children:
            for gs in isa.children:
                for st in gs.children:
                    for seg in st.children:
                        seg_codes.extend(c for c, *_ in seg.errors)
                        for ele in seg.elements:
                            ele_codes.extend(c for c, *_ in ele.errors)
        return seg_codes, ele_codes

    def test_walker_seg_errors_have_seg_prefix(self):
        # bad_2010AA_bug -> walker emits SEG_3_mandatory_loop_missing.
        errh = self._walk_tree("bad_2010AA_bug")
        seg_codes, _ = self._collect(errh)
        self.assertTrue(seg_codes, "expected at least one seg-level error")
        for code in seg_codes:
            self.assertTrue(
                code.startswith("SEG_"),
                f"seg-level err_cde {code!r} does not start with SEG_",
            )

    def test_validator_ele_errors_have_ele_or_comp_prefix(self):
        # 834_lui_id_5010_non_ascii -> ELE_6_invalid_type_char on REF02.
        errh = self._walk_tree("834_lui_id_5010_non_ascii")
        _, ele_codes = self._collect(errh)
        self.assertTrue(ele_codes, "expected at least one element-level error")
        for code in ele_codes:
            self.assertTrue(
                code.startswith("ELE_") or code.startswith("COMP_"),
                f"element-level err_cde {code!r} does not start with ELE_ or COMP_",
            )

    def test_no_raw_x12_code_leaks_into_seg_or_ele_errors(self):
        # Run several fixtures through and verify the prefix invariant
        # holds across the corpus.
        for datakey in (
            "bad_2010AA_bug",
            "834_lui_id_5010_non_ascii",
            "elements",
            "trailing_terms",
            "loop_counting",
            "loop_counting2",
            "multiple_trn",
        ):
            with self.subTest(datakey=datakey):
                errh = self._walk_tree(datakey)
                seg_codes, ele_codes = self._collect(errh)
                for code in seg_codes:
                    self.assertTrue(
                        code.startswith("SEG_"),
                        f"[{datakey}] seg-level err_cde {code!r} is not a SEG_-prefixed pyx12 code",
                    )
                for code in ele_codes:
                    self.assertTrue(
                        code.startswith("ELE_") or code.startswith("COMP_"),
                        f"[{datakey}] element-level err_cde {code!r} is not "
                        f"an ELE_- or COMP_-prefixed pyx12 code",
                    )


class SuppressErrorCodes(X12DocumentTestCase):
    """PR 6 of the error-code generalization plan: pyx12 codes can be
    suppressed via params.suppress_error_codes. Suppressed codes are
    filtered out at the apply_segment_errors / apply_walk_errors bridge
    point, so they never reach the err_handler tree, the 997/999 ack,
    or JSON output."""

    def setUp(self):
        super().setUp()
        # 834_lui_id_5010_non_ascii has REF02 = "00389\xe9999" which the
        # validator rejects as ELE_6_invalid_type_char. We use it as the
        # fixture source for the suppression scenario.
        self.suppress_target_source = datafiles["834_lui_id_5010_non_ascii"]["source"]

    def _run_with_suppression(self, codes: set[str]) -> tuple[str, dict[str, Any]]:
        param = pyx12.params.params()
        param.set("suppress_error_codes", codes)
        fd_source = self._makeFd(self.suppress_target_source)
        fd_997 = StringIO()
        fd_json = StringIO()
        pyx12.x12n_document.x12n_document(param, fd_source, fd_997, None, None, fd_json=fd_json)
        fd_997.seek(0)
        fd_json.seek(0)
        return fd_997.read(), json.loads(fd_json.read())

    def test_suppression_removes_element_error_from_999(self):
        # Without suppression, the 999 ack contains an IK4 segment for
        # the bad REF02 value.
        ack_no_suppress, _ = self._run_with_suppression(set())
        self.assertIn("IK4", ack_no_suppress)
        # With ELE_6_invalid_type_char suppressed, no IK4 in the ack.
        ack_suppressed, _ = self._run_with_suppression({"ELE_6_invalid_type_char"})
        self.assertNotIn("IK4", ack_suppressed)

    def test_suppression_removes_element_error_from_json(self):
        # Without suppression, the JSON output has an element error
        # entry with err_cde = "ELE_6_invalid_type_char".
        _, doc_no_suppress = self._run_with_suppression(set())
        all_errs_no_suppress = self._collect_err_cdes(doc_no_suppress)
        self.assertIn("ELE_6_invalid_type_char", all_errs_no_suppress)
        # With suppression, that code is gone from the JSON tree.
        _, doc_suppressed = self._run_with_suppression({"ELE_6_invalid_type_char"})
        all_errs_suppressed = self._collect_err_cdes(doc_suppressed)
        self.assertNotIn("ELE_6_invalid_type_char", all_errs_suppressed)

    def test_unrelated_code_suppression_is_no_op(self):
        # Suppressing a code that doesn't appear in this fixture's
        # errors leaves output unchanged.
        baseline_ack, baseline_doc = self._run_with_suppression(set())
        with_unrelated, with_unrelated_doc = self._run_with_suppression(
            {"SEG_4_loop_repeat_exceeded"}
        )
        self.assertEqual(baseline_doc, with_unrelated_doc)
        # The 999 ack content (modulo dynamic timestamps in the envelope)
        # should be byte-identical between the two runs. Skip envelope
        # comparison and just check that the IK segments match.
        self.assertEqual(
            [seg for seg in baseline_ack.split("~") if seg.startswith("IK")],
            [seg for seg in with_unrelated.split("~") if seg.startswith("IK")],
        )

    @staticmethod
    def _collect_err_cdes(doc: dict[str, Any]) -> list[str]:
        """Walk the JSON err_handler tree and return every err_cde."""
        out: list[str] = []
        for isa in doc.get("interchanges", []):
            out.extend(e["err_cde"] for e in isa.get("errors", []))
            for gs in isa.get("groups", []):
                out.extend(e["err_cde"] for e in gs.get("errors", []))
                for st in gs.get("transactions", []):
                    out.extend(e["err_cde"] for e in st.get("errors", []))
                    for seg in st.get("segments", []):
                        out.extend(e["err_cde"] for e in seg.get("errors", []))
                        for ele in seg.get("elements", []):
                            out.extend(e["err_cde"] for e in ele.get("errors", []))
        return out


class SuppressCLIArg(unittest.TestCase):
    """The --suppress CLI flag on x12valid parses comma-separated codes
    into a set and stores them in params.suppress_error_codes."""

    def test_single_code_via_argparse(self):
        from pyx12.scripts.x12valid import build_parser

        args = build_parser().parse_args(["--suppress", "ELE_6_invalid_type_char", "f.x12"])
        self.assertEqual(args.suppress, ["ELE_6_invalid_type_char"])

    def test_comma_separated_via_argparse(self):
        from pyx12.scripts.x12valid import build_parser

        args = build_parser().parse_args(
            ["-S", "ELE_6_invalid_type_char,SEG_3_too_many_elements", "f.x12"]
        )
        self.assertEqual(args.suppress, ["ELE_6_invalid_type_char,SEG_3_too_many_elements"])

    def test_repeated_flag_via_argparse(self):
        from pyx12.scripts.x12valid import build_parser

        args = build_parser().parse_args(
            [
                "--suppress",
                "ELE_6_invalid_type_char",
                "-S",
                "SEG_3_too_many_elements",
                "f.x12",
            ]
        )
        self.assertEqual(args.suppress, ["ELE_6_invalid_type_char", "SEG_3_too_many_elements"])
