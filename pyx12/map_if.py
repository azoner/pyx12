# Interface to a X12N IG Map
#
#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#               John Holland <jholland@kazoocmh.org> <john@zoner.org>
#
#    All rights reserved.
#
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#
#       1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer. 
#       
#       2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution. 
#       
#       3. The name of the author may not be used to endorse or promote
#       products derived from this software without specific prior written
#       permission. 
#
#       THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#       IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#       WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#       DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
#       INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#       (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#       SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#       HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#       STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#       IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#       POSSIBILITY OF SUCH DAMAGE.

"""
Interface to a X12N IG Map
"""
import cPickle
import libxml2
import logging
import os.path
import pdb
import string
import sys
from types import *
from stat import ST_MTIME
from stat import ST_SIZE

# Intrapackage imports
import errors
import codes
from utils import *

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

    def __del__(self):
        pass

    def __rept__(self):
        return self.name

    def getnodebypath(self, path):
        """
        Class:      x12_node
        Name:       getnodebypath
        """
        pathl = path.split('/')
        if len(pathl) == 0: return None
        for child in self.children:
            if child.id == pathl[0]:
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
        Name:    get_child_node_by_idx
        Desc:    
        Params:  
 
        Returns: 

        Note: idx is zero based
        """
        if idx >= len(self.children):
            return None
        else:
            return self.children[idx]
            
    def get_path(self):
        """
        Class:      x12_node 
        Name:       get_path 
        Desc:    
                 
        Returns: string of path - XPath style
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
        return False

    def is_map_root(self):
        return False

    def is_loop(self):
        return False
    
    def is_segment(self):
        return False
    
    def is_element(self):
        return False
    
    def is_composite(self):
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
        Class:      map_if
        Params:     params - map of parameters
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
        self.ext_codes = codes.ExternalCodes(param.get_param('map_path'), \
            param.get_param('exclude_external_codes'))
        try:
            map_path = param.get_param('map_path')
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
                
    def debug_print(self):
        sys.stdout.write(self.__repr__())
        for node in self.children:
            node.debug_print()

    def __repr__(self):
        #out = '%s%s %s %s %s\n' % (str(' '*self.base_level), \
        #   self.base_name, self.base_level, self.id, self.name)
        #out = '%s%s' % (str(' '*self.base_level), self.base_name)
        #out += '%sid %s\n' % (str(' '*(self.base_level+1)), self.id)
        #out += '%sname %s\n' % (str(' '*(self.base_level+1)), self.name)
        return '%s\n' % (self.id)

    def __path_parent__(self):
        return os.path.basename(os.path.dirname(self.cur_path))

    def get_path(self):
        return self.path

    def getnodebypath(self, path):
        """
        Class:      map_if
        Name:       getnodebypath
        """
        pathl = path.split('/')[1:]
        if len(pathl) == 0: return None
        #logger.debug('%s %s %s' % (self.base_name, self.id, pathl[1]))
        for child in self.children:
            if child.id == pathl[0]:
                if len(pathl) == 1:
                    return child
                else:
                    return child.getnodebypath(string.join(pathl[1:],'/'))
        return None
            
    def is_map_root(self):
        return True

    def reset_cur_count(self):
        for child in self.children:
            if child.is_loop():
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
        Name:    __init__
        Desc:    
        Params:  
 
        Returns: 

        Note: Should be entered with a loop node current
        """
        x12_node.__init__(self)
        self.root = root
        self.parent = parent
        self.index = my_index
        self.children = []
        self.path = ''
        self.base_name = 'loop'
        self.cur_count = 0
        
        self.id = None
        self.name = None
        self.usage = None
        self.seq = None
        self.repeat = None
        
        reader = self.root.reader

        index = 0
        self.base_level = reader.Depth()
#        if parent == None:
#            self.path = id
#        else:
#            self.path = path + '/' + id

        self.cur_level = reader.Depth()
        
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
                if cur_name == 'id' and self.base_name == 'loop':
                    self.id = reader.Value()
                    self.path = self.id
                elif cur_name == 'name' and self.base_name == 'loop':
                    self.name = reader.Value()
                elif cur_name == 'usage' and self.base_name == 'loop':
                    self.usage = reader.Value()
                elif cur_name == 'seq' and self.base_name == 'loop':
                    self.seq = reader.Value()
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
        if self.seq: 
            out += '  seq: %s' % (self.seq)
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

#    def is_valid(self, seg, errh):
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
        return True

    def reset_cur_count(self):
        for child in self.children:
            if child.is_loop():
                child.reset_cur_count()

############################################################
# Segment Interface
############################################################
class segment_if(x12_node):
    """
    """
    def __init__(self, root, parent, my_index):
        """
        Class: segment_if
        Name:    __init__
        Desc:    
        Params: parent - parent node 
                 
        Note: Should be entered with a segment node current
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
                if cur_name == 'id' and self.base_name == 'segment':
                    self.id = reader.Value()
                    self.path = self.id
                elif cur_name == 'end_tag' and self.base_name == 'segment':
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
        Class: segment_if
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

    def get_elemval_by_id(self, seg, id):
        """
        Class: segment_if
        Name:  get_elemval_by_id  
        Desc:  Return the value of an element or sub-element identified by the id
        Params: seg - segment object to search
                id - string 
        Returns: value of the element
        """
        for child in self.children:
            if child.is_element():
                if child.id == id:
                    return seg[child.seq].get_value()
            elif child.is_composite():
                for child in self.children:
                    if child.is_element():
                        if child.id == id:
                            return seg[child.seq]
        return None

    def get_max_repeat(self):
        if self.max_use is None or self.max_use == '>1':
            return MAXINT
        return int(self.max_use)
    
    def get_parent(self):
        """
        Class: segment_if
        Name:    
        Desc:    
        Params:  
                 
        Returns: ref to parent class instance
        """
        return self.parent

