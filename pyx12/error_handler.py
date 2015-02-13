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
Interface to X12 Errors
"""

import logging

# Intrapackage imports
from errors import IterOutOfBounds  # , IterDone

logger = logging.getLogger('pyx12.error_handler')


class err_iter(object):
    """
    Iterate over the error tree

    Implements an odd iterator???
    """

    def __init__(self, errh):
        """
        @param errh: Error_handler instance
        @type errh: L{error_handler.err_handler}
        """
        self.errh = errh
        self.cur_node = errh
        self.visit_stack = []

    def first(self):
        self.cur_node = self.errh

    def next(self):
        self.__next__()

    def __next__(self):
        #If at previosly visited branch, do not do children
        if self.cur_node in self.visit_stack:
            node = None
        else:
            node = self.cur_node.get_first_child()
        if node is not None:
            self.visit_stack.append(self.cur_node)
            self.cur_node = node
        else:
            node = self.cur_node.get_next_sibling()
            if node is not None:
                self.cur_node = node
            else:
                if not self.cur_node.is_closed():
                    raise IterOutOfBounds
                node = self.cur_node.get_parent()
                if node is None:
                    raise IterOutOfBounds
                if not node.is_closed():
                    raise IterOutOfBounds
                if self.cur_node in self.visit_stack:
                    del self.visit_stack[-1]
                self.cur_node = node
                if node.id == 'ROOT':
                    raise IterOutOfBounds
                #    raise IterDone

    def get_cur_node(self):
        return self.cur_node


class err_handler(object):
    """
    The interface to the error handling structures.
    """
    def __init__(self):
        """
        """

        self.id = 'ROOT'
        #self.isa_loop_count = 0
        self.children = []
        self.cur_node = self
        self.cur_isa_node = None
        self.cur_gs_node = None
        self.cur_st_node = None
        self.cur_seg_node = None
        self.seg_node_added = False
        self.cur_ele_node = None
        self.cur_line = 0

    def accept(self, visitor):
        """
        Params:     visitor - ref to visitor class
        """
        visitor.visit_root_pre(self)
        for child in self.children:
            child.accept(visitor)
        visitor.visit_root_post(self)

    def handle_errors(self, err_list):
        """
        @param err_list: list of errors to apply
        """
        for (err_type, err_cde, err_str, err_val, src_line) in err_list:
            if err_type == 'isa':
                self.isa_error(err_cde, err_str)
            elif err_type == 'gs':
                self.gs_error(err_cde, err_str)
            elif err_type == 'st':
                self.st_error(err_cde, err_str)
            elif err_type == 'seg':
                self.seg_error(err_cde, err_str, err_val, src_line)

    def get_cur_line(self):
        """
        @return: Current file line number
        @rtype: int
        """
        return self.cur_line

    def get_id(self):
        """
        """
        return self.id

    def add_isa_loop(self, seg_data, src):
        """
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        """
        #logger.debug('add_isa loop')
        self.children.append(err_isa(self, seg_data, src))
        self.cur_isa_node = self.children[-1]
        self.cur_seg_node = self.cur_isa_node
        self.seg_node_added = True

    def add_gs_loop(self, seg_data, src):
        """
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        """
        #logger.debug('add_gs loop')
        parent = self.cur_isa_node
        parent.children.append(err_gs(parent, seg_data, src))
        self.cur_gs_node = parent.children[-1]
        self.cur_seg_node = self.cur_gs_node
        self.seg_node_added = True

    def add_st_loop(self, seg_data, src):
        """
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        """
        #logger.debug('add_st loop')
        parent = self.cur_gs_node
        parent.children.append(err_st(parent, seg_data, src))
        self.cur_st_node = parent.children[-1]
        self.cur_seg_node = self.cur_st_node
        self.seg_node_added = True

    def add_seg(self, map_node, seg_data, seg_count, cur_line, ls_id):
        """
        @param map_node: current segment node
        @type map_node: L{node<map_if.segment_if>}
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        @param seg_count: Count of current segment in the ST Loop
        @type seg_count: int
        @param cur_line: Current line number in the file
        @type cur_line: int
        @param ls_id: The current LS loop identifier
        @type ls_id: string
        """
        parent = self.cur_st_node
        self.cur_seg_node = err_seg(
            parent, map_node, seg_data, seg_count, cur_line, ls_id)
        self.seg_node_added = False
        #logger.debug('add_seg: %s' % map_node.name)
        #if len(parent.children) > 0:
        #    if parent.children[-1].err_count() == 0:
        #        del parent.children[-1]
        #        logger.debug('del seg_data: %s' % map_node.name)
        #parent.children.append(err_seg(parent, map_node, seg_data, src))

    def _add_cur_seg(self):
        """
        """
        #pdb.set_trace()
        if not self.seg_node_added:
            self.cur_st_node.children.append(self.cur_seg_node)
            self.seg_node_added = True

    def add_ele(self, map_node):
        """
        """
        if self.cur_seg_node.id == 'ISA':
            self.cur_ele_node = err_ele(self.cur_isa_node, map_node)
        elif self.cur_seg_node.id == 'GS':
            self.cur_ele_node = err_ele(self.cur_gs_node, map_node)
        elif self.cur_seg_node.id == 'ST':
            self.cur_ele_node = err_ele(self.cur_st_node, map_node)
        else:
            self.cur_ele_node = err_ele(self.cur_seg_node, map_node)
        self.ele_node_added = False

    def _add_cur_ele(self):
        """
        """
        self._add_cur_seg()
        if not self.ele_node_added and self.cur_seg_node is not None:
            self.cur_seg_node.elements.append(self.cur_ele_node)
            self.ele_node_added = True
        #logger.debug('----  add_ele: %s' % self.cur_seg_node.elements[-1].name)

    def isa_error(self, err_cde, err_str):
        """
        @param err_cde: ISA level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        sout = ''
        sout += 'Line:%i ' % (self.cur_isa_node.get_cur_line())
        sout += 'ISA:%s - %s' % (err_cde, err_str)
        logger.error(sout)
        self.cur_isa_node.add_error(err_cde, err_str)

    def gs_error(self, err_cde, err_str):
        """
        @param err_cde: GS level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        sout = ''
        sout += 'Line:%i ' % (self.cur_gs_node.get_cur_line())
        sout += 'GS:%s - %s' % (err_cde, err_str)
        logger.error(sout)
        self.cur_gs_node.add_error(err_cde, err_str)

    def st_error(self, err_cde, err_str):
        """
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        sout = ''
        sout += 'Line:%i ' % (self.cur_st_node.get_cur_line())
        sout += 'ST:%s - %s' % (err_cde, err_str)
        logger.error(sout)
        self.cur_st_node.add_error(err_cde, err_str)

    def seg_error(self, err_cde, err_str, err_value=None, src_line=None):
        """
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        sout = ''
        try:
            self._add_cur_seg()
            self.cur_seg_node.add_error(err_cde, err_str, err_value)
        except:
            sout += 'No current segment in error_handler. '
        if src_line:
            sout += 'Line:%i ' % (src_line)
        else:
            if self.cur_seg_node is not None:
                sout += 'Line:%i ' % (self.cur_seg_node.get_cur_line())
        sout += 'SEG:%s - %s' % (err_cde, err_str)
        if err_value:
            sout += ' (%s)' % err_value
        logger.error(sout)

    def ele_error(self, err_cde, err_str, bad_value, refdes=None):
        """
        @param err_cde: Element level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self._add_cur_ele()
        self.cur_ele_node.add_error(
            err_cde, err_str, bad_value)  # , pos, data_ele)
        sout = ''
        sout += 'Line:%i ' % (self.cur_seg_node.get_cur_line())
        sout += 'ELE:%s - %s' % (err_cde, err_str)
        if bad_value:
            sout += ' (%s)' % (bad_value)
        logger.error(sout)
        #print self.cur_ele_node.errors

    def close_isa_loop(self, node, seg, src):
        """
        """
        self.cur_isa_node.close(node, seg, src)
        self.cur_seg_node = self.cur_isa_node
        self.seg_node_added = True

    def close_gs_loop(self, node, seg, src):
        """
        """
        self.cur_gs_node.close(node, seg, src)
        self.cur_seg_node = self.cur_gs_node
        self.seg_node_added = True

    def close_st_loop(self, node, seg, src):
        """
        """
        self.cur_st_node.close(node, seg, src)
        self.cur_seg_node = self.cur_st_node
        self.seg_node_added = True

    def find_node(self, type):
        """
        Find the last node of a type
        """
        new_node = self.cur_node
        node_order = {'ROOT': 1, 'ISA': 2, 'GS': 3, 'ST': 4, 'SEG':
                      5, 'ELE': 6}
        while node_order[type] > new_node[new_node.get_id()]:
            new_node = new_node.get_parent()
        #walk error tree to find place to append
        #if type == 'ISA':
        #return node

