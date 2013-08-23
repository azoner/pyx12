import os.path
import sys
import os
import unittest
try:
    from io import StringIO
except:
    from StringIO import StringIO

import tempfile

from pyx12.xmlwriter import XMLWriter


class TestWriter(unittest.TestCase):
    """
    """
    def setUp(self):
        self.res = '<?xml version="1.0" encoding="utf-8"?>\n<x12err>\n</x12err>\n'

    def test_write1(self):
        try:
            fd = StringIO(encoding='ascii')
        except:
            fd = StringIO()
        writer = XMLWriter(fd)
        writer.push(u"x12err")

        while len(writer) > 0:
            writer.pop()
        self.assertEqual(fd.getvalue(), self.res)
        fd.close()
        try:
            os.remove(filename)
        except:
            pass

    def test_write_temp(self):
        (fdesc, filename) = tempfile.mkstemp('.xml', 'pyx12_')
        fd = os.fdopen(fdesc, 'w+b')
        #fd = file(filename, 'rw')
        writer = XMLWriter(fd)
        writer.push(u"x12err")

        while len(writer) > 0:
            writer.pop()
        fd.seek(0)
        self.assertEqual(fd.read(), self.res)
        fd.close()
        try:
            os.remove(filename)
        except:
            pass
