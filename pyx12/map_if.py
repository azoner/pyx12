######################################################################
# Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Interface to a X12N IG Map
"""
import cPickle
import libxml2
import logging
import os.path
#import pdb
import string
import sys
from types import *
from stat import ST_MTIME
from stat import ST_SIZE

# Intrapackage imports
import errors
import codes

#Global Variables
NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3, 
    'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8, 
    'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12}

MAXINT = 2147483647

############################################################
# X12 Node Superclass
############################################################
class x12_node:
    def __init__(self):
        self.id = None
        self.name = None
        self.parent = None
        self.prev_node = None
        self.next_node = None
        self.children = []
        self.path = ''

#    def __del__(self):
#        pass

    def __repr__(self):
        """
        @rtype: string
        """
        return self.name

    def getnodebypath(self, path):
        """
        """
        pathl = path.split('/')
        if len(pathl) == 0: return None
        for child in self.children:
            if child.id.lower() == pathl[0].lower():
                if len(pathl) == 1:
                    return child
                else:
                    if child.is_loop():
                        return child.getnodebypath(string.join(pathl[1:],'/'))
                    else:
                        return None
        return None
 
    def get_child_count(self):
        return len(self.children)

    def get_child_node_by_idx(self, idx):
        """
        @param idx: zero based
        """
        if idx >= len(self.children):
            return None
        else:
            return self.children[idx]
            
    def get_path(self):
        """
        @return: path - XPath style
        @rtype: string
        """
        parent_path = self.parent.get_path()
        if parent_path == '/':
            return '/' + self.path
        else:
            return parent_path + '/' + self.path

#    def walk_tree(self, seg):
#        pass
        # handle loop events, pop, push
        # only concerned with loop and segment nodes

        # repeat of seg
        # next seg in loop
        # repeat of loop
        # child loop
        # sibling loop
        # parent loop
        # - first id element ==

    def is_first_seg_in_loop(self):
        """
        @rtype: boolean
        """
        return False

    def is_map_root(self):
        """
        @rtype: boolean
        """
        return False

    def is_loop(self):
        """
        @rtype: boolean
        """
        return False
    
    def is_segment(self):
        """
        @rtype: boolean
        """
        return False
    
    def is_element(self):
        """
        @rtype: boolean
        """
        return False
    
    def is_composite(self):
        """
        @rtype: boolean
        """
        return False


#    def debug_print(self):
#       sys.stdout.write('%s%s %s %s %s\n' % (str(' '*self.base_level), \
#           self.base_name, self.base_level, self.id, self.name))
#       for node in self.children:
#           node.debug_print()


############################################################
# Map file interface
############################################################
class map_if(x12_node):
    def __init__(self, map_file, param):
        """
        @param param: map of parameters
        """
        #codes = codes.ExternalCodes()
        #tab = Indent()
        x12_node.__init__(self)
        self.children = []
        index = 0
        cur_name = ''
        self.cur_path = '/transaction'
        self.path = '/'
        self.cur_level = -1 
        self.base_level = 0
        self.base_name = ''
        self.index = 0
        self.src_version = '$Revision$'

        self.id = None
        self.name = None

        self.cur_iter_node = self

        self.param = param
        #global codes
        self.ext_codes = codes.ExternalCodes(param.get('map_path'), \
            param.get('exclude_external_codes'))
        try:
            map_path = param.get('map_path')
            self.reader = libxml2.newTextReaderFilename(os.path.join(map_path, \
                map_file))
        except:
            raise errors.GSError, 'Map file not found: %s' % (map_file)
        try:    
            ret = self.reader.Read()
            if ret == -1:
                raise errors.XML_Reader_Error, 'Read Error'
            elif ret == 0:
                raise errors.XML_Reader_Error, 'End of Map File'
            while ret == 1:
                #print 'map_if', self.reader.NodeType(), self.reader.Depth(), self.reader.Name()
                tmpNodeType = self.reader.NodeType()
                if tmpNodeType == NodeType['element_start']:
                #       if self.reader.Name() in ('map', 'transaction', 'loop', 'segment', 'element'):
                #    print 't'*self.reader.Depth(), self.reader.Depth(), \
                #       self.base_level, self.reader.NodeType(), self.reader.Name()
                #sys.stdout.write('%s%i %s %s %s\n') % ('\t'*self.reader.Depth(), \
                #    self.reader.Depth(),  self.base_level, self.reader.Name())
                    cur_name = self.reader.Name()
                    if cur_name == 'transaction':
                        self.base_level = self.reader.Depth()
                        self.base_name = 'transaction'
                        pass
                    elif cur_name == 'segment':
                        self.children.append(segment_if(self, self, index))
                        if len(self.children) > 1:
                            self.children[-1].prev_node = self.children[-2]
                            self.children[-2].next_node = self.children[-1]
                        index += 1
                    elif cur_name == 'loop':
                        self.children.append(loop_if(self, self, index))
                        if len(self.children) > 1:
                            self.children[-1].prev_node = self.children[-2]
                            self.children[-2].next_node = self.children[-1]
                        index += 1
                    
                    #if self.cur_level < self.reader.Depth():
                        #    self.cur_path = os.path.join(self.cur_path, cur_name)
                    #elif self.cur_level > self.reader.Depth():
                    #    self.cur_path = os.path.dirname(self.cur_path)
                    self.cur_level = self.reader.Depth()
                elif tmpNodeType == NodeType['element_end']:
                    #print '--', self.reader.Name(), self.base_level, \
                    #   self.self.reader.Depth(), self.reader.Depth() <= self.base_level 
                    #print self.reader.Depth(),  self.base_level, self.reader.NodeType(), self.reader.Name()
                    if self.reader.Depth() <= self.base_level:
                        ret = self.reader.Read()
                        if ret == -1:
                            raise errors.XML_Reader_Error, 'Read Error'
                        elif ret == 0:
                            raise errors.XML_Reader_Error, 'End of Map File'
                        break 
                    #if cur_name == 'transaction':
                    #    pass
                    cur_name = ''
                
                elif tmpNodeType == NodeType['text'] and self.base_level + 2 == self.reader.Depth():
                    #print cur_name, self.reader.Value()
                    if cur_name == 'id' and self.base_name == 'transaction':
                        self.id = self.reader.Value()
                    elif cur_name == 'name' and self.base_name == 'transaction':
                        self.name = self.reader.Value()

                ret = self.reader.Read()
                if ret == -1:
                    raise errors.XML_Reader_Error, 'Read Error'
                elif ret == 0:
                    raise errors.XML_Reader_Error, 'End of Map File'
        except errors.XML_Reader_Error:
            pass

        del self.reader

    #def __del__(self):
    #    print 'Map root de-cronstructor'
                
    def debug_print(self):
        sys.stdout.write(self.__repr__())
        for node in self.children:
            node.debug_print()

    def __repr__(self):
        """
        @rtype: string
        """
        #out = '%s%s %s %s %s\n' % (str(' '*self.base_level), \
        #   self.base_name, self.base_level, self.id, self.name)
        #out = '%s%s' % (str(' '*self.base_level), self.base_name)
        #out += '%sid %s\n' % (str(' '*(self.base_level+1)), self.id)
        #out += '%sname %s\n' % (str(' '*(self.base_level+1)), self.name)
        return '%s\n' % (self.id)

    def _path_parent(self):
        """
        @rtype: string
        """
        return os.path.basename(os.path.dirname(self.cur_path))

    def get_path(self):
        """
        @rtype: string
        """
        return self.path

    def getnodebypath(self, path):
        """
        """
        pathl = path.split('/')[1:]
        if len(pathl) == 0: return None
        #logger.debug('%s %s %s' % (self.base_name, self.id, pathl[1]))
        for child in self.children:
            if child.id.lower() == pathl[0].lower():
                if len(pathl) == 1:
                    return child
                else:
                    return child.getnodebypath(string.join(pathl[1:],'/'))
        return None
            
    def is_map_root(self):
        """
        @rtype: boolean
        """
        return True

    def reset_cur_count(self):
        for child in self.children:
            #if child.is_loop():
            child.reset_cur_count()

    def __iter__(self):
        return self

    def next(self):
        #if self.cur_iter_node.id == 'GS06':
        #pdb.set_trace()
        if self.cur_iter_node.id == 'IEA':
            raise StopIteration
        #first, get first child
        if self.cur_iter_node.get_child_count() > 0:
            self.cur_iter_node = self.cur_iter_node.children[0]
            return self.cur_iter_node
        # Get original index of starting node
        #node_idx = self.cur_iter_node.index 
        cur_node = self.cur_iter_node
        #node = self._pop_to_parent(cur_node) 
        while 1:
            #second, get next sibling
            if cur_node is None:
                raise StopIteration
            if cur_node.next_node != None:
                self.cur_iter_node = cur_node.next_node
                return self.cur_iter_node
            #last, get siblings of parent
            cur_node = cur_node.parent
        return None


############################################################
# Loop Interface
############################################################
class loop_if(x12_node):
    """
    """
    def __init__(self, root, parent, my_index): 
        """
        @requires: Must be entered with a libxml2 loop node current
        """
        x12_node.__init__(self)
        self.root = root
        self.parent = parent
        self.index = my_index
        self.children = []
        self.path = ''
        self.base_name = 'loop'
        self.type = 'implicit'
        self.cur_count = 0
        
        self.id = None
        self.name = None
        self.usage = None
        #self.seq = None
        self.pos = None
        self.repeat = None
        
        reader = self.root.reader

        index = 0
        self.base_level = reader.Depth()
#        if parent == None:
#            self.path = id
#        else:
#            self.path = path + '/' + id

        self.cur_level = reader.Depth()

        while reader.MoveToNextAttribute():
            if reader.Name() == 'xid':
                self.id = reader.Value()
                self.path = self.id
            elif reader.Name() == 'type':
                self.type = reader.Value()
        
        ret = 1 
        while ret == 1:
            #print '--- loop while'
            #print reader.NodeType(), reader.Name()
            #print 'loop', reader.NodeType(), reader.Depth(), reader.Name()
            #processNode(reader)
            tmpNodeType = reader.NodeType()
            if tmpNodeType == NodeType['element_start']:
                #if reader.Name() in ('map', 'transaction', 'loop', \
                #   'segment', 'element'):
                #    print 'l'*reader.Depth(), reader.Depth(),  \
                #       self.base_level, reader.NodeType(), reader.Name()
                cur_name = reader.Name()
                if cur_name == 'loop' and self.base_level < reader.Depth():
                    self.children.append(loop_if(self.root, self, index))
                    if len(self.children) > 1:
                        self.children[-1].prev_node = self.children[-2]
                        self.children[-2].next_node = self.children[-1]
                    index += 1
                elif cur_name == 'segment':
                    self.children.append(segment_if(self.root, self, index))
                    if len(self.children) > 1:
                        self.children[-1].prev_node = self.children[-2]
                        self.children[-2].next_node = self.children[-1]
                    index += 1
                elif cur_name == 'element':
                    self.children.append(element_if(self.root, self))
                    if len(self.children) > 1:
                        self.children[-1].prev_node = self.children[-2]
                        self.children[-2].next_node = self.children[-1]
                    
                #if self.cur_level < reader.Depth():
                #    self.cur_path = os.path.join(self.cur_path, cur_name)
                #elif self.cur_level > reader.Depth():
                #    self.cur_path = os.path.dirname(self.cur_path)
                self.cur_level = reader.Depth()
            elif tmpNodeType == NodeType['element_end']:
                #print '--', reader.Name(), self.base_level, reader.Depth(), reader.Depth() <= self.base_level 
                if reader.Depth() <= self.base_level:
                    ret = reader.Read()
                    if ret == -1:
                        raise errors.XML_Reader_Error, 'Read Error'
                    elif ret == 0:
                        raise errors.XML_Reader_Error, 'End of Map File'
                    break
                #if reader.Name() == 'transaction':
                #    return
                #    pass
                cur_name = ''
                
            elif tmpNodeType == NodeType['text'] and self.base_level + 2 == \
                    reader.Depth():
                #print cur_name, reader.Value()
                #if cur_name == 'id' and self.base_name == 'loop':
                #    self.id = reader.Value()
                #    self.path = self.id
                if cur_name == 'name' and self.base_name == 'loop':
                    self.name = reader.Value()
                elif cur_name == 'usage' and self.base_name == 'loop':
                    self.usage = reader.Value()
                elif cur_name == 'pos' and self.base_name == 'loop':
                    self.pos = int(reader.Value())
                    #self.seq = self.pos  # XXX
                elif cur_name == 'repeat' and self.base_name == 'loop':
                    self.repeat = reader.Value()


            ret = reader.Read()
            if ret == -1:
                raise errors.XML_Reader_Error, 'Read Error'
            elif ret == 0:
                raise errors.XML_Reader_Error, 'End of Map File'
        
    def debug_print(self):
        sys.stdout.write(self.__repr__())
        for node in self.children:
            node.debug_print()

    def __repr__(self):
        """
        @rtype: string
        """
        #out = '%s%s %s %s %s\n' % (str(' '*self.base_level), self.base_name, \
        #    self.id, self.name, self.base_level)
        out = ''
        if self.id: 
            out += '%sLOOP %s' % (str(' '*(self.base_level+1)), self.id)
            #out += '%sid: %s  ' % (str(' '*(self.base_level+1)), self.id)
        if self.name: 
            out += '  "%s"' % (self.name)
        if self.usage: 
            out += '  usage: %s' % (self.usage)
        if self.pos: 
            out += '  pos: %s' % (self.pos)
        if self.repeat: 
            out += '  repeat: %s' % (self.repeat)
        out += '\n'
        return out

    def get_max_repeat(self):
        if self.repeat is None:
            return MAXINT
        if self.repeat == '&gt;1' or self.repeat == '>1':
            return MAXINT
        return int(self.repeat)

    def get_parent(self):
        return self.parent

#    def is_match(self):
#        pass

#    def is_valid(self, seg_data, errh):
#        pass

#    def parse(self):
#        pass

    def get_seg_count(self):
        i = 0
        for child in self.children:
            if child.is_segment():
                i += 1
        return i

    def is_loop(self):
        """
        @rtype: boolean
        """
        return True

    def is_match(self, seg_data):
        """
        @rtype: boolean
        """
        child = self.get_child_node_by_idx(0)
        if child.is_loop():
            return child.is_match(seg_data)
        elif child.is_segment():
            if child.is_match(seg_data):
                return True
            else:
                return False # seg does not match the first segment in loop, so not valid
        else:
            return False

    def reset_cur_count(self):
        for child in self.children:
            #if child.is_loop():
            child.reset_cur_count()

############################################################
# Segment Interface
############################################################
class segment_if(x12_node):
    """
    """
    def __init__(self, root, parent, my_index):
        """
        @requires: Must be entered with a libxml2 segment node current
        @param parent: parent node 
        """

        #global reader
        reader = root.reader
        x12_node.__init__(self)
        self.root = root
        self.parent = parent
        self.index = my_index
        self.children = []
        self.path = ''
        self.base_name = 'segment'
        self.base_level = reader.Depth()
        self.check_dte = '20030930'
        self.cur_count = 0
        #self.logger = logging.getLogger('pyx12')

        self.id = None
        self.end_tag = None
        self.name = None
        self.usage = None
        self.pos = None
        self.max_use = None
        self.syntax = []
 
#        if parent == None:
#            self.path = id
#        else:
#            self.path = path + '/' + id

        self.cur_level = reader.Depth()
        
        while reader.MoveToNextAttribute():
            if reader.Name() == 'xid':
                self.id = reader.Value()
                self.path = self.id

        ret = 1 
        while ret == 1:
            #print '--- segment while'
            #print 'seg', reader.NodeType(), reader.Depth(), reader.Name()
            tmpNodeType = reader.NodeType()
            if tmpNodeType == NodeType['element_start']:
                #if reader.Name() in ('map', 'transaction', 'loop', 'segment', 'element'):
                #    print 's'*reader.Depth(), reader.Depth(),  self.base_level, reader.NodeType(), reader.Name()
                cur_name = reader.Name()
                if cur_name == 'segment':
                    self.base_level = reader.Depth()
                    self.base_name = 'segment'
                elif cur_name == 'element':
                    self.children.append(element_if(self.root, self))
                    if len(self.children) > 1:
                        self.children[-1].prev_node = self.children[-2]
                        self.children[-2].next_node = self.children[-1]
                elif cur_name == 'composite':
                    self.children.append(composite_if(self.root, self))
                    if len(self.children) > 1:
                        self.children[-1].prev_node = self.children[-2]
                        self.children[-2].next_node = self.children[-1]
                    
                #if self.cur_level < reader.Depth():
                #    self.cur_path = os.path.join(self.cur_path, cur_name)
                #elif self.cur_level > reader.Depth():
                #    self.cur_path = os.path.dirname(self.cur_path)
                self.cur_level = reader.Depth()
            elif tmpNodeType == NodeType['element_end']:
                #print '--', reader.Name(), self.base_level, reader.Depth(), reader.Depth() <= self.base_level 
                if reader.Depth() <= self.base_level:
                    ret = reader.Read()
                    if ret == -1:
                        raise errors.XML_Reader_Error, 'Read Error'
                    elif ret == 0:
                        raise errors.XML_Reader_Error, 'End of Map File'
                    break 
                #if reader.Name() == 'transaction':
                #    return
                #    pass
                cur_name = ''
                
            elif tmpNodeType == NodeType['text'] and self.base_level + 2 == reader.Depth():
                #print cur_name, reader.Value()
                #if cur_name == 'id' and self.base_name == 'segment':
                #    self.id = reader.Value()
                #    self.path = self.id
                if cur_name == 'end_tag' and self.base_name == 'segment':
                    self.end_tag = reader.Value()
                elif cur_name == 'name' and self.base_name == 'segment':
                    self.name = reader.Value()
                elif cur_name == 'usage' and self.base_name == 'segment':
                    self.usage = reader.Value()
                elif cur_name == 'pos' and self.base_name == 'segment':
                    self.pos = int(reader.Value())
                elif cur_name == 'max_use' and self.base_name == 'segment':
                    self.max_use = reader.Value()
                elif cur_name == 'syntax' and self.base_name == 'segment':
                    syn_list = self._split_syntax(reader.Value())
                    if syn_list is not None:
                        self.syntax.append(syn_list)

            ret = reader.Read()
            if ret == -1:
                raise errors.XML_Reader_Error, 'Read Error'
            elif ret == 0:
                raise errors.XML_Reader_Error, 'End of Map File'
        
    def debug_print(self):
        sys.stdout.write(self.__repr__())
        for node in self.children:
            node.debug_print()

    def __repr__(self):
        """
        @rtype: string
        """
        t1 = str(' '*self.base_level)
        #t2 = str(' '*(self.base_level+1))
        #self.base_name
        out = '%s%s "%s"' % (t1, self.id, self.name)
        #if self.id: 
        #    out += '%sid %s\n' % (t2, self.id)
        #if self.name: 
        #    out += '%sname %s\n' % (t2, self.name)
        if self.usage: 
            out += '  usage: %s' % (self.usage)
        if self.pos: 
            out += '  pos: %i' % (self.pos)
        if self.max_use: 
            out += '  max_use: %s' % (self.max_use)
        out += '\n'
        return out

#    def get_elemval_by_id(self, seg_data, id):
#        """
#        Return the value of an element or sub-element identified by the id
#        @param seg_data: data segment instance to search
#        @param id: string 
#        @return: value of the element
#        @rtype: string
#        """
#        for child in self.children:
#            if child.is_element():
#                if child.id == id:
#                    return seg_data[child.pos].get_value()
#            elif child.is_composite():
#                for child in self.children:
#                    if child.is_element():
#                        if child.id == id:
#                            return seg_data[child.pos]
#        return None

    def get_max_repeat(self):
        if self.max_use is None or self.max_use == '>1':
            return MAXINT
        return int(self.max_use)
    
    def get_parent(self):
        """
        @return: ref to parent class instance
        @rtype: pyx12.x12_node
        """
        return self.parent

    def get_path(self):
        """
        @return: path - XPath style
        @rtype: string
        """
        parent_path = self.parent.get_path()
        if parent_path == '/':
            ret = '/' + self.path
        else:
            ret = parent_path + '/' + self.path
        if self.children[0].is_element() \
            and self.children[0].data_type == 'ID' \
            and len(self.children[0].valid_codes) > 0:
            ret += '[%s]' % (self.children[0].valid_codes[0])
        return ret

    def is_first_seg_in_loop(self):
        """
        @rtype: boolean
        """
        if self is self.get_parent().children[0]:
            return True
        else:
            return False

    def is_match(self, seg):
        """
        is segment given a match to this node?
        @param seg: data segment instance
        @return: boolean
        @rtype: boolean
        """
        if seg.get_seg_id() == self.id:
            if self.children[0].is_element() \
                and self.children[0].data_type == 'ID' \
                and len(self.children[0].valid_codes) > 0 \
                and seg[0].get_value() not in self.children[0].valid_codes:
                #logger.debug('is_match: %s %s' % (seg.get_seg_id(), seg[1]), self.children[0].valid_codes)
                #pdb.set_trace()
                return False
            elif self.children[0].is_composite() \
                and self.children[0].children[0].data_type == 'ID' \
                and len(self.children[0].children[0].valid_codes) > 0 \
                and seg[0][0].get_value() not in self.children[0].children[0].valid_codes:
                return False
            elif seg.get_seg_id() == 'HL' and self.children[2].is_element() \
                and len(self.children[2].valid_codes) > 0 \
                and seg[2].get_value() not in self.children[2].valid_codes:
                return False
            return True
        else:
            return False

    def is_segment(self):
        """
        @rtype: boolean
        """
        return True

    def is_valid(self, seg_data, errh):
        """
        @param seg_data: data segment instance
        @param errh: instance of error_handler
        @rtype: boolean
        """
        valid = True
        child_count = self.get_child_count()
        if len(seg_data) > child_count:
            child_node = self.get_child_node_by_idx(child_count+1)
            err_str = 'Too many elements in segment "%s" (%s). Has %i, should have %i' % \
                (self.name, seg_data.get_seg_id(), len(seg_data), child_count)
            #self.logger.error(err_str)
            err_value = seg_data[child_count+1].format()
            errh.ele_error('3', err_str, err_value)
            valid = False

        for i in xrange(len(seg_data)):
            #self.logger.debug('i=%i, len(seg_data)=%i / child_count=%i' % \
            #   (i, len(seg_data), self.get_child_count()))
            child_node = self.get_child_node_by_idx(i)
            if child_node.is_composite():
                # Validate composite
                comp_data = seg_data[i]
                subele_count = child_node.get_child_count()
                if len(comp_data) > subele_count and child_node.usage != 'N':
                    subele_node = child_node.get_child_node_by_idx(subele_count+1)
                    err_str = 'Too many sub-elements in composite "%s" (%s)' % \
                        (subele_node.name, subele_node.refdes)
                    err_value = comp_data[subele_count].get_value()
                    errh.ele_error('3', err_str, err_value)
                valid &= child_node.is_valid(comp_data, errh, self.check_dte)
            elif child_node.is_element():
                # Validate Element
                valid &= child_node.is_valid(seg_data[i][0], errh, self.check_dte)
        for i in xrange(len(seg_data), self.get_child_count()):
            #missing required elements?
            child_node = self.get_child_node_by_idx(i)
            valid &= child_node.is_valid(None, errh)
                
        for syn in self.syntax:
            (bResult, err_str) = is_syntax_valid(seg_data, syn)
            if not bResult:
                #pdb.set_trace()
                errh.ele_error('2', err_str, None)
                valid &= False

        return valid

    def _split_syntax(self, syntax):
        """
        Split a Syntax string into a list
        """
        if syntax[0] not in ['P', 'R', 'C', 'L', 'E']:
            #self.logger.error('Syntax %s is not valid' % (syntax))
            return None
        syn = [syntax[0]]
        for i in range(len(syntax[1:])/2):
            syn.append(int(syntax[i*2+1:i*2+3]))
        return syn
        
    def reset_cur_count(self):
        self.cur_count = 0

