######################################################################
# Copyright (c) 
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

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

from pyx12.errors import X12PathError


class X12Path(object):
    """
    Interface to an x12 path
    """

    re_seg_id = '(?P<seg_id>[A-Z][A-Z0-9]{1,2})?'
    re_id_val = '(\[(?P<id_val>[A-Z0-9]+)\])?'
    re_ele_idx = '(?P<ele_idx>[0-9]{2})?'
    re_subele_idx = '(-(?P<subele_idx>[0-9]+))?'
    re_str = '^%s%s%s%s$' % (re_seg_id, re_id_val, re_ele_idx, re_subele_idx)
    rec_path = re.compile(re_str, re.S)

    def __init__(self, path_str):
        """
        @param path_str:
        @type path_str: string

        """
        #self.loop_list =
        self.seg_id = None
        self.id_val = None
        self.ele_idx = None
        self.subele_idx = None
        self.relative = None
        self.loop_list = []
        if path_str == '':
            self.relative = True
            return
        if path_str[0] == '/':
            self.relative = False
            self.loop_list = path_str[1:].split('/')
            #self.loop_list = [x for x in path_str[1:].split('/') if x != '']
        else:
            self.relative = True
            self.loop_list = path_str.split('/') 
            #self.loop_list = [x for x in path_str.split('/') if x != '']
        if len(self.loop_list) == 0:
            return
        if len(self.loop_list) > 0 and self.loop_list[-1] == '':
            # Ended in a /, so no segment
            del self.loop_list[-1]
            return
        if len(self.loop_list) > 0:
            seg_str = self.loop_list[-1]
            m = X12Path.rec_path.search(seg_str)
            if m is not None:
                self.seg_id = m.group('seg_id')
                self.id_val = m.group('id_val')
                if m.group('ele_idx') is not None:
                    self.ele_idx = int(m.group('ele_idx'))
                if m.group('subele_idx') is not None:
                    self.subele_idx = int(m.group('subele_idx'))
                del self.loop_list[-1]
                if self.seg_id is None and self.id_val is not None:
                    raise X12PathError('Path "%s" is invalid. Must specify a segment identifier with a qualifier' % (path_str))
                if self.seg_id is None and (self.ele_idx is not None or self.subele_idx is not None) and len(self.loop_list) > 0:
                    raise X12PathError('Path "%s" is invalid. Must specify a segment identifier' % (path_str))

    def is_match(self, path_str):
        pass

    def empty(self):
        """
        Is the path empty?
        @return: True if contains no path data
        @rtype: boolean
        """
        return self.relative is True and len(self.loop_list) == 0 and self.seg_id is None and self.ele_idx is None

    def _is_child_path(self, root_path, child_path):
        """
        Is the child path really a child of the root path?
        @type root_path: string
        @type child_path: string
        @return: True if a child
        @rtype: boolean
        """
        root = root_path.split('/')
        child = child_path.split('/')
        if len(root) >= len(child):
            return False
        for i in range(len(root)):
            if root[i] != child[i]:
                return False
        return True

    def __eq__(self, other):
        if isinstance(other, X12Path):
            return self.loop_list == other.loop_list and self.seg_id == other.seg_id \
                and self.id_val == other.id_val and self.ele_idx == other.ele_idx \
                and self.subele_idx == other.subele_idx and self.relative == other.relative
        return NotImplemented

    def __ne__(self, other):
        res = type(self).__eq__(self, other)
        if res is NotImplemented:
            return res
        return not res

    def __lt__(self, other):
        return NotImplemented

    __le__ = __lt__
    __le__ = __lt__
    __gt__ = __lt__
    __ge__ = __lt__

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
        if self.seg_id and ret != '' and ret != '/':
            ret += '/'
        ret += self.format_refdes()
        return ret

    def __hash__(self):
        return self.__repr__().__hash__()

    def format(self):
        """
        @rtype: string
        """
        return self.__repr__()

    def format_refdes(self):
        ret = ''
        if self.seg_id:
            ret += self.seg_id
            if self.id_val:
                ret += '[%s]' % self.id_val
        if self.ele_idx:
            ret += '%02i' % (self.ele_idx)
            if self.subele_idx:
                ret += '-%i' % self.subele_idx
        return ret

    def is_child_path(self, child_path):
        """
        Is the child path a child of this path?
        @type child_path: string
        @return: True if a child
        @rtype: boolean
        """
        root = self.format().split('/')
        child = child_path.split('/')
        if len(root) >= len(child):
            return False
        for i in range(len(root)):
            if root[i] != child[i]:
                return False
        return True
