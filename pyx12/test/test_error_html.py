import unittest
from io import StringIO

import pyx12.error_handler
import pyx12.error_html


class Footer(unittest.TestCase):
    def test_no_envelopes(self):
        # No ISA/GS/ST node was ever added; footer used to raise AttributeError
        fd = StringIO()
        html = pyx12.error_html.error_html(pyx12.error_handler.err_handler(), fd, ("~", "*", ":"))
        html.footer()
        self.assertTrue(fd.getvalue().endswith("</html>\n"))
