import unittest
from io import StringIO

import pyx12.error_handler
import pyx12.error_html
import pyx12.x12n_document
from pyx12.test.test_x12n_document import X12DocumentTestCase
from pyx12.test.x12testdata import datafiles


class Footer(unittest.TestCase):
    def test_no_envelopes(self):
        # No ISA/GS/ST node was ever added; footer used to raise AttributeError
        fd = StringIO()
        html = pyx12.error_html.error_html(pyx12.error_handler.err_handler(), fd, ("~", "*", ":"))
        html.footer()
        self.assertTrue(fd.getvalue().endswith("</html>\n"))


class Escaping(unittest.TestCase):
    def _report(self):
        fd = StringIO()
        return pyx12.error_html.error_html(
            pyx12.error_handler.err_handler(), fd, ("~", "*", ":")
        ), fd

    def test_error_line_escapes_message_and_code(self):
        report, fd = self._report()
        report._write_error('bad "<script>alert(1)</script>" & more', "<b>", "Element")
        self.assertEqual(
            fd.getvalue(),
            '<span class="error">&nbsp;bad "&lt;script&gt;alert(1)&lt;/script&gt;" '
            "&amp; more (Element Error Code: &lt;b&gt;)</span><br />\n",
        )

    def test_segment_id_escaped(self):
        report, _ = self._report()
        self.assertEqual(report._seg_str("<img src=x>", ["1"]), "&lt;img&nbsp;src=x&gt;*1~")


class HostileValues(X12DocumentTestCase):
    """Attacker-controlled input must never reach the HTML report unescaped."""

    def test_markup_in_value_and_segment_id_is_escaped(self):
        src = datafiles["834_lui_id_5010"]["source"]
        src = src.replace("NM1*IL*1*DOE*", "NM1*IL*1*DOE<script>alert(1)</script>" + "A" * 40 + "*")
        src = src.replace("N3*777 ELM ST~", "<img src=x onerror=alert(2)>*777 ELM ST~")
        fd_html = StringIO()
        pyx12.x12n_document.x12n_document(self.param, self._makeFd(src), StringIO(), fd_html, None)
        out = fd_html.getvalue()
        self.assertNotIn("<script", out)
        self.assertNotIn("<img", out)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", out)
        self.assertIn('Segment identifier "&lt;img src=x onerror=alert(2)&gt;" is invalid', out)
