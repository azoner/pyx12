######################################################################
# Copyright (c) 2005-2009 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Parses an x12 path

An x12 path is comprised of a sequence of loop identifiers, a segment
identifier, and element position, and a composite position.

The last loop id might be a segment id.

/LOOP_1/LOOP_2
/LOOP_1/LOOP_2/SEG
/LOOP_1/LOOP_2/SEG02
/LOOP_1/LOOP_2/SEG[424]02-1
SEG[434]02-1
02-1
02

"""

import re

from pyx12.errors import *

class path(object):
    """
    Interface to an x12 path
    """

    def __init__(self, path_str):
        """
        @param path_str: 
        @type path_str: string
        
        """
        self.loop_list = path_str.split('/')
        self.seg_id = None
        self.id_val = None
        self.ele_idx = None
        self.subele_idx = None

        if len(self.loop_list) == 0:
            return None
        if self.loop_list[0] == '':
            self.relative = False
            del self.loop_list[0]
        else:
            self.relative = True
        if self.loop_list[-1] == '':
            # Ended in a /, so no segment
            del self.loop_list[-1]
        else:
            seg_str = self.loop_list[-1]
            re_seg_id = '(?P<seg_id>[A-Z][A-Z0-9]{1,2})?'
            re_id_val = '(\[(?P<id_val>[A-Z0-9]+)\])?'
            re_ele_idx = '(?P<ele_idx>[0-9]{2})?'
            re_subele_idx = '(-(?P<subele_idx>[0-9]+))?'
            re_str = '^%s%s%s%s$' % (re_seg_id, re_id_val, re_ele_idx, re_subele_idx)
            m = re.compile(re_str, re.S).search(seg_str)
            if m is not None:
                self.seg_id = m.group('seg_id')
                self.id_val = m.group('id_val')
                if m.group('ele_idx') is not None:
                    self.ele_idx = int(m.group('ele_idx'))
                if m.group('subele_idx') is not None:
                    self.subele_idx = int(m.group('subele_idx'))
                del self.loop_list[-1]
                if self.seg_id is None and self.id_val is not None:
                    raise X12PathError, 'Path "%s" is invalid. Must specify a segment identifier with a qualifier' % (path_str)
                if self.seg_id is None and (self.ele_idx is not None or self.subele_idx is not None) and len(self.loop_list) > 0:
                    raise X12PathError, 'Path "%s" is invalid. Must specify a segment identifier' % (path_str)
        
    def is_match(self, path_str):
        pass

    def __parse_ele_path(self, ele_str):
        """
        @param ele_str: An element path in the form '03' or '03-5'
        @type ele_str: string
        """
        #m = re.compile("^-?[0-9]*(\.[0-9]+)?", re.S).search(str_val)
        re_str = '^(?P<seg_id>[A-Z][A-Z0-9]{1,2})(?P<ele_idx>[0-9]{2})?(-(?P<subele_idx>[0-9]+))?$'
        m = re.compile(re_str, re.S).search(ele_str)
        if not m:
            raise IsValidError # nothing matched
        #if m.group(0) != ele_str:  # matched substring != original, bad

        if ele_str.find('-') != -1:
            ele_idx = ele_str[:ele_str.find('-')]
            subele_idx = ele_str[ele_str.find('-')+1:]
        else:
            ele_idx = ele_str
            subele_idx = None
        try:
            a = int(ele_idx)
        except:
            raise EngineError, 'Invalid element path: %s' % (ele_str)
        try:
            if subele_idx is not None:
                a = int(subele_idx)
        except:
            raise EngineError, 'Invalid element path: %s' % (ele_str)
        if len(ele_idx) != 2:
            raise EngineError, 'Invalid element path: %s' % (ele_str)
        return (ele_idx, subele_idx)
        
#    def __len__(self):
#        """
#        @rtype: int
#        """
#        return 1

    def __repr__(self):
        """
        @return: Formatted path
        @rtype: string
        """
        ret = ''
        if not self.relative: 
            ret += '/'
        ret += '/'.join(self.loop_list)
        if self.seg_id:
            if ret != '':
                ret += '/'
            ret += self.seg_id
            if self.id_val:
                ret += '[%s]' % self.id_val
        if self.ele_idx:
            ret += '%02i' % (self.ele_idx)
            if self.subele_idx:
                ret += '-%i' % self.subele_idx
        return ret

    def format(self):
        """
        @rtype: string
        """
        return self.__repr__()