#    def update_node(self, obj):
#        self.children[-1].update_node(obj)

    def _get_last_child(self):
        """
        """
        if len(self.children) != 0:
            return self.children[-1]
        else:
            return None

    def get_parent(self):
        return None

    def get_error_count(self):
        """
        """
        count = 0
        for child in self.children:
            count += child.get_error_count()
        return count

    def get_first_child(self):
        """
        """
        if len(self.children) > 0:
            return self.children[0]
        else:
            return None

    def get_next_sibling(self):
        """
        """
        return None
        #raise IterDone

    def __next__(self):
        """
        Return the next error node
        """
        for child in self.children:
            yield child

    def is_closed(self):
        """
        @rtype: boolean
        """
        return True

    def __repr__(self):
        """
        """
        return '%i: %s' % (-1, self.id)


class err_node(object):
    def __init__(self, parent):
        """
        """
        self.parent = parent
        self.id = None
        self.children = []
        self.cur_line = -1
        self.errors = []

    def accept(self, visitor):
        """
        """
        pass

#    def update_node(self, obj):
#        pass

    def get_cur_line(self):
        """
        @return: Current file line number
        @rtype: int
        """
        return self.cur_line

    def get_id(self):
        """
        """
        return self.id

    def get_parent(self):
        """
        """
        return self.parent

    def _get_last_child(self):
        """
        """
        if len(self.children) != 0:
            return self.children[-1]
        else:
            return None

    def get_next_sibling(self):
        """
        """
        #if self.id == 'ROOT': raise EngineError
        bFound = False
        for sibling in self.parent.children:
            if bFound:
                return sibling
            if sibling is self:
                bFound = True
        return None
        #raise IterOutOfBounds

    def get_first_child(self):
        """
        """
        if len(self.children) > 0:
            return self.children[0]
        else:
            return None

    def get_error_count(self):
        """
        """
        count = 0
        for child in self.children:
            count += child.get_error_count()
        return count

    def get_error_list(self, seg_id, pre=False):
        """
        """
        return self.errors

    def is_closed(self):
        """
        @rtype: boolean
        """
        return True


