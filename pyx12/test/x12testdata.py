from typing import Any

datafiles: dict[str, dict[str, Any]] = {
    "834_lui_id": {
        "source": """ISA*00*          *00*          *ZZ*D00XXX         *ZZ*00AA           *070305*1832*U*00401*000701336*0*P*:~
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
""",
        "res997": """ISA*00*          *00*          *ZZ*00GR           *ZZ*D00111         *070320*1721*U*00401*703201721*0*P*:~
GS*FA*00GR*D00111*20070320*172121*13360001*X*004010~
ST*997*0001~
AK1*BE*13360001~
AK2*834*0001~
AK5*A~
AK9*A*1*1*1~
SE*6*0001~
GE*1*13360001~
IEA*1*703201721~
""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000701336",
                    "ta1_req": "0",
                    "orig_date": "070305",
                    "orig_time": "1832",
                    "cur_line": 24,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "13360001",
                            "fic": "BE",
                            "vriic": "004010X095A1",
                            "ack_code": "A",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 23,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "834",
                                    "trn_set_control_num": "0001",
                                    "vriic": None,
                                    "ack_code": "A",
                                    "cur_line": 22,
                                    "errors": [],
                                    "segments": [],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "834_ls_le_ls": {
        "source": """ISA*00*          *00*          *ZZ*ORDHS          *ZZ*MB888880       *130312*0206*!*00501*000000238*0*P*:~
GS*BE*ORDHS*MB888880*20130312*020630*146*X*005010X220A1~
ST*834*146001*005010X220A1~
BGN*00*0158420020130310001*20130312*0206*PT***2~
REF*38*500647166~
N1*P5*OR-MMIS*FI*930592162~
N1*IN**FI*455492679~
INS*Y*18*001*AI*A*C**AC**N~
REF*0F*REF OF~
REF*23*REF 23~
REF*3H*REF 3H~
REF*F6*REF F6~
DTP*356*D8*20120901~
DTP*357*D8*20130331~
NM1*74*1*SUBSCRIBER LAST 1*SUBSCRIBER FIRST 1*M***34*544001234~
PER*IP**TE*5554718931~
N3*SUBSCRIBER1 ADDRESS 1~
N4*GRANTS PASS*OR*975260000**CY*033~
DMG*D8*19830719*F**C:RET:2186-5~
AMT*P3*82.25~
LUI*LE*ENG**7~
LUI*LE*ENG**5~
NM1*70*1*INCORRECT*FIRST*A***34*001223344~
DMG*D8*19930620*F~
NM1*31*1~
N3*RECIPIENT MAIL ADDRESS LINE 1*RECIPIENT MAIL ADDRESS LINE 2~
N4*SALEM*OR*97301~
NM1*QD*1*RESPONSIBLE PARTY*SMITH*JOHN~
NM1*GD*1*COMPANY NAME 40 CHARACTER OF DATA~
HD*001**HMO*12345678902012062020130415N*IND~
DTP*348*D8*20120901~
REF*17*D4~
COB*U*D183*5~
COB*U*J375*5~
LS*2700~
LX*1~
N1*75*NEWBORN INDICATOR~
REF*ZZ*Y~
LX*2~
N1*75*PREVIOUS PMP END DATE~
DTP*007*D8*20130615~
LX*3~
N1*75*ALTERNATE FORMAT~
REF*ZZ*10~
LX*4~
N1*75*DUE DATE~
DTP*007*D8*20130620~
LX*5~
N1*75*BRANCH - WORKER~
REF*3L*1234567~
LX*6~
N1*75*FIPS CODE~
REF*3L*88~
LX*7~
N1*75*NATIVE AMERICAN HERITAGE CODE~
REF*XX1*Y~
LX*8~
N1*75*GROUP CODE~
REF*XX1*A~
LX*9~
N1*75*BENEFIT PLAN~
REF*PID*BEN~
LX*10~
N1*75*PROGRAM ELIGIBILITY CODE~
REF*17*11~
LX*11~
N1*75*SNRG~
REF*XX1*7~
LX*12~
N1*75*TPL CODE~
REF*9X*99~
LX*13~
N1*75*END REASON~
REF*17*11~
LE*2700~
SE*74*146001~
GE*1*146~
IEA*1*000000238~
""",
        "resAck": """ISA*00*          *00*          *ZZ*MB888880       *ZZ*ORDHS          *130312*0206*!*00501*000000238*0*P*:~
GS*FA*MB888880*ORDHS*20130312*020630*146*X*005010X231~
ST*999*0001*005010X231~
AK1*BE*146*005010X220A1~
AK2*834*146001*005010X220A1~
IK5*A~
AK9*A*1*1*1~
SE*6*0001~
GE*1*146~
IEA*1*000000238~
""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000000238",
                    "ta1_req": "0",
                    "orig_date": "130312",
                    "orig_time": "0206",
                    "cur_line": 78,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "146",
                            "fic": "BE",
                            "vriic": "005010X220A1",
                            "ack_code": "A",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 77,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "834",
                                    "trn_set_control_num": "146001",
                                    "vriic": "005010X220A1",
                                    "ack_code": "A",
                                    "cur_line": 76,
                                    "errors": [],
                                    "segments": [],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "835id": {
        "res997": """ISA*00*          *00*          *ZZ*382999999      *ZZ*383319999      *090304*1036*U*00401*903041036*1*P*:~
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
""",
        "source": """ISA*00*          *00*          *ZZ*383319999      *ZZ*382999999      *090220*1816*U*00401*000003447*1*P*:~
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
""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000003447",
                    "ta1_req": "1",
                    "orig_date": "090220",
                    "orig_time": "1816",
                    "cur_line": 37,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "3444",
                            "fic": "HP",
                            "vriic": "004010X091A1",
                            "ack_code": "A",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 36,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "835",
                                    "trn_set_control_num": "40731",
                                    "vriic": None,
                                    "ack_code": "A",
                                    "cur_line": 35,
                                    "errors": [],
                                    "segments": [],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "837miss": {
        "res997": """ISA*00*          *00*          *ZZ*ZZ001          *ZZ*ZZ000          *041211*1902*U*00401*412111902*1*T*:~
GS*FA*ZZ001*ZZ000*20041211*190228*17*X*004010~
ST*997*0001~
AK1*HC*17~
AK2*837*11280001~
AK5*R*2~
AK9*R*0*0*0*3~
SE*6*0001~
GE*1*17~
TA1*000010121*030828*1128*R*023~
IEA*1*412111902~
""",
        "source": """ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*1*T*:~
GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098A1~
ST*837*11280001~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000010121",
                    "ta1_req": "1",
                    "orig_date": "030828",
                    "orig_time": "1128",
                    "cur_line": 1,
                    "errors": [
                        {
                            "err_cde": "023",
                            "x12_code": "023",
                            "err_str": 'Mandatory segment "Interchange Control Trailer" (IEA=000010121) missing',
                        }
                    ],
                    "groups": [
                        {
                            "gs_control_num": "17",
                            "fic": "HC",
                            "vriic": "004010X098A1",
                            "ack_code": "R",
                            "st_count_orig": 0,
                            "st_count_recv": 0,
                            "cur_line": 2,
                            "errors": [
                                {
                                    "err_cde": "3",
                                    "x12_code": "3",
                                    "err_str": 'Mandatory segment "Functional Group Trailer" (GE=17) missing',
                                }
                            ],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "11280001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 3,
                                    "errors": [
                                        {
                                            "err_cde": "2",
                                            "x12_code": "2",
                                            "err_str": 'Mandatory segment "Transaction Set Trailer" (SE=11280001) missing',
                                        }
                                    ],
                                    "segments": [],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "mult_isa": {
        "res997": """ISA*00*          *00*          *ZZ*ZZ001          *ZZ*ZZ000          *070328*1628*U*00401*703281628*0*T*:~
GS*FA*00GR*D00111*20070328*162824*383880001*X*004010~
ST*997*0001~
AK1*HI*17~
AK2*278*11280001~
AK3*HL*2**3~
AK5*R*5~
AK2*278*11280002~
AK3*HL*2**3~
AK5*R*5~
AK2*278*11280003~
AK3*HL*2**3~
AK5*R*5~
AK9*R*3*3*0~
SE*13*0001~
ST*997*0002~
AK1*HC*18~
AK2*837*11280001~
AK3*REF*2**3~
AK3*NM1*2**3~
AK3*NM1*2**3~
AK3*HL*2**3~
AK5*R*5~
AK9*R*1*1*0~
SE*10*0002~
ST*997*0003~
AK1*HP*383880001~
AK2*835*0001~
AK3*BPR*1**3~
AK5*R*5~
AK9*R*1*1*0~
SE*7*0003~
ST*997*0004~
AK1*HP*2~
AK2*835*0001~
AK3*BPR*1**3~
AK5*R*5~
AK9*R*1*1*0~
SE*7*0004~
ST*997*0005~
AK1*HP*3~
AK2*835*0001~
AK3*BPR*1**3~
AK5*R*5~
AK9*R*1*1*0~
SE*7*0005~
ST*997*0006~
AK1*HI*17~
AK2*278*11280001~
AK3*HL*2**3~
AK5*R*5~
AK2*278*11280002~
AK3*HL*2**3~
AK5*R*5~
AK2*278*11280003~
AK3*HL*2**3~
AK5*R*5~
AK9*R*3*3*0~
SE*13*0006~
ST*997*0007~
AK1*HC*18~
AK2*837*11280001~
AK3*REF*2**3~
AK3*NM1*2**3~
AK3*NM1*2**3~
AK3*HL*2**3~
AK5*R*5~
AK9*R*1*1*0~
SE*10*0007~
ST*997*0008~
AK1*HP*383880001~
AK2*835*0001~
AK3*BPR*1**3~
AK5*R*5~
AK9*R*1*1*0~
SE*7*0008~
GE*8*383880001~
IEA*1*703281628~""",
        "source": """ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010125*0*T*:~
GS*HI*ZZ000*ZZ001*20030828*1128*17*X*004010X094A1~
ST*278*11280001~
BHT*0078*11*121231*20050802*1202~
SE*3*11280001~
ST*278*11280002~
BHT*0078*13*121231*20050802*1202~
SE*3*11280002~
ST*278*11280003~
BHT*0078*11*121231*20050802*1202~
SE*3*11280003~
GE*3*17~
GS*HC*ZZ000*ZZ001*20030828*1128*18*X*004010X098A1~
ST*837*11280001~
BHT*0019*00*121231*20050802*1202*CH~
SE*3*11280001~
GE*1*18~
GS*HP*D00111*00GR*20041028*1609*383880001*X*004010X091A1~
ST*835*0001~
SE*2*0001~
GE*1*383880001~
GS*HP*D00111*00GR*20041028*1609*2*X*004010X091A1~
ST*835*0001~
SE*2*0001~
GE*1*2~
GS*HP*D00111*00GR*20041028*1609*3*X*004010X091A1~
ST*835*0001~
SE*2*0001~
GE*1*3~
IEA*5*000010125~
ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~
GS*HI*ZZ000*ZZ001*20030828*1128*17*X*004010X094A1~
ST*278*11280001~
BHT*0078*11*121231*20050802*1202~
SE*3*11280001~
ST*278*11280002~
BHT*0078*13*121231*20050802*1202~
SE*3*11280002~
ST*278*11280003~
BHT*0078*11*121231*20050802*1202~
SE*3*11280003~
GE*3*17~
GS*HC*ZZ000*ZZ001*20030828*1128*18*X*004010X098A1~
ST*837*11280001~
BHT*0019*00*121231*20050802*1202*CH~
SE*3*11280001~
GE*1*18~
GS*HP*D00111*00GR*20041028*1609*383880001*X*004010X091A1~
ST*835*0001~
SE*2*0001~
GE*1*383880001~
IEA*3*000010121~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000010125",
                    "ta1_req": "0",
                    "orig_date": "030828",
                    "orig_time": "1128",
                    "cur_line": 30,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "17",
                            "fic": "HI",
                            "vriic": "004010X094A1",
                            "ack_code": "R",
                            "st_count_orig": 3,
                            "st_count_recv": 3,
                            "cur_line": 12,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "278",
                                    "trn_set_control_num": "11280001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 5,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 2,
                                            "pos": 10,
                                            "name": "Utilization Management Organization (UMO) Level",
                                            "ls_id": None,
                                            "cur_line": 5,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Utilization Management Organization (UMO) Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                },
                                {
                                    "trn_set_id": "278",
                                    "trn_set_control_num": "11280002",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 8,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 2,
                                            "pos": 10,
                                            "name": "Utilization Management Organization (UMO) Level",
                                            "ls_id": None,
                                            "cur_line": 8,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Utilization Management Organization (UMO) Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                },
                                {
                                    "trn_set_id": "278",
                                    "trn_set_control_num": "11280003",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 11,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 2,
                                            "pos": 10,
                                            "name": "Utilization Management Organization (UMO) Level",
                                            "ls_id": None,
                                            "cur_line": 11,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Utilization Management Organization (UMO) Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                },
                            ],
                        },
                        {
                            "gs_control_num": "18",
                            "fic": "HC",
                            "vriic": "004010X098A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 17,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "11280001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 16,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "REF",
                                            "seg_count": 2,
                                            "pos": 15,
                                            "name": "Transmission Type Identification",
                                            "ls_id": None,
                                            "cur_line": 16,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_segment_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory segment "Transmission Type Identification" (REF) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "NM1",
                                            "seg_count": 2,
                                            "pos": 20,
                                            "name": "Submitter Name",
                                            "ls_id": None,
                                            "cur_line": 16,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Submitter Name" (1000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "NM1",
                                            "seg_count": 2,
                                            "pos": 20,
                                            "name": "Receiver Name",
                                            "ls_id": None,
                                            "cur_line": 16,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Receiver Name" (1000B) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 2,
                                            "pos": 1,
                                            "name": "Billing/Pay-To Provider Hierarchical Level",
                                            "ls_id": None,
                                            "cur_line": 16,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Billing/Pay-To Provider Hierarchical Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                    ],
                                }
                            ],
                        },
                        {
                            "gs_control_num": "383880001",
                            "fic": "HP",
                            "vriic": "004010X091A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 21,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "835",
                                    "trn_set_control_num": "0001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 20,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "BPR",
                                            "seg_count": 1,
                                            "pos": 20,
                                            "name": "Financial Information",
                                            "ls_id": None,
                                            "cur_line": 20,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Table 1 - Header" (HEADER) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "gs_control_num": "2",
                            "fic": "HP",
                            "vriic": "004010X091A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 25,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "835",
                                    "trn_set_control_num": "0001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 24,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "BPR",
                                            "seg_count": 1,
                                            "pos": 20,
                                            "name": "Financial Information",
                                            "ls_id": None,
                                            "cur_line": 24,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Table 1 - Header" (HEADER) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "gs_control_num": "3",
                            "fic": "HP",
                            "vriic": "004010X091A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 29,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "835",
                                    "trn_set_control_num": "0001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 28,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "BPR",
                                            "seg_count": 1,
                                            "pos": 20,
                                            "name": "Financial Information",
                                            "ls_id": None,
                                            "cur_line": 28,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Table 1 - Header" (HEADER) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                }
                            ],
                        },
                    ],
                },
                {
                    "isa_trn_set_id": "000010121",
                    "ta1_req": "0",
                    "orig_date": "030828",
                    "orig_time": "1128",
                    "cur_line": 52,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "17",
                            "fic": "HI",
                            "vriic": "004010X094A1",
                            "ack_code": "R",
                            "st_count_orig": 3,
                            "st_count_recv": 3,
                            "cur_line": 42,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "278",
                                    "trn_set_control_num": "11280001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 35,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 2,
                                            "pos": 10,
                                            "name": "Utilization Management Organization (UMO) Level",
                                            "ls_id": None,
                                            "cur_line": 35,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Utilization Management Organization (UMO) Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                },
                                {
                                    "trn_set_id": "278",
                                    "trn_set_control_num": "11280002",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 38,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 2,
                                            "pos": 10,
                                            "name": "Utilization Management Organization (UMO) Level",
                                            "ls_id": None,
                                            "cur_line": 38,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Utilization Management Organization (UMO) Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                },
                                {
                                    "trn_set_id": "278",
                                    "trn_set_control_num": "11280003",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 41,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 2,
                                            "pos": 10,
                                            "name": "Utilization Management Organization (UMO) Level",
                                            "ls_id": None,
                                            "cur_line": 41,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Utilization Management Organization (UMO) Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                },
                            ],
                        },
                        {
                            "gs_control_num": "18",
                            "fic": "HC",
                            "vriic": "004010X098A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 47,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "11280001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 46,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "REF",
                                            "seg_count": 2,
                                            "pos": 15,
                                            "name": "Transmission Type Identification",
                                            "ls_id": None,
                                            "cur_line": 46,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_segment_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory segment "Transmission Type Identification" (REF) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "NM1",
                                            "seg_count": 2,
                                            "pos": 20,
                                            "name": "Submitter Name",
                                            "ls_id": None,
                                            "cur_line": 46,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Submitter Name" (1000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "NM1",
                                            "seg_count": 2,
                                            "pos": 20,
                                            "name": "Receiver Name",
                                            "ls_id": None,
                                            "cur_line": 46,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Receiver Name" (1000B) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 2,
                                            "pos": 1,
                                            "name": "Billing/Pay-To Provider Hierarchical Level",
                                            "ls_id": None,
                                            "cur_line": 46,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Billing/Pay-To Provider Hierarchical Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                    ],
                                }
                            ],
                        },
                        {
                            "gs_control_num": "383880001",
                            "fic": "HP",
                            "vriic": "004010X091A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 51,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "835",
                                    "trn_set_control_num": "0001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 50,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "BPR",
                                            "seg_count": 1,
                                            "pos": 20,
                                            "name": "Financial Information",
                                            "ls_id": None,
                                            "cur_line": 50,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Table 1 - Header" (HEADER) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                }
                            ],
                        },
                    ],
                },
            ]
        },
    },
    "trailer_errors": {
        "res997": """ISA*00*          *00*          *ZZ*ENCOUNTER      *ZZ*00HP           *041206*1224*U*00401*412061224*0*P*:~
GS*FA*ENCOUNTER*00HP*20041206*122452*1*X*004010~
ST*997*0001~
AK1*HC*1~
AK2*837*300207436~
AK5*R*4~
AK2*837*300207437~
AK5*A~
AK9*R*2*2*1*4~
SE*8*0001~
GE*1*1~
TA1*000484950*040820*1133*R*018~
IEA*1*412061224~""",
        "source": """ISA*00*          *00*          *ZZ*00HP           *ZZ*ENCOUNTER      *040820*1133*U*00401*000484950*1*P*:~
GS*HC*00HP*ENCOUNTER*20040820*1133*1*X*004010X096A1~
ST*837*300207436~
BHT*0019*00*300207436*20040820*1133*RP~
REF*87*004010X096A1~
NM1*41*2*SENDER 1*****46*00HP~
PER*IC*CONTACT 1*TE*8005557487~
NM1*40*2*RECEIVER 1*****46*D00111~
HL*1**20*1~
NM1*85*2*BILLING PROVIDER 1*****24*445556666~
N3*456 MAIN STREET~
N4*THREE RIVERS*MI*49093~
REF*1D*1708146~
HL*2*1*22*0~
SBR*S*18*******MC~
NM1*IL*1*MANN*MICHAEL****MI*11331122~
N3*123 ELM STRET~
N4*BURR OAK*MI*49030~
DMG*D8*19950801*M~
REF*SY*363121212~
NM1*PR*2*MDCH*****PI*D00111~
N3*PO BOX 4321~
N4*LANSING*MI*48909~
CLM*1309590*0***11:A:1*Y*A*Y*A*********N~
DTP*434*RD8*20040618-20040623~
DTP*435*DT*200406180800~
CL1*9*9*09~
CN1*05~
HI*BK:31389*BJ:31389~
NM1*71*1*EXTERNAL*PROVIDER*C***34*999999999~
PRV*AT*ZZ*101Y00000X~
REF*0B*9999999~
NM1*FA*2*ST JOSEPH COUNTY CMH~
PRV*RP*ZZ*101Y00000X~
N3*456 MAIN STREET~
N4*THREE RIVERS*MI*49093~
SBR*P*18**KALAMAZOO CMH*****MC~
AMT*B6*632.5000~
DMG*D8*19950801*M~
OI***Y***I~
NM1*IL*1*MANN*MICHAEL****MI*00000006632~
N3*123 ELM STRET~
N4*BURR OAK*MI*49030~
NM1*PR*2*KALAMAZOO CMH*****PI*174456543~
DTP*573*D8*20040816~
REF*F8*1309590~
SBR*T*18**SENDER 1 HEALTH*****MC~
AMT*B6*632.5000~
DMG*D8*19950801*M~
OI***Y***I~
NM1*IL*1*MANN*MICHAEL****MI*00000006632~
N3*123 ELM STRET~
N4*BURR OAK*MI*49030~
NM1*PR*2*SENDER 1*****PI*174454370~
REF*F8*1309590~
LX*1~
SV2*0100**0*UN*5*0*0~
DTP*472*RD8*20040618-20040623~
SVD*174456543*0**0100*5~
DTP*573*D8*20040816~
SE*60*300207436~
ST*837*300207437~
BHT*0019*00*300207437*20040820*1133*RP~
REF*87*004010X096A1~
NM1*41*2*SENDER 1*****46*00HP~
PER*IC*CONTACT 1*TE*8005557487~
NM1*40*2*RECEIVER 1*****46*D00111~
HL*1**20*1~
NM1*85*2*BILLING PROVIDER 1*****24*445556666~
N3*456 MAIN STREET~
N4*THREE RIVERS*MI*49093~
REF*1D*1708146~
HL*2*1*22*0~
SBR*S*18*******MC~
NM1*IL*1*WAHL*JAMES****MI*12341234~
N3*MT PLEASANT CENTER*1400 W MAIN~
N4*MT. PLEASANT*MI*48858~
DMG*D8*19750704*M~
REF*SY*374121234~
NM1*PR*2*MDCH*****PI*D00111~
N3*PO BOX 4321~
N4*LANSING*MI*48909~
CLM*1304171*0***11:A:1*Y*A*Y*A*********N~
DTP*434*RD8*20040601-20040701~
DTP*435*DT*200406010800~
CL1*9*9*09~
CN1*05~
HI*BK:31234*BJ:31234~
NM1*71*1*EXTERNAL*PROVIDER*C***34*999999999~
PRV*AT*ZZ*101Y00000X~
REF*0B*9999999~
NM1*FA*2*ST JOSEPH COUNTY CMH~
PRV*RP*ZZ*101Y00000X~
N3*456 MAIN STREET~
N4*THREE RIVERS*MI*49093~
SBR*P*18**KALAMAZOO CMH*****MC~
AMT*B6*216.7000~
DMG*D8*19750704*M~
OI***Y***I~
NM1*IL*1*WAHL*JAMES****MI*00000000043~
N3*MT PLEASANT CENTER*1400 W MAIN~
N4*MT. PLEASANT*MI*48858~
NM1*PR*2*KALAMAZOO CMH*****PI*174456543~
DTP*573*D8*20040719~
REF*F8*1304171~
SBR*T*18**SENDER 1 HEALTH*****MC~
AMT*B6*216.7000~
DMG*D8*19750704*M~
OI***Y***I~
NM1*IL*1*WAHL*JAMES****MI*00000000043~
N3*MT PLEASANT CENTER*1400 W MAIN~
N4*MT. PLEASANT*MI*48858~
NM1*PR*2*SENDER 1*****PI*174454370~
REF*F8*1304171~
LX*1~
SV2*0100**0*UN*30*0*0~
DTP*472*RD8*20040601-20040701~
SVD*174456543*0**0100*30~
DTP*573*D8*20040719~
SE*59*300207437~
GE*2*333~
IEA*5*333~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000484950",
                    "ta1_req": "1",
                    "orig_date": "040820",
                    "orig_time": "1133",
                    "cur_line": 122,
                    "errors": [
                        {
                            "err_cde": "001",
                            "x12_code": "001",
                            "err_str": "IEA id=333 does not match ISA id=000484950",
                        },
                        {
                            "err_cde": "021",
                            "x12_code": "021",
                            "err_str": "IEA count for IEA02=333 is wrong",
                        },
                    ],
                    "groups": [
                        {
                            "gs_control_num": "1",
                            "fic": "HC",
                            "vriic": "004010X096A1",
                            "ack_code": "R",
                            "st_count_orig": 2,
                            "st_count_recv": 2,
                            "cur_line": 121,
                            "errors": [
                                {
                                    "err_cde": "4",
                                    "x12_code": "4",
                                    "err_str": "GE id=333 does not match GS id=1",
                                }
                            ],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "300207436",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 61,
                                    "errors": [
                                        {
                                            "err_cde": "4",
                                            "x12_code": "4",
                                            "err_str": "SE count of 60 for SE02=300207436 is wrong. I count 59",
                                        }
                                    ],
                                    "segments": [],
                                },
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "300207437",
                                    "vriic": None,
                                    "ack_code": "A",
                                    "cur_line": 120,
                                    "errors": [],
                                    "segments": [],
                                },
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "trailing_terms": {
        "res997": """ISA*00*          *00*          *ZZ*0000BBB        *ZZ*00000AAA       *070319*1742*U*00401*703191742*0*P*:~
GS*FA*0BBB*0AAA*20070319*174249*1*X*004010~
ST*997*0001~
AK1*HC*1~
AK2*837*300145997~
AK3*CLM*22**8~
AK4*18*1073*1~
AK5*R*5~
AK9*R*1*1*0~
SE*8*0001~
GE*1*1~
IEA*1*703191742~""",
        "source": """ISA*00*          *00*          *ZZ*00000AAA       *ZZ*0000BBB        *040709*1439*U*00401*000484889*0*P*:~
GS*HC*0AAA*0BBB*20040709*1439*1*X*004010X096A1~
ST*837*300145997~
BHT*0019*00*300145997*20040709*1439*RP~
REF*87*004010X096A1~
NM1*41*2*PROVIDER 1*****46*0AAA~
PER*IC*HELPDESK*EM*ADMIN@NULL.NULL*TE*8005557444~
NM1*40*2*RECEIVER 1*****46*000111~
HL*1**20*1~
NM1*85*2*PROVIDER 1*****24*555112222~
N3*PROVIDER 1~
N4*THREE RIVERS*MI*49093~
REF*1D*1705555~
HL*2*1*22*0~
SBR*S*18*******11~
NM1*IL*1*ARNOLD*TOM****MI*666333444~
N3*5324 ELM~
N4*STURGIS*MI*49091~
DMG*D8*19270312*M~
REF*SY*666333444~
NM1*PR*2*PAYER 2*****PI*000111~
N3*PO BOX 0000~
N4*KALAMAZOO*MI*48001~
CLM*12522228*0***11:A:7*Y*A*Y*A********~
DTP*434*RD8*20031213-20031218~
DTP*435*DT*200312130800~
CL1*9*9*09~
REF*F8*12522228~
HI*BK:29689*BJ:29689~
NM1*71*1*EXTERNAL*PROVIDER*C***34*999999999~
PRV*AT*ZZ*101Y00000X~
REF*0B*9999999~
NM1*FA*2*PROVIDER 1~
PRV*RP*ZZ*101Y00000X~
N3*PROVIDER 1~
N4*THREE RIVERS*MI*49093~
LX*1~
SV2*0100**0*UN*5*0*0~
DTP*472*RD8*20031213-20031218~
SE*38*300145997~
GE*1*1~
IEA*1*000484889~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000484889",
                    "ta1_req": "0",
                    "orig_date": "040709",
                    "orig_time": "1439",
                    "cur_line": 42,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "1",
                            "fic": "HC",
                            "vriic": "004010X096A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 41,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "300145997",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 40,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "CLM",
                                            "seg_count": 22,
                                            "pos": 130,
                                            "name": "Claim Information",
                                            "ls_id": None,
                                            "cur_line": 24,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_8_trailing_terminators",
                                                    "x12_code": "8",
                                                    "err_str": "Segment contains trailing element terminators",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [
                                                {
                                                    "ele_pos": 18,
                                                    "subele_pos": None,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "1073",
                                                    "name": "Explanation of Benefits Indicator",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_1_mandatory_missing",
                                                            "x12_code": "1",
                                                            "err_str": 'Mandatory data element "Explanation of Benefits Indicator" (CLM18) is missing',
                                                            "err_val": None,
                                                        }
                                                    ],
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "bad_2010AA_bug": {
        "res997": """ISA*00*          *00*          *ZZ*RECEIVER       *ZZ*SENDER         *040701*1620*U*00401*407011620*0*P*:~
GS*FA*RECEIVER*SENDER*20040701*162046*56*X*004010~
ST*997*0001~
AK1*HC*56~
AK2*837*000000001~
AK3*NM1*8**3~
AK5*R*5~
AK9*R*1*1*0~
SE*7*0001~
GE*1*56~
IEA*1*407011620~""",
        "source": """ISA*03*SENDER    *01*          *ZZ*SENDER         *ZZ*RECEIVER       *040608*1333*U*00401*000000288*0*P*:~
GS*HC*SENDER*RECEIVER*20040608*1333*56*X*004010X098A1~
ST*837*000000001~
BHT*0019*00*289*20040608*1333*CH~
REF*87*004010X098A1~
NM1*41*2*SENDER 1*****46*2309-0923~
PER*IC*Contact Name*TE*1115551111~
NM1*40*2*Payer*****46*21312311~
HL*1**20*1~
HL*2*1*22*0~
SBR*P*18*******11~
NM1*IL*1*GAIMAN*NEIL*M***MI*101911111~
N3*1123 OAKLAND~
N4*VOID*MI*49001~
DMG*D8*19460101*M~
REF*SY*370600001~
NM1*PR*2*PAYER 1*****PI*44-4444444~
N3*4444 ONE RD~
N4*VOID*MI*49001~
CLM*6643-1019AA*14.84***12::1*Y*A*N*Y*B~
HI*BK:29590~
LX*1~
SV1*HC:H2015*14.84*UN*6***1~
DTP*472*D8*20040501~
REF*6R*AKLKJ124231AD~
SE*24*000000001~
GE*1*56~
IEA*1*000000288~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000000288",
                    "ta1_req": "0",
                    "orig_date": "040608",
                    "orig_time": "1333",
                    "cur_line": 28,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "56",
                            "fic": "HC",
                            "vriic": "004010X098A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 27,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "000000001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 26,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "NM1",
                                            "seg_count": 8,
                                            "pos": 15,
                                            "name": "Billing Provider Name",
                                            "ls_id": None,
                                            "cur_line": 10,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Billing Provider Name" (2010AA) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "elements": {
        "res997": """ISA*00*          *00*          *ZZ*RECEIVER       *ZZ*SENDER         *070320*0942*U*00401*703200942*0*P*:~
GS*FA*RECEIVER*SENDER*20070320*094249*56*X*004010~
ST*997*0001~
AK1*HC*56~
AK2*837*000000001~
AK3*REF*3**8~
AK4*2*127*7*004010X098A2~
AK3*PER*5**8~
AK4*3*365*7*TA~
AK3*NM1*7**8~
AK4*8*66*7*47~
AK3*NM1*15**8~
AK4*8*66*5*MIM~
AK4*8*66*7*MIM~
AK3*DMG*18**8~
AK4*2*1251*8*19461301~
AK4*3*1068*7*R~
AK3*CLM*23**8~
AK4*5:1*1331*7*95~
AK5*R*4*5~
AK9*R*1*1*0~
SE*20*0001~
GE*1*56~
IEA*1*703200942~""",
        "source": """ISA*03*SENDER    *01*          *ZZ*SENDER         *ZZ*RECEIVER       *040608*1333*U*00401*000000288*0*P*:~
GS*HC*SENDER*RECEIVER*20040608*1333*56*X*004010X098A1~
ST*837*000000001~
BHT*0019*00*289*20040608*1333*CH~
REF*87*004010X098A2~
NM1*41*2*SENDER 1*****46*2309-0923~
PER*IC*Contact Name*TA*111-555-1111~
PER*IC*Contact Name*TE*111-555-1111~
NM1*40*2*Payer*****47*21312311~
HL*1**20*1~
NM1*85*2*Biller 1*****XX*2309-2222~
N3*1123 MILL~
N4*VOID*MI*49002~
PER*IC*Contact Name*TE*111-555-2222~
HL*2*1*22*0~
SBR*P*18*******11~
NM1*IL*1*GAIMAN*NEIL*MMMM***MIM*101911111~
N3*1123 OAKLAND~
N4*VOID*MI*49001~
DMG*D8*19461301*R~
REF*SY*370600000~
NM1*PR*2*PAYER 1*****PI*44-4444444~
N3*4444 ONE RD~
N4*VOID*MI*49001~
CLM*6643-1019AA*999.6***95::8*Y*A*N*Y*B~
HI*BK:29590~
LX*1~
SV1*HC:H2015*14.84*UN*6***1~
DTP*472*D8*20040501~
REF*6R*AKLKJ124231AD~
SE*30*000000001~
GE*1*56~
IEA*1*000000288~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000000288",
                    "ta1_req": "0",
                    "orig_date": "040608",
                    "orig_time": "1333",
                    "cur_line": 33,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "56",
                            "fic": "HC",
                            "vriic": "004010X098A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 32,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "000000001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 31,
                                    "errors": [
                                        {
                                            "err_cde": "4",
                                            "x12_code": "4",
                                            "err_str": "SE count of 30 for SE02=000000001 is wrong. I count 29",
                                        }
                                    ],
                                    "segments": [
                                        {
                                            "seg_id": "REF",
                                            "seg_count": 3,
                                            "pos": 15,
                                            "name": "Transmission Type Identification",
                                            "ls_id": None,
                                            "cur_line": 5,
                                            "errors": [],
                                            "elements": [
                                                {
                                                    "ele_pos": 2,
                                                    "subele_pos": None,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "127",
                                                    "name": "Transmission Type Code",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_7_invalid_code",
                                                            "x12_code": "7",
                                                            "err_str": "(004010X098A2) is not a valid code for Transmission Type Code (REF02)",
                                                            "err_val": "004010X098A2",
                                                        }
                                                    ],
                                                }
                                            ],
                                        },
                                        {
                                            "seg_id": "PER",
                                            "seg_count": 5,
                                            "pos": 45,
                                            "name": "Submitter EDI Contact Information",
                                            "ls_id": None,
                                            "cur_line": 7,
                                            "errors": [],
                                            "elements": [
                                                {
                                                    "ele_pos": 3,
                                                    "subele_pos": None,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "365",
                                                    "name": "Communication Number Qualifier",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_7_invalid_code",
                                                            "x12_code": "7",
                                                            "err_str": "(TA) is not a valid code for Communication Number Qualifier (PER03)",
                                                            "err_val": "TA",
                                                        }
                                                    ],
                                                }
                                            ],
                                        },
                                        {
                                            "seg_id": "NM1",
                                            "seg_count": 7,
                                            "pos": 20,
                                            "name": "Receiver Name",
                                            "ls_id": None,
                                            "cur_line": 9,
                                            "errors": [],
                                            "elements": [
                                                {
                                                    "ele_pos": 8,
                                                    "subele_pos": None,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "66",
                                                    "name": "Identification Code Qualifier",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_7_invalid_code",
                                                            "x12_code": "7",
                                                            "err_str": "(47) is not a valid code for Identification Code Qualifier (NM108)",
                                                            "err_val": "47",
                                                        }
                                                    ],
                                                }
                                            ],
                                        },
                                        {
                                            "seg_id": "NM1",
                                            "seg_count": 15,
                                            "pos": 15,
                                            "name": "Subscriber Name",
                                            "ls_id": None,
                                            "cur_line": 17,
                                            "errors": [],
                                            "elements": [
                                                {
                                                    "ele_pos": 8,
                                                    "subele_pos": None,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "66",
                                                    "name": "Identification Code Qualifier",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_5_too_long",
                                                            "x12_code": "5",
                                                            "err_str": 'Data element "Identification Code Qualifier" (NM108) is too long: len("MIM") = 3 > 2 (max_len)',
                                                            "err_val": "MIM",
                                                        },
                                                        {
                                                            "err_cde": "ELE_7_invalid_code",
                                                            "x12_code": "7",
                                                            "err_str": "(MIM) is not a valid code for Identification Code Qualifier (NM108)",
                                                            "err_val": "MIM",
                                                        },
                                                    ],
                                                }
                                            ],
                                        },
                                        {
                                            "seg_id": "DMG",
                                            "seg_count": 18,
                                            "pos": 32,
                                            "name": "Subscriber Demographic Information",
                                            "ls_id": None,
                                            "cur_line": 20,
                                            "errors": [],
                                            "elements": [
                                                {
                                                    "ele_pos": 2,
                                                    "subele_pos": None,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "1251",
                                                    "name": "Subscriber Birth Date",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_8_invalid_date_range",
                                                            "x12_code": "8",
                                                            "err_str": 'Data element "Subscriber Birth Date" (DMG02) contains an invalid date (19461301)',
                                                            "err_val": "19461301",
                                                        }
                                                    ],
                                                },
                                                {
                                                    "ele_pos": 3,
                                                    "subele_pos": None,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "1068",
                                                    "name": "Subscriber Gender Code",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_7_invalid_code",
                                                            "x12_code": "7",
                                                            "err_str": "(R) is not a valid code for Subscriber Gender Code (DMG03)",
                                                            "err_val": "R",
                                                        }
                                                    ],
                                                },
                                            ],
                                        },
                                        {
                                            "seg_id": "CLM",
                                            "seg_count": 23,
                                            "pos": 130,
                                            "name": "Claim Information",
                                            "ls_id": None,
                                            "cur_line": 25,
                                            "errors": [],
                                            "elements": [
                                                {
                                                    "ele_pos": 5,
                                                    "subele_pos": 1,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "1331",
                                                    "name": "Facility Type Code",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_7_invalid_code",
                                                            "x12_code": "7",
                                                            "err_str": "(95) is not a valid code for Facility Type Code (CLM05-01)",
                                                            "err_val": "95",
                                                        }
                                                    ],
                                                }
                                            ],
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "bad_header_looping": {
        "res997": """ISA*00*          *00*          *ZZ*00AA           *ZZ*D00000         *070405*0014*U*00401*704050014*0*P*:~
GS*FA*00GR*D00111*20070405*001406*383880001*X*004010~
ST*997*0001~
AK1*HP*383880001~
AK2*835*0001~
AK3*DTM*5**8~
AK4*2*373*8*11111111~
AK3*N1*39**1~
AK3*N3*40**1~
AK3*N4*41**1~
AK3*N1*42**1~
AK5*R*4*5~
AK9*R*1*1*0~
SE*12*0001~
GE*1*383880001~
IEA*1*704050014~""",
        "source": """ISA*00*          *00*          *ZZ*D00000         *ZZ*00AA           *041028*1609*U*00401*000238388*0*P*:~
GS*HP*D00111*00GR*20041028*1609*383880001*X*004010X091A1~
ST*835*0001~
BPR*H*0*C*NON************20041028~
TRN*1*000000000*1386000134~
REF*EV*00GR~
DTM*405*11111111~
N1*PR*PAYER~
N3*P.O. BOX 30479~
N4*LANSING*MI*48909~
N1*PE*UNKNOWN*FI*444313000~
LX*1~
TS3*653423424*12*20041231*1*915.39~
CLP*2005555A*4*915.39*0**MC*4276512332~
NM1*QC*1*BACH*JOHANN*S***MR*00001612~
NM1*82*2*PAYEE*****MC*44452736~
SVC*HC:T1005*500.04*0**68~
DTM*150*20031129~
DTM*151*20031129~
CAS*CO*16*500.04~
LQ*HE*N14~
LQ*HE*N14~
LQ*HE*N14~
LQ*HE*N14~
SVC*HC:T1005*127.8*0**16~
DTM*150*20031030~
DTM*151*20031030~
CAS*OA*A7*127.8~
LQ*HE*N14~
LQ*HE*N14~
LQ*HE*N14~
LQ*HE*N14~
SVC*HC:T1005*287.55*0**36~
DTM*150*20031031~
DTM*151*20031031~
CAS*OA*A7*287.55~
LQ*HE*N14~
LQ*HE*N14~
LQ*HE*N14~
LQ*HE*N14~
N1*PR*PAYER~
N3*P.O. BOX 30479~
N4*LANSING*MI*48909~
N1*PE*UNKNOWN*FI*444313000~
LX*1~
TS3*653423424*12*20041231*1*915.39~
CLP*2005555A*4*915.39*0**MC*4276512332~
NM1*QC*1*BACH*JOHANN*S***MR*00001612~
NM1*82*2*PAYEE*****MC*44452736~
SVC*HC:T1005*500.04*0**68~
DTM*150*20031129~
DTM*151*20031129~
CAS*CO*16*500.04~
LQ*HE*N14~
LQ*HE*N14~
LQ*HE*N14~
LQ*HE*N14~
SVC*HC:T1005*127.8*0**16~
DTM*150*20031030~
DTM*151*20031030~
CAS*OA*A7*127.8~
LQ*HE*N14~
LQ*HE*N14~
LQ*HE*N14~
LQ*HE*N14~
SVC*HC:T1005*287.55*0**36~
DTM*150*20031031~
DTM*151*20031031~
CAS*OA*A7*287.55~
LQ*HE*N14~
LQ*HE*N14~
LQ*HE*N14~
LQ*HE*N14~
SE*39*0001~
GE*1*383880001~
IEA*1*000238388~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000238388",
                    "ta1_req": "0",
                    "orig_date": "041028",
                    "orig_time": "1609",
                    "cur_line": 76,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "383880001",
                            "fic": "HP",
                            "vriic": "004010X091A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 75,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "835",
                                    "trn_set_control_num": "0001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 74,
                                    "errors": [
                                        {
                                            "err_cde": "4",
                                            "x12_code": "4",
                                            "err_str": "SE count of 39 for SE02=0001 is wrong. I count 72",
                                        }
                                    ],
                                    "segments": [
                                        {
                                            "seg_id": "DTM",
                                            "seg_count": 5,
                                            "pos": 70,
                                            "name": "Production Date",
                                            "ls_id": None,
                                            "cur_line": 7,
                                            "errors": [],
                                            "elements": [
                                                {
                                                    "ele_pos": 2,
                                                    "subele_pos": None,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "373",
                                                    "name": "Production Date",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_8_invalid_date",
                                                            "x12_code": "8",
                                                            "err_str": 'Data element "Production Date" (DTM02) contains an invalid date (11111111)',
                                                            "err_val": "11111111",
                                                        }
                                                    ],
                                                }
                                            ],
                                        },
                                        {
                                            "seg_id": "N1",
                                            "seg_count": 39,
                                            "pos": 130,
                                            "name": "Health Care Remark Codes",
                                            "ls_id": None,
                                            "cur_line": 41,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_1_segment_not_found",
                                                    "x12_code": "1",
                                                    "err_str": "Segment N1*PR not found.  Started at /ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/LQ",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "N3",
                                            "seg_count": 40,
                                            "pos": 130,
                                            "name": "Health Care Remark Codes",
                                            "ls_id": None,
                                            "cur_line": 42,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_1_segment_not_found",
                                                    "x12_code": "1",
                                                    "err_str": "Segment N3*P.O. BOX 30479 not found.  Started at /ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/LQ",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "N4",
                                            "seg_count": 41,
                                            "pos": 130,
                                            "name": "Health Care Remark Codes",
                                            "ls_id": None,
                                            "cur_line": 43,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_1_segment_not_found",
                                                    "x12_code": "1",
                                                    "err_str": "Segment N4*LANSING not found.  Started at /ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/LQ",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "N1",
                                            "seg_count": 42,
                                            "pos": 130,
                                            "name": "Health Care Remark Codes",
                                            "ls_id": None,
                                            "cur_line": 44,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_1_segment_not_found",
                                                    "x12_code": "1",
                                                    "err_str": "Segment N1*PE not found.  Started at /ISA_LOOP/GS_LOOP/ST_LOOP/DETAIL/2000/2100/2110/LQ",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "blank1": {
        "res997": """ISA*00*          *00*          *ZZ*0000BBB        *ZZ*00000AAA       *050721*1643*U*00401*507211643*0*P*:~
GS*FA*0BBB*0AAA*20050721*164347*1*X*004010~
ST*997*0001~
AK1*HC*1~
AK2*837*300145997~
AK3*SV2*57**8~
AK4*2:1*235*7*  ~
AK4*2:2*234*1~
AK3*SVD*59**8~
AK4*3:1*235*7*  ~
AK4*3:2*234*1~
AK5*R*5~
AK9*R*1*1*0~
SE*12*0001~
GE*1*1~
IEA*1*507211643~""",
        "source": """ISA*00*          *00*          *ZZ*00000AAA       *ZZ*0000BBB        *040709*1439*U*00401*000484889*0*P*:~
GS*HC*0AAA*0BBB*20040709*1439*1*X*004010X096A1~
ST*837*300145997~
BHT*0019*00*300145997*20040709*1439*RP~
REF*87*004010X096A1~
NM1*41*2*PROVIDER 1*****46*0AAA~
PER*IC*HELPDESK*EM*ADMIN@NULL.NULL*TE*8005557444~
NM1*40*2*RECEIVER 1*****46*000111~
HL*1**20*1~
NM1*85*2*PROVIDER 1*****24*555112222~
N3*PROVIDER 1~
N4*THREE RIVERS*MI*49093~
REF*1D*1705555~
HL*2*1*22*0~
SBR*S*18*******11~
NM1*IL*1*ARNOLD*TOM****MI*666333444~
N3*5324 ELM~
N4*STURGIS*MI*49091~
DMG*D8*19270312*M~
REF*SY*666333444~
NM1*PR*2*PAYER 2*****PI*000111~
N3*PO BOX 0000~
N4*KALAMAZOO*MI*48001~
CLM*12522228*0***11:A:7*Y*A*Y*A*********N~
DTP*434*RD8*20031213-20031218~
DTP*435*DT*200312130800~
CL1*9*9*09~
REF*F8*12522228~
HI*BK:29689*BJ:29689~
NM1*71*1*EXTERNAL*PROVIDER*C***34*999999999~
PRV*AT*ZZ*101Y00000X~
REF*0B*9999999~
NM1*FA*2*PROVIDER 1~
PRV*RP*ZZ*101Y00000X~
N3*PROVIDER 1~
N4*THREE RIVERS*MI*49093~
SBR*T*18**PAYER A*****11~
AMT*B6*605.0000~
AMT*C4*0~
DMG*D8*19570312*M~
OI***Y***I~
NM1*IL*1*ARNOLD*TOM****MI*00000007018~
N3*5324 ELM~
N4*STURGIS*MI*49091~
NM1*PR*2*PAYER A*****PI*552312313~
DTP*573*D8*20040210~
REF*F8*1253278~
SBR*P*18**PROVIDER 1*****11~
AMT*B6*605.0000~
AMT*C4*0~
DMG*D8*19570312*M~
OI***Y***I~
NM1*IL*1*ARNOLD*TOM****MI*00000007018~
N3*5324 ELM~
N4*STURGIS*MI*49091~
NM1*PR*2*PROVIDER 1*****PI*13256235~
REF*F8*1253278~
LX*1~
SV2*0100*  :*0*UN*5*0*0~
DTP*472*RD8*20031213-20031218~
SVD*5222312313*0*  :*0100*5~
DTP*573*D8*20040210~
SVD*13256235*0**0100*5~
DTP*573*D8*20040210~
SE*63*300145997~
GE*1*1~
IEA*1*000484889~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000484889",
                    "ta1_req": "0",
                    "orig_date": "040709",
                    "orig_time": "1439",
                    "cur_line": 67,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "1",
                            "fic": "HC",
                            "vriic": "004010X096A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 66,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "300145997",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 65,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "SV2",
                                            "seg_count": 57,
                                            "pos": 375,
                                            "name": "Institutional Service Line",
                                            "ls_id": None,
                                            "cur_line": 59,
                                            "errors": [],
                                            "elements": [
                                                {
                                                    "ele_pos": 2,
                                                    "subele_pos": 1,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "235",
                                                    "name": "Product or Service ID Qualifier",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_7_invalid_code",
                                                            "x12_code": "7",
                                                            "err_str": "(  ) is not a valid code for Product or Service ID Qualifier (SV202-01)",
                                                            "err_val": "  ",
                                                        }
                                                    ],
                                                },
                                                {
                                                    "ele_pos": 2,
                                                    "subele_pos": 2,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "234",
                                                    "name": "Procedure Code",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_1_mandatory_missing",
                                                            "x12_code": "1",
                                                            "err_str": 'Mandatory data element "Procedure Code" (SV202-02) is missing',
                                                            "err_val": None,
                                                        }
                                                    ],
                                                },
                                            ],
                                        },
                                        {
                                            "seg_id": "SVD",
                                            "seg_count": 59,
                                            "pos": 540,
                                            "name": "Service Line Adjudication Information",
                                            "ls_id": None,
                                            "cur_line": 61,
                                            "errors": [],
                                            "elements": [
                                                {
                                                    "ele_pos": 3,
                                                    "subele_pos": 1,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "235",
                                                    "name": "Product or Service ID Qualifier",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_7_invalid_code",
                                                            "x12_code": "7",
                                                            "err_str": "(  ) is not a valid code for Product or Service ID Qualifier (SVD03-01)",
                                                            "err_val": "  ",
                                                        }
                                                    ],
                                                },
                                                {
                                                    "ele_pos": 3,
                                                    "subele_pos": 2,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "234",
                                                    "name": "Procedure Code",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_1_mandatory_missing",
                                                            "x12_code": "1",
                                                            "err_str": 'Mandatory data element "Procedure Code" (SVD03-02) is missing',
                                                            "err_val": None,
                                                        }
                                                    ],
                                                },
                                            ],
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "ele": {
        "res997": """ISA*00*          *00*          *ZZ*0000BBB        *ZZ*00000AAA       *041214*1129*U*00401*412141129*1*P*:~
GS*FA*0BBB*0AAA*20041214*112925*1*X*004010~
ST*997*0001~
AK1*HC*1~
AK2*837*300145997~
AK5*R*3*7~
AK9*R*1*1*0*1~
SE*6*0001~
GE*1*1~
TA1*000484889*040709*3339*R*015~
IEA*1*412141129~""",
        "source": """ISA*00*          *00*          *ZZ*00000AAA       *ZZ*0000BBB        *040709*3339*U*00401*000484889*1*P*:~
GS*HC*0AAA *0BBB *20040709*1439*1*X*004010X096A1~
ST*837*300145997 ~
BHT*0019*00*300145997*20040709*1439*RP~
REF*87*004010X096A1~
NM1*41*2*PROVIDER 1*****46*0AAA~
PER*IC*HELPDESK*EM*ADMIN@NULL.NULL*TE*8005557444~
NM1*40*2*RECEIVER 1*****46*000111~
HL*1**20*1~
NM1*85*2*PROVIDER 1*****24*555112222~
N3*PROVIDER 1~
N4*THREE RIVERS*MI*49093~
REF*1D*1705555~
HL*2*1*22*0~
SBR*S*18*******11~
NM1*IL*1*ARNOLD*TOM****MI*666333444~
N3*5324 ELM~
N4*STURGIS*MI*49091~
DMG*D8*19270312*M~
REF*SY*666333444~
NM1*PR*2*PAYER 2*****PI*000111~
N3*PO BOX 0000~
N4*KALAMAZOO*MI*48001~
CLM*12522228*0***11:A:7*Y*A*Y*A*********N~
DTP*434*RD8*20031213-20031218~
DTP*435*DT*200312130800~
CL1*9*9*09~
REF*F8*12522228~
HI*BK:29689*BJ:29689~
NM1*71*1*EXTERNAL*PROVIDER*C***34*999999999~
PRV*AT*ZZ*101Y00000X~
REF*0B*9999999~
NM1*FA*2*PROVIDER 1~
PRV*RP*ZZ*101Y00000X~
N3*PROVIDER 1~
N4*THREE RIVERS*MI*49093~
SBR*T*18**PAYER A*****11~
AMT*B6*605.0000~
AMT*C4*0~
DMG*D8*19570312*M~
OI***Y***I~
NM1*IL*1*ARNOLD*TOM****MI*00000007018~
N3*5324 ELM~
N4*STURGIS*MI*49091~
NM1*PR*2*PAYER A*****PI*552312313~
DTP*573*D8*20040210~
REF*F8*1253278~
SBR*P*18**PROVIDER 1*****11~
AMT*B6*605.0000~
AMT*C4*0~
DMG*D8*19570312*M~
OI***Y***I~
NM1*IL*1*ARNOLD*TOM****MI*00000007018~
N3*5324 ELM~
N4*STURGIS*MI*49091~
NM1*PR*2*PROVIDER 1*****PI*13256235~
REF*F8*1253278~
LX*1~
SV2*0100**0*UN*5*0*0~
DTP*472*RD8*20031213-20031218~
SVD*5222312313*0**0100*5~
DTP*573*D8*20040210~
SVD*13256235*0**0100*5~
DTP*573*D8*20040210~
SE*63*300145997~
GE*1*1~
IEA*1*000484889~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000484889",
                    "ta1_req": "1",
                    "orig_date": "040709",
                    "orig_time": "3339",
                    "cur_line": 67,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "1",
                            "fic": "HC",
                            "vriic": "004010X096A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 66,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "300145997 ",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 65,
                                    "errors": [
                                        {
                                            "err_cde": "3",
                                            "x12_code": "3",
                                            "err_str": "SE id=300145997 does not match ST id=300145997 ",
                                        }
                                    ],
                                    "segments": [],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "fail_no_IEA": {
        "res997": """ISA*00*          *00*          *ZZ*ZZ001          *ZZ*ZZ000          *040701*1621*U*00401*407011621*0*T*:~
GS*FA*ZZ001*ZZ000*20040701*162104*17*X*004010~
ST*997*0001~
AK1*HC*17~
AK2*837*11280001~
AK3*BHT*1**3~
AK3*HL*1**3~
AK5*R*4*5~
AK9*R*1*1*0~
SE*8*0001~
GE*1*17~
TA1*000010121*030828*1128*R*023~
IEA*1*407011621~""",
        "source": """ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*1*T*:~
GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098A1~
ST*837*11280001~
SE*0*11280001~
GE*1*17~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000010121",
                    "ta1_req": "1",
                    "orig_date": "030828",
                    "orig_time": "1128",
                    "cur_line": 1,
                    "errors": [
                        {
                            "err_cde": "023",
                            "x12_code": "023",
                            "err_str": 'Mandatory segment "Interchange Control Trailer" (IEA=000010121) missing',
                        }
                    ],
                    "groups": [
                        {
                            "gs_control_num": "17",
                            "fic": "HC",
                            "vriic": "004010X098A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 5,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "11280001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 4,
                                    "errors": [
                                        {
                                            "err_cde": "4",
                                            "x12_code": "4",
                                            "err_str": "SE count of 0 for SE02=11280001 is wrong. I count 2",
                                        }
                                    ],
                                    "segments": [
                                        {
                                            "seg_id": "BHT",
                                            "seg_count": 1,
                                            "pos": 10,
                                            "name": "Beginning of Hierarchical Transaction",
                                            "ls_id": None,
                                            "cur_line": 4,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Table 1 - Header" (HEADER) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 1,
                                            "pos": 1,
                                            "name": "Billing/Pay-To Provider Hierarchical Level",
                                            "ls_id": None,
                                            "cur_line": 4,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Billing/Pay-To Provider Hierarchical Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "loop_counting": {
        "res997": """ISA*00*          *00*          *ZZ*BBBBBBBBB      *ZZ*AAAAAAAA       *041210*0057*U*00401*412100057*1*P*:~
GS*FA*BBBBBBBBB*AAAA*20041210*005722*1167*X*004010~
ST*997*0001~
AK1*HC*1167~
AK2*837*1179~
AK3*LX*385**4~
AK3*LX*392**4~
AK3*LX*399**4~
AK3*LX*406**4~
AK5*R*5~
AK9*R*1*1*0~
SE*10*0001~
GE*1*1167~
TA1*000001168*041105*1526*A*000~
IEA*1*412100057~""",
        "source": """ISA*00*          *00*          *ZZ*AAAAAAAA       *ZZ*BBBBBBBBB      *041105*1526*U*00401*000001168*1*P*:~
GS*HC*AAAA*BBBBBBBBB*20041105*1526*1167*X*004010X098A1~
ST*837*1179~
BHT*0019*00*AAAA1179*20041105*1526*RP~
REF*87*004010X098A1~
NM1*41*2*Sender 1*****46*99999~
PER*IC*SUPPORT*EM*Support@dev.null*TE*8005553333~
NM1*40*2*Receiver 1*****46*8888888~
HL*1**20*1~
NM1*85*2*Sender 1*****24*999999999~
N3*399 ELM ROAD~
N4*Kalamazoo*MI*49001~
REF*1D*333402169~
HL*2*1*22*0~
SBR*P*18*******MC~
NM1*IL*1*THE FIFTH*RICHARD****MI*1212121~
N3*156 ELM~
N4*KALAMAZOO*MI*49001~
DMG*D8*19051104*M~
NM1*PR*2*PAYER 1*****PI*8888888~
CLM*3215338*21***12::1*Y*A*Y*A*B~
CN1*05~
HI*BK:317~
NM1*82*2*PROVIDER 1*****24*222185735~
PRV*PE*ZZ*103T00000X~
SBR*P*18***MC****MC~
AMT*B6*0~
DMG*D8*19051104*M~
OI***Y*B**I~
NM1*IL*1*THE FIFTH*RICHARD****MI*0000000004~
N3*156 ELM~
N4*KALAMAZOO*MI*49001~
REF*SY*777777777~
NM1*PR*2*Sender 1S*****PI*12128909~
REF*F8*3215338~
REF*G1*121282~
LX*1~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040407~
REF*6R*1057296~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*2~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040414~
REF*6R*1057297~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*3~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040421~
REF*6R*1057298~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*4~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*5~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*6~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*7~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*8~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*9~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*10~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*11~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*12~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*13~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*14~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*15~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*16~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*17~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*18~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*19~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*20~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*21~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*22~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*23~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*24~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*25~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*26~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*27~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*28~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*29~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*30~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*31~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*32~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*33~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*34~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*35~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*36~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*37~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*38~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*39~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*40~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*41~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*42~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*43~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*44~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*45~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*46~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*47~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*48~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*49~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*50~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*51~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*52~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*53~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*54~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
SE*413*1179~
GE*1*1167~
IEA*1*000001168~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000001168",
                    "ta1_req": "1",
                    "orig_date": "041105",
                    "orig_time": "1526",
                    "cur_line": 417,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "1167",
                            "fic": "HC",
                            "vriic": "004010X098A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 416,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "1179",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 415,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "LX",
                                            "seg_count": 385,
                                            "pos": 365,
                                            "name": "Service Line",
                                            "ls_id": None,
                                            "cur_line": 387,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_4_loop_repeat_exceeded",
                                                    "x12_code": "4",
                                                    "err_str": "Loop 2400 exceeded max count.  Found 51, should have 50",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "LX",
                                            "seg_count": 392,
                                            "pos": 365,
                                            "name": "Service Line",
                                            "ls_id": None,
                                            "cur_line": 394,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_4_loop_repeat_exceeded",
                                                    "x12_code": "4",
                                                    "err_str": "Loop 2400 exceeded max count.  Found 52, should have 50",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "LX",
                                            "seg_count": 399,
                                            "pos": 365,
                                            "name": "Service Line",
                                            "ls_id": None,
                                            "cur_line": 401,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_4_loop_repeat_exceeded",
                                                    "x12_code": "4",
                                                    "err_str": "Loop 2400 exceeded max count.  Found 53, should have 50",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "LX",
                                            "seg_count": 406,
                                            "pos": 365,
                                            "name": "Service Line",
                                            "ls_id": None,
                                            "cur_line": 408,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_4_loop_repeat_exceeded",
                                                    "x12_code": "4",
                                                    "err_str": "Loop 2400 exceeded max count.  Found 54, should have 50",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "loop_counting2": {
        "res997": """ISA*00*          *00*          *ZZ*BBBBBBBBB      *ZZ*AAAAAAAA       *120718*1046*U*00401*207181046*1*P*:~
GS*FA*BBBBBBBBB*AAAA*20120718*104632*1167*X*004010~
ST*997*0001~
AK1*HC*1167~
AK2*837*1179~
AK3*LX*385**4~
AK3*LX*392**4~
AK3*LX*399**4~
AK3*LX*406**4~
AK5*R*5~
AK9*R*1*1*0~
SE*10*0001~
GE*1*1167~
TA1*000001168*041105*1526*A*000~
IEA*1*207181046~""",
        "source": """ISA*00*          *00*          *ZZ*AAAAAAAA       *ZZ*BBBBBBBBB      *041105*1526*U*00401*000001168*1*P*:~
GS*HC*AAAA*BBBBBBBBB*20041105*1526*1167*X*004010X098A1~
ST*837*1179~
BHT*0019*00*AAAA1179*20041105*1526*RP~
REF*87*004010X098A1~
NM1*41*2*Sender 1*****46*99999~
PER*IC*SUPPORT*EM*Support@dev.null*TE*8005553333~
NM1*40*2*Receiver 1*****46*8888888~
HL*1**20*1~
NM1*85*2*Sender 1*****24*999999999~
N3*399 ELM ROAD~
N4*Kalamazoo*MI*49001~
REF*1D*333402169~
HL*2*1*22*0~
SBR*P*18*******MC~
NM1*IL*1*THE FIFTH*RICHARD****MI*1212121~
N3*156 ELM~
N4*KALAMAZOO*MI*49001~
DMG*D8*19051104*M~
NM1*PR*2*PAYER 1*****PI*8888888~
CLM*3215338*21***12::1*Y*A*Y*A*B~
CN1*05~
HI*BK:317~
NM1*82*2*PROVIDER 1*****24*222185735~
PRV*PE*ZZ*103T00000X~
SBR*P*18***MC****MC~
AMT*B6*0~
DMG*D8*19051104*M~
OI***Y*B**I~
NM1*IL*1*THE FIFTH*RICHARD****MI*0000000004~
N3*156 ELM~
N4*KALAMAZOO*MI*49001~
REF*SY*777777777~
NM1*PR*2*Sender 1S*****PI*12128909~
REF*F8*3215338~
REF*G1*121282~
LX*1~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040407~
REF*6R*1057296~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*2~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040414~
REF*6R*1057297~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*3~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040421~
REF*6R*1057298~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*4~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*5~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*6~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*7~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*8~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*9~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*10~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*11~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*12~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*13~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*14~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*15~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*16~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*17~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*18~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*19~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*20~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*21~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*22~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*23~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*24~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*25~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*26~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*27~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*28~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*29~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*30~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*31~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*32~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*33~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*34~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*35~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*36~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*37~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*38~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*39~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*40~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*41~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*42~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*43~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*44~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*45~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*46~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*47~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*48~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*49~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*50~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*51~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*52~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*53~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*54~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040428~
REF*6R*1057299~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
SE*413*1179~
GE*1*1167~
IEA*1*000001168~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000001168",
                    "ta1_req": "1",
                    "orig_date": "041105",
                    "orig_time": "1526",
                    "cur_line": 417,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "1167",
                            "fic": "HC",
                            "vriic": "004010X098A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 416,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "1179",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 415,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "LX",
                                            "seg_count": 385,
                                            "pos": 365,
                                            "name": "Service Line",
                                            "ls_id": None,
                                            "cur_line": 387,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_4_loop_repeat_exceeded",
                                                    "x12_code": "4",
                                                    "err_str": "Loop 2400 exceeded max count.  Found 51, should have 50",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "LX",
                                            "seg_count": 392,
                                            "pos": 365,
                                            "name": "Service Line",
                                            "ls_id": None,
                                            "cur_line": 394,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_4_loop_repeat_exceeded",
                                                    "x12_code": "4",
                                                    "err_str": "Loop 2400 exceeded max count.  Found 52, should have 50",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "LX",
                                            "seg_count": 399,
                                            "pos": 365,
                                            "name": "Service Line",
                                            "ls_id": None,
                                            "cur_line": 401,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_4_loop_repeat_exceeded",
                                                    "x12_code": "4",
                                                    "err_str": "Loop 2400 exceeded max count.  Found 53, should have 50",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "LX",
                                            "seg_count": 406,
                                            "pos": 365,
                                            "name": "Service Line",
                                            "ls_id": None,
                                            "cur_line": 408,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_4_loop_repeat_exceeded",
                                                    "x12_code": "4",
                                                    "err_str": "Loop 2400 exceeded max count.  Found 54, should have 50",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "multiple_trn": {
        "res997": """ISA*00*          *00*          *ZZ*ZZ001          *ZZ*ZZ000          *050807*0207*U*00401*508070207*0*T*:~
GS*FA*00GR*D00111*20050807*020749*383880001*X*004010~
ST*997*0001~
AK1*HI*17~
AK2*278*11280001~
AK3*HL*2**3~
AK5*R*5~
AK2*278*11280002~
AK3*HL*2**3~
AK5*R*5~
AK2*278*11280003~
AK3*HL*2**3~
AK5*R*5~
AK9*R*3*3*0~
SE*13*0001~
ST*997*0002~
AK1*HC*18~
AK2*837*11280001~
AK3*REF*2**3~
AK3*NM1*2**3~
AK3*NM1*2**3~
AK3*HL*2**3~
AK5*R*5~
AK9*R*1*1*0~
SE*10*0002~
ST*997*0003~
AK1*HP*383880001~
AK2*835*0001~
AK3*BPR*1**3~
AK5*R*5~
AK9*R*1*1*0~
SE*7*0003~
GE*3*383880001~
IEA*1*508070207~""",
        "source": """ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~
GS*HI*ZZ000*ZZ001*20030828*1128*17*X*004010X094A1~
ST*278*11280001~
BHT*0078*11*121231*20050802*1202~
SE*3*11280001~
ST*278*11280002~
BHT*0078*13*121231*20050802*1202~
SE*3*11280002~
ST*278*11280003~
BHT*0078*11*121231*20050802*1202~
SE*3*11280003~
GE*3*17~
GS*HC*ZZ000*ZZ001*20030828*1128*18*X*004010X098A1~
ST*837*11280001~
BHT*0019*00*121231*20050802*1202*CH~
SE*3*11280001~
GE*1*18~
GS*HP*D00111*00GR*20041028*1609*383880001*X*004010X091A1~
ST*835*0001~
SE*2*0001~
GE*1*383880001~
IEA*3*000010121~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000010121",
                    "ta1_req": "0",
                    "orig_date": "030828",
                    "orig_time": "1128",
                    "cur_line": 22,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "17",
                            "fic": "HI",
                            "vriic": "004010X094A1",
                            "ack_code": "R",
                            "st_count_orig": 3,
                            "st_count_recv": 3,
                            "cur_line": 12,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "278",
                                    "trn_set_control_num": "11280001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 5,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 2,
                                            "pos": 10,
                                            "name": "Utilization Management Organization (UMO) Level",
                                            "ls_id": None,
                                            "cur_line": 5,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Utilization Management Organization (UMO) Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                },
                                {
                                    "trn_set_id": "278",
                                    "trn_set_control_num": "11280002",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 8,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 2,
                                            "pos": 10,
                                            "name": "Utilization Management Organization (UMO) Level",
                                            "ls_id": None,
                                            "cur_line": 8,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Utilization Management Organization (UMO) Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                },
                                {
                                    "trn_set_id": "278",
                                    "trn_set_control_num": "11280003",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 11,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 2,
                                            "pos": 10,
                                            "name": "Utilization Management Organization (UMO) Level",
                                            "ls_id": None,
                                            "cur_line": 11,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Utilization Management Organization (UMO) Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                },
                            ],
                        },
                        {
                            "gs_control_num": "18",
                            "fic": "HC",
                            "vriic": "004010X098A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 17,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "11280001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 16,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "REF",
                                            "seg_count": 2,
                                            "pos": 15,
                                            "name": "Transmission Type Identification",
                                            "ls_id": None,
                                            "cur_line": 16,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_segment_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory segment "Transmission Type Identification" (REF) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "NM1",
                                            "seg_count": 2,
                                            "pos": 20,
                                            "name": "Submitter Name",
                                            "ls_id": None,
                                            "cur_line": 16,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Submitter Name" (1000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "NM1",
                                            "seg_count": 2,
                                            "pos": 20,
                                            "name": "Receiver Name",
                                            "ls_id": None,
                                            "cur_line": 16,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Receiver Name" (1000B) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 2,
                                            "pos": 1,
                                            "name": "Billing/Pay-To Provider Hierarchical Level",
                                            "ls_id": None,
                                            "cur_line": 16,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Billing/Pay-To Provider Hierarchical Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                    ],
                                }
                            ],
                        },
                        {
                            "gs_control_num": "383880001",
                            "fic": "HP",
                            "vriic": "004010X091A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 21,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "835",
                                    "trn_set_control_num": "0001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 20,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "BPR",
                                            "seg_count": 1,
                                            "pos": 20,
                                            "name": "Financial Information",
                                            "ls_id": None,
                                            "cur_line": 20,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Table 1 - Header" (HEADER) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                }
                            ],
                        },
                    ],
                }
            ]
        },
    },
    "ordinal": {
        "res997": """ISA*00*          *00*          *ZZ*0000BBB        *ZZ*00000AAA       *040809*1625*U*00401*408091625*0*P*:~
GS*FA*0BBB*0AAA*20040809*162519*1*X*004010~
ST*997*0001~
AK1*HC*1~
AK2*837*300145997~
AK5*A~
AK9*A*1*1*1~
SE*6*0001~
GE*1*1~
IEA*1*408091625~""",
        "source": """ISA*00*          *00*          *ZZ*00000AAA       *ZZ*0000BBB        *040709*1439*U*00401*000484889*0*P*:~
GS*HC*0AAA*0BBB*20040709*1439*1*X*004010X096A1~
ST*837*300145997~
BHT*0019*00*300145997*20040709*1439*RP~
REF*87*004010X096A1~
NM1*41*2*PROVIDER 1*****46*0AAA~
PER*IC*HELPDESK*EM*ADMIN@NULL.NULL*TE*8005557444~
NM1*40*2*RECEIVER 1*****46*000111~
HL*1**20*1~
NM1*85*2*PROVIDER 1*****24*555112222~
N3*PROVIDER 1~
N4*THREE RIVERS*MI*49093~
REF*1D*1705555~
HL*2*1*22*0~
SBR*S*18*******11~
NM1*IL*1*ARNOLD*TOM****MI*666333444~
N3*5324 ELM~
N4*STURGIS*MI*49091~
DMG*D8*19270312*M~
REF*SY*666333444~
NM1*PR*2*PAYER 2*****PI*000111~
N3*PO BOX 0000~
N4*KALAMAZOO*MI*48001~
CLM*12522228*0***11:A:7*Y*A*Y*A*********N~
DTP*434*RD8*20031213-20031218~
DTP*435*DT*200312130800~
CL1*9*9*09~
REF*F8*12522228~
HI*BK:29689*BJ:29689~
NM1*71*1*EXTERNAL*PROVIDER*C***34*999999999~
PRV*AT*ZZ*101Y00000X~
REF*0B*9999999~
NM1*FA*2*PROVIDER 1~
PRV*RP*ZZ*101Y00000X~
N3*PROVIDER 1~
N4*THREE RIVERS*MI*49093~
SBR*T*18**PAYER A*****11~
AMT*B6*605.0000~
AMT*C4*0~
DMG*D8*19570312*M~
OI***Y***I~
NM1*IL*1*ARNOLD*TOM****MI*00000007018~
N3*5324 ELM~
N4*STURGIS*MI*49091~
NM1*PR*2*PAYER A*****PI*552312313~
DTP*573*D8*20040210~
REF*F8*1253278~
SBR*P*18**PROVIDER 1*****11~
AMT*B6*605.0000~
AMT*C4*0~
DMG*D8*19570312*M~
OI***Y***I~
NM1*IL*1*ARNOLD*TOM****MI*00000007018~
N3*5324 ELM~
N4*STURGIS*MI*49091~
NM1*PR*2*PROVIDER 1*****PI*13256235~
REF*F8*1253278~
LX*1~
SV2*0100**0*UN*5*0*0~
DTP*472*RD8*20031213-20031218~
SVD*5222312313*0**0100*5~
DTP*573*D8*20040210~
SVD*13256235*0**0100*5~
DTP*573*D8*20040210~
SE*63*300145997~
GE*1*1~
IEA*1*000484889~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000484889",
                    "ta1_req": "0",
                    "orig_date": "040709",
                    "orig_time": "1439",
                    "cur_line": 67,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "1",
                            "fic": "HC",
                            "vriic": "004010X096A1",
                            "ack_code": "A",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 66,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "300145997",
                                    "vriic": None,
                                    "ack_code": "A",
                                    "cur_line": 65,
                                    "errors": [],
                                    "segments": [],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "per_segment_repeat": {
        "res997": """ISA*00*          *00*          *ZZ*RECEIVER       *ZZ*SENDER         *041210*0107*U*00401*412100107*0*P*:~
GS*FA*RECEIVER*SENDER*20041210*010712*56*X*004010~
ST*997*0001~
AK1*HC*56~
AK2*837*000000001~
AK3*PER*7**5~
AK5*R*5~
AK9*R*1*1*0~
SE*7*0001~
GE*1*56~
IEA*1*412100107~""",
        "source": """ISA*03*SENDER    *01*          *ZZ*SENDER         *ZZ*RECEIVER       *040608*1333*U*00401*000000288*0*P*:~
GS*HC*SENDER*RECEIVER*20040608*1333*56*X*004010X098A1~
ST*837*000000001~
BHT*0019*00*289*20040608*1333*CH~
REF*87*004010X098A1~
NM1*41*2*SENDER 1*****46*2309-0923~
PER*IC*Contact Name*TE*111-555-1111~
PER*IC*Contact Name*TE*111-555-1111~
PER*IC*Contact Name*TE*111-555-1111~
NM1*40*2*Payer*****46*21312311~
HL*1**20*1~
NM1*85*2*Biller 1*****XX*2309-2222~
N3*1123 MILL~
N4*VOID*MI*49002~
PER*IC*Contact Name*TE*111-555-2222~
HL*2*1*22*0~
SBR*P*18*******11~
NM1*IL*1*GAIMAN*NEIL*M***MI*101911111~
N3*1123 OAKLAND~
N4*VOID*MI*49001~
DMG*D8*19460101*M~
REF*SY*370600000~
NM1*PR*2*PAYER 1*****PI*44-4444444~
N3*4444 ONE RD~
N4*VOID*MI*49001~
CLM*6643-1019AA*999.6***12::1*Y*A*N*Y*B~
HI*BK:29590~
LX*1~
SV1*HC:H2015*14.84*UN*6***1~
DTP*472*D8*20040501~
REF*6R*AKLKJ124231AD~
SE*30*000000001~
GE*1*56~
IEA*1*000000288~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000000288",
                    "ta1_req": "0",
                    "orig_date": "040608",
                    "orig_time": "1333",
                    "cur_line": 34,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "56",
                            "fic": "HC",
                            "vriic": "004010X098A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 33,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "000000001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 32,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "PER",
                                            "seg_count": 7,
                                            "pos": 45,
                                            "name": "Submitter EDI Contact Information",
                                            "ls_id": None,
                                            "cur_line": 9,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_5_segment_repeat_exceeded",
                                                    "x12_code": "5",
                                                    "err_str": "Segment PER exceeded max count.  Found 3, should have 2",
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "repeat_init_segment": {
        "res997": """ISA*00*          *00*          *ZZ*111111960      *ZZ*111111536      *070829*1105*U*00401*708291105*0*T*:~
GS*FA*111111960*111111536*20070829*110552*1*X*004010~
ST*997*0001~
AK1*HS*1~
AK2*270*0001~
AK5*A~
AK9*A*1*1*1~
SE*6*0001~
GE*1*1~
IEA*1*708291105~""",
        "source": """ISA*00*          *00*          *ZZ*111111536      *ZZ*111111960      *000816*2105*U*00401*000168037*0*T*:~
GS*HS*111111536*111111960*20070816*2105*1*X*004010X092A1~
ST*270*0001~
BHT*0022*13*1764*20070816*2105~
HL*1**20*1~
NM1*PR*2*TEST PAYER*****PI*100111~
HL*2*1*21*1~
NM1*1P*2*test*****SV*111111111~
HL*3*2*22*0~
TRN*1*1764*9174458207*test~
NM1*IL*1*Blok*Ingrid****MI*00111111~
REF*SY*382111111~
DMG*D8*19950111~
DTP*472*D8*20070801~
EQ*30**IND~
EQ*30**CHD~
SE*15*0001~
GE*1*1~
IEA*1*000168037~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000168037",
                    "ta1_req": "0",
                    "orig_date": "000816",
                    "orig_time": "2105",
                    "cur_line": 19,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "1",
                            "fic": "HS",
                            "vriic": "004010X092A1",
                            "ack_code": "A",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 18,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "270",
                                    "trn_set_control_num": "0001",
                                    "vriic": None,
                                    "ack_code": "A",
                                    "cur_line": 17,
                                    "errors": [],
                                    "segments": [],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "simple1": {
        "res997": """ISA*00*          *00*          *ZZ*ZZ001          *ZZ*ZZ000          *040701*1611*U*00401*407011611*0*T*:~
GS*FA*ZZ001*ZZ000*20040701*161145*17*X*004010~
ST*997*0001~
AK1*HC*17~
AK2*837*11280001~
AK3*BHT*1**3~
AK3*HL*1**3~
AK5*R*5~
AK9*R*1*1*0~
SE*8*0001~
GE*1*17~
IEA*1*407011611~""",
        "source": """ISA*00*          *00*          *ZZ*ZZ000          *ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:~
GS*HC*ZZ000*ZZ001*20030828*1128*17*X*004010X098A1~
ST*837*11280001~
SE*2*11280001~
GE*1*17~
IEA*1*000010121~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000010121",
                    "ta1_req": "0",
                    "orig_date": "030828",
                    "orig_time": "1128",
                    "cur_line": 6,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "17",
                            "fic": "HC",
                            "vriic": "004010X098A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 5,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "11280001",
                                    "vriic": None,
                                    "ack_code": "R",
                                    "cur_line": 4,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "BHT",
                                            "seg_count": 1,
                                            "pos": 10,
                                            "name": "Beginning of Hierarchical Transaction",
                                            "ls_id": None,
                                            "cur_line": 4,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Table 1 - Header" (HEADER) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                        {
                                            "seg_id": "HL",
                                            "seg_count": 1,
                                            "pos": 1,
                                            "name": "Billing/Pay-To Provider Hierarchical Level",
                                            "ls_id": None,
                                            "cur_line": 4,
                                            "errors": [
                                                {
                                                    "err_cde": "SEG_3_mandatory_loop_missing",
                                                    "x12_code": "3",
                                                    "err_str": 'Mandatory loop "Billing/Pay-To Provider Hierarchical Level" (2000A) missing',
                                                    "err_val": None,
                                                }
                                            ],
                                            "elements": [],
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "simple_837p": {
        "res997": """ISA*00*          *00*          *ZZ*BBBBBBBBB      *ZZ*AAAAAAAA       *081117*1543*U*00401*811171543*1*P*:~
GS*FA*BBBBBBBBB*AAAA*20081117*154310*1167*X*004010~
ST*997*0001~
AK1*HC*1167~
AK2*837*1179~
AK5*A~
AK9*A*1*1*1~
SE*6*0001~
GE*1*1167~
TA1*000001168*041105*1526*A*000~
IEA*1*811171543~""",
        "source": """ISA*00*          *00*          *ZZ*AAAAAAAA       *ZZ*BBBBBBBBB      *041105*1526*U*00401*000001168*1*P*:~
GS*HC*AAAA*BBBBBBBBB*20041105*1526*1167*X*004010X098A1~
ST*837*1179~
BHT*0019*00*AAAA1179*20041105*1526*RP~
REF*87*004010X098A1~
NM1*41*2*Sender 1*****46*99999~
PER*IC*SUPPORT*EM*Support@dev.null*TE*8005553333~
NM1*40*2*Receiver 1*****46*8888888~
HL*1**20*1~
NM1*85*2*Sender 1*****24*999999999~
N3*399 ELM ROAD~
N4*Kalamazoo*MI*49001~
REF*1D*333402169~
HL*2*1*22*0~
SBR*P*18*******MC~
NM1*IL*1*THE FIFTH*RICHARD****MI*1212121~
N3*156 ELM~
N4*KALAMAZOO*MI*49001~
DMG*D8*19051104*M~
NM1*PR*2*PAYER 1*****PI*8888888~
CLM*3215338*21***12::1*Y*A*Y*A*B~
CN1*05~
HI*BK:317~
NM1*82*2*PROVIDER 1*****24*222185735~
PRV*PE*ZZ*103T00000X~
SBR*P*18***MC****MC~
AMT*B6*0~
DMG*D8*19051104*M~
OI***Y*B**I~
NM1*IL*1*THE FIFTH*RICHARD****MI*0000000004~
N3*156 ELM~
N4*KALAMAZOO*MI*49001~
REF*SY*777777777~
NM1*PR*2*Sender 1S*****PI*12128909~
REF*F8*3215338~
REF*G1*121282~
LX*1~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040407~
REF*6R*1057296~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
LX*2~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040414~
REF*6R*1057297~
AMT*AAE*21~
SVD*174456543*21*HC:H2015:TT**12~
DTP*573*D8*20040929~
CLM*5555*21***12::1*Y*A*Y*A*B~
HI*BK:317~
LX*1~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040407~
REF*6R*1057296~
LX*2~
SV1*HC:H2015:TT*21*UN*12***1~
DTP*472*D8*20040414~
REF*6R*1057297~
LX*3~
SV1*HC:H2017:TT*1*UN*12***1~
DTP*472*D8*20050414~
REF*6R*105797~
SE*63*1179~
GE*1*1167~
IEA*1*000001168~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000001168",
                    "ta1_req": "1",
                    "orig_date": "041105",
                    "orig_time": "1526",
                    "cur_line": 67,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "1167",
                            "fic": "HC",
                            "vriic": "004010X098A1",
                            "ack_code": "A",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 66,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "1179",
                                    "vriic": None,
                                    "ack_code": "A",
                                    "cur_line": 65,
                                    "errors": [],
                                    "segments": [],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "simple_837i": {
        "source": """ISA*00*          *00*          *ZZ*00000AAA       *ZZ*0000BBB        *040709*1439*U*00401*000484889*0*P*:~
GS*HC*0AAA*0BBB*20040709*1439*1*X*004010X096A1~
ST*837*300145997~
BHT*0019*00*300145997*20040709*1439*RP~
REF*87*004010X096A1~
NM1*41*2*PROVIDER 1*****46*0AAA~
PER*IC*HELPDESK*EM*ADMIN@NULL.NULL*TE*8005557444~
NM1*40*2*RECEIVER 1*****46*000111~
HL*1**20*1~
NM1*85*2*PROVIDER 1*****24*555112222~
N3*PROVIDER 1~
N4*THREE RIVERS*MI*49093~
REF*1D*1705555~
HL*2*1*22*0~
SBR*S*18*******11~
NM1*IL*1*ARNOLD*TOM****MI*666333444~
N3*5324 ELM~
N4*STURGIS*MI*49091~
DMG*D8*19270312*M~
REF*SY*666333444~
NM1*PR*2*PAYER 2*****PI*000111~
N3*PO BOX 0000~
N4*KALAMAZOO*MI*48001~
CLM*12522228*0***11:A:7*Y*A*Y*A*********N~
DTP*434*RD8*20031213-20031218~
DTP*435*DT*200312130800~
CL1*9*9*09~
REF*F8*12522228~
HI*BK:29689*BJ:29689~
NM1*71*1*EXTERNAL*PROVIDER*C***34*999999999~
PRV*AT*ZZ*101Y00000X~
REF*0B*9999999~
NM1*FA*2*PROVIDER 1~
PRV*RP*ZZ*101Y00000X~
N3*PROVIDER 1~
N4*THREE RIVERS*MI*49093~
SBR*T*18**PAYER A*****11~
AMT*B6*605.0000~
AMT*C4*0~
DMG*D8*19570312*M~
OI***Y***I~
NM1*IL*1*ARNOLD*TOM****MI*00000007018~
N3*5324 ELM~
N4*STURGIS*MI*49091~
NM1*PR*2*PAYER A*****PI*552312313~
DTP*573*D8*20040210~
REF*F8*1253278~
SBR*P*18**PROVIDER 1*****11~
AMT*B6*605.0000~
AMT*C4*0~
DMG*D8*19570312*M~
OI***Y***I~
NM1*IL*1*ARNOLD*TOM****MI*00000007018~
N3*5324 ELM~
N4*STURGIS*MI*49091~
NM1*PR*2*PROVIDER 1*****PI*13256235~
REF*F8*1253278~
LX*1~
SV2*0100**0*UN*5*0*0~
DTP*472*RD8*20031213-20031218~
SVD*5222312313*0**0100*5~
DTP*573*D8*20040210~
SVD*13256235*0**0100*5~
DTP*573*D8*20040210~
LX*2~
SV2*0101**0*UN*5*0*0~
DTP*472*RD8*20031214-20031218~
SVD*5222312313*0**0100*5~
DTP*573*D8*20040210~
SVD*13256235*0**0100*5~
DTP*573*D8*20040210~
LX*3~
SV2*0102**0*UN*5*0*0~
DTP*472*RD8*20031212-20031218~
SVD*5222312313*0**0100*5~
DTP*573*D8*20040210~
SVD*13256235*0**0100*5~
DTP*573*D8*20040210~
CLM*12522229*0***11:A:7*Y*A*Y*A*********N~
DTP*434*RD8*20031213-20031218~
DTP*435*DT*200312130800~
CL1*9*9*09~
REF*F8*12522228~
HI*BK:29689*BJ:29689~
NM1*71*1*EXTERNAL*PROVIDER*C***34*999999999~
PRV*AT*ZZ*101Y00000X~
REF*0B*9999999~
NM1*FA*2*PROVIDER 1~
PRV*RP*ZZ*101Y00000X~
N3*PROVIDER 1~
N4*THREE RIVERS*MI*49093~
SBR*T*18**PAYER A*****11~
AMT*B6*605.0000~
AMT*C4*0~
DMG*D8*19570312*M~
OI***Y***I~
NM1*IL*1*ARNOLD*TOM****MI*00000007018~
N3*5324 ELM~
N4*STURGIS*MI*49091~
NM1*PR*2*PAYER A*****PI*552312313~
DTP*573*D8*20040210~
REF*F8*1253278~
SBR*P*18**PROVIDER 1*****11~
AMT*B6*605.0000~
AMT*C4*0~
DMG*D8*19570312*M~
OI***Y***I~
NM1*IL*1*ARNOLD*TOM****MI*00000007018~
N3*5324 ELM~
N4*STURGIS*MI*49091~
NM1*PR*2*PROVIDER 1*****PI*13256235~
REF*F8*1253278~
LX*1~
SV2*0103**0*UN*5*0*0~
DTP*472*RD8*20031213-20031218~
SVD*5222312313*0**0100*5~
DTP*573*D8*20040210~
SVD*13256235*0**0100*5~
DTP*573*D8*20040210~
LX*2~
SV2*0104**0*UN*5*0*0~
DTP*472*RD8*20031214-20031218~
SVD*5222312313*0**0100*5~
DTP*573*D8*20040210~
SVD*13256235*0**0100*5~
DTP*573*D8*20040210~
LX*3~
SV2*0105**0*UN*5*0*0~
DTP*472*RD8*20031212-20031218~
SVD*5222312313*0**0100*5~
DTP*573*D8*20040210~
SVD*13256235*0**0100*5~
DTP*573*D8*20040210~
SE*132*300145997~
GE*1*1~
IEA*1*000484889~""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000484889",
                    "ta1_req": "0",
                    "orig_date": "040709",
                    "orig_time": "1439",
                    "cur_line": 136,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "1",
                            "fic": "HC",
                            "vriic": "004010X096A1",
                            "ack_code": "A",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 135,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "837",
                                    "trn_set_control_num": "300145997",
                                    "vriic": None,
                                    "ack_code": "A",
                                    "cur_line": 134,
                                    "errors": [],
                                    "segments": [],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "834_lui_id_5010": {
        "source": """ISA*00*          *00*          *ZZ*D00XXX         *ZZ*00AA           *070305*1832*U*00501*000701336*0*P*:~
GS*BE*D00XXX*00AA*20070305*1832*13360001*X*005010X220A1~
ST*834*0001*005010X220A1~
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
""",
        "resAck": """ISA*00*          *00*          *ZZ*00GR           *ZZ*D00111         *070320*1721*U*00501*703201721*0*P*:~
GS*FA*00GR*D00111*20070320*172121*13360001*X*005010X231~
ST*997*0001*005010X231~
AK1*BE*13360001*005010X220A1~
AK2*834*0001*005010X220A1~
IK5*A~
AK9*A*1*1*1~
SE*6*0001~
GE*1*13360001~
IEA*1*703201721~
""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000701336",
                    "ta1_req": "0",
                    "orig_date": "070305",
                    "orig_time": "1832",
                    "cur_line": 24,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "13360001",
                            "fic": "BE",
                            "vriic": "005010X220A1",
                            "ack_code": "A",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 23,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "834",
                                    "trn_set_control_num": "0001",
                                    "vriic": "005010X220A1",
                                    "ack_code": "A",
                                    "cur_line": 22,
                                    "errors": [],
                                    "segments": [],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "834_lui_id_5010_non_ascii": {
        # Variant of 834_lui_id_5010 with a non-ASCII char (`é`, 0xE9 in
        # latin-1) embedded in REF02. Demonstrates two things end-to-end:
        # (a) the parser tolerates non-ASCII bytes (issue #157, #173);
        # (b) the validator flags the bad char with err_cde "6" via the
        #     rec_ID_B regex; and
        # (c) the 999 output sanitizes the bad_value when copying it into
        #     IK4-04 — `00389é999` becomes `00389?999` so the ack stays
        #     pure ASCII per X12 spec.
        # The JSON output preserves the original codepoint in err_str /
        # err_val (JSON is unicode-safe, full fidelity is useful).
        "source": """ISA*00*          *00*          *ZZ*D00XXX         *ZZ*00AA           *070305*1832*U*00501*000701336*0*P*:~
GS*BE*D00XXX*00AA*20070305*1832*13360001*X*005010X220A1~
ST*834*0001*005010X220A1~
BGN*00*88880070301  00*20070305*181245****4~
DTP*007*D8*20070301~
N1*P5*PAYER 1*FI*999999999~
N1*IN*KCMHSAS*FI*999999999~
INS*Y*18*030*XN*A*C**FT~
REF*0F*00389\xe9999~
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
""",
        "resAck": """ISA*00*          *00*          *ZZ*00GR           *ZZ*D00111         *070320*1721*U*00501*703201721*0*P*:~
GS*FA*00GR*D00111*20070320*172121*13360001*X*005010X231~
ST*999*0001*005010X231~
AK1*BE*13360001*005010X220A1~
AK2*834*0001*005010X220A1~
IK3*REF*7**8~
IK4*2*127*6*00389?999~
IK5*R*5~
AK9*R*1*1*0~
SE*8*0001~
GE*1*703201721~
IEA*1*703201721~
""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000701336",
                    "ta1_req": "0",
                    "orig_date": "070305",
                    "orig_time": "1832",
                    "cur_line": 24,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "13360001",
                            "fic": "BE",
                            "vriic": "005010X220A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 23,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "834",
                                    "trn_set_control_num": "0001",
                                    "vriic": "005010X220A1",
                                    "ack_code": "R",
                                    "cur_line": 22,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "REF",
                                            "seg_count": 7,
                                            "pos": 200,
                                            "name": "Subscriber Identifier",
                                            "ls_id": None,
                                            "cur_line": 9,
                                            "errors": [],
                                            "elements": [
                                                {
                                                    "ele_pos": 2,
                                                    "subele_pos": None,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "127",
                                                    "name": "Subscriber Identifier",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_6_invalid_type_char",
                                                            "x12_code": "6",
                                                            "err_str": 'Data element "Subscriber Identifier" (REF02) is type AN, contains an invalid character(00389é999)',
                                                            "err_val": "00389é999",
                                                        }
                                                    ],
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
    "834_eol_in_element": {
        "source": """ISA*00*          *00*          *ZZ*D00XXX         *ZZ*00AA           *070305*1832*U*00501*000701336*0*P*:~
GS*BE*D00XXX*00AA*20070305*1832*13360001*X*005010X220A1~
ST*834*0001*005010X220A1~
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
N3*777 ELM ST
APT 55~
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
""",
        "resAck": """ISA*00*          *00*          *ZZ*00AA           *ZZ*D00XXX         *131107*1503*^*00501*311071503*0*P*:~
GS*FA*00AA*D00XXX*20131107*150355*608852007*X*005010X231~
ST*999*0001*005010X231~
AK1*BE*13360001*005010X220A1~
AK2*834*0001*005010X220A1~
IK3*N3*12**8~
IK4*1*166*6*<LF>~
IK5*R*5~
AK9*R*1*1*0~
SE*8*0001~
GE*1*608852007~
IEA*1*311071503~
""",
        "resJson": {
            "interchanges": [
                {
                    "isa_trn_set_id": "000701336",
                    "ta1_req": "0",
                    "orig_date": "070305",
                    "orig_time": "1832",
                    "cur_line": 24,
                    "errors": [],
                    "groups": [
                        {
                            "gs_control_num": "13360001",
                            "fic": "BE",
                            "vriic": "005010X220A1",
                            "ack_code": "R",
                            "st_count_orig": 1,
                            "st_count_recv": 1,
                            "cur_line": 23,
                            "errors": [],
                            "transactions": [
                                {
                                    "trn_set_id": "834",
                                    "trn_set_control_num": "0001",
                                    "vriic": "005010X220A1",
                                    "ack_code": "R",
                                    "cur_line": 22,
                                    "errors": [],
                                    "segments": [
                                        {
                                            "seg_id": "N3",
                                            "seg_count": 12,
                                            "pos": 500,
                                            "name": "Member Residence Street Address",
                                            "ls_id": None,
                                            "cur_line": 14,
                                            "errors": [],
                                            "elements": [
                                                {
                                                    "ele_pos": 1,
                                                    "subele_pos": None,
                                                    "repeat_pos": None,
                                                    "ele_ref_num": "166",
                                                    "name": "Member Address Line",
                                                    "errors": [
                                                        {
                                                            "err_cde": "ELE_6_control_char",
                                                            "x12_code": "6",
                                                            "err_str": 'Data element "Member Address Line" (N301), contains an invalid control character(<LF>)',
                                                            "err_val": "<LF>",
                                                        }
                                                    ],
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    },
}

if __name__ == "__main__":
    import os.path

    for k in datafiles:
        if "source" in datafiles[k]:
            with open(os.path.join("files", k + ".txt"), "w") as f:
                f.write(datafiles[k]["source"])
