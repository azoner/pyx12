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
#       Redistribution and use in source and binary forms, with or without modification, 
#       are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice, this list 
#          of conditions and the following disclaimer. 
#       
#       2. Redistributions in binary form must reproduce the above copyright notice, this 
#          list of conditions and the following disclaimer in the documentation and/or other 
#          materials provided with the distribution. 
#       
#       3. The name of the author may not be used to endorse or promote products derived 
#          from this software without specific prior written permission. 
#
#       THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED 
#       WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
#       MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
#       EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#       EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
#       OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
#       INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
#       CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
#       ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
#       THE POSSIBILITY OF SUCH DAMAGE.

# THIS IS PRE-ALPHA CODE.  IT DOES NOT WORK. 

"""
Interface to a X12N IG Map
"""
import libxml2
import logging
import os.path
import pdb
import string
import sys
from types import *

# Intrapackage imports
import errors
import codes
from utils import *

#Global Variables
subele_term = None
__version__ = "0.1.0"
reader = None

codes = codes.ExternalCodes()

NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3, 'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8, 'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12}

MAXINT = 2147483647

############################################################
# X12 Node Superclass
############################################################
class x12_node:
    def __init__(self):
        global reader
        self.id = None
        self.name = None
        self.parent = None
        self.children = []

    def __del__(self):
        pass

    def getnodebypath(self, path):
        #pdb.set_trace()
        pathl = path.split('/')
        if len(pathl) <= 1: return None
        #print self.base_name, self.id, pathl[1]
        if self.id == pathl[1]:
            return self
        if len(pathl) <=2: return None
        for child in self.children:
            node = child.getnodebypath('/' + string.join(pathl[2:],'/'))
            if node != None:
                return node
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
#       sys.stdout.write('%s%s %s %s %s\n' % (str(' '*self.base_level), self.base_name, self.base_level, self.id, self.name))
#       for node in self.children:
#           node.debug_print()


############################################################
# Map file interface
############################################################
class map_if(x12_node):
    def __init__(self, map_file):
        #codes = codes.ExternalCodes()
        #tab = Indent()
        global reader
        x12_node.__init__(self)
        self.children = []
        index = 0
        cur_name = ''
        self.cur_path = '/transaction'
        self.cur_level = -1 
        self.base_level = 0
        self.base_name = ''
        self.index = 0

        self.id = None
        self.name = None

        try:
            reader = libxml2.newTextReaderFilename(map_file)
        except:
            raise errors.GSError, 'Map file not found: %s' % (map_file)
        try:    
            ret = reader.Read()
            if ret == -1:
                raise errors.XML_Reader_Error, 'Read Error'
            elif ret == 0:
                raise errors.XML_Reader_Error, 'End of Map File'
            while ret == 1:
                #print 'map_if', reader.NodeType(), reader.Depth(), reader.Name()
                if reader.NodeType() == NodeType['element_start']:
                #       if reader.Name() in ('map', 'transaction', 'loop', 'segment', 'element'):
                #    print 't'*reader.Depth(), reader.Depth(), self.base_level, reader.NodeType(), reader.Name()
                #sys.stdout.write('%s%i %s %s %s\n') % ('\t'*reader.Depth(), reader.Depth(),  self.base_level, reader.Name())
                    cur_name = reader.Name()
                    if cur_name == 'transaction':
                        self.base_level = reader.Depth()
                        self.base_name = 'transaction'
                        pass
                    elif cur_name == 'segment':
                        self.children.append(segment_if(self, index))
                        index += 1
                    elif cur_name == 'loop':
                        self.children.append(loop_if(self, index))
                        index += 1
                    
                    #if self.cur_level < reader.Depth():
                        #    self.cur_path = os.path.join(self.cur_path, cur_name)
                    #elif self.cur_level > reader.Depth():
                    #    self.cur_path = os.path.dirname(self.cur_path)
                    self.cur_level = reader.Depth()
                elif reader.NodeType() == NodeType['element_end']:
                    #print '--', reader.Name(), self.base_level, reader.Depth(), reader.Depth() <= self.base_level 
                    #print reader.Depth(),  self.base_level, reader.NodeType(), reader.Name()
                    if reader.Depth() <= self.base_level:
                        ret = reader.Read()
                        if ret == -1:
                            raise errors.XML_Reader_Error, 'Read Error'
                        elif ret == 0:
                            raise errors.XML_Reader_Error, 'End of Map File'
                        break 
                    #if cur_name == 'transaction':
                    #    pass
                    cur_name = ''
                
                elif reader.NodeType() == NodeType['text'] and self.base_level + 2 == reader.Depth():
                    #print cur_name, reader.Value()
                    if cur_name == 'id' and self.base_name == 'transaction':
                        self.id = reader.Value()
                    elif cur_name == 'name' and self.base_name == 'transaction':
                        self.name = reader.Value()

                ret = reader.Read()
                if ret == -1:
                    raise errors.XML_Reader_Error, 'Read Error'
                elif ret == 0:
                    raise errors.XML_Reader_Error, 'End of Map File'
        except errors.XML_Reader_Error:
            pass
                
    def debug_print(self):
        sys.stdout.write('%s%s %s %s %s\n' % (str(' '*self.base_level), self.base_name, self.base_level, self.id, self.name))
        sys.stdout.write('%sid %s\n' % (str(' '*(self.base_level+1)), self.id))
        sys.stdout.write('%sname %s\n' % (str(' '*(self.base_level+1)), self.name))
        for node in self.children:
            node.debug_print()

    def __path_parent__(self):
        return os.path.basename(os.path.dirname(self.cur_path))

    def getnodebypath(self, path):
        pathl = path.split('/')
        if len(pathl) <= 1: return None
        if self.id == pathl[1]:
            return self
        for child in self.children:
            node = child.getnodebypath('/' + string.join(pathl[1:],'/'))
            if node != None:
                return node
        return None
        
    def is_map_root(self):
        return True

    def reset_cur_count(self):
        for child in self.children:
            if child.is_loop():
                child.reset_cur_count()


