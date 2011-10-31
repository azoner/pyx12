######################################################################
# Copyright (c) 2001-2011 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
External Codes interface
"""

import os, os.path
#import sys
import xml.etree.cElementTree as et
import datetime 

# Intrapackage imports
from pyx12.errors import EngineError, XML_Reader_Error

class CodesError(Exception):
    """Class for code modules errors."""


class ExternalCodes(object):
    """
    Validates an ID against an external list of codes
    """

    def __init__(self, base_path, exclude=None):
        """
        Initialize the external list of codes
        @param base_path: path to codes.xml
        @type base_path: string
        @param exclude: comma separated string of external codes to ignore
        @type exclude: string

        @note: self.codes - map of a tuple of two dates and a list of codes 
        {codeset_id: (eff_dte, exp_dte, [code_values])}
        """
        
        self.codes = {} 
        code_file = base_path + '/codes.xml'
        codeset_id = None
        base_name = None
        
        self.exclude_list = exclude.split(',') if exclude is not None else []

        t = et.parse(code_file)
        for c in t.iter('codeset'):
            codeset_id = c.findtext('id')
            name = c.findtext('name')
            data_ele = c.findtext('data_ele')
            codes = []
            for code in c.iterfind('version/code'):
                codes.append(code.text)
            self.codes[codeset_id] = {'name':name, 'dataele': data_ele, 'codes': codes}

    def isValid(self, key, code, check_dte=None):
        """
        Is the code in the list identified by key
        @param key: the external codeset identifier
        @type key: string
        @param code: code to be verified
        @type code: string
        @param check_dte: deprecated
        @type check_dte: string
        @return: True if code is valid, False if not
        @rtype: boolean
        """
        #if not given a key, do not flag an error
        if not key:
            raise EngineError, 'bad key %s' % (key)
        #check the code against the list indexed by key
        else:
            if key in self.exclude_list:
                return True
            if key not in self.codes:
                raise EngineError, 'External Code "%s" is not defined' % (key)
            if code in self.codes[key]['codes']:
                return True
        return False

    def debug_print(self):
        for key in self.codes.keys():
            print(self.codes[key][:10])

