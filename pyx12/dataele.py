######################################################################
# Copyright (c) 2001-2007 Kalamazoo Community Mental Health Services,
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
#import sys
#import re
import cPickle
import libxml2
from stat import ST_MTIME

# Intrapackage imports
from pyx12.errors import EngineError, XML_Reader_Error

class DataElementsError(Exception):
    """Class for data elements module errors."""

NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3, \
    'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8, \
    'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12}

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
        {ele_num: (data_type, min_len, max_len, name)}
        """
        
        self.dataele = {} 
        code_file = os.path.join(base_path, 'dataele.xml')
        pickle_file = '%s.%s' % (os.path.splitext(code_file)[0], 'pkl')
        
        ele_num = None
        data_type = None
        min_len = None
        max_len = None
        name = None
        # init the map of dataele from the pickled file dataele.pkl
        try:
            if os.stat(code_file)[ST_MTIME] < os.stat(pickle_file)[ST_MTIME]:
                self.dataele = cPickle.load(open(pickle_file))
            else: 
                raise DataElementsError, "reload data elements"
        except:
            try:
                reader = libxml2.newTextReaderFilename(code_file)
            except:
                raise EngineError, 'Data Element file not found: %s' % (code_file)
            try:
                ret = reader.Read()
                if ret == -1:
                    raise XML_Reader_Error, 'Read Error'
                elif ret == 0:
                    raise XML_Reader_Error, 'End of Map File'
                while ret == 1:
                    if reader.NodeType() == NodeType['element_start']:
                        cur_name = reader.Name()
                        if cur_name == 'data_ele':
                            while reader.MoveToNextAttribute():
                                if reader.Name() == 'ele_num':
                                    ele_num = reader.Value()
                                elif reader.Name() == 'data_type':
                                   data_type = reader.Value()
                                elif reader.Name() == 'min_len':
                                   min_len = int(reader.Value())
                                elif reader.Name() == 'max_len':
                                   max_len = int(reader.Value())
                                elif reader.Name() == 'name':
                                   name = reader.Value()
                            if ele_num is None or data_type is None or \
                                    min_len is None or max_len is None or \
                                    name is None:
                                raise EngineError, 'Invalid Data Element %s' \
                                    % (ele_num)
                            self.dataele[ele_num] = (data_type, min_len, max_len) #, name)
                    elif reader.NodeType() == NodeType['element_end']:
                        if cur_name == 'data_ele':
                            ele_num = None
                            data_type = None
                            min_len = None
                            max_len = None
                            name = None
                    ret = reader.Read()
                    if ret == -1:
                        raise XML_Reader_Error, 'Read Error'
                    elif ret == 0:
                        raise XML_Reader_Error, 'End of Map File'
            except XML_Reader_Error:
                pass


    def get_by_elem_num(self, ele_num):
        """
        Get the element characteristics for the indexed element code
        @param ele_num: the data element code
        @type ele_num: string
        @return: (data_type, min_len, max_len)
        @rtype: (string, int, int)
        """
        if not ele_num:
            raise EngineError, 'Bad data element %s' % (ele_num)
        if not self.dataele.has_key(ele_num):
            raise EngineError, 'Data Element "%s" is not defined' \
                % (ele_num)
        #data_type = self.dataele[ele_num][0]
        #min_len = self.dataele[ele_num][1]
        #max_len = self.dataele[ele_num][2]
        # name = self.dataele[ele_num][3]
        return self.dataele[ele_num]

    def __repr__(self):
        for ele_num in self.dataele.keys():
            print self.dataele[ele_num]

    def debug_print(self):
        self.__repr__()
