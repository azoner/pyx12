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
X12 data element validation
"""
import re

# Intrapackage imports
from errors import IsValidError, EngineError


def IsValidDataType(str_val, data_type, charset='B', icvn='00401'):
    """
    Is str_val a valid X12 data value

    @param str_val: data value to validate
    @type str_val: string
    @param data_type: X12 data element identifier
    @type data_type: string
    @param charset: [optional] - 'B' for Basic X12 character set, 'E' for extended
    @type charset: string
    @rtype: boolean
    @todo: need to generalize control character validation
    """
    if not data_type:
        return True
    if not isinstance(str_val, str):
        return False

    try:
        if data_type[0] == 'N':
            if not match_re('N', str_val):
                raise IsValidError  # not a number
        elif data_type == 'R':
            if not match_re('R', str_val):
                raise IsValidError  # not a number
        elif data_type in ('ID', 'AN'):
            if not_match_re('ID', str_val, charset, icvn):
                raise IsValidError
        elif data_type == 'RD8':
            if '-' in str_val:
                (start, end) = str_val.split('-')
                return IsValidDataType(start, 'D8', charset) and IsValidDataType(end, 'D8', charset)
            else:
                return False
        elif data_type in ('DT', 'D8', 'D6'):
            if not is_valid_date(data_type, str_val):
                raise IsValidError
        elif data_type == 'TM':
            if not is_valid_time(str_val):
                raise IsValidError
        elif data_type == 'B':
            pass
        else:
            raise IsValidError('Unknown data type %s' % data_type)
    except IsValidError:
        return False
    return True

rec_N = re.compile("^-?[0-9]+", re.S)
rec_R = re.compile("^-?[0-9]*(\.[0-9]+)?", re.S)
rec_ID_E = re.compile(
    "[^A-Z0-9!\"&'()*+,\-\./:;?=\sa-z%~@\[\]_{}\\\|<>#$\s]", re.S)
rec_ID_E5 = re.compile(
    "[^A-Z0-9!\"&'()*+,\-\./:;?=\sa-z%~@\[\]_{}\\\|<>^`#$\s]", re.S)
rec_ID_B = re.compile("[^A-Z0-9!\"&'()*+,\-\./:;?=\s]", re.S)
rec_DT = re.compile("[^0-9]+", re.S)
rec_TM = re.compile("[^0-9]+", re.S)


def match_re(short_data_type, val):
    """
    @param short_data_type: simplified data type
    @type short_data_type: string
    @param val: data value to be verified
    @type val: string
    @return: True if matched, False if not
    @rtype: boolean
    """
    if short_data_type == 'N':
        rec = rec_N
    elif short_data_type == 'R':
        rec = rec_R
    else:
        raise EngineError('Unknown data type %s' % (short_data_type))
    m = rec.search(val)
    if not m:
        return False
    if m.group(0) != val:  # matched substring != original, bad
        return False  # nothing matched
    return True


def not_match_re(short_data_type, val, charset='B', icvn='00401'):
    """
    @param short_data_type: simplified data type
    @type short_data_type: string
    @param val: data value to be verified
    @type val: string
    @param charset: [optional] - 'B' for Basic X12 character set, 'E' for extended, E5 for 5010 Extended
    @type charset: string
    @return: True if found invalid characters, False if none
    @rtype: boolean
    """
    if short_data_type in ('ID', 'AN'):
        if charset == 'E':  # extended charset
            if icvn == '00501':
                rec = rec_ID_E5
            else:
                rec = rec_ID_E
        elif charset == 'B':  # basic charset:
            rec = rec_ID_B
    elif short_data_type == 'DT':
        rec = rec_DT
    elif short_data_type == 'TM':
        rec = rec_TM
    else:
        raise EngineError('Unknown data type %s' % (short_data_type))
    m = rec.search(val)
    if m and m.group(0):
        return True  # Invalid char matched
    return False


def is_valid_date(data_type, val):
    """
    @param data_type: Date type
    @type data_type: string
    @param val: data value to be verified
    @type val: string
    @return: True if valid, False if not
    @rtype: boolean
    """
    try:
        if data_type == 'D8' and len(val) != 8:
            raise IsValidError
        if data_type == 'D6' and len(val) != 6:
            raise IsValidError
        if not_match_re('DT', val):
            raise IsValidError
        if len(val) in (6, 8, 12):  # valid lengths for date
            try:
                if 6 == len(val):  # if 2 digit year, add CC
                    val = '20' + val if val[0:2] < 50 else '19' + val
                year = int(val[0:4])  # get year
                month = int(val[4:6])
                day = int(val[6:8])
                # Should not have dates before 1/1/1800
                if year < 1800:
                    raise IsValidError
                # check month
                if month < 1 or month > 12:
                    raise IsValidError
                if month in (1, 3, 5, 7, 8, 10, 12):  # 31 day month
                    if day < 1 or day > 31:
                        raise IsValidError
                elif month in (4, 6, 9, 11):  # 30 day month
                    if day < 1 or day > 30:
                        raise IsValidError
                else:  # else 28 day
                    if not year % 4 and not (not year % 100 and year % 400):
                    #if not (year % 4) and ((year % 100) or (not (year % 400)) ):  # leap year
                        if day < 1 or day > 29:
                            raise IsValidError
                    elif day < 1 or day > 28:
                        raise IsValidError
                if len(val) == 12:
                    if not is_valid_time(val[8:12]):
                        raise IsValidError
            except TypeError:
                raise IsValidError
        else:
            raise IsValidError
    except IsValidError:
        return False
    return True


def is_valid_time(val):
    """
    @param val: time value to be verified
    @type val: string
    """
    try:
        not_match_re('TM', val)
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
    except IsValidError:
        return False
    return True


def contains_control_character(str_val, charset='B', icvn='00401'):
    if '\n' in str_val:
        return (True, '<LF>')
    if '\r' in str_val:
        return (True, '<CR>')
    return (False, None)
