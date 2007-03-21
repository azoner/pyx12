######################################################################
# Copyright (c) 2001-2007 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id: codes.py 896 2006-02-09 22:23:38Z johnholland $

"""
Interface to normalized Data Elements

Validates element values based on data element number

Check length, charset, invalid characters for type, 
valid dates and times.
"""

import os, os.path
#import sys
import re
import cPickle
import libxml2
from stat import ST_MTIME
from types import StringType

# Intrapackage imports
from pyx12.errors import EngineError, XML_Reader_Error, IsValidError

class DataElementsError(Exception):
    """Class for data elements module errors."""

NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3, \
    'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8, \
    'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12}


class DataElements(object):
    """
    Validates by the data element number
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
        code_file = base_path + '/dataele.xml'
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
                            self.dataele[ele_num] = (data_type, min_len, max_len, name)
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
        self.rec_N = re.compile("^-?[0-9]+", re.S)
        self.rec_R = re.compile("^-?[0-9]*(\.[0-9]+)?", re.S)
        self.rec_ID_E = re.compile("[^A-Z0-9!\"&'()*+,\-\\\./:;?=\sa-z%~@\[\]_{}\\\|<>#$\s]", re.S)
        self.rec_ID_B = re.compile("[^A-Z0-9!\"&'()*+,\-\\\./:;?=\s]", re.S)
        self.rec_DT = re.compile("[^0-9]+", re.S)
        self.rec_TM = re.compile("[^0-9]+", re.S)

    def __match_re(self, short_data_type, val):
        """
        @param short_data_type: simplified data type
        @type short_data_type: string
        @param val: data value to be verified
        @type val: string
        @param charset: [optional] - 'B' for Basic X12 character set, 'E' for extended
        @type charset: string
        @return: True if matched, False if not
        @rtype: boolean
        """
        if short_data_type == 'N':
            rec = self.rec_N
        elif short_data_type == 'R':
            rec = self.rec_R
        else:
            raise EngineError, 'Unknown data type %s' % (short_data_type)
        m = rec.search(val)
        if not m:
            return False
        if m.group(0) != val:  # matched substring != original, bad
            return False # nothing matched
        return True
 
    def __not_match_re(self, short_data_type, val, charset = 'B'):
        """
        @param short_data_type: simplified data type
        @type short_data_type: string
        @param val: data value to be verified
        @type val: string
        @param charset: [optional] - 'B' for Basic X12 character set, 'E' for extended
        @type charset: string
        @return: True if found invalid characters, False if none
        @rtype: boolean
        """
        if short_data_type in ('ID', 'AN'):
            if charset == 'E':  # extended charset
                rec = self.rec_ID_E
            elif charset == 'B':  # basic charset:
                rec = self.rec_ID_B
        elif short_data_type == 'DT':
            rec = self.rec_DT
        elif short_data_type == 'TM':
            rec = self.rec_TM
        else:
            raise EngineError, 'Unknown data type %s' % (short_data_type)
        m = rec.search(val)
        if m and m.group(0):
            return True # Invalid char matched
        return False

    def __is_valid_date(self, data_type, val):
        """
        @param data_type: Date type
        @type data_type: string
        @param val: data value to be verified
        @type val: string
        """
        if data_type == 'D8' and len(val) != 8:
            raise IsValidError
        if data_type == 'D6' and len(val) != 6:
            raise IsValidError
        self.__not_match_re('DT', val)
        if len(val) in (6, 8, 12): # valid lengths for date
            try:
                if 6 == len(val):  # if 2 digit year, add CC
                    if val[0:2] < 50:
                        val = '20' + val
                    else:
                        val = '19' + val
                month = int(val[4:6])  # check month
                if month < 1 or month > 12:
                    raise IsValidError
                day = int(val[6:8])  # check day
                if month in (1, 3, 5, 7, 8, 10, 12):  # 31 day month
                    if day < 1 or day > 31:
                        raise IsValidError
                elif month in (4, 6, 9, 11):  # 30 day month
                    if day < 1 or day > 30:
                        raise IsValidError
                else: # else 28 day
                    year = int(val[0:4])  # get year
                    if not year%4 and not (not year%100 and year%400):
                    #if not (year % 4) and ((year % 100) or (not (year % 400)) ):  # leap year
                        if day < 1 or day > 29:
                            raise IsValidError
                    elif day < 1 or day > 28:
                        raise IsValidError
                if len(val) == 12:
                    if not self.__is_valid_time(val[8:12]):
                        raise IsValidError
            except TypeError:
                raise IsValidError
        else:
            raise IsValidError

    def __is_valid_time(self, val):
        """
        @param val: time value to be verified
        @type val: string
        """
        self.__not_match_re('TM', val)
        if val[0:2] > '23' or val[2:4] > '59':  # check hour, minute segment
            raise IsValidError
        elif len(val) > 4:  # time contains seconds
            if len(val) < 6:  # length is munted
                raise IsValidError
            elif val[4:6] > '59':  # check seconds
                raise IsValidError
            # check decimal seconds here in the future
            elif len(val) > 8:
                # print 'unhandled decimal seconds encountered'
                raise IsValidError
        return True

    def isValid(self, ele_num, val, charset = 'B'):
        """
        Is the value valid based on the data element number
        @param ele_num: the data element number
        @type ele_num: string
        @param val: data value to be verified
        @type val: string
        @param charset: [optional] - 'B' for Basic X12 character set, 'E' for extended
        @type charset: string
        @return: True if value is valid, False if not
        @rtype: boolean
        """
        if not ele_num:
            raise EngineError, 'bad data element %s' % (ele_num)
        if not self.dataele.has_key(ele_num):
            raise EngineError, 'Data Element "%s" is not defined' \
                % (ele_num)
            data_type = self.dataele[ele_num][0]
            min_len = self.dataele[ele_num][1]
            max_len = self.dataele[ele_num][2]
           # name = self.dataele[ele_num][3]

        if type(val) is not StringType:
            raise EngineError, 'Value is not a string'

        # RE/value checks
        # length checks - min_len, max_len
        try:
            if data_type[0] == 'N':
                if not self.__match_re('N', val):
                    err_str = 'Data element error: (%s) contained invalid characters for element number %s' % (val, 'N')
            elif data_type == 'R':
                if not self.__match_re('R', val):
                    err_str = 'Data element error: (%s) contained invalid characters for element number %s' % (val, 'R')
            elif data_type in ('ID', 'AN'):
                self.__not_match_re('ID', val, charset)
            elif data_type == 'RD8':
                if '-' in val:
                    (start, end) = val.split('-')
                    return self.__is_valid_date('D8', start) and self.__is_valid_date('D8', end)
                else:
                    return False
            elif data_type in ('DT', 'D8', 'D6'):
                self.__is_valid_date(data_type, val)
            elif data_type == 'TM':
                self.__is_valid_time(val)
            elif data_type == 'B':
                pass
            else:
                raise IsValidError, 'Unknown data type %s' % data_type
        except IsValidError:
            return False
        return True

    def __repr__(self):
        for ele_num in self.dataele.keys():
            print self.dataele[ele_num]

    def debug_print(self):
        self.__repr__()
