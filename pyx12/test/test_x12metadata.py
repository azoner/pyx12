import os
import unittest
from io import StringIO

import pyx12.params
from pyx12.x12metadata import get_x12file_metadata, get_x12file_metadata_headers


TESTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'tests')

NEW_ENROLL_FILE = os.path.join(TESTS_DIR, '834_deident_new_enroll.txt')
FAMILY_FILE = os.path.join(TESTS_DIR, '834_deident_family.txt')
TERM_FILE = os.path.join(TESTS_DIR, '834_deident_term.txt')


class TestGetX12FileMetadata(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()

    def test_new_enroll_returns_success(self):
        ok, isa_data, node_summary = get_x12file_metadata(self.param, NEW_ENROLL_FILE)
        self.assertTrue(ok)

    def test_new_enroll_isa_data_present(self):
        ok, isa_data, node_summary = get_x12file_metadata(self.param, NEW_ENROLL_FILE)
        self.assertIsNotNone(isa_data)

    def test_new_enroll_isa_sender(self):
        ok, isa_data, _ = get_x12file_metadata(self.param, NEW_ENROLL_FILE)
        self.assertEqual(isa_data['InterchangeSenderID'].strip(), 'ACMECORP')

    def test_new_enroll_icvn_00501(self):
        ok, isa_data, _ = get_x12file_metadata(self.param, NEW_ENROLL_FILE)
        self.assertEqual(isa_data['InterchangeControlVersionNumber'], '00501')

    def test_new_enroll_gs_loops_count(self):
        ok, isa_data, _ = get_x12file_metadata(self.param, NEW_ENROLL_FILE)
        self.assertEqual(len(isa_data['GSLoops']), 1)

    def test_new_enroll_fic_be(self):
        ok, isa_data, _ = get_x12file_metadata(self.param, NEW_ENROLL_FILE)
        gs = isa_data['GSLoops'][0]
        self.assertEqual(gs['FunctionalGroupHeader'], 'BE')

    def test_new_enroll_st_loops_count(self):
        ok, isa_data, _ = get_x12file_metadata(self.param, NEW_ENROLL_FILE)
        gs = isa_data['GSLoops'][0]
        self.assertEqual(len(gs['STLoops']), 1)

    def test_new_enroll_st_identifier_code(self):
        ok, isa_data, _ = get_x12file_metadata(self.param, NEW_ENROLL_FILE)
        st = isa_data['GSLoops'][0]['STLoops'][0]
        self.assertEqual(st['TransactionSetIdentifierCode'], '834')

    def test_new_enroll_no_node_summary_by_default(self):
        ok, isa_data, node_summary = get_x12file_metadata(self.param, NEW_ENROLL_FILE)
        self.assertIsNone(node_summary)

    def test_new_enroll_node_summary_when_requested(self):
        ok, isa_data, node_summary = get_x12file_metadata(
            self.param, NEW_ENROLL_FILE, do_node_summary=True)
        self.assertTrue(ok)
        self.assertIsNotNone(node_summary)
        self.assertGreater(len(node_summary), 0)

    def test_family_gs_loops(self):
        ok, isa_data, _ = get_x12file_metadata(self.param, FAMILY_FILE)
        self.assertTrue(ok)
        self.assertEqual(len(isa_data['GSLoops']), 1)

    def test_term_gs_loops(self):
        ok, isa_data, _ = get_x12file_metadata(self.param, TERM_FILE)
        self.assertTrue(ok)
        self.assertEqual(len(isa_data['GSLoops']), 1)

    def test_invalid_file_returns_false(self):
        fd = StringIO('this is not x12 data')
        ok, isa_data, node_summary = get_x12file_metadata(self.param, fd)
        self.assertFalse(ok)
        self.assertIsNone(isa_data)
        self.assertIsNone(node_summary)


class TestGetX12FileMetadataHeaders(unittest.TestCase):
    def setUp(self):
        self.param = pyx12.params.params()

    def test_new_enroll_returns_success(self):
        ok, isa_data = get_x12file_metadata_headers(self.param, NEW_ENROLL_FILE)
        self.assertTrue(ok)

    def test_new_enroll_isa_data_present(self):
        ok, isa_data = get_x12file_metadata_headers(self.param, NEW_ENROLL_FILE)
        self.assertIsNotNone(isa_data)

    def test_new_enroll_receiver(self):
        ok, isa_data = get_x12file_metadata_headers(self.param, NEW_ENROLL_FILE)
        self.assertEqual(isa_data['InterchangeReceiverID'].strip(), 'HEALTHPLAN')

    def test_new_enroll_gs_present(self):
        ok, isa_data = get_x12file_metadata_headers(self.param, NEW_ENROLL_FILE)
        self.assertEqual(len(isa_data['GSLoops']), 1)

    def test_new_enroll_st_identifier(self):
        ok, isa_data = get_x12file_metadata_headers(self.param, NEW_ENROLL_FILE)
        st = isa_data['GSLoops'][0]['STLoops'][0]
        self.assertEqual(st['TransactionSetIdentifierCode'], '834')

    def test_invalid_file_returns_false(self):
        fd = StringIO('not x12')
        ok, isa_data = get_x12file_metadata_headers(self.param, fd)
        self.assertFalse(ok)
        self.assertIsNone(isa_data)


if __name__ == '__main__':
    unittest.main()
