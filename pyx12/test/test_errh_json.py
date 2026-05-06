import json
import unittest
from io import StringIO
from unittest.mock import MagicMock

import pyx12.errh_json
import pyx12.error_handler
import pyx12.segment


def _fake_src(isa_id="000000001", gs_id="1", st_id="0001", cur_line=1, st_count=1):
    src = MagicMock()
    src.get_isa_id.return_value = isa_id
    src.get_gs_id.return_value = gs_id
    src.get_st_id.return_value = st_id
    src.get_cur_line.return_value = cur_line
    src.st_count = st_count
    return src


def _isa_segment():
    raw = (
        "ISA*00*          *00*          *ZZ*SENDER         *ZZ*RECEIVER       "
        "*200101*1200*U*00501*000000001*0*P*:~"
    )
    return pyx12.segment.Segment(raw, "~", "*", ":")


def _gs_segment():
    return pyx12.segment.Segment(
        "GS*HC*SENDER*RECEIVER*20200101*1200*1*X*005010X222A1", "~", "*", ":"
    )


def _st_segment():
    return pyx12.segment.Segment("ST*837*0001*005010X222A1", "~", "*", ":")


def _build_tree_with_errors() -> pyx12.error_handler.err_handler:
    """Build a small but complete err_handler tree exercising every level
    that the JSON visitor cares about: an ISA-level error, a GS-level
    error, an ST-level error, a segment with seg-level errors plus two
    element children carrying their own errors."""
    eh = pyx12.error_handler.err_handler()
    src = _fake_src()
    eh.add_isa_loop(_isa_segment(), src)
    eh.cur_isa_node.add_error("100", "ISA-level error")

    eh.add_gs_loop(_gs_segment(), src)
    eh.cur_gs_node.add_error("4", "GS-level error")
    eh.cur_gs_node.ack_code = "R"
    eh.cur_gs_node.st_count_orig = 1
    eh.cur_gs_node.st_count_recv = 1

    eh.add_st_loop(_st_segment(), src)
    eh.cur_st_node.add_error("23", "ST-level error")
    eh.cur_st_node.ack_code = "R"

    seg_map = MagicMock()
    seg_map.name = "Claim Information"
    seg_map.pos = 130
    eh.add_seg(seg_map, _seg_segment_clm(), seg_count=5, cur_line=42, ls_id="2300")
    eh.seg_error("8", "Segment has data element errors", None, 42)

    ele_map_a = MagicMock()
    ele_map_a.data_ele = "1028"
    ele_map_a.name = "Claim Submitter's Identifier"
    ele_map_a.seq = 1
    ele_map_a.parent.is_composite.return_value = False
    eh.add_ele(ele_map_a)
    eh.ele_error("7", "Invalid Code Value", "BAD", "CLM01")

    ele_map_b = MagicMock()
    ele_map_b.data_ele = "782"
    ele_map_b.name = "Monetary Amount"
    ele_map_b.seq = 2
    ele_map_b.parent.is_composite.return_value = False
    eh.add_ele(ele_map_b)
    eh.ele_error("6", "Invalid character in data element", "X", "CLM02")

    return eh


def _seg_segment_clm():
    return pyx12.segment.Segment("CLM*ABC*100***11:B:1", "~", "*", ":")