#    def get_seg_count(self):
#        """
#        Class: segment_if
#        Name:    
#        Desc:    
#        Params:  
#                 
#        Returns: 
#        """
#        pass

    def is_first_seg_in_loop(self):
        if self is self.get_parent().children[0]:
            return True
        else:
            return False

    def is_match(self, seg):
        """
        Class: segment_if
        Name: is_match
        Desc: is segment given a match to this node?
        Params:  seg - list of element values
        Returns: boolean
        """
        if seg.get_seg_id() == self.id:
            if self.children[0].is_element() \
                and self.children[0].data_type == 'ID' \
                and len(self.children[0].valid_codes) > 0 \
                and seg[1] not in self.children[0].valid_codes:
                #logger.debug('is_match: %s %s' % (seg.get_seg_id(), seg[1]), self.children[0].valid_codes)
                #pdb.set_trace()
                return False
            elif self.children[0].is_composite() \
                and self.children[0].children[0].data_type == 'ID' \
                and len(self.children[0].children[0].valid_codes) > 0 \
                and seg[1][0] not in self.children[0].children[0].valid_codes:
                return False
            elif seg.get_seg_id() == 'HL' and self.children[2].is_element() \
                and len(self.children[2].valid_codes) > 0 \
                and seg[3] not in self.children[2].valid_codes:
                return False
            return True
        else:
            return False

    def is_segment(self): return True

    def is_valid(self, seg, errh):
        """
        Class:      segment_if
        Name:       is_valid
        Desc:    
        Params:     seg - data segment list 
                    errh - instance of error_handler
        Returns: boolean
        """
        valid = True
        child_count = self.get_child_count()
        if len(seg) > child_count:
            child_node = self.get_child_node_by_idx(child_count+1)
            err_str = 'Too many elements in segment %s. Has %i, should have %i' % \
                (seg.get_seg_id(), len(seg), child_count)
            #self.logger.error(err_str)
            err_value = seg[child_count+1]
            errh.seg_error('3', err_str, err_value)
            valid = False

        for i in xrange(len(seg)):
            #self.logger.debug('i=%i, len(seg)=%i / child_count=%i' % \
            #   (i, len(seg), self.get_child_count()))
            child_node = self.get_child_node_by_idx(i)
            if i < len(seg):
                #if type(seg[i+1]) is ListType: # composite
                #self.logger.debug('i=%i, elem=%s, id=%s' % (i, seg[i+1], child_node.id))
                if child_node.is_composite():
                    # Validate composite
                    comp = seg[i+1]
                    subele_count = child_node.get_child_count()
                    if len(comp) > subele_count:
                        subele_node = child_node.get_child_node_by_idx(subele_count+1)
                        err_str = 'Too many sub-elements in composite %s' % (subele_node.refdes)
                        err_value = comp[subele_count]
                        errh.seg_error('3', err_str, err_value)
                    valid &= child_node.is_valid(seg[i+1], errh, self.check_dte)
                elif child_node.is_element():
                    # Validate Element
                    valid &= child_node.is_valid(seg[i+1], errh, self.check_dte)
        for i in xrange(len(seg), self.get_child_count()):
            #missing required elements
            valid &= child_node.is_valid(None, errh)
                
        for syn in self.syntax:
            (bResult, err_str) = is_syntax_valid(seg, syn)
            if not bResult:
                #pdb.set_trace()
                errh.ele_error('2', err_str, None)
                valid &= False

        return valid

    def _split_syntax(self, syntax):
        """
        Class:      segment_if
        Desc:       Split a Syntax string into a list
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
        Class: element_if
        Name:    __init__
        Desc:    
        Params: parent - parent node 
                 
        Returns: 
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
                elif cur_name == 'refdes':
                    self.refdes = reader.Value()
                    self.id = self.refdes
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
        Class: element_if
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
   
    def __del__(self):
        pass

    def __error__(self, errh, err_str, err_cde, elem_val):
        """
        Class:      element_if
        Name:       __error__
        Desc:       Forward the error to an error_handler
        Params:  
        """
        errh.ele_error(err_cde, err_str, elem_val) #, pos=self.seq, data_ele=self.data_ele)
        
    def __valid_code__(self, code):
        """
        Class:  element_if
        Name:   __valid_code__
        Desc:   Verify the x12 element value is in the given list of valid codes
        Params:  
        Returns: True if found, else False
        """
        #if not self.valid_codes:
        #    return True
        if code in self.valid_codes:
            return True
        return False

    def get_parent(self):
        """
        Class: element_if
        Name:    
        Desc:    
        Params:  
                 
        Returns: ref to parent class instance
        """
        return self.parent

    def is_match(self):
        """
        Class: element_if
        Name:    
        Desc:    
        Params:  
                 
        Returns: boolean
        """
        # match also by ID
        pass

    def is_valid(self, elem_val, errh, check_dte=None):
        """
        Class:  element_if
        Name:   is_valid 
        Desc:    
        Params:  
            elem_val - value of element data
            errh - instance of error_handler
            check_dte - date string to check against (YYYYMMDD)
                 
        Returns: boolean
        """
        errh.add_ele(self)

        if type(elem_val) is ListType:
            err_str = 'Data element %s is an invalid composite' % (self.refdes)
            self.__error__(errh, err_str, '6', elem_val)

        if elem_val == '' or elem_val is None:
            if self.usage in ('N', 'S'):
                return True
            elif self.usage == 'R':
                if self.seq != 1 or not self.parent.is_composite() or self.parent.usage == 'R':
                    err_str = 'Mandatory data element "%s" (%s) is missing' % (self.name, self.refdes)
                    self.__error__(errh, err_str, '1', None)
                    return False
                else:
                    return True
                
        valid = True
        if (not self.data_type is None) and (self.data_type == 'R' or self.data_type[0] == 'N'):
            elem = string.replace(string.replace(elem_val, '-', ''), '.', '')
            if len(elem) < int(self.min_len):
                err_str = 'Data element %s is too short: "%s" should be at least %i characters' % \
                    (self.refdes, elem_val, int(self.min_len))
                self.__error__(errh, err_str, '4', elem_val)
                valid = False
            if len(elem) > int(self.max_len):
                err_str = 'Element %s is too long: "%s" should only be %i characters' % (self.refdes,\
                    elem_val, int(self.max_len))
                self.__error__(errh, err_str, '5', elem_val)
                valid = False
        else:
            if len(elem_val) < int(self.min_len):
                err_str = 'Data element %s is too short: "%s" should be at least %i characters' % \
                    (self.refdes, elem_val, int(self.min_len))
                self.__error__(errh, err_str, '4', elem_val)
                valid = False
            if len(elem_val) > int(self.max_len):
                err_str = 'Element %s is too long: "%s" should only be %i characters' % (self.refdes,\
                    elem_val, int(self.max_len))
                self.__error__(errh, err_str, '5', elem_val)
                valid = False

        if self.data_type in ['AN', 'ID'] and elem_val[-1] == ' ':
            if len(elem_val.rstrip()) >= int(self.min_len):
                err_str = 'Element %s has unnecessary trailing spaces. (%s)' % \
                    (self.refdes, elem_val)
                self.__error__(errh, err_str, '6', elem_val)
                valid = False
            
        if not self.__is_valid_code__(elem_val, errh, check_dte):
            valid = False
           
        if not IsValidDataType(elem_val, self.data_type, self.root.param.get_param('charset')):
            if self.data_type == 'DT':
                err_str = 'Data element %s contains an invalid date (%s)' % \
                    (self.refdes, elem_val)
                self.__error__(errh, err_str, '8', elem_val)
                valid = False
            elif self.data_type == 'TM':
                err_str = 'Data element %s contains an invalid time (%s)' % \
                    (self.refdes, elem_val)
                self.__error__(errh, err_str, '9', elem_val)
                valid = False
            else:
                err_str = 'Data element %s is type %s, contains an invalid character(%s)' % \
                    (self.refdes, self.data_type, elem_val)
                self.__error__(errh, err_str, '6', elem_val)
                valid = False
        return valid

    def __is_valid_code__(self, elem_val, errh, check_dte=None):
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
            self.__error__(errh, err_str, '7', elem_val)
            return False
        return True
        


    def get_seg_count(self):
        """
        Class: element_if
        Name:    
        Desc:    
        Params:  
                 
        Returns: 
        """
        pass

    def is_element(self):
        return True


############################################################
# Composite Interface
############################################################
class composite_if(x12_node):
    def __init__(self, root, parent):
        """
        Class: composite_if
        Name:    __init__
        Desc:    Get the values for this composite
        Params:         parent - parent node 
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
                
    def __error__(self, errh, err_str, err_cde, elem_val):
        """
        Class:      composite_if
        Name:       __error__
        Desc:       Forward the error to an error_handler
        Params:  
        """
        errh.ele_error(err_cde, err_str, elem_val)
            #, pos=self.seq, data_ele=self.data_ele)
        
    def debug_print(self):
        sys.stdout.write(self.__repr__())
        for node in self.children:
            node.debug_print()

    def __repr__(self):
        """
        Class: composite_if
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
        Class:      composite_if
        Name:       xml
        Desc:       Sends an xml representation of the composite to stdout
        Params:  
        Returns: 
        """
        sys.stdout.write('<composite>\n')
        for sub_elem in self.children:
            sub_elem.xml()
        sys.stdout.write('</composite>\n')

    def is_valid(self, comp, errh, check_dte=None):
        """
        Class:      composite_if
        Name:       validate
        Desc:       Validates the composite
        Params:     comp - composite value or list
                    errh - instance of error_handler
        Returns:    True on success
        """
        valid = True
        if comp is None or len(comp) == 0 and self.usage == 'N':
            return True

        if not type(comp) is ListType: # composite
            comp = [comp] 

        if self.usage == 'R':
            good_flag = False
            for sub_ele in comp:
                if sub_ele is not None and len(sub_ele) > 0:
                    good_flag = True
                    break
            if not good_flag:
                err_str = 'At least one component of composite "%s" is required' % (self.name)
                errh.ele_error('2', err_str, None)
                return False

        if len(comp) > self.get_child_count():
            err_str = 'Too many sub-elements in composite %s' % (self.refdes)
            errh.ele_error('3', err_str, None)
            valid = False
        for i in xrange(len(comp)):
            valid &= self.get_child_node_by_idx(i).is_valid(comp[i], errh, check_dte)
        for i in xrange(len(comp), self.get_child_count()): #Check missing required elements
            valid &= self.get_child_node_by_idx(i).is_valid(None, errh)
        return valid

