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

if __name__ == "__main__":
    unittest.main()