############################################################
# Element Interface
############################################################
class element_if(x12_node):
    def __init__(self, root, parent):
        """
        @requires: Must be entered with a libxml2 element node current
        @param parent: parent node 
        """

        #global reader
        reader = root.reader
        x12_node.__init__(self)
        self.children = []
        self.root = root
        self.parent = parent
        self.path = ''
        self.base_name = 'element'
        self.base_level = reader.Depth()

        self.id = None
        self.name = None
        self.usage = None
        #self.pos = None
        #self.max_use = None
        self.data_ele = None
        self.seq = None
        self.refdes = None
        self.data_type = None
        self.min_len = None
        #self.max_len = None

        self.valid_codes = []
        self.external_codes = None
        #self.logger = logging.getLogger('pyx12')

#        ret = 1 
#        while ret == 1 and self.cur_level <= reader.Depth():
#            #print 'ele', reader.NodeType(), reader.Depth(), reader.Name()
#            ret = reader.Read()
#            if ret == -1:
#                raise errors.XML_Reader_Error, 'Read Error'
#            elif ret == 0:
#                raise errors.XML_Reader_Error, 'End of Map File'
#        return

        self.cur_level = reader.Depth()
        
        while reader.MoveToNextAttribute():
            if reader.Name() == 'xid':
                self.id = reader.Value()
                self.refdes = self.id

        ret = 1 
        while ret == 1:
            #print '--- segment while'
            #print 'seg', reader.NodeType(), reader.Depth(), reader.Name()
            tmpNodeType = reader.NodeType()
            if tmpNodeType == NodeType['element_start']:
                #if reader.Name() in ('map', 'transaction', 'loop', 'segment', 'element'):
                #    print 's'*reader.Depth(), reader.Depth(),  self.base_level, reader.NodeType(), reader.Name()
                cur_name = reader.Name()
                if cur_name == 'element':
                    self.base_level = reader.Depth()
                    self.base_name = 'element'
                elif cur_name == 'valid_codes':
                    while reader.MoveToNextAttribute():
                        #sys.stderr.write('attrib: %s - %s' % (reader.Name(), reader.Value()))
                        if reader.Name() == 'external':
                            self.external_codes = reader.Value()
                #if self.cur_level < reader.Depth():
                #    self.cur_path = os.path.join(self.cur_path, cur_name)
                #elif self.cur_level > reader.Depth():
                #    self.cur_path = os.path.dirname(self.cur_path)
                self.cur_level = reader.Depth()
            elif tmpNodeType == NodeType['element_end']:
                #print '--', reader.Name(), self.base_level, reader.Depth(), reader.Depth() <= self.base_level 
                if reader.Depth() <= self.base_level:
                    ret = reader.Read()
                    if ret == -1:
                        raise errors.XML_Reader_Error, 'Read Error'
                    elif ret == 0:
                        raise errors.XML_Reader_Error, 'End of Map File'
                    break 
                #if reader.Name() == 'transaction':
                #    return
                #    pass
                cur_name = ''
                
            elif tmpNodeType == NodeType['text'] and self.base_level + 2 <= reader.Depth():
                #print cur_name, reader.Value()
