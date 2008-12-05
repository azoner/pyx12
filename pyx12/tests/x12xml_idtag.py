#! /usr/bin/env /usr/local/bin/python

import unittest
import sys
try:
    from io import StringIO
except:
    from StringIO import StringIO

from os.path import dirname, abspath, join, isdir, isfile

import pyx12.x12xml_idtag
import pyx12.map_if
import pyx12.params
import pyx12.segment
#from pyx12.errors import *
from pyx12.tests.support import getMapPath

class ConvertToXML(unittest.TestCase):
    def setUp(self):
        map_path = getMapPath()
        param = pyx12.params.params('pyx12.conf.xml')
        if not map_path:
            map_path = param.get('map_path')
        if map_path:
            param.set('map_path', map_path)
            param.set('pickle_path', map_path)
        self.map = pyx12.map_if.load_map_file('837.4010.X098.A1.xml', param)
        self.fd = StringIO(encoding='utf-8')
        self.xml = pyx12.x12xml_idtag.x12xml_idtag(self.fd)

    def test_valid1(self):
        seg_data = None
        node = self.map.getnodebypath('/ISA_LOOP/ISA')
        self.assertNotEqual(node, None, 'node not found')
        seg_str = 'ISA*00*          *00*          *ZZ*ZZ000          '
        seg_str += '*ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~\n'
        seg_data = pyx12.segment.Segment(seg_str, '~', '*', ':')
        a = len(self.fd.getvalue())
        self.xml.seg(node, seg_data)
        res = self.fd.getvalue()[a:] # filter(lambda x: x!= '\n', self.fd.getvalue())
        test_res = '  <LISA_LOOP>\n    <ISA>\n      <ISA01>00</ISA01>\n      <ISA02>          </ISA02>\n      <ISA03>00</ISA03>\n      <ISA04>          </ISA04>\n      <ISA05>ZZ</ISA05>\n      <ISA06>ZZ000          </ISA06>\n      <ISA07>ZZ</ISA07>\n      <ISA08>ZZ001          </ISA08>\n      <ISA09>030828</ISA09>\n      <ISA10>1128</ISA10>\n      <ISA11>U</ISA11>\n      <ISA12>00401</ISA12>\n      <ISA13>000010121</ISA13>\n      <ISA14>0</ISA14>\n      <ISA15>T</ISA15>\n      <ISA16>:~\n</ISA16>\n    </ISA>\n'
        self.assertEqual(res, test_res)
