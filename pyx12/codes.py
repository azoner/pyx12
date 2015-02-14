######################################################################
# Copyright 
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
External Codes interface
"""

import os.path
import logging
from pkg_resources import resource_stream
import xml.etree.cElementTree as et

# Intrapackage imports
from pyx12.errors import EngineError


class CodesError(Exception):
    """Class for code modules errors."""


class ExternalCodes(object):
    """
    Validates an ID against an external list of codes
    """

    def __init__(self, base_path=None, exclude=None):
        """
        Initialize the external list of codes
        @param base_path: Override directory containing codes.xml.  If None,
            uses package resource folder
        @type base_path: string
        @param exclude: comma separated string of external codes to ignore
        @type exclude: string

        @note: self.codes - map of a tuple of two dates and a list of codes
        {codeset_id: (eff_dte, exp_dte, [code_values])}
        """
        logger = logging.getLogger('pyx12')
        self.codes = {}
        codes_file = 'codes.xml'
        if base_path is not None:
            logger.debug("Looking for codes file '{}' in map_path '{}'".format(codes_file, base_path))
            code_fd = open(os.path.join(base_path, codes_file))
        else:
            logger.debug("Looking for codes file '{}' in pkg_resources".format(codes_file))
            code_fd = resource_stream(__name__, os.path.join('map', codes_file))

        self.exclude_list = exclude.split(',') if exclude is not None else []

        for cElem in et.parse(code_fd).iter('codeset'):
            codeset_id = cElem.findtext('id')
            name = cElem.findtext('name')
            data_ele = cElem.findtext('data_ele')
            codes = []
            for code in cElem.iterfind('version/code'):
                codes.append(code.text)
            self.codes[codeset_id] = {'name': name, 'dataele':
                                      data_ele, 'codes': codes}


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
            raise EngineError('bad key %s' % (key))
        #check the code against the list indexed by key
        else:
            if key in self.exclude_list:
                return True
            if key not in self.codes:
                raise EngineError('External Code "%s" is not defined' % (key))
            if code in self.codes[key]['codes']:
                return True
        return False


    def debug_print(self, count=10):
        """
        Debug print first <count> codes
        """
        for key in list(self.codes.keys()):
            print((self.codes[key][:count]))