############################################################
# Loop Interface
############################################################
class loop_if(x12_node):
    """
    """
    def __init__(self, parent, my_index): 
        """
        Name:    __init__
        Desc:    
        Params:  
 
        Returns: 

        Note: Should be entered with a loop node current
        """
        global reader
        x12_node.__init__(self)
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
            if reader.NodeType() == NodeType['element_start']:
                #if reader.Name() in ('map', 'transaction', 'loop', 'segment', 'element'):
                #    print 'l'*reader.Depth(), reader.Depth(),  self.base_level, reader.NodeType(), reader.Name()
                cur_name = reader.Name()
                if cur_name == 'loop' and self.base_level < reader.Depth():
                    self.children.append(loop_if(self, index))
                    index += 1
                elif cur_name == 'segment':
                    self.children.append(segment_if(self, index))
                    index += 1
                elif cur_name == 'element':
                    self.children.append(element_if(self))
                    
                #if self.cur_level < reader.Depth():
                #    self.cur_path = os.path.join(self.cur_path, cur_name)
                #elif self.cur_level > reader.Depth():
                #    self.cur_path = os.path.dirname(self.cur_path)
                self.cur_level = reader.Depth()
            elif reader.NodeType() == NodeType['element_end']:
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
                
            elif reader.NodeType() == NodeType['text'] and self.base_level + 2 == reader.Depth():
                #print cur_name, reader.Value()
                if cur_name == 'id' and self.base_name == 'loop':
                    self.id = reader.Value()
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
        sys.stdout.write('%s%s %s %s %s\n' % (str(' '*self.base_level), self.base_name, self.base_level, self.id, self.name))
        if self.id: sys.stdout.write('%sid %s\n' % (str(' '*(self.base_level+1)), self.id))
        if self.name: sys.stdout.write('%sname %s\n' % (str(' '*(self.base_level+1)), self.name))
        if self.usage: sys.stdout.write('%susage %s\n' % (str(' '*(self.base_level+1)), self.usage))
        if self.seq: sys.stdout.write('%sseq %s\n' % (str(' '*(self.base_level+1)), self.seq))
        if self.repeat: sys.stdout.write('%srepeat%s\n' % (str(' '*(self.base_level+1)), self.repeat))
        for node in self.children:
            node.debug_print()

    def get_max_repeat(self):
        if self.repeat is None:
            return MAXINT
        if self.repeat == '&gt;1' or self.repeat == '>1':
            return MAXINT
        return int(self.repeat)

    def get_path(self):
        return self.path

    def get_parent(self):
        return self.parent

    def is_match(self):
        pass

    def is_valid(self, seg, errh):
        pass

    def parse(self):
        pass

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
    def __init__(self, parent, my_index):
        """
        Class: segment_if
        Name:    __init__
        Desc:    
        Params: parent - parent node 
                 
        Note: Should be entered with a segment node current
        """

        global reader
        x12_node.__init__(self)
        self.parent = parent
        self.index = my_index
        self.children = []
        self.path = ''
        self.base_name = 'segment'
        self.base_level = reader.Depth()
        self.check_dte = '20030930'
        self.cur_count = 0
        self.logger = logging.getLogger('pyx12')

        self.id = None
        self.end_tag = None
        self.name = None
        self.usage = None
        self.pos = None
        self.max_use = None
 