class err_isa(err_node):
    """
    Holds source ISA loop errors
    """

    def __init__(self, parent, seg_data, src):
        """
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        @param src: X12file source
        @type src: L{X12file<x12file.X12Reader>}
        """
        self.seg_data = seg_data
        self.isa_id = src.get_isa_id()
        self.cur_line_isa = src.get_cur_line()
        self.cur_line_iea = None

        self.isa_trn_set_id = seg_data.get_value('ISA13')
        self.ta1_req = seg_data.get_value('ISA14')
        self.orig_date = seg_data.get_value('ISA09')
        self.orig_time = seg_data.get_value('ISA10')
        self.id = 'ISA'

        self.parent = parent
        self.children = []
        self.errors = []
        self.elements = []

    def is_closed(self):
        """
        @rtype: boolean
        """
        if self.cur_line_iea:
            return True
        else:
            return False

    def accept(self, visitor):
        """
        Params:     visitor - ref to visitor class
        """
        visitor.visit_isa_pre(self)
        for child in self.children:
            child.accept(visitor)
        visitor.visit_isa_post(self)

    def add_error(self, err_cde, err_str):
        """
        @param err_cde: Error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.errors.append((err_cde, err_str))

    def close(self, node, seg, src):
        self.cur_line_iea = src.get_cur_line()

    def get_cur_line(self):
        """
        @return: Current file line number
        @rtype: int
        """
        if self.cur_line_iea:
            return self.cur_line_iea
        else:
            return self.cur_line_isa

    def get_error_count(self):
        """
        """
        count = 0
        for ele in self.elements:
            count += ele.get_error_count()
        for child in self.children:
            count += child.get_error_count()
        return count + len(self.errors)

    def get_error_list(self, seg_id, pre=False):
        """
        """
        if seg_id == 'ISA':
            return [err for err in self.errors if 'ISA' in err[0]]
        elif seg_id == 'IEA':
            return [err for err in self.errors if 'IEA' in err[0]]
        else:
            return []
        #err_list = []
        #for err in self.errors:
        #    if seg_id in err[0]:
        #        err_list.append(err)
        #return err_list

    def __next__(self):
        """
        Return the next error node
        """
        for child in self.children:
            yield child
        next(self.parent)

    def __repr__(self):
        return '%i: %s' % (self.get_cur_line(), self.id)


class err_gs(err_node):
    """
    Holds source GS loop information
    """

    def __init__(self, parent, seg_data, src):
        """
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        @param src: X12file source
        @type src: L{X12file<x12file.X12Reader>}

        """
        self.seg_data = seg_data
        self.isa_id = src.get_isa_id()
        self.cur_line_gs = src.get_cur_line()
        self.cur_line_ge = None
        self.gs_control_num = src.get_gs_id()
        self.fic = self.seg_data.get_value('GS01')
        self.vriic = self.seg_data.get_value('GS08')
        self.id = 'GS'

        self.st_loops = []

        # From GE loop
        self.ack_code = None  # AK901
        self.st_count_orig = 0  # AK902
        self.st_count_recv = 0  # AK903
        #self.st_count_accept = None # AK904

        self.parent = parent
        self.children = []
        self.errors = []
        self.elements = []

    def accept(self, visitor):
        """
        Params:     visitor - ref to visitor class
        """
        visitor.visit_gs_pre(self)
        for child in self.children:
            child.accept(visitor)
        visitor.visit_gs_post(self)

    def add_error(self, err_cde, err_str):
        """
        @param err_cde: Error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.errors.append((err_cde, err_str))

    def close(self, node, seg_data, src):
        """
        """
        # From GE loop
        self.cur_line_ge = src.get_cur_line()

        self.ack_code = self._get_ack_code()

        if seg_data is None:
            self.st_count_orig = 0
        else:
            self.st_count_orig = int(seg_data.get_value('GE01'))  # AK902
        self.st_count_recv = src.st_count  # AK903
        #self.st_count_accept = self.st_count_recv - len(self.children) # AK904

    def _get_ack_code(self):
        for child in self.children:
            if child.get_error_count() > 0:
                return 'R'
        #err_codes = map(lambda x:x[0], self.errors)
        #if '1' in err_codes: return 'R'
        #elif '2' in err_codes: return 'R'
        #elif '3' in err_codes: return 'R'
        #elif '4' in err_codes: return 'R'
        #elif '5' in err_codes: return 'E'
        #elif '6' in err_codes: return 'E'
        if len(self.errors) > 0:
            return 'R'
        return 'A'

    def count_failed_st(self):
        ct = 0
        for child in self.children:
            if child.ack_code not in ['A', 'E']:
                ct += 1
        return ct

    def get_cur_line(self):
        """
        @return: Current file line number
        @rtype: int
        """
        if self.cur_line_ge:
            return self.cur_line_ge
        else:
            return self.cur_line_gs

    def get_error_count(self):
        """
        """
        count = 0
        for ele in self.elements:
            count += ele.get_error_count()
        for child in self.children:
            count += child.get_error_count()
        return count + len(self.errors)

    def get_error_list(self, seg_id, pre=False):
        """
        """
        if seg_id == 'GS':
            return [err for err in self.errors if err[0] in ('6')]
        elif seg_id == 'GE':
            return [err for err in self.errors if err[0] not in ('6')]
        else:
            return []

    def is_closed(self):
        """
        @rtype: boolean
        """
        if self.cur_line_ge:
            return True
        else:
            return False

    def __next__(self):
        """
        Return the next error node
        """
        for child in self.children:
            yield child
        next(self.parent)

    def __repr__(self):
        return '%i: %s' % (self.get_cur_line(), self.id)