#                if cur_name == 'id':
#                    self.id = reader.Value()
                if cur_name == 'name':
                    self.name = reader.Value()
                elif cur_name == 'data_ele':
                    self.data_ele= reader.Value()
                elif cur_name == 'usage':
                    self.usage = reader.Value()
                elif cur_name == 'seq':
                    self.seq = int(reader.Value())
                    self.path = reader.Value()
                #elif cur_name == 'pos':
                #    self.pos = reader.Value()
                #elif cur_name == 'refdes':
                #    self.refdes = reader.Value()
                #    self.id = self.refdes
                elif cur_name == 'data_type':
                    self.data_type = reader.Value()
                elif cur_name == 'min_len':
                    self.min_len = reader.Value()
                elif cur_name == 'max_len':
                    self.max_len = reader.Value()
                #elif cur_name == 'max_use':
                #    self.max_use= reader.Value()
                elif cur_name == 'code':
                    self.valid_codes.append(reader.Value())
#               <valid_codes external="prov_taxonomy"/>


            ret = reader.Read()
            if ret == -1:
                raise errors.XML_Reader_Error, 'Read Error'
            elif ret == 0:
                raise errors.XML_Reader_Error, 'End of Map File'
        
    def debug_print(self):
        sys.stdout.write(self.__repr__())
        for node in self.children:
            node.debug_print()

    def __repr__(self):
        """
        @rtype: string
        """
        out = '%s%s "%s"' % (str(' '*self.base_level), self.refdes, self.name)
        if self.data_ele: 
            out += '  data_ele: %s' % (self.data_ele)
        #if self.name: 
        #    out += '  name: %s' % (self.name)
        if self.usage: 
            out += '  usage: %s' % (self.usage)
        if self.seq: 
            out += '  seq: %i' % (self.seq)
        #if self.refdes: 
        #    out += '  refdes: %s' % (self.refdes)
        #if self.data_type: 
        #    out += '  data_type: %s' % (self.data_type)
        out += '  %s(%s, %s)' % (self.data_type, self.min_len, self.max_len)
        #if self.min_len: 
        #    out += '  min_len: %s' % (self.min_len)
        #if self.max_len: 
        #    out += '  max_len: %s' % (self.max_len)
        if self.external_codes: 
            out += '   external codes: %s' % (self.external_codes)
        #if self.valid_codes:
        #    out += '%svalid codes:\n' % (str(' '*(self.base_level+1)))
        #    for code in self.valid_codes:
        #        out += '%scode %s\n' % (str(' '*(self.base_level+2)), code)
        out += '\n'
        return out
   
