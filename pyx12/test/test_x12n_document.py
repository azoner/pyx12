import json
import os
import tempfile
import unittest
from io import StringIO

import pyx12.error_handler
import pyx12.params
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