#        if parent == None:
#            self.path = id
#        else:
#            self.path = path + '/' + id

        self.cur_level = reader.Depth()
        
        ret = 1 
        while ret == 1:
            #print '--- segment while'
            #print 'seg', reader.NodeType(), reader.Depth(), reader.Name()
            if reader.NodeType() == NodeType['element_start']:
                #if reader.Name() in ('map', 'transaction', 'loop', 'segment', 'element'):
                #    print 's'*reader.Depth(), reader.Depth(),  self.base_level, reader.NodeType(), reader.Name()
                cur_name = reader.Name()
                if cur_name == 'segment':
                    self.base_level = reader.Depth()
                    self.base_name = 'segment'
                elif cur_name == 'element':
                    self.children.append(element_if(self))
                elif cur_name == 'composite':
                    self.children.append(composite_if(self))
                    
                #if self.cur_level < reader.Depth():
                #    self.cur_path = os.path.join(self.cur_path, cur_name)
                #elif self.cur_level > reader.Depth():
                #    self.cur_path = os.path.dirname(self.cur_path)
                self.cur_level = reader.Depth()
            elif reader.NodeType() == NodeType['element_end']:
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
                
            elif reader.NodeType() == NodeType['text'] and self.base_level + 2 == reader.Depth():
                #print cur_name, reader.Value()
                if cur_name == 'id' and self.base_name == 'segment':
                    self.id = reader.Value()
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

            ret = reader.Read()
            if ret == -1:
                raise errors.XML_Reader_Error, 'Read Error'
            elif ret == 0:
                raise errors.XML_Reader_Error, 'End of Map File'
        

    def debug_print(self):
        """
        Class: segment_if
        """
        sys.stdout.write('%s%s %s %s %s\n' % (str(' '*self.base_level), self.base_name, self.base_level, self.id, self.name))
        if self.id: sys.stdout.write('%sid %s\n' % (str(' '*(self.base_level+1)), self.id))
        if self.name: sys.stdout.write('%sname %s\n' % (str(' '*(self.base_level+1)), self.name))
        if self.usage: sys.stdout.write('%susage %s\n' % (str(' '*(self.base_level+1)), self.usage))
        if self.pos: sys.stdout.write('%spos %i\n' % (str(' '*(self.base_level+1)), self.pos))
        if self.max_use: sys.stdout.write('%smax_use %s\n' % (str(' '*(self.base_level+1)), self.max_use))
        for node in self.children:
            node.debug_print()

    def get_path(self):
        """
        Class: segment_if
        Name:    
        Desc:    
        Params:  
                 
        Returns: string of path - XPath style
        """
        return self.path

    def get_elemval_by_id(self, seg, id):
        """
        Class: segment_if
        Name:  get_elemval_by_id  
        Desc:  Return the value of an element or sub-element identified by the id
        Params: seg - segment list to search
                id - string 
        Returns: value of the element
        """
        for child in self.children:
            if child.is_element():
                if child.id == id:
                    return seg[child.seq]
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

    def get_seg_count(self):
        """
        Class: segment_if
        Name:    
        Desc:    
        Params:  
                 
        Returns: 
        """
        pass

    def is_match(self, seg):
        """
        Class: segment_if
        Name: is_match
        Desc: is segment given a match to this node?
        Params:  seg - list of element values
        Returns: boolean
        """
        if seg[0] == self.id:
            if self.children[0].data_type == 'ID' and seg[1] not in self.children[0].valid_codes:
                #logger.debug('is_match: %s %s' % (seg[0], seg[1]), self.children[0].valid_codes)
                #pdb.set_trace()
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
        # XXXX handle intra-segment dependancies
        # syntax tags
        child_count = self.get_child_count()
        if (len(seg)-1) > child_count:
            child_node = self.get_child_node_by_idx(child_count+1)
            err_str = 'Too many elements in segment %s. Has %i, should have %i' % \
                (seg[0], len(seg)-1, child_count)
            self.logger.error(err_str)
            err = {}
            err['id'] = 'SEG'
            err['seq'] = child_node.seq
            err['str'] = err_str
            err['code'] = '3'
            err['data_ele'] = child_node.data_ele
            err['value'] = seg[child_count+1]
            errh.add_error(err)
        valid = True