#    def __del__(self):
#        pass

    def _error(self, errh, err_str, err_cde, elem_val):
        """
        Forward the error to an error_handler
        """
        errh.ele_error(err_cde, err_str, elem_val) #, pos=self.seq, data_ele=self.data_ele)
        
    def _valid_code(self, code):
        """
        Verify the x12 element value is in the given list of valid codes
        @return: True if found, else False
        @rtype: boolean
        """
        #if not self.valid_codes:
        #    return True
        if code in self.valid_codes:
            return True
        return False

    def get_parent(self):
        """
        @return: ref to parent class instance
        """
        return self.parent

    def is_match(self):
        """
        @return: 
        @rtype: boolean
        """
        # match also by ID
        pass

    def is_valid(self, elem, errh, check_dte=None):
        """
        Is this a valid element
        @param elem: element instance
        @type elem: pyx12.element
        @param errh: instance of error_handler
        @param check_dte: date string to check against (YYYYMMDD)
        @return: True if valid
        @rtype: boolean
        """
        errh.add_ele(self)

        if elem and elem.is_composite():
            err_str = 'Data element "%s" (%s) is an invalid composite' % \
                (self.name, self.refdes)
            self._error(errh, err_str, '6', elem.__repr__())
            return False

        if elem is None or elem.get_value() == '':
            if self.usage in ('N', 'S'):
                return True
            elif self.usage == 'R':
                if self.seq != 1 or not self.parent.is_composite() or self.parent.usage == 'R':
                    err_str = 'Mandatory data element "%s" (%s) is missing' % (self.name, self.refdes)
                    self._error(errh, err_str, '1', None)
                    return False
                else:
                    return True
        if self.usage == 'N' and elem.get_value() != '':
            err_str = 'Data element "%s" (%s) is marked as Not Used' % (self.name, self.refdes)
            self._error(errh, err_str, '5', None)
            return False

        elem_val = elem.get_value()
        valid = True
        if (not self.data_type is None) and (self.data_type == 'R' or self.data_type[0] == 'N'):
            elem_strip = string.replace(string.replace(elem_val, '-', ''), '.', '')
            if len(elem_strip) < int(self.min_len):
                err_str = 'Data element "%s" (%s) is too short: "%s" should be at least %i characters' % \
                    (self.name, self.refdes, elem_val, int(self.min_len))
                self._error(errh, err_str, '4', elem_val)
                valid = False
            if len(elem_strip) > int(self.max_len):
                err_str = 'Element "%s" (%s) is too long: "%s" should only be %i characters' % \
                    (self.name, self.refdes, elem_val, int(self.max_len))
                self._error(errh, err_str, '5', elem_val)
                valid = False
        else:
            if len(elem_val) < int(self.min_len):
                err_str = 'Data element "%s" (%s) is too short: "%s" should be at least %i characters' % \
                    (self.name, self.refdes, elem_val, int(self.min_len))
                self._error(errh, err_str, '4', elem_val)
                valid = False
            if len(elem_val) > int(self.max_len):
                err_str = 'Element "%s" (%s) is too long: "%s" should only be %i characters' % \
                    (self.name, self.refdes, elem_val, int(self.max_len))
                self._error(errh, err_str, '5', elem_val)
                valid = False

        if self.data_type in ['AN', 'ID'] and elem_val[-1] == ' ':
            if len(elem_val.rstrip()) >= int(self.min_len):
                err_str = 'Element "%s" (%s) has unnecessary trailing spaces. (%s)' % \
                    (self.name, self.refdes, elem_val)
                self._error(errh, err_str, '6', elem_val)
                valid = False
            
        if not self._is_valid_code(elem_val, errh, check_dte):
            valid = False
           
        if not IsValidDataType(elem_val, self.data_type, self.root.param.get('charset')):
            if self.data_type == 'DT':
                err_str = 'Data element "%s" (%s) contains an invalid date (%s)' % \
                    (self.name, self.refdes, elem_val)
                self._error(errh, err_str, '8', elem_val)
                valid = False
            elif self.data_type == 'TM':
                err_str = 'Data element "%s" (%s) contains an invalid time (%s)' % \
                    (self.name, self.refdes, elem_val)
                self._error(errh, err_str, '9', elem_val)
                valid = False
            else:
                err_str = 'Data element "%s" (%s) is type %s, contains an invalid character(%s)' % \
                    (self.name, self.refdes, self.data_type, elem_val)
                self._error(errh, err_str, '6', elem_val)
                valid = False
        return valid

    def _is_valid_code(self, elem_val, errh, check_dte=None):
        """
        @rtype: boolean
        """
        bValidCode = False
        if len(self.valid_codes) == 0 and self.external_codes is None:
            bValidCode = True
        if elem_val in self.valid_codes:
            bValidCode = True
        if self.external_codes is not None and \
            self.root.ext_codes.IsValid(self.external_codes, elem_val, check_dte):
            bValidCode = True
        if not bValidCode:
            err_str = '(%s) is not a valid code for %s (%s)' % (elem_val, self.name, self.refdes)
            self._error(errh, err_str, '7', elem_val)
            return False
        return True
        

    def get_seg_count(self):
        """
        """
        pass

    def is_element(self):
        """
        @rtype: boolean
        """
        return True


