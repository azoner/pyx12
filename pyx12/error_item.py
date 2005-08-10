######################################################################
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
"""

import errors

class ErrorItem:
    """
    Wrap an X12 validation error
    """
    def __init__(self, err_type, err_cde, err_str, err_val=None, src_line=None):
        """
        @param err_type: At what level did the error occur
        @type err_type: string
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string

        @param 
        @type 
        """
        isa_errors = ('000' ,'001' ,'002' ,'003' ,'004' ,'005' ,'006' ,'007' ,'008' ,
            '009' ,'010' ,'011' ,'012' ,'013' ,'014' ,'015' ,'016' ,
            '017' ,'018' ,'019' ,'020' ,'021' ,'022' ,'023' ,'024' ,
            '025' ,'026' ,'027' ,'028' ,'029' ,'030' ,'031')
        seg_errors = ('1', '2', '3', '4', '5', '6', '7', '8')
        ele_errors = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        if err_type == 'isa' and err_cde not in isa_errors:
            raise error.EngineError, 'Invalid ISA level error code "%s"' % (err_cde) 
        elif err_type in ('gs', 'st', 'seg') and and err_cde not in seg_errors:
            raise error.EngineError, 'Invalid Segment level error code "%s"' % (err_cde) 
        self.err_type = err_type
        self.err_cde = err_cde
        self.err_str = err_str
        self.err_val = err_val
        self.src_line = src_line


    def getErrType(self):
        return self.err_type

    def getErrCde(self):
        return self.err_cde

    def getErrStr(self):
        return self.err_str

    def getErrVal(self):
        return self.err_val

    def getSrcLine(self):
        return self.src_line



