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
Implements an interface to a x12 segment.

A segment is comprised of a segment identifier and a sequence of elements.
An element can be a simple element or a composite.  A simple element is
treated as a composite element with one sub-element.

All indexing is zero based.
"""
import re

import pyx12.path
from pyx12.errors import EngineError

rec_seg_id = re.compile('^[A-Z][A-Z0-9]{1,2}$', re.S)

class Element(object):
    """
    Holds a simple element, which is just a simple string.
    """

    def __init__(self, ele_str):
        """
        @param ele_str: 1::2
        @type ele_str: string

        """
        self.value = ele_str if ele_str is not None else ''

    def __eq__(self, other):
        if isinstance(other, Element):
            return self.value == other.value
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
    __hash__ = None

    def __len__(self):
        """
        @rtype: int
        """
        return 1

    def __repr__(self):
        """
        @rtype: string
        """
        return self.value

    def format(self):
        """
        @rtype: string
        """
        return self.value

    def get_value(self):
        """
        @rtype: string
        """
        return self.value

    def set_value(self, elem_str):
        """
        @param elem_str: Element string value
        @type elem_str: string
        """
        self.value = elem_str if elem_str is not None else ''

    def is_composite(self):
        """
        @rtype: boolean
        """
        return False

    def is_element(self):
        """
        @rtype: boolean
        """
        return True

    def is_empty(self):
        """
        @rtype: boolean
        """
        if self.value is not None and self.value != '':
            return False
        else:
            return True

    # return ''.join([`num` for num in xrange(loop_count)])
    # def has_invalid_character(self, 

class Composite(object):
    """
    Can be a simple element or a composite.
    A simple element is treated as a composite element with one sub-element.
    """
    # Attributes:

    # Operations
    def __init__(self, ele_str, subele_term=None):
        """
        @type ele_str: string
        @raise EngineError: If a terminator is None and no default
        """
        if subele_term is None or len(subele_term) != 1:
            raise EngineError('The sub-element terminator must be a single character, is %s' % (subele_term))
        self.subele_term = subele_term
        self.subele_term_orig = subele_term
        if ele_str is None:
            raise EngineError('Element string is None')
        members = ele_str.split(self.subele_term)
        self.elements = []
        for elem in members:
            self.elements.append(Element(elem))

    def __eq__(self, other):
        if isinstance(other, Composite):
            if len(self.elements) != len(other.elements):
                return False
            for i in range(len(self.elements)):
                if self.elements[i] != other.elements[i]:
                    return False
            return True
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
    __hash__ = None

    def __getitem__(self, idx):
        """
        returns Element instance for idx
        """
        return self.elements[idx]

    def __setitem__(self, idx, val):
        """
        1 based index
        [0] throws exception
        sets element value for idx
        """
        self.elements[idx] = val

    def __len__(self):
        """
        @rtype: int
        """
        return len(self.elements)

    def __repr__(self):
        """
        @rtype: string
        """
        return self.format(self.subele_term)

    def format(self, subele_term=None):
        """
        Format a composite

        @return: string
        @raise EngineError: If terminator is None and no default
        """
        if subele_term is None:
            subele_term = self.subele_term
        if subele_term is None:
            raise EngineError('subele_term is None')
        for i in range(len(self.elements) - 1, -1, -1):
            if not self.elements[i].is_empty():
                break
        return subele_term.join([Element.__repr__(x) for x in self.elements[:i + 1]])

    def get_value(self):
        """
        Get value of simple element
        """
        if len(self.elements) == 1:
            return self.elements[0].get_value()
        else:
            raise IndexError('value of composite is undefined')

    def set_subele_term(self, subele_term):
        """
        @param subele_term: Sub-element terminator value
        @type subele_term: string
        """
        self.subele_term = subele_term

    def is_composite(self):
        """
        @rtype: boolean
        """
        if len(self.elements) > 1:
            return True
        else:
            return False

    def is_element(self):
        """
        @rtype: boolean
        """
        if len(self.elements) == 1:
            return True
        else:
            return False

    def is_empty(self):
        """
        @rtype: boolean
        """
        for ele in self.elements:
            if not ele.is_empty():
                return False
        return True

    def values_iterator(self):
        for j in range(len(self.elements)):
            if not self.elements[j].is_empty():
                subele_ord = '{comp}'.format(comp=j+1)
                yield (subele_ord, self.elements[j].get_value())


class Segment(object):
    """
    Encapsulates a X12 segment.  Contains composites.
    """
    # Attributes:

    # Operations
    def __init__(self, seg_str, seg_term, ele_term, subele_term, repetition_term='^'):
        """
        """
        self.seg_term = seg_term
        self.seg_term_orig = seg_term
        self.ele_term = ele_term
        self.ele_term_orig = ele_term
        self.subele_term = subele_term
        self.subele_term_orig = subele_term
        self.repetition_term = repetition_term
        self.seg_id = None
        self.elements = []
        if seg_str is None or seg_str == '':
            return
        if seg_str[-1] == seg_term:
            elems = seg_str[:-1].split(self.ele_term)
        else:
            elems = seg_str.split(self.ele_term)
        if elems:
            self.seg_id = elems[0]
        for ele in elems[1:]:
            if self.seg_id == 'ISA':
                #Special handling for ISA segment
                #guarantee subele_term will not be matched
                self.elements.append(Composite(ele, ele_term))
            else:
                self.elements.append(Composite(ele, subele_term))

    def __eq__(self, other):
        if isinstance(other, Segment):
            if self.seg_id != other.seg_id:
                return False
            if len(self.elements) != len(other.elements):
                return False
            for i in range(len(self.elements)):
                if self.elements[i] != other.elements[i]:
                    return False
            return True
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
    __hash__ = None

    def __repr__(self):
        """
        @rtype: string
        """
        return self.format(self.seg_term, self.ele_term, self.subele_term)

    def append(self, val):
        """
        Append a composite to the segment

        @param val: String value of composite
        @type val: string
        """
        self.elements.append(Composite(val, self.subele_term))

    def __len__(self):
        """
        @rtype: int
        """
        return len(self.elements)

    def get_seg_id(self):
        """
        @rtype: string
        """
        return self.seg_id

    def _parse_refdes(self, ref_des):
        """
        Format of ref_des:
            - a simple element: TST02
            - a composite: TST03 where TST03 is a composite
            - a sub-element: TST03-2
            - or any of the above with the segment ID omitted (02, 03, 03-1)

        @param ref_des: X12 Reference Designator
        @type ref_des: string
        @rtype: tuple(ele_idx, subele_idx)
        @raise EngineError: If the given ref_des does not match the segment ID
            or if the indexes are not valid integers
        """
        xp = pyx12.path.X12Path(ref_des)
        if xp.seg_id is not None and xp.seg_id != self.seg_id:
            err_str = 'Invalid Reference Designator: %s, seg_id: %s' \
                % (ref_des, self.seg_id)
            raise EngineError(err_str)
        ele_idx = xp.ele_idx - 1 if xp.ele_idx is not None else None
        comp_idx = xp.subele_idx - 1 if xp.subele_idx is not None else None
        return (ele_idx, comp_idx)

    def get(self, ref_des):
        """
        @param ref_des: X12 Reference Designator
        @type ref_des: string
        @return: Element or Composite
        @rtype: L{segment.Composite}
        @raise IndexError: If ref_des does not contain a valid element index
        """
        (ele_idx, comp_idx) = self._parse_refdes(ref_des)
        if ele_idx is None:
            raise IndexError('{} is not a valid element index'.format(ref_des))
        if ele_idx >= self.__len__():
            return None
        if comp_idx is None:
            return self.elements[ele_idx]
        else:
            if comp_idx >= self.elements[ele_idx].__len__():
                return None
            return self.elements[ele_idx][comp_idx]

    def get_value(self, ref_des):
        """
        @param ref_des: X12 Reference Designator
        @type ref_des: string
        """
        comp1 = self.get(ref_des)
        if comp1 is None:
            return None
        else:
            return comp1.format()

    def get_value_by_ref_des(self, ref_des):
        """
        @param ref_des: X12 Reference Designator
        @type ref_des: string
        @attention: Deprecated - use get_value
        """
        raise DeprecationWarning('Use Segment.get_value')

    def set(self, ref_des, val):
        """
        Set the value of an element or subelement identified by the
        Reference Designator

        @param ref_des: X12 Reference Designator
        @type ref_des: string
        @param val: New value
        @type val: string
        """
        (ele_idx, comp_idx) = self._parse_refdes(ref_des)
        while len(self.elements) <= ele_idx:
            # insert blank values before our value if needed
            self.elements.append(Composite('', self.subele_term))
        if self.seg_id == 'ISA' and ele_idx == 15:
            #Special handling for ISA segment
            #guarantee subele_term will not be matched
            self.elements[ele_idx] = Composite(val, self.ele_term)
            return
        if comp_idx is None:
            self.elements[ele_idx] = Composite(val, self.subele_term)
        else:
            while len(self.elements[ele_idx]) <= comp_idx:
                # insert blank values before our value if needed
                self.elements[ele_idx].elements.append(Element(''))
            self.elements[ele_idx][comp_idx] = Element(val)

    def is_element(self, ref_des):
        """
        @param ref_des: X12 Reference Designator
        @type ref_des: string
        """
        ele_idx = self._parse_refdes(ref_des)[0]
        return self.elements[ele_idx].is_element()

    def is_composite(self, ref_des):
        """
        @param ref_des: X12 Reference Designator
        @type ref_des: string
        """
        ele_idx = self._parse_refdes(ref_des)[0]
        return self.elements[ele_idx].is_composite()

    def ele_len(self, ref_des):
        """
        @param ref_des: X12 Reference Designator
        @type ref_des: string
        @return: number of sub-elements in an element or composite
        @rtype: int
        """
        ele_idx = self._parse_refdes(ref_des)[0]
        return len(self.elements[ele_idx])

    def set_seg_term(self, seg_term):
        """
        @param seg_term: Segment terminator
        @type seg_term: string
        """
        self.seg_term = seg_term

    def set_ele_term(self, ele_term):
        """
        @param ele_term: Element terminator
        @type ele_term: string
        """
        self.ele_term = ele_term

    def set_subele_term(self, subele_term):
        """
        @param subele_term: Sub-element terminator
        @type subele_term: string
        """
        self.subele_term = subele_term

    def format(self, seg_term=None, ele_term=None, subele_term=None):
        """
        @rtype: string
        @raise EngineError: If a terminator is None and no default
        """
        if seg_term is None:
            seg_term = self.seg_term
        if ele_term is None:
            ele_term = self.ele_term
        if subele_term is None:
            subele_term = self.subele_term
        if seg_term is None:
            raise EngineError('seg_term is None')
        if ele_term is None:
            raise EngineError('ele_term is None')
        if subele_term is None:
            raise EngineError('subele_term is None')
        str_elems = []
        # get index of last non-empty element
        i = 0
        for i in range(len(self.elements) - 1, -1, -1):
            if not self.elements[i].is_empty():
                break
        for ele in self.elements[:i + 1]:
            str_elems.append(ele.format(subele_term))
        return '%s%s%s%s' % (self.seg_id, ele_term, ele_term.join(str_elems), seg_term)

    def format_ele_list(self, str_elems, subele_term=None):
        """
        Modifies the parameter str_elems
        Strips trailing empty composites
        """
        if subele_term is None:
            subele_term = self.subele_term
        # Find last non-empty composite
        for i in range(len(self.elements) - 1, -1, -1):
            if not self.elements[i].is_empty():
                break
        for ele in self.elements[:i + 1]:
            str_elems.append(ele.format(subele_term))

    def is_empty(self):
        """
        @rtype: boolean
        """
        if len(self.elements) == 0:
            return True
        for ele in self.elements:
            if not ele.is_empty():
                return False
        return True

    def is_seg_id_valid(self):
        """
        Is the Segment identifier valid?
        EBNF: 
        <seg_id> ::= <letter_or_digit> <letter_or_digit> [<letter_or_digit>]
        @rtype: boolean
        """
        if not self.seg_id or len(self.seg_id) < 2 or len(self.seg_id) > 3:
            return False
        else:
            m = rec_seg_id.search(self.seg_id)
            if not m:
                return False # Invalid char matched
        return True

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return Segment(self.format(), self.seg_term, self.ele_term, self.subele_term)

    def values_iterator(self):
        for i in range(len(self.elements)):
            if self.elements[i].is_composite():
                for (comp_ord, val) in self.elements[i].values_iterator():
                    ele_ord = '{idx:0>2}'.format(idx=i+1)
                    refdes = '{segid}{ele_ord}-{comp_ord}'.format(segid=self.seg_id, ele_ord=ele_ord, comp_ord=comp_ord)
                    yield (refdes, ele_ord, comp_ord, val)
            else:
                if not self.elements[i].is_empty():
                    ele_ord = '{idx:0>2}'.format(idx=i+1)
                    refdes = '{segid}{ele_ord}'.format(segid=self.seg_id, ele_ord=ele_ord)
                    yield (refdes, ele_ord, None, self.elements[i].get_value())
