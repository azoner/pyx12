import unittest
from io import StringIO

import pyx12.error_handler
from pyx12.errors import EngineError  # , X12PathError
import pyx12.x12context
import pyx12.params
from pyx12.test.x12testdata import datafiles


class X12fileTestCase(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()

    def _makeFd(self, x12str=None):
        try:
            if x12str:
                fd = StringIO(x12str)
            else:
                fd = StringIO()
        except:
            if x12str:
                fd = StringIO(x12str, encoding='ascii')
            else:
                fd = StringIO(encoding='ascii')
        fd.seek(0)
        return fd


class Delimiters(X12fileTestCase):

    def test_arbitrary_delimiters(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str1 += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&004010X098A1+\n'
        str1 += 'ST&837&11280001+\n'
        str1 += 'REF&87&004010X098A1+\n'
        str1 += 'SE&3&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        fd = self._makeFd(str1)
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(self.param, errh, fd)
        for datatree in src.iter_segments():
            pass
        self.assertEqual(src.subele_term, '!')
        self.assertEqual(src.ele_term, '&')
        self.assertEqual(src.seg_term, '+')

    def test_binary_delimiters(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str1 += 'GS&HC&ZZ000&ZZ001&20030828&1128&17&X&004010X098A1+\n'
        str1 += 'ST&837&11280001+\n'
        str1 += 'REF&87&004010X098A1+\n'
        str1 += 'SE&3&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        str1 = str1.replace('&', chr(0x1C))
        str1 = str1.replace('+', chr(0x1D))
        str1 = str1.replace('!', chr(0x1E))
        fd = self._makeFd(str1)
        errors = []
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(self.param, errh, fd)
        for datatree in src.iter_segments():
            pass
        self.assertEqual(src.subele_term, chr(0x1E))
        self.assertEqual(src.ele_term, chr(0x1C))
        self.assertEqual(src.seg_term, chr(0x1D))


class TreeGetValue(X12fileTestCase):

    def setUp(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_get_line_numbers_2200(self):
        loop2400 = self.loop2300.first('2400')
        self.assertEqual(self.loop2300.seg_count, 19)
        self.assertEqual(self.loop2300.cur_line_number, 21)
        for seg in loop2400.select('CLM'):
            self.assertEqual(seg.seg_count, 25)
            self.assertEqual(seg.cur_line_number, 2271)
            break

    def test_get_line_numbers_2400(self):
        loop2400 = self.loop2300.first('2400')
        self.assertEqual(loop2400.seg_count, 35)
        self.assertEqual(loop2400.cur_line_number, 37)
        for svc in loop2400.select('SV1'):
            self.assertEqual(svc.seg_count, 36)
            self.assertEqual(svc.cur_line_number, 38)
            break

    def test_get_seg_value(self):
        self.assertEqual(self.loop2300.get_value('CLM02'), '21')
        self.assertEqual(self.loop2300.get_value('CLM99'), None)

    def test_get_seg_value_fail_no_element_index(self):
        self.assertRaises(IndexError, self.loop2300.get_value, 'CLM')

    def test_get_parent_value(self):
        loop2400 = self.loop2300.first('2400')
        self.assertEqual(loop2400.get_value('../CLM01'), '3215338')
        self.assertEqual(loop2400.get_value('../2310B/NM109'), '222185735')

    def test_get_seg_value_idx(self):
        for clm in self.loop2300.select('CLM'):
            self.assertEqual(clm.get_value('02'), '21')
            self.assertEqual(clm.get_value('05-3'), '1')

    def test_get_first_value(self):
        self.assertEqual(self.loop2300.get_value('2400/SV101'), 'HC:H2015:TT')
        self.assertEqual(self.loop2300.get_value('2400/SV101-2'), 'H2015')
        self.assertEqual(self.loop2300.get_value('2400/REF[6R]02'), '1057296')
        self.assertEqual(self.loop2300.get_value('2400/2430/SVD02'), '21')
        self.assertEqual(self.loop2300.get_value('2400/AMT[AAE]02'), '21')

    def test_get_first_value_2400(self):
        loop2400 = self.loop2300.first('2400')
        self.assertEqual(loop2400.get_value('AMT[AAE]02'), '21')
        self.assertEqual(loop2400.get_value('2430/AMT[AAE]02'), None)

    def test_get_no_value(self):
        self.assertEqual(self.loop2300.get_value('2400/SV199'), None)
        self.assertEqual(self.loop2300.get_value('2400'), None)

    def test_get_parent_no_value(self):
        loop2400 = self.loop2300.first('2400')
        self.assertEqual(loop2400.get_value('../2310E/NM109'), None)

    def test_get_specific_qual(self):
        self.assertEqual(self.loop2300.get_value('2400/REF[6R]02'), '1057296')
        self.assertEqual(self.loop2300.get_value('2400/REF[G1]02'), None)
        self.assertEqual(self.loop2300.get_value('2400/REF[XX]02'), None)


class TreeSetValue(X12fileTestCase):

    def setUp(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_set_seg_value(self):
        self.loop2300.set_value('CLM02', '50')
        self.assertEqual(self.loop2300.get_value('CLM02'), '50')

    def test_set_first_value_2400(self):
        loop2400 = self.loop2300.first('2400')
        loop2400.set_value('AMT[AAE]02', '25')
        self.assertEqual(loop2400.get_value('AMT[AAE]02'), '25')


class TreeSelect(X12fileTestCase):

    def setUp(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        self.param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(self.param, errh, fd)
        for datatree in src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    #def test_select_loop_and_parent(self):
    #    loop2400 = self.loop2300.first('2400')
    #    assert loop2400.id == '2400', 'Not in 2400'
    #    ct = 0
    #    newtree = loop2400.parent
    #    for newtree in loop2400.select('../'):
    #        self.assertEqual(newtree.id, '2300')
    #        ct += 1
    #    self.assertEqual(ct, 1)

    def test_select_loops(self):
        ct = 0
        for newtree in self.loop2300.select('2400'):
            self.assertEqual(newtree.id, '2400')
            ct += 1
        self.assertEqual(ct, 2)

    def test_select_seg(self):
        ct = 0
        for newtree in self.loop2300.select('2400/SV1'):
            self.assertEqual(newtree.id, 'SV1')
            self.assertEqual(newtree.get_value('SV102'), '21')
            ct += 1
        self.assertEqual(ct, 2)

    def test_select_parent_seg(self):
        loop2400 = self.loop2300.first('2400')
        assert loop2400.id == '2400', 'Not in 2400'
        ct = 0
        for newtree in loop2400.select('../CLM'):
            self.assertEqual(newtree.id, 'CLM')
            self.assertEqual(newtree.get_value('CLM01'), '3215338')
            ct += 1
        self.assertEqual(ct, 1)

    def test_select_from_st(self):
        fd = self._makeFd(datafiles['835id']['source'])
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(self.param, errh, fd)
        ct = 0
        for datatree in src.iter_segments('ST_LOOP'):
            if datatree.id == 'ST_LOOP':
                for claim in datatree.select('DETAIL/2000/2100'):
                    self.assertEqual(claim.id, '2100')
                    ct += 1
        self.assertEqual(
            ct, 3, 'Found %i 2100 loops.  Should have %i' % (ct, 3))

    def test_select_from_gs(self):
        fd = self._makeFd(datafiles['simple_837i']['source'])
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(self.param, errh, fd)
        ct = 0
        for datatree in src.iter_segments('GS_LOOP'):
            if datatree.id == 'GS_LOOP':
                for sub in datatree.select('ST_LOOP/DETAIL/2000A/2000B/2300/2400'):
                    self.assertEqual(sub.id, '2400')
                    ct += 1
        self.assertEqual(
            ct, 6, 'Found %i 2400 loops.  Should have %i' % (ct, 6))


class TreeSelectFromSegment(X12fileTestCase):

    def test_select_from_seg_fail(self):
        fd = self._makeFd(datafiles['835id']['source'])
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(param, errh, fd)
        for datatree in src.iter_segments('ST_LOOP'):
            if datatree.id == 'GS':
                #self.assertFalseRaises(AttributeError, datatree.select, 'DETAIL/2000/2100')
                for claim in datatree.select('DETAIL/2000/2100'):
                    pass


class TreeAddSegment(X12fileTestCase):

    def setUp(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_add_new_plain(self):
        seg_data = pyx12.segment.Segment('HCP*00*7.11~', '~', '*', ':')
        new_node = self.loop2300.add_segment(seg_data)
        self.assertNotEqual(new_node, None)

    def test_add_new_id(self):
        seg_data = pyx12.segment.Segment('REF*F5*6.11~', '~', '*', ':')
        new_node = self.loop2300.add_segment(seg_data)
        self.assertNotEqual(new_node, None)

    def test_add_new_not_exists(self):
        seg_data = pyx12.segment.Segment('ZZZ*00~', '~', '*', ':')
        self.assertRaises(pyx12.errors.X12PathError,
                          self.loop2300.add_segment, seg_data)


class TreeAddSegmentString(X12fileTestCase):

    def setUp(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_add_new_plain(self):
        new_node = self.loop2300.add_segment('HCP*00*7.11~')
        self.assertNotEqual(new_node, None)

    def test_add_new_id(self):
        new_node = self.loop2300.add_segment('REF*F5*6.11')
        self.assertNotEqual(new_node, None)

    def test_add_new_not_exists(self):
        self.assertRaises(pyx12.errors.X12PathError,
                          self.loop2300.add_segment, 'ZZZ*00~')


class SegmentExists(X12fileTestCase):

    def setUp(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        self.param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(self.param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_qual_segment(self):
        self.assertTrue(self.loop2300.exists('2310B'))
        self.assertTrue(self.loop2300.exists('2310B/NM1[82]'))
        for loop2310b in self.loop2300.select('2310B'):
            self.assertTrue(loop2310b.exists('NM1'))
            self.assertTrue(loop2310b.exists('NM1[82]'))

    def test_qual_segment_sub_loop(self):
        self.assertTrue(self.loop2300.exists('2400/2430'))
        self.assertTrue(self.loop2300.exists('2400/2430/DTP[573]'))
        self.assertFalse(self.loop2300.exists('2400/2430/DTP[111]'))
        self.assertTrue(self.loop2300.exists('2400/2430/DTP[573]03'))

    def test_qual_segment_select_sub_loop(self):
        loop2430 = self.loop2300.first('2400/2430')
        self.assertTrue(loop2430.exists('DTP'))
        self.assertTrue(loop2430.exists('DTP[573]'))
        self.assertTrue(loop2430.exists('DTP[573]03'))

    def test_qual_834_dtp(self):
        fd = self._makeFd(datafiles['834_lui_id']['source'])
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(self.param, errh, fd)
        for datatree in src.iter_segments('2300'):
            if datatree.id == '2300':
                loop2300 = datatree
                break
        self.assertTrue(loop2300.exists('DTP[348]'))
        self.assertFalse(loop2300.exists('DTP[349]'))


class TreeAddLoop(X12fileTestCase):

    def setUp(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_add_new_plain(self):
        seg_data = pyx12.segment.Segment(
            'NM1*82*2*Provider 1*****ZZ*9898798~', '~', '*', ':')
        new_node = self.loop2300.add_loop(seg_data)
        self.assertNotEqual(new_node, None)
        self.assertTrue(self.loop2300.exists('2310B'))
        for loop2310b in self.loop2300.select('2310B'):
            self.assertTrue(loop2310b.exists('NM1'))
            self.assertTrue(loop2310b.exists('NM1[82]'))

    def test_add_new_string_seg(self):
        old_ct = self.loop2300.count('2400')
        new_node = self.loop2300.add_loop('LX*5~')
        self.assertNotEqual(new_node, None)
        self.assertTrue(self.loop2300.exists('2400'))
        self.assertEqual(old_ct + 1, self.loop2300.count('2400'))
        for loop2400 in self.loop2300.select('2400'):
            self.assertTrue(loop2400.exists('LX'))


class TreeAddLoopDetail(X12fileTestCase):
    def test_add_loops_under_detail(self):
        str1 = 'ISA&00&          &00&          &ZZ&ZZ000          &ZZ&ZZ001          &030828&1128&U&00401&000010121&0&T&!+\n'
        str1 += 'GS&BE&ZZ000&ZZ001&20030828&1128&17&X&004010X095A1+\n'
        str1 += 'ST&834&11280001+\n'
        str1 += 'BGN&+\n'
        str1 += 'INS&Y&18&30&XN&AE&RT+\n'
        str1 += 'SE&4&11280001+\n'
        str1 += 'GE&1&17+\n'
        str1 += 'IEA&1&000010121+\n'
        fd = self._makeFd(str1)
        errors = []
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(param, errh, fd)
        for st_loop in src.iter_segments('ST_LOOP'):
            if st_loop.id == 'ST_LOOP' and st_loop.exists('DETAIL'):
                detail = st_loop.first('DETAIL')
                self.assertTrue(detail.exists('2000'))
                detail.first('2000').delete()
                self.assertFalse(detail.exists('2000'))
                detail.add_loop('INS&Y&18&30&XN&AE&RT+')
                self.assertTrue(detail.exists('2000'))


class TreeAddNode(X12fileTestCase):
    def setUp(self):
        self.param = pyx12.params.params()

    def test_add_loop(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(self.param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                loop2300 = datatree
                break
        self.assertEqual(self._get_count(loop2300, '2400'), 2)
        for node in loop2300.select('2400'):
            loop2300.add_node(node)
        self.assertEqual(self._get_count(loop2300, '2400'), 4)

    def test_add_segment(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(self.param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                loop2300 = datatree
                break
        self.assertEqual(self._get_count(loop2300, 'CN1'), 1)
        for node in loop2300.select('CN1'):
            loop2300.add_node(node)
        self.assertEqual(self._get_count(loop2300, 'CN1'), 2)

    def test_fail(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(self.param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                loop2300 = datatree
                break
        for node in loop2300.select('CN1'):
            cn1 = node
            break
        n2400 = None
        for node in loop2300.select('2400'):
            n2400 = node
            break
        assert n2400 is not None, 'Loop 2400 was not matched'
        self.assertRaises(pyx12.errors.X12PathError, n2400.add_node, cn1)

    def _get_count(self, node, loop_id):
        ct = 0
        for n in node.select(loop_id):
            ct += 1
        return ct


class CountRepeatingLoop(X12fileTestCase):

    def setUp(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300' and datatree.get_value('CLM01') == '5555':
                self.loop2300 = datatree
                break

    def test_repeat_2400(self):
        ct = 0
        for loop_2400 in self.loop2300.select('2400'):
            ct += 1
        self.assertEqual(
            ct, 3, 'Found %i 2400 loops.  Should have %i' % (ct, 3))

    def test_repeat_2430(self):
        ct = 0
        for loop_2430 in self.loop2300.select('2400/2430'):
            ct += 1
        self.assertEqual(
            ct, 0, 'Found %i 2430 loops.  Should have %i' % (ct, 0))


class IterateTree(X12fileTestCase):

    def setUp(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd)

    def test_iterate_all(self):
        ct_2000a = 0
        ct_other = 0
        for datatree in self.src.iter_segments('2000A'):
            if datatree.id == '2000A':
                ct_2000a += 1
            else:
                ct_other += 1
        self.assertEqual(ct_2000a, 1,
                         'Found %i 2000A loops.  Should have %i' % (ct_2000a, 1))
        self.assertEqual(ct_other, 11, 'Found %i external segments.  Should have %i' % (ct_other, 11))


class TreeDeleteSegment(X12fileTestCase):

    def setUp(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_delete(self):
        assert self.loop2300.get_value('CN101') == '05'
        seg_data = pyx12.segment.Segment('CN1*05~', '~', '*', ':')
        self.assertTrue(self.loop2300.delete_segment(seg_data))
        self.assertEqual(self.loop2300.get_value('CN101'), None)

    def test_delete_fail(self):
        seg_data = pyx12.segment.Segment('HCP*00*7.11~', '~', '*', ':')
        self.assertFalse(self.loop2300.delete_segment(seg_data))


class TreeDeleteLoop(X12fileTestCase):

    def setUp(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_delete(self):
        self.assertEqual(self.loop2300.get_value('2400/LX01'), '1')
        self.assertTrue(self.loop2300.delete_node('2400'))
        self.assertEqual(self.loop2300.get_value('2400/LX01'), '2')

    def test_delete_fail(self):
        self.assertFalse(self.loop2300.delete_node('2500'))


class NodeDeleteSelf(X12fileTestCase):

    def setUp(self):
        fd = self._makeFd(datafiles['simple_837p']['source'])
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        self.src = pyx12.x12context.X12ContextReader(param, errh, fd)
        for datatree in self.src.iter_segments('2300'):
            if datatree.id == '2300':
                self.loop2300 = datatree
                break

    def test_delete(self):
        cn1 = self.loop2300.first('CN1')
        assert cn1.id == 'CN1'
        cn1.delete()
        try:
            a = cn1.id
        except EngineError:
            pass
        except:
            a = cn1.id
        #self.assertRaises(EngineError, cn1.id)


class TreeCopy(X12fileTestCase):
    def setUp(self):
        self.param = pyx12.params.params()

    def test_add_node(self):
        fd = self._makeFd(datafiles['835id']['source'])
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(self.param, errh, fd)
        for datatree in src.iter_segments('2100'):
            if datatree.id == '2100':
                for svc in datatree.select('2110'):
                    new_svc = svc.copy()
                    new_svc.set_value('SVC01', 'XX:AAAAA')
                    self.assertTrue(not svc is new_svc)
                    datatree.add_node(new_svc)
                #for svc in datatree.select('2110'):
                #    print svc.get_value('SVC01')
                break

    def test_copy_seg(self):
        fd = self._makeFd(datafiles['835id']['source'])
        errh = pyx12.error_handler.errh_null()
        src = pyx12.x12context.X12ContextReader(self.param, errh, fd)
        for datatree in src.iter_segments('2100'):
            if datatree.id == '2100':
                for svc in datatree.select('2110'):
                    new_svc = svc.copy()
                    self.assertFalse(svc is new_svc)
                    self.assertEqual(svc.get_value('SVC01'),
                                     new_svc.get_value('SVC01'))
                    new_svc.set_value('SVC01', 'XX:AAAAA')
                    self.assertFalse(svc is new_svc)
                    self.assertNotEqual(svc.get_value('SVC01'),
                                        new_svc.get_value('SVC01'))
                    break
