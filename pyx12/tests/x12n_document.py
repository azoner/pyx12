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
        segs1 = [x.format() for x in src1 if x.get_seg_id() not in ('ISA', 'GS', 'ST', 'SE', 'GE', 'IEA')]
        segs2 = [x.format() for x in src2 if x.get_seg_id() not in ('ISA', 'GS', 'ST', 'SE', 'GE', 'IEA')]
        self.assertListEqual(segs1, segs2)

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
        self._isX12Diff(fd_997_base, fd_997)


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


class Test835(X12DocumentTestCase):
    def test_835id(self):
        res997 = """ISA*00*          *00*          *ZZ*382999999      *ZZ*383319999      *090304*1036*U*00401*903041036*1*P*:~
GS*FA*382999999*383319999*20090304*103618*3444*X*004010~
ST*997*0001~
AK1*HP*3444~
AK2*835*40731~
AK5*A~
AK9*A*1*1*1~
SE*6*0001~
GE*1*3444~
TA1*000003447*090220*1816*A*000~
IEA*1*903041036~
"""
        source = """ISA*00*          *00*          *ZZ*383319999      *ZZ*382999999      *090220*1816*U*00401*000003447*1*P*:~
GS*HP*383319999*382999999*20090220*1816*3444*X*004010X091A1~
ST*835*40731~
BPR*I*5950.21*C*CHK************20090220~
TRN*1*0004926*1382999999~
DTM*405*20090209~
N1*PR*Payer 1~
N3*123 Elm~
N4*Nowhere*MI*49000~
N1*PE*Provider 1*FI*382999999~
N3*456 Oak~
N4*Nowhere*MI*49000~
LX*1~
CLP*123839-24635*22*-310*-210*0*HM*6363451~
NM1*QC*1*Flintstone*Fred****34*373899999~
AMT*AU*580~
SVC*HC:T1017*-310*-210**6~
DTM*150*20080111~
CAS*CR*45*-100~
REF*G1*20540~
CLP*123839-24635*1*300*200*0*HM*6363451~
NM1*QC*1*Flintstone*Fred****34*373899999~
AMT*AU*590~
SVC*HC:T1017*300*200**6~
DTM*150*20080111~
CAS*CR*45*100~
REF*G1*20540~
CLP*134158-27488*22*-500.25*-500.25*0*HM*6397645~
NM1*QC*1*Rubble*Barney****34*376899999~
AMT*AU*595~
SVC*HC:T1017:TG*-500.25*-500.25**6~
DTM*150*20080402~
REF*G1*20908~
PLB*382999999*20090930*CS*-1008.1*CS*24.21*CS*5.95~
SE*33*40731~
GE*1*3444~
IEA*1*000003447~
"""
        self._test_997(source, res997)