class err_st(err_node):
    """
    ST loops

    Needs:
        1. Transaction set id code (837, 834)
        2. Transaction set control number
        3. trn set error codes
        4. At SE, Determine final ack code
    """

    def __init__(self, parent, seg_data, src):
        """
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        @param src: X12file source
        @type src: L{X12file<x12file.X12Reader>}
        """
        self.seg_data = seg_data
        self.trn_set_control_num = src.get_st_id()
        self.cur_line_st = src.get_cur_line()
        self.cur_line_se = None
        self.trn_set_id = seg_data.get_value('ST01')
        self.vriic = seg_data.get_value('ST03')
        self.id = 'ST'

        self.ack_code = 'R'
        self.parent = parent
        self.children = []
        self.errors = []
        self.elements = []
        #self.rejected = None

    def accept(self, visitor):
        """
        Params:     visitor - ref to visitor class
        """
        visitor.visit_st_pre(self)
        for child in self.children:
            child.accept(visitor)
        visitor.visit_st_post(self)

    def add_error(self, err_cde, err_str):
        """
        @param err_cde: Error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.errors.append((err_cde, err_str))

    def close(self, node, seg_data, src):
        """
        Close ST loop

        @param node: SE node
        @type node: L{node<map_if.x12_node>}
        @param seg_data: Segment object
        @type seg_data: L{segment<segment.Segment>}
        @param src: X12file source
        @type src: L{X12file<x12file.X12Reader>}
        """
        self.cur_line_se = src.get_cur_line()
        #pdb.set_trace()
        if self.err_count() > 0:
            self.ack_code = 'R'
        else:
            self.ack_code = 'A'

    def err_count(self):
        """
        @return: Count of ST/SE loop errors
        @rtype: int
        """
        seg_err_ct = 0
        if self.child_err_count() > 0:
            seg_err_ct = 1
        return len(self.errors) + seg_err_ct

    def get_error_count(self):
        return self.err_count()

    def get_error_list(self, seg_id, pre=False):
        """
        """
        if seg_id == 'ST':
            return [err for err in self.errors if err[0] in ('1', '6', '7', '23')]
        elif seg_id == 'SE':
            return [err for err in self.errors if err[0] not in ('1', '6', '7', '23')]
        else:
            return []

    def child_err_count(self):
        ct = 0
        for child in self.children:
            if child.err_count() > 0:
                ct += 1
        return ct

    def get_cur_line(self):
        """
        @return: Current file line number
        @rtype: int
        """
        if self.cur_line_se:
            return self.cur_line_se
        else:
            return self.cur_line_st

    def is_closed(self):
        """
        @rtype: boolean
        """
        if self.cur_line_se:
            return True
        else:
            return False

    def __next__(self):
        """
        Return the next error node
        """
        for child in self.children:
            yield child
        return
        #self.parent.next()

    def __repr__(self):
        return '%i: %s' % (self.get_cur_line(), self.id)


class err_seg(err_node):
    """
    Segment Errors
    """
    def __init__(self, parent, map_node, seg_data, seg_count, cur_line, ls_id):
        """
        Needs:
            1. seg_id_code
            2. seg_pos - pos in ST loop
            3, loop_id - LS loop id
            4. seg_count - in parent
        """
        self.parent = parent
        if map_node is None:
            self.name = 'Unknown'
            self.pos = -1
        else:
            self.name = map_node.name
            self.pos = map_node.pos
        self.seg_id = seg_data.get_seg_id()
        self.seg_count = seg_count
        self.cur_line = cur_line
        self.ls_id = ls_id

        self.id = 'SEG'

        self.elements = []
        self.errors = []

    def accept(self, visitor):
        """
        Params:     visitor - ref to visitor class
        """
        visitor.visit_seg(self)
        for elem in self.elements:
            elem.accept(visitor)

    def add_error(self, err_cde, err_str, err_value=None):
        """
        @param err_cde: Error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.errors.append((err_cde, err_str, err_value))

    def err_count(self):
        """
        Returns:    count of errors
        """
        ele_err_ct = 0
        if self.child_err_count() > 0:
            ele_err_ct = 1
        return len(self.errors) + ele_err_ct

    def get_error_count(self):
        return self.err_count()

    def child_err_count(self):
        ct = 0
        for ele in self.elements:
            if ele.err_count() > 0:
                ct += 1
        return ct

    def __next__(self):
        """
        Desc:       Return the next error node
        """
        #for child in self.children:
        #    yield child
        #pdb.set_trace()
        return self
        #self.parent.next()

    def __repr__(self):
        return '%i: %s %s' % (self.get_cur_line(), self.id, self.seg_id)

    def get_first_child(self):
        return None
        #raise IterOutOfBounds


