import unittest
try:
    from StringIO import StringIO
except:
    from io import StringIO

import pyx12.error_handler
import pyx12.x12n_document
import pyx12.params
from pyx12.tests.support import getMapPath


class X12DocumentTestCase(unittest.TestCase):
    def setUp(self):
        map_path = getMapPath()
        self.param = pyx12.params.params('pyx12.conf.xml')
        if map_path:
            self.param.set('map_path', map_path)

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

    def _isX12Diff(self, fd1, fd2):
        """
        Just want to know if the important bits of the 997 are different
        """
        src1 = pyx12.x12file.X12Reader(fd1)
        src2 = pyx12.x12file.X12Reader(fd2)
        done1 = False
        done2 = False
        while True:
            try:
                seg1 = src1.next()
            except StopIteration:
                done1 = True
            try:
                seg2 = src2.next()
            except StopIteration:
                done2 = True
            #id1 = seg1.get_seg_id()
            #id2 = seg2.get_seg_id()
            if seg1.format() != seg2.format() \
                    and (seg1.get_seg_id() not in ('ISA', 'GS', 'ST', 'SE', 'GE', 'IEA') \
                    or seg2.get_seg_id() not in ('ISA', 'GS', 'ST', 'SE', 'GE', 'IEA')):
                return True
            if done1 and done2:
                return False
        return False

    def _test_997(self, source, res_997):
        fd_source = self._makeFd(source)
        fd_997_base = self._makeFd(res_997)
        fd_997 = StringIO()
        fd_html = StringIO()
        #import logging
        #logger = logging.getLogger('pyx12')
        #logger.setLevel(logging.DEBUG)
        #formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        #hdlr = logging.StreamHandler()
        #hdlr.setFormatter(formatter)
        #logger.addHandler(hdlr)

        fd_source.seek(0)
        #print fd_source.read()
        pyx12.x12n_document.x12n_document(self.param, fd_source, fd_997, fd_html, None)
        fd_997.seek(0)
        res = self._isX12Diff(fd_997_base, fd_997)
        self.assertFalse(res)


class Test834(X12DocumentTestCase):

    def test_834_lui_id(self):
        source = """ISA*00*          *00*          *ZZ*D00XXX         *ZZ*00AA           *070305*1832*U*00401*000701336*0*P*:~
GS*BE*D00XXX*00AA*20070305*1832*13360001*X*004010X095A1~
ST*834*0001~
BGN*00*88880070301  00*20070305*181245****4~
DTP*007*D8*20070301~
N1*P5*PAYER 1*FI*999999999~
N1*IN*KCMHSAS*FI*999999999~
INS*Y*18*030*XN*A*C**FT~
REF*0F*00389999~
REF*1L*000003409999~
REF*3H*K129999A~
DTP*356*D8*20070301~
NM1*IL*1*DOE*JOHN*A***34*999999999~
N3*777 ELM ST~
N4*ALLEGAN*MI*49010**CY*03~
DMG*D8*19670330*M**O~
LUI***ESSPANISH~
HD*030**AK*064703*IND~
DTP*348*D8*20070301~
AMT*P3*45.34~
REF*17*E  1F~
SE*20*0001~
GE*1*13360001~
IEA*1*000701336~
"""
        res_997 = """ISA*00*          *00*          *ZZ*00GR           *ZZ*D00111         *070320*1721*U*00401*703201721*0*P*:~
GS*FA*00GR*D00111*20070320*172121*13360001*X*004010~
ST*997*0001~
AK1*BE*13360001~
AK2*834*0001~
AK5*A~
AK9*A*1*1*1~
SE*6*0001~
GE*1*13360001~
IEA*1*703201721~
"""
        self._test_997(source, res_997)
