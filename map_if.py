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
import os.path
#import stat
import sys
import string
#import time
#import pdb
import libxml2
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


############################################################
# Loop Interface
############################################################
class loop_if(x12_node):
    """
    """
    def __init__(self, parent, index): 
        """
        Name:    __init__
        Desc:    
        Params:  
 
        Returns: 

        Note: Should be entered with a loop node current
        """
        global reader
        x12_node.__init__(self)
        self.children = []
        index = 0
        self.parent = parent
        self.path = ''
        self.base_name = 'loop'
        self.index = index
        
        self.id = None
        self.name = None
        self.usage = None
        self.seq = None
        self.repeat = None

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


    def get_path(self):
        return self.path

    def get_parent(self):
        return self.parent

    def is_match(self):
        pass

    def is_valid(self, seg):
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

############################################################
# Segment Interface
############################################################
class segment_if(x12_node):
    """
    """
    def __init__(self, parent, index):
        """
        Class: segment_if
        Name:    __init__
        Desc:    
        Params: parent - parent node 
                 
        Note: Should be entered with a segment node current
        """

        global reader
        x12_node.__init__(self)
        self.children = []
        self.parent = parent
        self.path = ''
        self.base_name = 'segment'
        self.base_level = reader.Depth()
        self.index = index
        self.check_dte = '20030930'

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
                    self.max_use = int(reader.Value())

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
            if self.children[1].data_type == 'ID' and seg[1] in self.children[1].valid_codes:
                return False
            return True
        else:
            return False

    def is_segment(self): return True

    def is_valid(self, seg):
        """
        Class: segment_if
        Name:   
        Desc:    
        Params:  
                 
        Returns: boolean
        """
        # handle intra-segment dependancies
        if len(seg) > self.get_child_count() + 1: 
            raise errors.WEDI1Error, \
                'Too many elements in segment %s. Has %i, should have %i' % \
                (seg[0], len(seg), self.get_child_count())
        for i in xrange(self.get_child_count()):
            # Validate Elements
            if i < len(seg) - 1:
                self.get_child_node_by_idx(i).is_valid(seg[i+1], self.check_dte)
#                if type(seg[i]) is ListType: # composite
                    # Validate composite
#                    comp = seg[i]
#                    node.get_child_node_by_idx(i).is_valid(comp)
#                else: # element
#                    self.get_child_node_by_idx(i).is_valid(seg[i])
            else: #missing required elements
                self.get_child_node_by_idx(i).is_valid(None)

    def parse(self):
        """
        Class: segment_if
        Name:    
        Desc:    
        Params:  
                 
        Returns: list of elements??? 
        """
        pass

        

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

    def __valid_code__(self, code):
        """
        Class: element_if
        Name:    __valid_code__
        Desc:    Verify the x12 element value is in the given list of valid codes
        Params:  
        Returns: 1 if found, else 0
        """
        if not self.valid_codes:
            return 1
        if code in self.valid_codes:
            return 1
        return 0

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

    def is_valid(self, elem_val, check_dte=None):
        """
        Class:  element_if
        Name:   is_valid 
        Desc:    
        Params:  
            elem_val - value of element data
            check_dte - date string to check against (YYYYMMDD)
                 
        Returns: boolean
        """
        # handle intra-segment dependancies
        global codes
        if elem_val == '' or elem_val is None:
            if self.usage == 'N':
                return 1
            elif self.usage == 'R':
                raise errors.WEDI1Error, 'Element %s is required' % (self.refdes)
        if (not self.data_type is None) and (self.data_type == 'R' or self.data_type[0] == 'N'):
            elem = string.replace(string.replace(elem_val, '-', ''), '.', '')
            if len(elem) < int(self.min_len):
                raise errors.WEDI1Error, 'Element %s is too short - "%s" is len=%i' % (self.refdes,
                    elem, int(self.min_len))
            if len(elem) > int(self.max_len):
                raise errors.WEDI1Error, 'Element %s is too short - "%s" is len=%i' % (self.refdes,
                    elem, int(self.min_len))
        else:
            if len(elem_val) < int(self.min_len):
                raise errors.WEDI1Error, 'Element %s is too short - "%s" is len=%i' % (self.refdes,
                    elem_val, int(self.min_len))
            if len(elem_val) > int(self.max_len):
                raise errors.WEDI1Error, 'Element %s is too short: "%s" is %i characters, \
                    should be %i' % (self.refdes, elem_val, len(elem_val), int(self.min_len))

        if elem_val == None and self.usage == 'R':
            raise errors.WEDI3Error
        if not (self.__valid_code__(elem_val) or codes.IsValid(self.external_codes, elem_val, check_dte) ):
            raise errors.WEDIError, "Not a valid code for this ID element"
        if not IsValidDataType(elem_val, self.data_type, 'E'):
            raise errors.WEDI1Error, "Invalid X12 datatype: '%s' is not a '%s'" % (elem_val, self.data_type) 
        return 1


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
        self.usage = None
        self.seq= None
        self.refdes = None

        self.cur_level = reader.Depth()
        
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
        Class: composite_if
        Name:    xml
        Desc:    Sends an xml representation of the composite to stdout
        Params:  
        Returns: 
        """
        sys.stdout.write('<composite>\n')
        for sub_elem in self.children:
            sub_elem.xml()
        sys.stdout.write('</composite>\n')

    def is_valid(self, comp):
        """
        Class: composite_if
        Name:    validate
        Desc:    Validates the composite
        Params:  
        Returns: True on success
        """
        
        if comp is None or len(comp) == 0:
            if self.usage == 'N':
                return True
            elif self.usage == 'R':
                raise errors.WEDI1Error, 'Composite "%s" is required' % (self.name)

        if not type(comp) is ListType: # composite
            comp = [comp] 

        if len(comp) > self.get_child_count():
            raise errors.WEDI1Error, 'Too many sub-elements in composite %s' % (self.refdes)
        for i in xrange(len(comp)):
            if i < len(comp):
                self.get_child_node_by_idx(i).is_valid(comp[i], self.check_dte)
            else: #missing required elements
                self.get_child_node_by_idx(i).is_valid(None)
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