class ErrhJsonVisitorOutput(unittest.TestCase):
    """The JSON visitor walks the err_handler tree and emits a nested
    document with one entry per ISA / GS / ST / segment / element level."""

    def setUp(self):
        eh = _build_tree_with_errors()
        out = StringIO()
        visitor = pyx12.errh_json.errh_json_visitor(out, indent=None)
        eh.accept(visitor)
        out.seek(0)
        self.doc = json.loads(out.read())

    def test_top_level_shape(self):
        self.assertEqual(list(self.doc.keys()), ["interchanges"])
        self.assertEqual(len(self.doc["interchanges"]), 1)

    def test_isa_level_error_captured(self):
        isa = self.doc["interchanges"][0]
        self.assertEqual(isa["isa_trn_set_id"], "000000001")
        # x12_code falls through to err_cde for any code not in
        # pyx12.error_codes.ERROR_CODES (legacy raw-X12 codes; PR 1).
        self.assertEqual(
            isa["errors"],
            [{"err_cde": "100", "x12_code": "100", "err_str": "ISA-level error"}],
        )
        self.assertEqual(len(isa["groups"]), 1)

    def test_gs_level_error_captured(self):
        gs = self.doc["interchanges"][0]["groups"][0]
        self.assertEqual(gs["fic"], "HC")
        self.assertEqual(gs["vriic"], "005010X222A1")
        self.assertEqual(gs["ack_code"], "R")
        self.assertEqual(
            gs["errors"],
            [{"err_cde": "4", "x12_code": "4", "err_str": "GS-level error"}],
        )
        self.assertEqual(len(gs["transactions"]), 1)

    def test_st_level_error_captured(self):
        st = self.doc["interchanges"][0]["groups"][0]["transactions"][0]
        self.assertEqual(st["trn_set_id"], "837")
        self.assertEqual(st["trn_set_control_num"], "0001")
        self.assertEqual(st["ack_code"], "R")
        self.assertEqual(
            st["errors"],
            [{"err_cde": "23", "x12_code": "23", "err_str": "ST-level error"}],
        )
        self.assertEqual(len(st["segments"]), 1)

    def test_seg_level_error_captured(self):
        seg = self.doc["interchanges"][0]["groups"][0]["transactions"][0]["segments"][0]
        self.assertEqual(seg["seg_id"], "CLM")
        self.assertEqual(seg["seg_count"], 5)
        self.assertEqual(seg["pos"], 130)
        self.assertEqual(seg["name"], "Claim Information")
        self.assertEqual(seg["ls_id"], "2300")
        self.assertEqual(
            seg["errors"],
            [
                {
                    "err_cde": "8",
                    "x12_code": "8",
                    "err_str": "Segment has data element errors",
                    "err_val": None,
                }
            ],
        )
        self.assertEqual(len(seg["elements"]), 2)

    def test_element_level_errors_captured(self):
        elements = self.doc["interchanges"][0]["groups"][0]["transactions"][0]["segments"][0][
            "elements"
        ]
        self.assertEqual(elements[0]["ele_pos"], 1)
        self.assertEqual(elements[0]["ele_ref_num"], "1028")
        self.assertEqual(elements[0]["name"], "Claim Submitter's Identifier")
        self.assertEqual(
            elements[0]["errors"],
            [
                {
                    "err_cde": "7",
                    "x12_code": "7",
                    "err_str": "Invalid Code Value",
                    "err_val": "BAD",
                }
            ],
        )
        self.assertEqual(elements[1]["ele_pos"], 2)
        self.assertEqual(elements[1]["ele_ref_num"], "782")


class ErrhJsonVisitorEmptyTree(unittest.TestCase):
    """A fresh err_handler with no children should produce a well-formed
    JSON document with an empty interchanges list — no exceptions."""

    def test_empty_tree_emits_empty_document(self):
        eh = pyx12.error_handler.err_handler()
        out = StringIO()
        visitor = pyx12.errh_json.errh_json_visitor(out, indent=None)
        eh.accept(visitor)
        out.seek(0)
        doc = json.loads(out.read())
        self.assertEqual(doc, {"interchanges": []})


class ErrhJsonVisitorIndent(unittest.TestCase):
    """The indent argument is passed through to json.dump."""

    def test_default_indent_produces_pretty_output(self):
        eh = pyx12.error_handler.err_handler()
        out = StringIO()
        visitor = pyx12.errh_json.errh_json_visitor(out)  # default indent=2
        eh.accept(visitor)
        out.seek(0)
        text = out.read()
        self.assertIn("\n", text)

    def test_indent_none_produces_compact_output(self):
        eh = pyx12.error_handler.err_handler()
        out = StringIO()
        visitor = pyx12.errh_json.errh_json_visitor(out, indent=None)
        eh.accept(visitor)
        out.seek(0)
        text = out.read()
        self.assertNotIn("\n", text)


if __name__ == "__main__":
    unittest.main()