#    def getnodebypath(self, path):
#        """
#        Class:  composite_if
#        Name:    
#        Desc:    
#        Params:  
#        Returns: 
#        """
#        pathl = path.split('/')
#        if len(pathl) <=2: return None
#        for child in self.children:
#            node = child.getnodebypath(pathl[2:])
#            if node != None:
#                return node
#        return None
           
    def is_composite(self):
        return True

class Pickle_Errors(Exception):
    """Class for map pickling errors."""


def load_map_file(map_file, param):
    """
    map_file - absolute path for file
    """
    logger = logging.getLogger('pyx12.pickler')
    map_path = param.get_param('map_path')
    pickle_path = param.get_param('pickle_path')
    pickle_file = '%s.%s' % (os.path.splitext(os.path.join(pickle_path, \
        map_file))[0], 'pkl')
    map_full = os.path.join(map_path, map_file)
    try:
        if os.stat(map_full)[ST_MTIME] < os.stat(pickle_file)[ST_MTIME]:
            map = cPickle.load(open(pickle_file))
            if map.cur_path != '/transaction' or len(map.children) == 0 \
                or map.src_version != '$Revision$':
                raise Pickle_Errors, "reload map"
            logger.debug('Map %s loaded from pickle %s' % (map_full, pickle_file))
        else:
            raise Pickle_Errors, "reload map"
    except:
        try:
            logger.debug('Create map from %s' % (map_full))
            map = map_if(map_file, param)
        except:
            raise errors.EngineError, 'Load of map file failed: %s%s' % \
                (param.get_param('map_path'), map_file)
        #try:
            #pdb.set_trace()
        #    cPickle.dump(map, open(pickle_file,'w'))
        #except:
        #    logger.debug('Pickle of map %s failed' % (map_file))
            #os.remove(pickle_file)
            #raise
    return map

