import logging
import tempfile
import unittest
from io import StringIO
from types import SimpleNamespace

import pyx12.error_handler
import pyx12.map_if
import pyx12.params
import pyx12.segment
import pyx12.x12file
import pyx12.x12n_document
import pyx12.x12xml_simple
import pyx12.xmlx12_simple
from pyx12.test.x12testdata import datafiles


class XmlTransformTestCase(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()
        self.logger = logging.getLogger("pyx12")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        hdlr = logging.NullHandler()
        self.logger.addHandler(hdlr)

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
        Just want to know if the important bits of the 997 are different
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

    def _test_x12xml_simple(self, datakey):
        self.assertIn(datakey, datafiles)
        self.assertIn("source", datafiles[datakey])
        # self.assertIn('res997', datafiles[datakey])
        fd_source = self._makeFd(datafiles[datakey]["source"])

        (fdesc, filename) = tempfile.mkstemp(".xml", "pyx12_")
        with open(filename, "r+") as fd_xml:
            # fd_xml = tempfile.TemporaryFile(mode='w+', encoding='ascii')
            fd_result = StringIO()
            self.param.set("xmlout", "simple")
            result = pyx12.x12n_document.x12n_document(
                param=self.param,
                src_file=fd_source,
                fd_997=None,
                fd_html=None,
                fd_xmldoc=fd_xml,
                xslt_files=None,
            )
            self.assertTrue(result)
            fd_xml.seek(0)
            fd_result.seek(0)
            result = pyx12.xmlx12_simple.convert(fd_xml, fd_result)
            fd_source.seek(0)
            fd_result.seek(0)
            self._isX12Diff(fd_source, fd_result)


class Test834(XmlTransformTestCase):
    def test_834_lui_id(self):
        self._test_x12xml_simple("834_lui_id")

    def test_834_ls_le_ls(self):
        self._test_x12xml_simple("834_ls_le_ls")


class Test835(XmlTransformTestCase):
    def test_835id(self):
        self._test_x12xml_simple("835id")


# class ExplicitMissing(XmlTransformTestCase):
#    def test_837miss(self):
#        self._test_x12xml_simple('837miss')


class X12Structure(XmlTransformTestCase):
    # def test_mult_isa(self):
    #    self._test_x12xml_simple('mult_isa')

    # def test_trailer_errors(self):
    #    self._test_x12xml_simple('trailer_errors')

    # def test_trailing_terms(self):
    #    self._test_x12xml_simple('trailing_terms')

    # def test_elements(self):
    #    self._test_x12xml_simple('elements')

    # def test_blank1(self):
    #    self._test_x12xml_simple('blank1')

    # def test_ele(self):
    #    self._test_x12xml_simple('ele')

    # def test_loop_counting(self):
    #    self._test_x12xml_simple('loop_counting')

    # def test_loop_counting2(self):
    #    self._test_x12xml_simple('loop_counting2')

    # def test_multiple_trn(self):
    #    self._test_x12xml_simple('multiple_trn')

    def test_ordinal(self):
        self._test_x12xml_simple("ordinal")

    # def test_per_segment_repeat(self):
    #    self._test_x12xml_simple('per_segment_repeat')

    def test_repeat_init_segment(self):
        self._test_x12xml_simple("repeat_init_segment")

    # def test_simple1(self):
    #    self._test_x12xml_simple('simple1')

    def test_simple_837p(self):
        self._test_x12xml_simple("simple_837p")


def _seg_node(seg_id, loop_path, first_in_loop):
    loop = SimpleNamespace(
        is_loop=lambda: True, is_map_root=lambda: False, get_path=lambda: loop_path
    )
    return SimpleNamespace(
        id=seg_id,
        parent=loop,
        is_segment=lambda: True,
        is_map_root=lambda: False,
        is_first_seg_in_loop=lambda: first_in_loop,
    )


class LoopPathTransition(unittest.TestCase):
    def test_sibling_loop_ids_sharing_a_string_prefix(self):
        # "B" is a string prefix of sibling "BC"; entering B must not close and reopen parent A
        fd = StringIO()
        xml = pyx12.x12xml_simple.x12xml_simple(fd)
        xml.seg(_seg_node("S1", "/A/BC", True), [])
        xml.seg(_seg_node("S2", "/A/B", True), [])
        xml.close()
        self.assertEqual(fd.getvalue().count("<loop id='A'>"), 1)


class ValuesBeyondTheMap(XmlTransformTestCase):
    """Issue #35: values with no map node used to crash the XML writer."""

    def _seg_xml(self, path, seg_str):
        cmap = pyx12.map_if.load_map_file("837.4010.X098.A1.xml", self.param)
        fd = StringIO()
        xml = pyx12.x12xml_simple.x12xml_simple(fd)
        xml.seg(cmap.getnodebypath(path), pyx12.segment.Segment(seg_str, "~", "*", ":"))
        xml.close()
        return fd.getvalue()

    def test_extra_element_is_omitted(self):
        out = self._seg_xml(
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2010AA/N3", "N3*399 ELM ROAD*SUITE 1*EXTRA~"
        )
        self.assertIn("SUITE 1", out)
        self.assertNotIn("EXTRA", out)

    def test_extra_subelement_is_omitted(self):
        out = self._seg_xml(
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000A/2000B/2300/HI", "HI*BK:317:::::::EXTRA~"
        )
        self.assertIn("317", out)
        self.assertNotIn("EXTRA", out)

    def test_document_with_extra_element(self):
        # The extra element is dropped, so the XML converts back to the original file
        original = datafiles["simple_837p"]["source"]
        fd_source = self._makeFd(original.replace("N3*399 ELM ROAD~", "N3*399 ELM ROAD**EXTRA~"))
        fd_xml = StringIO()
        result = pyx12.x12n_document.x12n_document(
            self.param, fd_source, None, None, fd_xmldoc=fd_xml
        )
        self.assertFalse(result)
        fd_xml.seek(0)
        fd_result = StringIO()
        pyx12.xmlx12_simple.convert(fd_xml, fd_result)
        fd_result.seek(0)
        self._isX12Diff(self._makeFd(original), fd_result)
