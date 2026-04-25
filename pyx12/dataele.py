######################################################################
# Copyright (c) 2001-2019
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Interface to normalized Data Elements
"""

import os.path
import logging
import defusedxml.ElementTree as et
from importlib.resources import files as _res_files

# Intrapackage imports
from pyx12.errors import EngineError

class DataElementsError(Exception):
    """Class for data elements module errors."""

class DataElements:
    """
    Interface to normalized Data Elements
    """

    def __init__(self, base_path=None):
        """
        Initialize the list of data elements
        :param base_path: Override directory containing dataele.xml.  If None,
            uses package resource folder
        :type base_path: string

        Note: self.dataele - map to the data element
        {ele_num: {data_type, min_len, max_len, name}}
        """
        logger = logging.getLogger('pyx12')
        self.dataele = {}
        dataele_file = 'dataele.xml'
        if base_path is not None:
            logger.debug(f"Looking for data element definition file '{dataele_file}' in map_path '{base_path}'")
            fd = open(os.path.join(base_path, dataele_file), encoding='utf-8')
        else:
            logger.debug(f"Looking for data element definition file '{dataele_file}' in package resources")
            fd = _res_files('pyx12').joinpath('map', dataele_file).open('rb')
        with fd:
            parser = et.XMLParser(encoding='utf-8')
            for eElem in et.parse(fd, parser=parser).iter('data_ele'):
                ele_num = eElem.get('ele_num')
                self.dataele[ele_num] = {
                    'data_type': eElem.get('data_type'),
                    'min_len': int(eElem.get('min_len')),
                    'max_len': int(eElem.get('max_len')),
                    'name': eElem.get('name'),
                }

    def get_by_elem_num(self, ele_num):
        """
        Get the element characteristics for the indexed element code
        :param ele_num: the data element code
        :type ele_num: string
        :return: {data_type, min_len, max_len, name}
        :rtype: dict
        """
        if not ele_num:
            raise EngineError(f'Bad data element {ele_num!r}')
        if ele_num not in self.dataele:
            raise EngineError(f'Data Element "{ele_num}" is not defined')
        return self.dataele[ele_num]

    def __repr__(self):
        for ele_num in self.dataele:
            print((self.dataele[ele_num]))

    def debug_print(self):
        """
        Debug print data elements
        """
        self.__repr__()
