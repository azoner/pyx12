import unittest
import os.path

import pyx12.error_handler
import pyx12.map_if
import pyx12.params
import pyx12.path
import pyx12.segment


class IsValidHierarchy(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.param = pyx12.params.params()
        self.map_path = os.path.join(os.path.dirname(pyx12.codes.__file__), 'map')

    def test_835_4010_A1(self):
        map_file = '835.4010.X091.A1.xml'
        loops = [
            "/", 
            "/ISA_LOOP", 
            "/ISA_LOOP/ISA", 
            "/ISA_LOOP/GS_LOOP", 
            "/ISA_LOOP/GS_LOOP/GS", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/ST", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BPR", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/TRN", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/CUR", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF[EV]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF[F2]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/DTM", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N1", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N3", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N4", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/REF", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/PER", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N1", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N3", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N4", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/REF", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/LX", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/TS3", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/TS2", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/CLP", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/CAS", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[QC]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[IL]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[74]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[82]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[TT]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[PR]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/MIA", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/MOA", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/REF[1L]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/REF[1A]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/DTM", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/PER", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/AMT", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/QTY", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/SVC", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/DTM", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/CAS", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/REF[1S]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/REF[1A]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/AMT", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/QTY", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/LQ", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/FOOTER", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/FOOTER/PLB", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/SE", 
            "/ISA_LOOP/GS_LOOP/GE", 
            "/ISA_LOOP/TA1", 
            "/ISA_LOOP/IEA"
        ]
        map = pyx12.map_if.load_map_file(map_file, self.param, self.map_path)
        mylist = list([x for x in self._loop_node_iter(map)])
        #self.assertItemsEqual(loops, mylist)
        newloops = self._add_isa_gs_loops(loops)
        self.assertEqual(loops, mylist)

    def test_835_5010(self):
        map_file = '835.5010.X221.A1.xml'
        loops = [
            "/", 
            "/ISA_LOOP", 
            "/ISA_LOOP/ISA", 
            "/ISA_LOOP/GS_LOOP", 
            "/ISA_LOOP/GS_LOOP/GS", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/ST", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BPR", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/TRN", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/CUR", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF[EV]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF[F2]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/DTM", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N1", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N3", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N4", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/REF", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/PER[CX]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/PER[BL]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/PER[IC]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N1", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N3", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N4", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/REF", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/RDM", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/LX", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/TS3", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/TS2", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/CLP", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/CAS", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[QC]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[IL]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[74]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[82]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[TT]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[PR]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[GB]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/MIA", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/MOA", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/REF[1L]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/REF[0B]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/DTM[232]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/DTM[036]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/DTM[050]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/PER", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/AMT", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/QTY", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/SVC", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/DTM", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/CAS", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/REF[1S]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/REF[6R]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/REF[0B]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/REF[0K]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/AMT", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/QTY", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/LQ", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/FOOTER", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/FOOTER/PLB", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/SE", 
            "/ISA_LOOP/GS_LOOP/GE", 
            "/ISA_LOOP/TA1", 
            "/ISA_LOOP/IEA"
        ]
        map = pyx12.map_if.load_map_file(map_file, self.param, self.map_path)
        mylist = list([x for x in self._loop_node_iter(map)])
        #self.assertItemsEqual(loops, mylist)
        newloops = self._add_isa_gs_loops(loops)
        self.assertEqual(loops, mylist)

    def test_835_5010_v2(self):
        map_file = '835.5010.X221.A1.v2.xml'
        loops = [
            "/", 
            "/ISA_LOOP", 
            "/ISA_LOOP/ISA", 
            "/ISA_LOOP/GS_LOOP", 
            "/ISA_LOOP/GS_LOOP/GS", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/ST", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BPR", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/TRN", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/CUR", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF[EV]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/REF[F2]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/DTM", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N1", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N3", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/N4", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/REF", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/PER[CX]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/PER[BL]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000A/PER[IC]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N1", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N3", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/N4", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/REF", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/1000B/RDM", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/LX", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/TS3", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/TS2", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/CLP", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/CAS", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[QC]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[IL]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[74]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[82]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[TT]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[PR]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/NM1[GB]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/MIA", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/MOA", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/REF[1L]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/REF[0B]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/DTM[232]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/DTM[036]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/DTM[050]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/PER", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/AMT", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/QTY", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/SVC", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/DTM", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/CAS", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/REF[1S]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/REF[6R]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/REF[0B]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/REF[0K]", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/AMT", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/QTY", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/LQ", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/FOOTER", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/FOOTER/PLB", 
            "/ISA_LOOP/GS_LOOP/ST_LOOP/SE", 
            "/ISA_LOOP/GS_LOOP/GE", 
            "/ISA_LOOP/TA1", 
            "/ISA_LOOP/IEA"
        ]
        map = pyx12.map_if.load_map_file(map_file, self.param, self.map_path)
        mylist = list([x for x in self._loop_node_iter(map)])
        #self.assertItemsEqual(loops, mylist)
        newloops = self._add_isa_gs_loops(mylist)
        self.assertEqual(loops, newloops)

    def _add_isa_gs_loops(self, loop_list):
        ret = [
               '/', 
               '/ISA_LOOP', 
               '/ISA_LOOP/ISA', 
               '/ISA_LOOP/GS_LOOP', 
               '/ISA_LOOP/GS_LOOP/GS'
               ]
        ret.extend(['/ISA_LOOP/GS_LOOP' + x for x in loop_list if x != '/'])
        ret.extend(('/ISA_LOOP/GS_LOOP/GE', '/ISA_LOOP/TA1', '/ISA_LOOP/IEA'))
        return ret

    def _donode(self, node, mylist):
        #print node.get_path()
        mylist.append(node.get_path())
        #print(node.id)
        for ord1 in sorted(node.pos_map):
            for child in node.pos_map[ord1]:
                if child.is_loop():  # or child.is_segment():
                    donode(child, mylist)

    def _loop_node_iter(self, node):
        yield node.get_path()
        #print(node.id)
        for ord1 in sorted(node.pos_map):
            for child in node.pos_map[ord1]:
                if child.is_loop():  # or child.is_segment():
                    for n in self._loop_node_iter(child):
                        yield n
                elif child.is_segment():
                    yield child.get_path()