############################################################
# Composite Interface
############################################################
class composite_if(x12_node):
    def __init__(self, root, parent):
        """
        Get the values for this composite
        @param parent: parent node 
        """

        #global reader
        reader = root.reader
        x12_node.__init__(self)

        self.children = []
        self.root = root
        self.parent = parent
        self.path = ''
        self.base_name = 'composite'
        self.base_level = reader.Depth()
        self.check_dte = '20030930'

        #self.id = None
        self.name = None
        self.data_ele = None
        self.usage = None
        self.seq = None
        self.refdes = None

        self.cur_level = reader.Depth()
        #self.logger = logging.getLogger('pyx12')
        
        ret = 1 
        while ret == 1:
            #print '--- segment while'
            #print 'seg', reader.NodeType(), reader.Depth(), reader.Name()
            tmpNodeType = reader.NodeType()
            if tmpNodeType == NodeType['element_start']:
                #if reader.Name() in ('map', 'transaction', 'loop', 'segment', 'element'):
                #    print 's'*reader.Depth(), reader.Depth(),  self.base_level, reader.NodeType(), reader.Name()
                cur_name = reader.Name()
                if cur_name == 'composite':
                    self.base_level = reader.Depth()
                    self.base_name = 'composite'
                elif cur_name == 'element':
                    self.children.append(element_if(self.root, self))
                    if len(self.children) > 1:
                        self.children[-1].prev_node = self.children[-2]
                        self.children[-2].next_node = self.children[-1]
                    
                #if self.cur_level < reader.Depth():
                #    self.cur_path = os.path.join(self.cur_path, cur_name)
                #elif self.cur_level > reader.Depth():
                #    self.cur_path = os.path.dirname(self.cur_path)
                self.cur_level = reader.Depth()
            elif tmpNodeType == NodeType['element_end']:
                #print '--', reader.Name(), self.base_level, reader.Depth(), reader.Depth() <= self.base_level 
                if reader.Depth() <= self.base_level:
                    ret = reader.Read()
                    if ret == -1:
                        raise errors.XML_Reader_Error, 'Read Error'
                    elif ret == 0:
                        raise errors.XML_Reader_Error, 'End of Map File'
                    break 
                #if reader.Name() == 'transaction':
                #    return
                #    pass
                cur_name = ''
                
            elif tmpNodeType == NodeType['text'] and self.base_level + 2 == reader.Depth():
                #print cur_name, reader.Value()
                if cur_name == 'name':
                    self.name = reader.Value()
                elif cur_name == 'data_ele':
                    self.data_ele = reader.Value()
                elif cur_name == 'usage':
                    self.usage = reader.Value()
                elif cur_name == 'seq':
                    self.seq = int(reader.Value())
                elif cur_name == 'refdes':
                    self.refdes = reader.Value()

            ret = reader.Read()
            if ret == -1:
                raise errors.XML_Reader_Error, 'Read Error'
            elif ret == 0:
                raise errors.XML_Reader_Error, 'End of Map File'
                
    def _error(self, errh, err_str, err_cde, elem_val):
        """
        Forward the error to an error_handler
        """
        errh.ele_error(err_cde, err_str, elem_val)
            #, pos=self.seq, data_ele=self.data_ele)
        
    def debug_print(self):
        sys.stdout.write(self.__repr__())
        for node in self.children:
            node.debug_print()

    def __repr__(self):
        """
        @rtype: string
        """
        out = '%s%s "%s"' % (str(' '*self.base_level), \
            self.id, self.name)
        if self.usage: 
            out += '  usage %s' % (self.usage)
        if self.seq: 
            out += '  seq %i' % (self.seq)
        if self.refdes: 
            out += '  refdes %s' % (self.refdes)
        out += '\n'
        return out

    def xml(self):
        """
        Sends an xml representation of the composite to stdout
        """
        sys.stdout.write('<composite>\n')
        for sub_elem in self.children:
            sub_elem.xml()
        sys.stdout.write('</composite>\n')

    def is_valid(self, comp_data, errh, check_dte=None):
        """
        Validates the composite
        @param comp_data: data composite instance, has multiple values
        @param errh: instance of error_handler
        @rtype: boolean
        """
        valid = True
        if (comp_data is None or comp_data.is_empty()) and self.usage in ('N', 'S'):
            return True

        if self.usage == 'R':
            good_flag = False
            for sub_ele in comp_data:
                if sub_ele is not None and len(sub_ele.get_value()) > 0:
                    good_flag = True
                    break
            if not good_flag:
                err_str = 'At least one component of composite "%s" (%s) is required' % \
                    (self.name, self.refdes)
                errh.ele_error('2', err_str, None)
                return False

        if self.usage == 'N' and not comp_data.is_empty():
            err_str = 'Composite "%s" (%s) is marked as Not Used' % (self.name, self.refdes)
            errh.ele_error('5', err_str, None)
            return False

        #try:
        #    a = len(comp_data)
        #except:
        #    pdb.set_trace()
        if len(comp_data) > self.get_child_count():
            err_str = 'Too many sub-elements in composite "%s" (%s)' % (self.name, self.refdes)
            errh.ele_error('3', err_str, None)
            valid = False
        for i in xrange(min(len(comp_data), self.get_child_count())):
            valid &= self.get_child_node_by_idx(i).is_valid(comp_data[i], errh, check_dte)
        for i in xrange(min(len(comp_data), self.get_child_count()), \
                self.get_child_count()): 
            if i < self.get_child_count():
                #Check missing required elements
                valid &= self.get_child_node_by_idx(i).is_valid(None, errh)
        return valid