def is_syntax_valid(seg, syn):
    """
    Name:       is_syntax_valid
    Desc:       Verifies the syntax 
    Params:     seg - data segment list 
                syn - list containing the syntax type, 
                    and the indices of elements
    Returns: (boolean, error string)
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
            if len(seg) >= s and seg[s].get_value() != '':
                count += 1
        if count != 0 and count != len(syn)-1:
            err_str = 'Syntax Error (%s): If any of %s is present, then all are required'\
                % (syntax_str(syn), syntax_ele_id_str(seg.get_seg_id(), syn[1:]))
            return (False, err_str)
        else:
            return (True, None)
    elif syn[0] == 'R':
        count = 0
        for s in syn[1:]:
            if len(seg) >= s and seg[s].get_value() != '':
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
            if len(seg) >= s and seg[s].get_value() != '':
                count += 1
        if count > 1:
            err_str = 'Syntax Error (%s): At most one of %s may be present'\
                % (syntax_str(syn), syntax_ele_id_str(seg.get_seg_id(), syn[1:]))
            return (False, err_str)
        else:
            return (True, None)
    elif syn[0] == 'C':
        # If the first is present, then all others are required
        if len(seg) >= syn[1] and seg[syn[1]].get_value() != '':
            count = 0
            for s in syn[2:]:
                if len(seg) >= s and seg[s].get_value() != '':
                    count += 1
            if count != len(syn)-2:
                if len(syn[2:]) > 1: verb = 'are'
                else: verb = 'is'
                err_str = 'Syntax Error (%s): If %s%02i is present, then %s %s required'\
                    % (syntax_str(syn), seg.get_seg_id(), syn[1], syntax_ele_id_str(seg.get_seg_id(), syn[2:]), verb)
                return (False, err_str)
            else:
                return (True, None)
        else:
            return (True, None)
    elif syn[0] == 'L':
        if seg[syn[1]].get_value() != '':
            count = 0
            for s in syn[2:]:
                if len(seg) >= s and seg[s].get_value() != '':
                    count += 1
            if count == 0:
                err_str = 'Syntax Error (%s): If %s%02i is present, then at least one of '\
                    % (syntax_str(syn), seg.get_seg_id(), syn[1])
                err_str += syntax_ele_id_str(seg.get_seg_id(), syn[2:])
                err_str += ' is required'
                return (False, err_str)
            else:
                return (True, None)
        else:
            return (True, None)
    #raise errors.EngineError
    return (False, 'Syntax Type %s Not Found' % (syntax_str(syn)))
        
def syntax_str(syntax):
    str = syntax[0]
    for i in syntax[1:]:
        str += '%02i' % (i)
    return str

def syntax_ele_id_str(seg_id, ele_pos_list):
    str = ''
    str += '%s%02i' % (seg_id, ele_pos_list[0])
    for i in range(len(ele_pos_list)-1):
        if i == len(ele_pos_list)-2:    
            str += ' or %s%02i' % (seg_id, ele_pos_list[i+1])
        else:
            str += ', %s%02i' % (seg_id, ele_pos_list[i+1])
    return str
        
    

