import os.path
import sys
import os
import unittest

try:
    from StringIO import StringIO
except:
    from io import StringIO

import tempfile

from pyx12.jsonwriter import JSONriter

class TestJsonWriter(unittest.TestCase):
    """
    """
    
    def test_write_loop_first(self):
        # With StringIO Object
        try:
            fd = StringIO(encoding='ascii')
        except:
            fd = StringIO()
        
        writer = JSONriter(fd)
        attrs = {'id': 'TestLoopFirst'}
        writer.push('loop', attrs, first=True)
        while len(writer) > 0:
            writer.pop()
        writer.pop()
        expected = """{"TestLoopFirst": []}"""
        self.assertEqual(fd.getvalue(), expected)
        fd.close()

        # With Temp File
        _, filename = tempfile.mkstemp('.json', 'pyx12_')
        with open(filename, 'w') as fd:
            writer = JSONriter(fd)
            attrs = {'id': 'TestLoopFirst'}
            writer.push('loop', attrs, first=True)
            while len(writer) > 0:
                writer.pop()
        
        with open(filename, 'r') as fd:
            self.assertEqual(fd.read(), expected)
        
        try:
            os.remove(filename)
        except:
            pass

    def test_write_loop(self):
        # With StringIO Object
        try:
            fd = StringIO(encoding='ascii')
        except:
            fd = StringIO()
        
        writer = JSONriter(fd)
        attrs = {'id': 'TestLoopFirst'}
        writer.push('loop', attrs)
        writer.pop()
        expected = """,{"TestLoopFirst": []}"""
        self.assertEqual(fd.getvalue(), expected)
        fd.close()

        # With Temp File
        _, filename = tempfile.mkstemp('.json', 'pyx12_')
        with open(filename, 'w') as fd:
            writer = JSONriter(fd)
            attrs = {'id': 'TestLoopFirst'}
            writer.push('loop', attrs)
            while len(writer) > 0:
                writer.pop()
        
        with open(filename, 'r') as fd:
            self.assertEqual(fd.read(), expected)
        
        try:
            os.remove(filename)
        except:
            pass

if __name__ == "__main__":
    unittest.main()