#        if seg[0] == 'BGN':
#            pdb.set_trace()
        for i in xrange(self.get_child_count()):
            #self.logger.debug('i=%i, len(seg)-1=%i / child_count=%i' % (i, len(seg)-1, self.get_child_count()))
            child_node = self.get_child_node_by_idx(i)
            if i < len(seg)-1:
                #if type(seg[i+1]) is ListType: # composite
                #self.logger.debug('i=%i, elem=%s, id=%s' % (i, seg[i+1], child_node.id))
                if child_node.is_composite():
                    # Validate composite
                    comp = seg[i+1]
                    subele_count = child_node.get_child_count()
                    if len(comp) > subele_count:
                        subele_node = child_node.get_child_node_by_idx(subele_count+1)
                        err = {}
                        err['id'] = 'SEG'
                        err['seq'] = subele_node.seq
                        err['str'] = 'Too many sub-elements in composite %s' % (subele_node.refdes)
                        err['code'] = '3'
                        err['data_ele'] = subele_node.data_ele
                        err['value'] = comp[subele_count+1]
                        errh.add_error(err)
                    valid &= child_node.is_valid(seg[i+1], errh, self.check_dte)
                elif child_node.is_element():
                    # Validate Element
                    valid &= child_node.is_valid(seg[i+1], errh, self.check_dte)
            else: #missing required elements
                #self.logger.debug('id=%s, name=%s' % (child_node.id, child_node.base_name))
                valid &= child_node.is_valid(None, errh)
        return valid

    def parse(self):
        """
        Class: segment_if
        Name:    
        Desc:    
        Params:  
                 
        Returns: list of elements??? 
        """
        pass

    def reset_cur_count(self):
        cur_count = 0

############################################################
# Element Interface
############################################################
class element_if(x12_node):
    def __init__(self, parent):
        """
        Class: element_if
        Name:    __init__
        Desc:    
        Params: parent - parent node 
                 
        Returns: 
        """

        global reader
        x12_node.__init__(self)
        self.children = []
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
        self.logger = logging.getLogger('pyx12')

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
            if reader.NodeType() == NodeType['element_start']:
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
            elif reader.NodeType() == NodeType['element_end']:
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
                
            elif reader.NodeType() == NodeType['text'] and self.base_level + 2 <= reader.Depth():
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
        """
        Class: element_if
        """
        sys.stdout.write('%s%s %s %s\n' % (str(' '*self.base_level), self.base_name, self.base_level, self.name))