#    def getnodebypath(self, path):
#        """
#        """
#        pathl = path.split('/')
#        if len(pathl) <=2: return None
#        for child in self.children:
#            node = child.getnodebypath(pathl[2:])
#            if node != None:
#                return node
#        return None
           
    def is_composite(self):
        """
        @rtype: boolean
        """
        return True

class Pickle_Errors(Exception):
    """Class for map pickling errors."""


def load_map_file(map_file, param):
    """
    Loads the map by pickle if available
    @param map_file: absolute path for file
    @type map_file: string
    @rtype: pyx12.map_if
    """
    logger = logging.getLogger('pyx12.pickler')
    map_path = param.get('map_path')
    pickle_path = param.get('pickle_path')
    pickle_file = '%s.%s' % (os.path.splitext(os.path.join(pickle_path, \
        map_file))[0], 'pkl')
    map_full = os.path.join(map_path, map_file)
    try:
        if os.stat(map_full)[ST_MTIME] < os.stat(pickle_file)[ST_MTIME]:
            imap = cPickle.load(open(pickle_file))
            if imap.cur_path != '/transaction' or len(imap.children) == 0 \
                or imap.src_version != '$Revision$':
                raise Pickle_Errors, "reload map"
            logger.debug('Map %s loaded from pickle %s' % (map_full, pickle_file))
        else:
            raise Pickle_Errors, "reload map"
    except:
        try:
            logger.debug('Create map from %s' % (map_full))
            imap = map_if(map_file, param)
        except:
            raise errors.EngineError, 'Load of map file failed: %s%s' % \
                (param.get('map_path'), map_file)
        #try:
            #pdb.set_trace()
        #    cPickle.dump(map, open(pickle_file,'w'))
        #except:
        #    logger.debug('Pickle of map %s failed' % (map_file))
            #os.remove(pickle_file)
            #raise
    return imap

