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
Capture X12 Errors
"""

import logging
#from types import *
#import pdb
import tempfile
#import lxml
import os

# Intrapackage imports
from errors import EngineError
from xmlwriter import XMLWriter

#class error_node:
#    def __init__(self)
logger = logging.getLogger('pyx12.errh_xml')
#logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)

class err_handler(object):
    """
    The interface to the error handling structures.
    """
    def __init__(self, xml_out=None, basedir=None):
        """
        @param xml_out: Output filename, if None, will dump to tempfile
        @param basedir: working directory, where file will be created
        """
        if xml_out:
            self.filename = xml_out
            fd = open(xml_out, 'w')
        else:
            try:
                (fdesc, self.filename) = tempfile.mkstemp('.xml', 'pyx12_')
                fd = os.fdopen(fdesc, 'w+b')
                #fd = tempfile.NamedTemporaryFile()
                #self.filename = fd.name
            except:
                #self.filename = '997.tmp.xml'
                (fdesc, self.filename) = tempfile.mkstemp(suffix='.xml',
                                                          prefix='pyx12_', dir=basedir)
                fd = os.fdopen(fdesc, 'w+b')
                #fd = file(os.path.join(basedir, self.filename), 'w')
        self.cur_line = None
        self.errors = []
        if not fd:
            raise EngineError('Could not open temp error xml file')
        self.writer = XMLWriter(fd)
        #self.writer.doctype(
        #    u"x12simple", u"-//J Holland//DTD XML X12 Document
        #    Conversion1.0//EN//XML",
        #    u"%s" % (dtd_urn))
        self.writer.push("x12err")

    def __del__(self):
        while len(self.writer) > 0:
            self.writer.pop()

    def getFilename(self):
        return self.filename

    def handleErrors(self, err_list):
        """
        @param err_list: list of errors to apply
        """
        self.errors.extend(err_list)
        #for (err_type, err_cde, err_str, err_val, src_line) in err_list:
        #    if err_type == 'isa':
        #        self.isa_error(err_cde, err_str)
        #    elif err_type == 'gs':
        #        self.gs_error(err_cde, err_str)
        #    elif err_type == 'st':
        #        self.st_error(err_cde, err_str)
        #    elif err_type == 'seg':
        #        self.seg_error(err_cde, err_str, err_val, src_line)

    def getCurLine(self):
        """
        @return: Current file line number
        @rtype: int
        """
        return self.cur_line

    def Write(self, cur_line):
        """
        Generate XML for the segment data and matching map node

        """
        if len(self.errors) > 0:
            self.writer.push("seg", attrs={'line': '%i' % (cur_line)})
            for (err_type, err_cde, err_str, err_val, src_line) in self.errors:
                self.writer.push("err", attrs={"code": err_cde})
                #self.writer.elem(u"type", err_type)
                #self.writer.elem(u"code", err_cde)
                self.writer.elem("desc", err_str)
                if err_val:
                    self.writer.elem("errval", err_val)
                #self.writer.push(u"seg", {u'line': '%i'%(cur_line)})
                        #self.writer.elem(u'ele', seg_data.get_value('%02i' %
                        #(i+1)),
                        #    attrs={u'id': child_node.id})
                self.writer.pop()  # end err
            self.writer.pop()  # end segment
            self.errors = []


class ErrorErrhNull(Exception):
    """Class for errh_null errors."""


class errh_list(object):
    """
    A null error object - used for testing.
    Stores the current error in simple variables.
    """
    def __init__(self):
        #self.id = 'ROOT'
        self.errors = []
        #self.cur_node = self
        self.cur_line = 0
        #self.err_cde = None
        #self.err_str = None

    def get_errors(self):
        return self.errors

    def reset(self):
        self.errors = []

    def get_cur_line(self):
        """
        @return: Current file line number
        @rtype: int
        """
        return self.cur_line

    def set_cur_line(self, cur_line):
        """
        """
        self.cur_line = cur_line

#    def get_id(self):
#        """
#        @return: Error node type
#        @rtype: string
#        """
#        return self.id

    def add_isa_loop(self, seg, src):
        """
        """
        #raise ErrorErrhNull, 'add_isa loop'
        pass

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
        self.errors.append(('isa', err_cde, err_str, None, None))
        sout = ''
        sout += 'Line:%i ' % (self.cur_line)
        sout += 'ISA:%s - %s' % (err_cde, err_str)
        logger.error(sout)

    def gs_error(self, err_cde, err_str):
        """
        @param err_cde: GS level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.errors.append(('gs', err_cde, err_str, None, None))
        sout = ''
        sout += 'Line:%i ' % (self.cur_line)
        sout += 'GS:%s - %s' % (err_cde, err_str)
        logger.error(sout)

    def st_error(self, err_cde, err_str):
        """
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.errors.append(('st', err_cde, err_str, None, None))
        sout = ''
        sout += 'Line:%i ' % (self.cur_line)
        sout += 'ST:%s - %s' % (err_cde, err_str)
        logger.error(sout)

    def seg_error(self, err_cde, err_str, err_value=None, src_line=None):
        """
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.errors.append(('seg', err_cde, err_str, err_value, src_line))
        sout = ''
        sout += 'Line:%i ' % (self.cur_line)
        sout += 'SEG:%s - %s' % (err_cde, err_str)
        if err_value:
            sout += ' (%s)' % err_value
        logger.error(sout)

    def ele_error(self, err_cde, err_str, bad_value):
        """
        @param err_cde: Element level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.errors.append(('ele', err_cde, err_str, bad_value, None))
        sout = ''
        sout += 'Line:%i ' % (self.cur_line)
        sout += 'ELE:%s - %s' % (err_cde, err_str)
        if bad_value:
            sout += ' (%s)' % (bad_value)
        logger.error(sout)

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

    def find_node(self, atype):
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
        return len(self.errors)

    def is_closed(self):
        """
        @rtype: boolean
        """
        return True
