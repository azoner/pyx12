import os
import os.path
import sys
import tempfile
import unittest
from io import StringIO

from pyx12.xmlwriter import XMLWriter


class TestWriter(unittest.TestCase):
    """ """

    def setUp(self):
        self.res = '<?xml version="1.0" encoding="utf-8"?>\n<x12err>\n</x12err>\n'

    def test_write1(self):
        try:
            fd = StringIO(encoding="ascii")
            # print('CASE 1:')
        except Exception:
            fd = StringIO()
            # print('CASE 2:')
        writer = XMLWriter(fd)
        writer.push("x12err")

        while len(writer) > 0:
            writer.pop()
        self.assertEqual(fd.getvalue(), self.res)
        fd.close()

    def test_write_temp(self):
        (fdesc, filename) = tempfile.mkstemp(".xml", "pyx12_")
        with open(filename, "w") as fd:
            writer = XMLWriter(fd)
            writer.push("x12err")

            while len(writer) > 0:
                writer.pop()

        with open(filename) as fd:
            self.assertEqual(fd.read(), self.res)

        try:
            os.remove(filename)
        except Exception:
            pass


class IllegalCharacters(unittest.TestCase):
    def _write(self, content, attrs=None):
        fd = StringIO()
        writer = XMLWriter(fd)
        writer.elem("ele", content, attrs)
        return fd.getvalue().split(chr(10), 1)[1].rstrip(chr(10))

    def test_control_characters_in_content_substituted(self):
        self.assertEqual(self._write("A\x01B\x1fC\x0bD"), "<ele>A?B?C?D</ele>")

    def test_control_characters_in_attribute_substituted(self):
        self.assertEqual(self._write("x", {"id": "1\x00\x7f"}), "<ele id='1?\x7f'>x</ele>")

    def test_tab_newline_and_latin1_kept(self):
        self.assertEqual(self._write("a\tb\nc\xe9"), "<ele>a\tb\nc\xe9</ele>")

    def test_markup_still_escaped(self):
        self.assertEqual(self._write("<&>", {"id": "'"}), "<ele id='&apos;'>&lt;&amp;&gt;</ele>")
