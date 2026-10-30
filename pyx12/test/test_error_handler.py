import unittest
from unittest.mock import MagicMock

from pyx12.error_handler import err_handler


class TestErrHandlerInit(unittest.TestCase):
    def test_ele_node_added_initialized(self):
        # Both bookkeeping flags must be initialized in __init__ — see
        # test_ele_error_before_add_ele_does_not_raise for why this matters.
        eh = err_handler()
        self.assertFalse(eh.ele_node_added)

    def test_seg_node_added_initialized(self):
        eh = err_handler()
        self.assertFalse(eh.seg_node_added)


class TestEleErrorBeforeAddEle(unittest.TestCase):
    def test_ele_error_before_add_ele_does_not_raise(self):
        # Regression for the call chain x12n_document.x12n_document ->
        # apply_segment_errors -> err_handler.ele_error -> _add_cur_ele,
        # which reads self.ele_node_added. apply_segment_errors iterates
        # element-level errors discovered during segment validation and
        # calls ele_error directly without going through add_ele, so on a
        # fresh err_handler ele_node_added would be unset and reading it
        # raised AttributeError.
        eh = err_handler()
        # Simulate state after a segment has been added but no element has
        # yet been added (apply_segment_errors emits element-level errors
        # without going through add_ele first).
        eh.cur_seg_node = MagicMock()
        eh.cur_seg_node.get_cur_line.return_value = 1
        eh.cur_seg_node.elements = []
        eh.seg_node_added = True
        eh.cur_ele_node = MagicMock()
        eh.ele_error("8", "Invalid Code Value", "bad", "REF02")
        self.assertTrue(eh.ele_node_added)
        self.assertEqual(len(eh.cur_seg_node.elements), 1)


class TestSegErrorOutsideTransactionSet(unittest.TestCase):
    def _errh_after_add_seg(self, cur_st_node):
        # State after errh.add_seg(): a new segment node is pending under cur_st_node
        eh = err_handler()
        eh.cur_isa_node = MagicMock()
        eh.cur_isa_node.get_cur_line.return_value = 1
        eh.cur_st_node = cur_st_node
        eh.cur_seg_node = MagicMock()
        eh.seg_node_added = False
        return eh

    def test_no_transaction_set_goes_to_interchange(self):
        eh = self._errh_after_add_seg(None)
        eh.seg_error("SEG_3_mandatory_loop_missing", "ST_LOOP missing")
        eh.cur_isa_node.add_error.assert_called_once_with(
            "ISA_024_invalid_content", "ST_LOOP missing"
        )
        eh.cur_seg_node.add_error.assert_not_called()

    def test_closed_transaction_set_goes_to_interchange(self):
        st = MagicMock()
        st.is_closed.return_value = True
        eh = self._errh_after_add_seg(st)
        eh.seg_error("SEG_5_segment_repeat_exceeded", "Segment GE exceeded max count")
        eh.cur_isa_node.add_error.assert_called_once_with(
            "ISA_024_invalid_content", "Segment GE exceeded max count"
        )
        st.children.append.assert_not_called()

    def test_open_transaction_set_keeps_segment_error(self):
        st = MagicMock()
        st.is_closed.return_value = False
        eh = self._errh_after_add_seg(st)
        eh.seg_error("SEG_5_segment_repeat_exceeded", "Segment N3 exceeded max count")
        st.children.append.assert_called_once_with(eh.cur_seg_node)
        eh.cur_seg_node.add_error.assert_called_once_with(
            "SEG_5_segment_repeat_exceeded", "Segment N3 exceeded max count", None
        )
        eh.cur_isa_node.add_error.assert_not_called()


if __name__ == "__main__":
    unittest.main()
