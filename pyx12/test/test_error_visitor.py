import unittest

import pyx12.segment
from pyx12.error_visitor import ack_safe, sanitize_ack_segment
from pyx12.test.test_x12n_document import X12DocumentTestCase


class AckSafe(unittest.TestCase):
    def test_plain_ascii_unchanged(self):
        self.assertEqual(ack_safe("SMITH JOHN A-1 (2) ?!"), "SMITH JOHN A-1 (2) ?!")

    def test_ack_delimiters_substituted(self):
        self.assertEqual(ack_safe("a~b*c:d^e"), "a?b?c?d?e")

    def test_control_and_non_ascii_substituted(self):
        self.assertEqual(ack_safe("a\x01b\x7fc\xe9d☃e"), "a?b?c?d?e")

    def test_length_preserved(self):
        self.assertEqual(len(ack_safe("~" * 120)), 120)

    def test_empty(self):
        self.assertEqual(ack_safe(""), "")


class SanitizeAckSegment(unittest.TestCase):
    def _fmt(self, seg):
        return seg.format("~", "*", ":")

    def test_unknown_seg_id_in_ik3(self):
        seg = pyx12.segment.Segment("IK3", "~", "*", ":")
        seg.set("01", "AAA~IEA*1*X~")
        seg.set("02", "7")
        sanitize_ack_segment(seg)
        self.assertEqual(self._fmt(seg), "IK3*AAA?IEA?1?X?*7~")

    def test_subelement_separator_collapsed_to_single_element(self):
        seg = pyx12.segment.Segment("IK4*3*1035*5", "~", "*", ":")
        seg.set("IK404", "A:B:C")
        self.assertEqual(len(seg.get("IK404")), 3)
        sanitize_ack_segment(seg)
        self.assertEqual(len(seg.get("IK404")), 1)
        self.assertEqual(self._fmt(seg), "IK4*3*1035*5*A?B?C~")

    def test_ik4_position_composite_kept(self):
        seg = pyx12.segment.Segment("IK4*3:2:1*1035*5*x", "~", "*", ":")
        sanitize_ack_segment(seg)
        self.assertEqual(self._fmt(seg), "IK4*3:2:1*1035*5*x~")

    def test_ak4_position_composite_kept(self):
        seg = pyx12.segment.Segment("AK4*3:2*1035*5*x", "~", "*", ":")
        sanitize_ack_segment(seg)
        self.assertEqual(self._fmt(seg), "AK4*3:2*1035*5*x~")

    def test_isa_delimiter_slots_kept_and_ids_sanitized(self):
        seg = pyx12.segment.Segment(
            "ISA*00*          *00*          *ZZ*SEND           *ZZ*RECV           "
            "*261031*1200*^*00501*000000001*0*P*:",
            "~",
            "*",
            ":",
        )
        seg.set("06", "A~B*C^D        ")
        sanitize_ack_segment(seg)
        self.assertEqual(seg.get_value("ISA06"), "A?B?C?D        ")
        self.assertEqual(seg.get_value("ISA11"), "^")
        self.assertEqual(seg.get_value("ISA16"), ":")

    def test_clean_segment_untouched(self):
        seg = pyx12.segment.Segment("AK9*R*1*1*0*5", "~", "*", ":")
        sanitize_ack_segment(seg)
        self.assertEqual(self._fmt(seg), "AK9*R*1*1*0*5~")


class AckInjection(X12DocumentTestCase):
    """A hostile data value must not forge segments in the 997 / 999."""

    def test_999_ik4_04_sanitized_and_truncated(self):
        self._test_999("834_lui_id_5010_ack_injection")

    def test_997_ak4_04_sanitized(self):
        self._test_997("270_4010_ack_injection")
