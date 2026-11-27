from io import StringIO

import pyx12.params
import pyx12.x12file
import pyx12.x12n_document
from pyx12.test.test_x12n_document import X12DocumentTestCase
from pyx12.test.x12testdata import datafiles


class Ack997GroupVersion(X12DocumentTestCase):
    """GS08 of a 997 is the functional group version (004010), not ISA12 (00401)."""

    def _make_997(self, datakey):
        fd_997 = StringIO()
        pyx12.x12n_document.x12n_document(
            self.param, self._makeFd(datafiles[datakey]["source"]), fd_997, None, None
        )
        return fd_997.getvalue()

    def _gs08_values(self, ack):
        src = pyx12.x12file.X12Reader(StringIO(ack))
        return [seg.get_value("GS08") for seg in src if seg.get_seg_id() == "GS"]

    def test_gs08_is_004010(self):
        for datakey in (k for k, v in datafiles.items() if "res997" in v):
            with self.subTest(datakey=datakey):
                self.assertEqual(set(self._gs08_values(self._make_997(datakey))), {"004010"})

    def test_997_validates_against_the_997_map(self):
        ack = self._make_997("simple1")
        result = pyx12.x12n_document.x12n_document(
            pyx12.params.params(), StringIO(ack), StringIO(), None, None
        )
        self.assertTrue(result)