#        sys.stdout.write('%sid %s\n' % (str(' '*(self.base_level+1)), self.id))
        if self.data_ele: sys.stdout.write('%sdata_ele %s\n' % (str(' '*(self.base_level+1)), self.data_ele))
        if self.name: sys.stdout.write('%sname %s\n' % (str(' '*(self.base_level+1)), self.name))
        if self.usage: sys.stdout.write('%susage %s\n' % (str(' '*(self.base_level+1)), self.usage))
        if self.seq: sys.stdout.write('%sseq %s\n' % (str(' '*(self.base_level+1)), self.seq))
        if self.refdes: sys.stdout.write('%srefdes %s\n' % (str(' '*(self.base_level+1)), self.refdes))
        if self.data_type: sys.stdout.write('%sdata_type %s\n' % (str(' '*(self.base_level+1)), self.data_type))
        if self.min_len: sys.stdout.write('%smin_len %s\n' % (str(' '*(self.base_level+1)), self.min_len))
        if self.max_len: sys.stdout.write('%smax_len %s\n' % (str(' '*(self.base_level+1)), self.max_len))
        if self.external_codes: sys.stdout.write('%sexternal codes %s\n' % (str(' '*(self.base_level+1)), self.external_codes))
        if self.valid_codes:
            sys.stdout.write('%svalid codes:\n' % (str(' '*(self.base_level+1))))
            for code in self.valid_codes:
                sys.stdout.write('%scode %s\n' % (str(' '*(self.base_level+2)), code))
        for node in self.children:
            node.debug_print()

   
    def __del__(self):
        pass

    def __error__(self, errh, err_str, err_cde, elem_val):
        """
        Class:      element_if
        Name:       __error__
        Desc:       Forward the error to an error_handler
        Params:  
        """
        errh.ele_error(err_cde, err_str, elem_val, pos=self.seq, data_ele=self.data_ele)
        
    def __valid_code__(self, code):
        """
        Class:  element_if
        Name:   __valid_code__
        Desc:   Verify the x12 element value is in the given list of valid codes
        Params:  
        Returns: True if found, else False
        """
        if not self.valid_codes:
            return True
        if code in self.valid_codes:
            return True
        return False

    def get_path(self):
        """
        Class: element_if
        Name:    
        Desc:    
        Params:  
                 
        Returns: string of path - XPath style
        """
        return self.path

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
        global codes
        if self.parent.is_composite():
            errh.add_ele(self.parent.seq, self.data_ele, self.seq)
        else:
            errh.add_ele(self.seq, self.data_ele)
        if elem_val == '' or elem_val is None:
            if self.usage == 'N':
                return True
            elif self.usage == 'R':
                err_str = 'Mandatory data element %s is missing' % (self.refdes)
                self.__error__(errh, err_str, '1', None)
                return False
            elif self.usage == 'S':
                return True
        if (not self.data_type is None) and (self.data_type == 'R' or self.data_type[0] == 'N'):
            elem = string.replace(string.replace(elem_val, '-', ''), '.', '')
            if len(elem) < int(self.min_len):
                err_str = 'Data element %s is too short: "%s" is len=%i' % (self.refdes,\
                    elem_val, int(self.min_len))
                self.__error__(errh, err_str, '4', elem_val)
            if len(elem) > int(self.max_len):
                err_str = 'Element %s is too long: "%s" is len=%i' % (self.refdes,\
                    elem_val, int(self.max_len))
                self.__error__(errh, err_str, '5', elem_val)
        else:
            if len(elem_val) < int(self.min_len):
                err_str = 'Data element %s is too short: "%s" is len=%i' % (self.refdes,\
                    elem_val, int(self.min_len))
                self.__error__(errh, err_str, '4', elem_val)
            if len(elem_val) > int(self.max_len):
                err_str = 'Element %s is too long: "%s" is len=%i' % (self.refdes,\
                    elem_val, int(self.max_len))
                self.__error__(errh, err_str, '5', elem_val)

        if not (self.__valid_code__(elem_val) or codes.IsValid(self.external_codes, elem_val, check_dte) ):
            err_str = '(%s) is not a valid code for data element %s' % (elem_val, self.refdes)
            self.__error__(errh, err_str, '7', elem_val)
        if not IsValidDataType(elem_val, self.data_type, 'E'):
            if self.data_type == 'DT':
                err_str = 'Data element %s contains an invalid date (%s)' % \
                    (self.refdes, elem_val)
                self.__error__(errh, err_str, '8', elem_val)
            elif self.data_type == 'TM':
                err_str = 'Data element %s contains an invalid time (%s)' % \
                    (self.refdes, elem_val)
                self.__error__(errh, err_str, '9', elem_val)
            else:
                err_str = 'Data element %s is type %s, contains an invalid character(%s)' % \
                    (self.refdes, self.data_type, elem_val)
                self.__error__(errh, err_str, '6', elem_val)
        return True


    def parse(self):
        """
        Class: element_if
        Name:    
        Desc:    
        Params:  
                 
        Returns: list of elements??? 
        """
        pass

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
    def __init__(self, parent):
        """
        Class: composite_if
        Name:    __init__
        Desc:    Get the values for this composite
        Params:         parent - parent node 
        """

        global reader
        x12_node.__init__(self)

        self.children = []
        self.parent = parent
        self.path = ''
        self.base_name = 'composite'
        self.base_level = reader.Depth()
        self.check_dte = '20030930'

        #self.id = None
        self.name = None
        self.data_ele = None
        self.usage = None
        self.seq= None
        self.refdes = None

        self.cur_level = reader.Depth()
        self.logger = logging.getLogger('pyx12')
        
        ret = 1 
        while ret == 1:
            #print '--- segment while'
            #print 'seg', reader.NodeType(), reader.Depth(), reader.Name()
            if reader.NodeType() == NodeType['element_start']:
                #if reader.Name() in ('map', 'transaction', 'loop', 'segment', 'element'):
                #    print 's'*reader.Depth(), reader.Depth(),  self.base_level, reader.NodeType(), reader.Name()
                cur_name = reader.Name()
                if cur_name == 'composite':
                    self.base_level = reader.Depth()
                    self.base_name = 'composite'
                elif cur_name == 'element':
                    self.children.append(element_if(self))
                    
                #if self.cur_level < reader.Depth():
                #    self.cur_path = os.path.join(self.cur_path, cur_name)
                #elif self.cur_level > reader.Depth():
                #    self.cur_path = os.path.dirname(self.cur_path)
                self.cur_level = reader.Depth()
            elif reader.NodeType() == NodeType['element_end']:
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
                
            elif reader.NodeType() == NodeType['text'] and self.base_level + 2 == reader.Depth():
                #print cur_name, reader.Value()
                if cur_name == 'name':
                    self.name = reader.Value()
                elif cur_name == 'data_ele':
                    self.data_ele= reader.Value()
                elif cur_name == 'usage':
                    self.usage = reader.Value()
                elif cur_name == 'seq':
                    self.seq = reader.Value()
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
        err = {}
        err['id'] = 'ELE'
        err['str'] = err_str
        err['code'] = err_cde
        err['value'] = elem_val
        err['pos'] = self.seq
        err['data_ele'] = self.data_ele
        errh.add_error(err)
        
    def debug_print(self):
        """
        Class: composite_if
        """
        sys.stdout.write('%s%s %s %s %s\n' % (str(' '*self.base_level), self.base_name, self.base_level, self.id, self.name))
        if self.name: sys.stdout.write('%sname %s\n' % (str(' '*(self.base_level+1)), self.name))
        if self.usage: sys.stdout.write('%susage %s\n' % (str(' '*(self.base_level+1)), self.usage))
        if self.seq: sys.stdout.write('%sseq %s\n' % (str(' '*(self.base_level+1)), self.seq))
        if self.refdes: sys.stdout.write('%srefdes %s\n' % (str(' '*(self.base_level+1)), self.refdes))
        for node in self.children:
            node.debug_print()


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

    def is_valid(self, comp, errh):
        """
        Class:      composite_if
        Name:       validate
        Desc:       Validates the composite
        Params:     comp - composite value or list
                    errh - instance of error_handler
        Returns:    True on success
        """
        if comp is None or len(comp) == 0:
            if self.usage == 'N':
                return True
            elif self.usage == 'R':
                err = {}
                err['id'] = 'ELE' # ??? COMP
                err['str'] = 'Composite "%s" is required' % (self.name)
                err['code'] = '1'
                #err['value'] = elem_val
                errh.add_error(err)

        if not type(comp) is ListType: # composite
            comp = [comp] 

        if len(comp) > self.get_child_count():
            err = {}
            err['id'] = 'ELE' # ??? COMP
            err['str'] = 'Too many sub-elements in composite %s' % (self.refdes)
            err['code'] = '1'
            #err['value'] = elem_val
            errh.add_error(err)
        for i in xrange(len(comp)):
            if i < len(comp):
                self.get_child_node_by_idx(i).is_valid(comp[i], errh, self.check_dte)
            else: #missing required elements
                self.get_child_node_by_idx(i).is_valid(None, errh)
        return True

    def getnodebypath(self, path):
        """
        Class:  composite_if
        Name:    
        Desc:    
        Params:  
        Returns: 
        """
        pathl = path.split('/')
        #if len(pathl) <= 1: return None
        #if self.id == pathl[1]:
        #    return self
        #print self.base_name, pathl[2]
        if len(pathl) <=2: return None
        for child in self.children:
            node = child.getnodebypath(pathl[2:])
            if node != None:
                return node
        return None
    
    def is_composite(self):
        return True