def is_syntax_valid(seg_data, syn):
    """
    Verifies the segment against the syntax
    @param seg_data: data segment instance
    @type seg_data: pyx12.segment
    @param syn: list containing the syntax type, and the indices of elements
    @type syn: list[string]
    @rtype: tuple(boolean, error string)
    """
    # handle intra-segment dependancies
    if len(syn) < 3:
        err_str = 'Syntax string must have at least two comparators (%s)' \
            % (syntax_str(syn))
        return (False, err_str)

    if syn[0] == 'P':
        #pdb.set_trace()
        count = 0
        for s in syn[1:]:
            if len(seg_data) >= s and seg_data[s-1].get_value() != '':
                count += 1
        if count != 0 and count != len(syn)-1:
            err_str = 'Syntax Error (%s): If any of %s is present, then all are required'\
                % (syntax_str(syn), syntax_ele_id_str(seg_data.get_seg_id(), syn[1:]))
            return (False, err_str)
        else:
            return (True, None)
    elif syn[0] == 'R':
        count = 0
        for s in syn[1:]:
            if len(seg_data) >= s and seg_data[s-1].get_value() != '':
                count += 1
        if count == 0:
            err_str = 'Syntax Error (%s): At least one element is required' % \
                (syntax_str(syn))
            return (False, err_str)
        else:
            return (True, None)
    elif syn[0] == 'E':
        count = 0
        for s in syn[1:]:
            if len(seg_data) >= s and seg_data[s-1].get_value() != '':
                count += 1
        if count > 1:
            err_str = 'Syntax Error (%s): At most one of %s may be present'\
                % (syntax_str(syn), syntax_ele_id_str(seg_data.get_seg_id(), syn[1:]))
            return (False, err_str)
        else:
            return (True, None)
    elif syn[0] == 'C':
        # If the first is present, then all others are required
        if len(seg_data) >= syn[1] and seg_data[syn[1]-1].get_value() != '':
            count = 0
            for s in syn[2:]:
                if len(seg_data) >= s and seg_data[s-1].get_value() != '':
                    count += 1
            if count != len(syn)-2:
                if len(syn[2:]) > 1: verb = 'are'
                else: verb = 'is'
                err_str = 'Syntax Error (%s): If %s%02i is present, then %s %s required'\
                    % (syntax_str(syn), seg_data.get_seg_id(), syn[1], \
                    syntax_ele_id_str(seg_data.get_seg_id(), syn[2:]), verb)
                return (False, err_str)
            else:
                return (True, None)
        else:
            return (True, None)
    elif syn[0] == 'L':
        if seg_data[syn[1]-1].get_value() != '':
            count = 0
            for s in syn[2:]:
                if len(seg_data) >= s and seg_data[s-1].get_value() != '':
                    count += 1
            if count == 0:
                err_str = 'Syntax Error (%s): If %s%02i is present, then at least one of '\
                    % (syntax_str(syn), seg_data.get_seg_id(), syn[1])
                err_str += syntax_ele_id_str(seg_data.get_seg_id(), syn[2:])
                err_str += ' is required'
                return (False, err_str)
            else:
                return (True, None)
        else:
            return (True, None)
    #raise errors.EngineError
    return (False, 'Syntax Type %s Not Found' % (syntax_str(syn)))
        