class err_ele(err_node):
    """
    Element Errors - Holds and generates output for element and
    composite/sub-element errors

    Each element with an error creates a new err_ele instance.
    """
    def __init__(self, parent, map_node):
        """
        """
        #, self.id, self.name, self.seq, self.data_ele)
        self.ele_ref_num = map_node.data_ele
        self.name = map_node.name
        if map_node.parent.is_composite():
            self.ele_pos = map_node.parent.seq
            self.subele_pos = map_node.seq
        else:
            self.ele_pos = map_node.seq
            self.subele_pos = None
        self.repeat_pos = None

        #self.bad_val = bad_val
        self.id = 'ELE'

        self.parent = parent
        #self.children = []
        self.errors = []

    def accept(self, visitor):
        """
        Params:     visitor - ref to visitor class
        """
        visitor.visit_ele(self)

    def add_error(self, err_cde, err_str, bad_value):
        """
        @param err_cde: Error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        #logger.debug('err_ele.add_error: %s %s %s' % (err_cde, err_str, bad_value))
        self.errors.append((err_cde, err_str, bad_value))

    def err_count(self):
        return len(self.errors)

    def get_error_count(self):
        return len(self.errors)


class ErrorErrhNull(Exception):
    """Class for errh_null errors."""


class errh_null(object):
    """
    A null error object - used for testing.
    Stores the current error in simple variables.
    """
    def __init__(self):
        self.id = 'ROOT'
        #self.children = []
        self.cur_node = self
        #self.cur_isa_node = None
        #self.cur_gs_node = None
        #self.cur_st_node = None
        #self.cur_seg_node = None
        #self.seg_node_added = False
        #self.cur_ele_node = None
        self.cur_line = 0
        self.err_cde = None
        self.err_str = None

    def reset(self):
        """
        Clear any errors
        """
        self.err_cde = None
        self.err_str = None

    def get_cur_line(self):
        """
        @return: Current file line number
        @rtype: int
        """
        return self.cur_line

    def get_id(self):
        """
        @return: Error node type
        @rtype: string
        """
        return self.id

    def add_isa_loop(self, seg, src):
        """
        """
        pass
        #raise ErrorErrhNull, 'add_isa loop'

    def add_gs_loop(self, seg, src):
        """
        """
        pass

    def add_st_loop(self, seg, src):
        """
        """
        pass

    def add_seg(self, map_node, seg, seg_count, cur_line, ls_id):
        """
        """
        pass

    def add_ele(self, map_node):
        """
        """
        pass

    def isa_error(self, err_cde, err_str):
        """
        @param err_cde: ISA level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def gs_error(self, err_cde, err_str):
        """
        @param err_cde: GS level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def st_error(self, err_cde, err_str):
        """
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def seg_error(self, err_cde, err_str, err_value=None, src_line=None):
        """
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def ele_error(self, err_cde, err_str, bad_value, refdes=None):
        """
        @param err_cde: Element level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def close_isa_loop(self, node, seg, src):
        """
        """
        pass

    def close_gs_loop(self, node, seg, src):
        """
        """
        pass

    def close_st_loop(self, node, seg, src):
        """
        """
        pass

    def find_node(self, type):
        """
        Find the last node of a type
        """
        pass

    def get_parent(self):
        return None

