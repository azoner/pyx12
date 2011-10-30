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
Interface to normalized Data Elements
"""

import os, os.path
import xml.etree.cElementTree as et

# Intrapackage imports
from pyx12.errors import EngineError

class DataElementsError(Exception):
    """Class for data elements module errors."""

    
class DataElements(object):
    """
    Interface to normalized Data Elements
    """

    def __init__(self, base_path):
        """
        Initialize the list of data elements
        @param base_path: path to dataele.xml
        @type base_path: string

        @note: self.dataele - map to the data element
        {ele_num: {data_type, min_len, max_len, name}}
        """
        
        self.dataele = {} 
        code_file = os.path.join(base_path, 'dataele.xml')
        t = et.parse(code_file)
        for e in t.iter('data_ele'):
            ele_num = e.get('ele_num')
            data_type = e.get('data_type')
            min_len = int(e.get('min_len'))
            max_len = int(e.get('max_len'))
            name = e.get('name')
            self.dataele[ele_num] = {'data_type':data_type, 'min_len':min_len, 'max_len':max_len, 'name':name}

    def get_by_elem_num(self, ele_num):
        """
        Get the element characteristics for the indexed element code
        @param ele_num: the data element code
        @type ele_num: string
        @return: {data_type, min_len, max_len, name}
        @rtype: dict
        """
        if not ele_num:
            raise EngineError, 'Bad data element %s' % (ele_num)
        if not self.dataele.has_key(ele_num):
            raise EngineError, 'Data Element "%s" is not defined' % (ele_num)
        return self.dataele[ele_num]

    def __repr__(self):
        for ele_num in self.dataele.keys():
            print(self.dataele[ele_num])

    def debug_print(self):
        self.__repr__()