def syntax_str(syntax):
    """
    @rtype: string
    """
    output = syntax[0]
    for i in syntax[1:]:
        output += '%02i' % (i)
    return output

def syntax_ele_id_str(seg_id, ele_pos_list):
    """
    @rtype: string
    """
    output = ''
    output += '%s%02i' % (seg_id, ele_pos_list[0])
    for i in range(len(ele_pos_list)-1):
        if i == len(ele_pos_list)-2:    
            output += ' or %s%02i' % (seg_id, ele_pos_list[i+1])
        else:
            output += ', %s%02i' % (seg_id, ele_pos_list[i+1])
    return output
        
    
class IsValidError(Exception): pass

def IsValidDataType(str_val, data_type, charset = 'B'):
    """
    Is str_val a valid X12 data value

    @param str_val: data value to validate
    @type str_val: string
    @param data_type: X12 data element identifier
    @type data_type: string
    @param charset: [optional] - 'B' for Basic X12 character set, 'E' for extended
    @type charset: string
    @rtype: boolean
    """
    import re
    #print str_val, data_type, charset
    if not data_type:
        return True
    if type(str_val) is not StringType:
        return False

    try:
        if data_type[0] == 'N':
            m = re.compile("^-?[0-9]+", re.S).search(str_val)
            if not m:
                raise IsValidError # nothing matched
            if m.group(0) != str_val:  # matched substring != original, bad
                raise IsValidError # nothing matched
        elif data_type == 'R':
            m = re.compile("^-?[0-9]*(\.[0-9]+)?", re.S).search(str_val)
            if not m: 
                raise IsValidError # nothing matched
            if m.group(0) != str_val:  # matched substring != original, bad
                raise IsValidError 
        elif data_type in ('ID', 'AN'):
            if charset == 'E':  # extended charset
                m = re.compile("[^A-Z0-9!\"&'()*+,\-\\\./:;?=\sa-z%~@\[\]_{}\\\|<>#$\s]", re.S).search(str_val)
                if m and m.group(0):
                    raise IsValidError 
            elif charset == 'B':  # basic charset:
                m = re.compile("[^A-Z0-9!\"&'()*+,\-\\\./:;?=\s]", re.S).search(str_val)
                if m and m.group(0):  # invalid string found
                    raise IsValidError 
        elif data_type == 'RD8':
            (start, end) = str_val.split('-')
            return IsValidDataType(start, 'D8', charset) and IsValidDataType(end, 'D8', charset) 
        elif data_type in ('DT', 'D8', 'D6'):
            if data_type == 'D8' and len(str_val) != 8:
                raise IsValidError
            if data_type == 'D6' and len(str_val) != 6:
                raise IsValidError
            m = re.compile("[^0-9]+", re.S).search(str_val)  # first test date for non-numeric chars
            if m:  # invalid string found
                raise IsValidError 
            if len(str_val) in (6, 8, 12): # valid lengths for date
                try:
                    if 6 == len(str_val):  # if 2 digit year, add CC
                        if str_val[0:2] < 50:
                            str_val = '20' + str_val
                        else:
                            str_val = '19' + str_val
                    month = int(str_val[4:6])  # check month
                    if month < 1 or month > 12:
                        raise IsValidError
                    day = int(str_val[6:8])  # check day
                    if month in (1, 3, 5, 7, 8, 10, 12):  # 31 day month
                        if day < 1 or day > 31:
                            raise IsValidError
                    elif month in (4, 6, 9, 11):  # 30 day month
                        if day < 1 or day > 30:
                            raise IsValidError
                    else: # else 28 day
                        year = int(str_val[0:4])  # get year
                        if not year%4 and not (not year%100 and year%400):
                        #if not (year % 4) and ((year % 100) or (not (year % 400)) ):  # leap year
                            if day < 1 or day > 29:
                                raise IsValidError
                        elif day < 1 or day > 28:
                            raise IsValidError
                    if len(str_val) == 12:
                        if not IsValidDataType(str_val[8:12], 'TM', charset):
                            raise IsValidError
                except TypeError:
                    raise IsValidError
            else:
                raise IsValidError 
        elif data_type == 'TM':
            m = re.compile("[^0-9]+", re.S).search(str_val)  # first test time for non-numeric chars
            if m:  # invalid string found
                raise IsValidError 
            elif str_val[0:2] > '23' or str_val[2:4] > '59':  # check hour, minute segment
                raise IsValidError 
            elif len(str_val) > 4:  # time contains seconds
                if len(str_val) < 6:  # length is munted
                    raise IsValidError 
                elif str_val[4:6] > '59':  # check seconds
                    raise IsValidError 
                # check decimal seconds here in the future
                elif len(str_val) > 8:
                    # print 'unhandled decimal seconds encountered'
                    raise IsValidError 
        elif data_type == 'B': pass
    except IsValidError:
        return False
    #    else:  
    #        # print 'data_type parameter is not valid, abort'
    #        return 1
    return True