#    def get_first_child(self):
#        """
#        """
#        if len(self.children) > 0:
#            return self.children[0]
#        else:
#            return None

    def get_next_sibling(self):
        """
        """
        return None

    def get_error_count(self):
        """
        """
        if self.err_cde is not None:
            return 1
        else:
            return 0

    def handle_errors(self, err_list):
        pass

    def is_closed(self):
        """
        @rtype: boolean
        """
        return True

    def __repr__(self):
        """
        """
        return '%i: %s' % (-1, self.id)


class errh_list(object):
    """
    Capture validation errors in a list
    Used to refactor away from error_handler
    """
    def __init__(self):
        self.id = 'ROOT'
        self.cur_node = self
        self.cur_line = 0
        self.err_isa = []
        self.err_gs = []
        self.err_st = []
        self.err_seg = []
        self.err_ele = []

    def reset(self):
        """
        Clear any errors
        """
        self.err_isa = []
        self.err_gs = []
        self.err_st = []
        self.err_seg = []
        self.err_ele = []

    def get_cur_line(self):
        """
        @return: Current file line number
        @rtype: int
        """
        return self.cur_line

    def get_id(self):
        """
        @return: Error node type
        @rtype: string
        """
        return self.id

    def add_isa_loop(self, seg, src):
        pass

    def add_gs_loop(self, seg, src):
        pass

    def add_st_loop(self, seg, src):
        pass

    def add_seg(self, map_node, seg, seg_count, cur_line, ls_id):
        pass

    def add_ele(self, map_node):
        pass

    def isa_error(self, err_cde, err_str):
        """
        @param err_cde: ISA level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_isa.append((err_cde, err_str))

    def gs_error(self, err_cde, err_str):
        """
        @param err_cde: GS level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_gs.append((err_cde, err_str))

    def st_error(self, err_cde, err_str):
        """
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_st.append((err_cde, err_str))

    def seg_error(self, err_cde, err_str, err_value=None, src_line=None):
        """
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_seg.append((err_cde, err_str, err_value))

    def ele_error(self, err_cde, err_str, bad_value, refdes=None):
        """
        @param err_cde: Element level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_ele.append((err_cde, err_str, bad_value, refdes))

    def close_isa_loop(self, node, seg, src):
        pass

    def close_gs_loop(self, node, seg, src):
        pass

    def close_st_loop(self, node, seg, src):
        pass

    def find_node(self, type):
        pass

    def get_parent(self):
        return None

    def get_next_sibling(self):
        return None

    def get_error_count(self):
        return len(self.err_isa) + len(self.err_gs) + len(self.err_st) + len(self.err_seg) + len(self.err_ele)

    def handle_errors(self, err_list):
        """
        Handles errors generated by X12Reader
        @param err_list: List of errors
        @type err_list: [(type, error code, error string)]
        """
        for (etype, err_cde, err_str, err_value, src_line) in err_list:
            if etype == 'isa':
                self.isa_error(err_cde, err_str)
            elif etype == 'gs':
                self.gs_error(err_cde, err_str)
            elif etype == 'st':
                self.st_error(err_cde, err_str)
            elif etype == 'seg':
                self.seg_error(err_cde, err_str, err_value, src_line)

    def is_closed(self):
        """
        @rtype: boolean
        """
        return True

    def __repr__(self):
        """
        """
        return '%i: %s' % (-1, self.id)
