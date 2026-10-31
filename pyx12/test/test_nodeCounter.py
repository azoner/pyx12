import unittest

from pyx12.nodeCounter import NodeCounter


class TestNodeCounterInit(unittest.TestCase):
    def test_empty_init(self):
        nc = NodeCounter()
        self.assertEqual(nc.get_count("/ISA_LOOP/GS_LOOP"), 0)

    def test_init_with_counts(self):
        nc = NodeCounter({"/ISA_LOOP/GS_LOOP": 3})
        self.assertEqual(nc.get_count("/ISA_LOOP/GS_LOOP"), 3)

    def test_init_copy_is_independent(self):
        initial = {"/ISA_LOOP/GS_LOOP": 2}
        nc = NodeCounter(initial)
        nc.increment("/ISA_LOOP/GS_LOOP")
        self.assertEqual(initial["/ISA_LOOP/GS_LOOP"], 2)


class TestNodeCounterIncrement(unittest.TestCase):
    def setUp(self):
        self.nc = NodeCounter()

    def test_increment_new_path(self):
        self.nc.increment("/ISA_LOOP/GS_LOOP")
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP"), 1)

    def test_increment_twice(self):
        self.nc.increment("/ISA_LOOP/GS_LOOP")
        self.nc.increment("/ISA_LOOP/GS_LOOP")
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP"), 2)

    def test_increment_multiple_paths(self):
        self.nc.increment("/ISA_LOOP/GS_LOOP")
        self.nc.increment("/ISA_LOOP/GS_LOOP/ST_LOOP")
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP"), 1)
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP/ST_LOOP"), 1)

    def test_unincremented_path_returns_zero(self):
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP"), 0)


class TestNodeCounterSetCount(unittest.TestCase):
    def setUp(self):
        self.nc = NodeCounter()

    def test_set_count(self):
        self.nc.setCount("/ISA_LOOP/GS_LOOP", 5)
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP"), 5)

    def test_set_count_overrides_increment(self):
        self.nc.increment("/ISA_LOOP/GS_LOOP")
        self.nc.increment("/ISA_LOOP/GS_LOOP")
        self.nc.setCount("/ISA_LOOP/GS_LOOP", 10)
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP"), 10)

    def test_set_count_zero(self):
        self.nc.increment("/ISA_LOOP/GS_LOOP")
        self.nc.setCount("/ISA_LOOP/GS_LOOP", 0)
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP"), 0)


class TestNodeCounterResetToNode(unittest.TestCase):
    def setUp(self):
        self.nc = NodeCounter()
        self.nc.setCount("/ISA_LOOP", 1)
        self.nc.setCount("/ISA_LOOP/GS_LOOP", 2)
        self.nc.setCount("/ISA_LOOP/GS_LOOP/ST_LOOP", 3)
        self.nc.setCount("/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL", 4)

    def test_reset_removes_children(self):
        self.nc.reset_to_node("/ISA_LOOP/GS_LOOP")
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP/ST_LOOP"), 0)
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL"), 0)

    def test_reset_preserves_parent(self):
        self.nc.reset_to_node("/ISA_LOOP/GS_LOOP")
        self.assertEqual(self.nc.get_count("/ISA_LOOP"), 1)
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP"), 2)

    def test_reset_leaf_node_no_children(self):
        self.nc.reset_to_node("/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL")
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP/ST_LOOP"), 3)
        self.assertEqual(self.nc.get_count("/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL"), 4)


class TestNodeCounterGetState(unittest.TestCase):
    def test_state_reflects_increments(self):
        nc = NodeCounter()
        nc.increment("/ISA_LOOP")
        nc.increment("/ISA_LOOP/GS_LOOP")
        state = nc.getState()
        self.assertEqual(len(state), 2)

    def test_empty_state(self):
        nc = NodeCounter()
        self.assertEqual(len(nc.getState()), 0)


class TestNodeCounterMakeX12Path(unittest.TestCase):
    def test_string_input(self):
        from pyx12.path import X12Path

        result = NodeCounter.makeX12Path("/ISA_LOOP/GS_LOOP")
        self.assertIsInstance(result, X12Path)

    def test_x12path_input_passthrough(self):
        from pyx12.path import X12Path

        p = X12Path("/ISA_LOOP/GS_LOOP")
        result = NodeCounter.makeX12Path(p)
        self.assertIs(result, p)


if __name__ == "__main__":
    unittest.main()


class TestNodeCounterLoopRepeat(unittest.TestCase):
    """Walk an 835 skeleton: resetting to a loop keeps that loop's own count
    (so a repeat increments it) while clearing the counts beneath it."""

    def test_loop_repeat(self):
        counter = NodeCounter({})
        counter.reset_to_node("/ISA_LOOP/GS_LOOP/ST_LOOP")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/ST")
        counter.reset_to_node("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BPR")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/TRN")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF[EV]")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/DTM")
        counter.reset_to_node("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N1")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N3")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N4")
        counter.reset_to_node("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N1")
        counter.reset_to_node("/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/LX")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/TS3")
        counter.reset_to_node("/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100")
        counter.increment("/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100")

        svc = "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110"
        self.assertEqual(0, counter.get_count(svc))
        counter.reset_to_node(svc)
        self.assertEqual(0, counter.get_count(svc))
        counter.increment(svc)
        self.assertEqual(1, counter.get_count(svc))
        counter.increment(svc + "/SVC")
        counter.increment(svc + "/DTM")
        counter.increment(svc + "/DTM")
        counter.increment(svc + "/CAS")
        counter.increment(svc + "/LQ")

        self.assertEqual(1, counter.get_count(svc))
        counter.reset_to_node(svc)
        self.assertEqual(1, counter.get_count(svc))
        counter.increment(svc)
        self.assertEqual(2, counter.get_count(svc))
