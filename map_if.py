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
        if idx >= len(self.children):
            return None
        else:
            return self.children[idx]

    def is_match(self):
        # match also by ID
        pass

    def walk_tree(self, seg):
        pass
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
                        self.children.append(segment_if(self))
                    elif cur_name == 'loop':
                        self.children.append(loop_if(self))
                    
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
    def __init__(self, parent): 
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
        self.parent = parent
        self.path = ''
        self.base_name = 'loop'
        
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
                    self.children.append(loop_if(self))
                elif cur_name == 'segment':
                    self.children.append(segment_if(self))
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
        pass

    def is_loop(self):
        return True

############################################################
# Segment Interface
############################################################
class segment_if(x12_node):
    """
    """
    def __init__(self, parent):
        """
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

        self.id = None
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
                elif cur_name == 'name' and self.base_name == 'segment':
                    self.name = reader.Value()
                elif cur_name == 'usage' and self.base_name == 'segment':
                    self.usage = reader.Value()
                elif cur_name == 'pos' and self.base_name == 'segment':
                    self.pos = reader.Value()
                elif cur_name == 'max_use' and self.base_name == 'segment':
                    self.max_use = reader.Value()

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
        if self.pos: sys.stdout.write('%spos %s\n' % (str(' '*(self.base_level+1)), self.pos))
        if self.max_use: sys.stdout.write('%smax_use %s\n' % (str(' '*(self.base_level+1)), self.max_use))
        for node in self.children:
            node.debug_print()

    def __del__(self):
        pass

    def get_path(self):
        """
        Name:    
        Desc:    
        Params:  
                 
        Returns: string of path - XPath style
        """
        return self.path
    
    def get_parent(self):
        """
        Name:    
        Desc:    
        Params:  
                 
        Returns: ref to parent class instance
        """
        return self.parent

    def is_match(self, seg):
        """
        Name: is_match
        Desc: is segment given a match to this node?
        Params:  seg - list of element values
        Returns: boolean
        """
        if seg[0] == self.id:
            if self.children[1].data_type == 'ID' and self.children[1].value != seg[1]:
                return False
            return True
        else:
            return False

    def is_valid(self, seg):
        """
        Name:   
        Desc:    
        Params:  
                 
        Returns: boolean
        """
        # handle intra-segment dependancies
        pass

    def parse(self):
        """
        Name:    
        Desc:    
        Params:  
                 
        Returns: list of elements??? 
        """
        pass

    def get_seg_count(self):
        """
        Name:    
        Desc:    
        Params:  
                 
        Returns: 
        """
        pass

    def is_segment(self): return True
        

############################################################
# Element Interface
############################################################
class element_if(x12_node):
    def __init__(self, parent):
        """
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
                    self.seq = reader.Value()
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
        Name:    
        Desc:    
        Params:  
                 
        Returns: string of path - XPath style
        """
        return self.path

    def get_parent(self):
        """
        Name:    
        Desc:    
        Params:  
                 
        Returns: ref to parent class instance
        """
        return self.parent

    def is_match(self):
        """
        Name:    
        Desc:    
        Params:  
                 
        Returns: boolean
        """
        # match also by ID
        pass

    def is_valid(self, elem_val):
        """
        Name:   
        Desc:    
        Params:  
            elem_val - value of element data
                 
        Returns: boolean
        """
        # handle intra-segment dependancies
        pass
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
                raise errors.WEDI1Error, 'Element %s is too short - "%s" is len=%i' % (self.refdes,
                    elem_val, int(self.min_len))

        if elem_val == None and self.usage == 'R':
            raise errors.WEDI3Error
        if not (self.__valid_code__(elem_val) or codes.IsValid(self.external_codes, elem_val) ):
            raise errors.WEDIError, "Not a valid code for this ID element"
        if not IsValidDataType(elem_val, self.data_type, 'E'):
            raise errors.WEDI1Error, "Invalid X12 datatype: '%s' is not a '%s'" % (elem_val, self.data_type) 
        return 1


    def parse(self):
        """
        Name:    
        Desc:    
        Params:  
                 
        Returns: list of elements??? 
        """
        pass

    def get_seg_count(self):
        """
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
        sys.stdout.write('%s%s %s %s %s\n' % (str(' '*self.base_level), self.base_name, self.base_level, self.id, self.name))
        if self.name: sys.stdout.write('%sname %s\n' % (str(' '*(self.base_level+1)), self.name))
        if self.usage: sys.stdout.write('%susage %s\n' % (str(' '*(self.base_level+1)), self.usage))
        if self.seq: sys.stdout.write('%sseq %s\n' % (str(' '*(self.base_level+1)), self.seq))
        if self.refdes: sys.stdout.write('%srefdes %s\n' % (str(' '*(self.base_level+1)), self.refdes))
        for node in self.children:
            node.debug_print()


    def xml(self):
        """
        Name:    xml
        Desc:    Sends an xml representation of the composite to stdout
        Params:  
        Returns: 
        """
        sys.stdout.write('<composite>\n')
        for sub_elem in self.children:
            sub_elem.xml()
        sys.stdout.write('</composite>\n')

    def validate(self, code):
        """
        Name:    validate
        Desc:    Validates the composite
        Params:  
        Returns: 1 on success
        """
        if code == '' or code is None:
            if self.usage == 'N':
                return 1
            elif self.usage == 'R':
                raise errors.WEDI1Error, 'Composite "%s" is required' % (self.name)
        for sub_elem in self.children:
            sub_elem.validate()
        return 1

    def getnodebypath(self, path):
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

######################################################################

#AttributeCount: provides the number of attributes of the current node. 
#BaseUri: the base URI of the node. See the XML Base W3C specification. 
#Depth: the depth of the node in the tree, starts at 0 for the root node. 
#HasAttributes: whether the node has attributes. 
#HasValue: whether the node can have a text value. 
#IsDefault: whether an Attribute node was generated from the default value 
#        defined in the DTD or schema (unsupported yet). 
#IsEmptyElement: check if the current node is empty, this is a bit bizarre 
#        in the sense that <a/> will be considered empty while <a></a> will not. 
#LocalName: the local name of the node. 
#Name: the qualified name of the node, equal to (Prefix:)LocalName. 
#NamespaceUri: the URI defining the namespace associated with the node. 
#Prefix: a shorthand reference to the namespace associated with the node. 
#Value: provides the text value of the node if present. 
#XmlLang: the xml:lang scope within which the node resides. 

#GetAttributeNo(no): provides the value of the attribute with the specified 
#        index no relative to the containing element. 
#GetAttribute(name): provides the value of the attribute with the specified qualified name. 
#GetAttributeNs(localName, namespaceURI): provides the value of the attribute 
#        with the specified local name and namespace URI. 
#MoveToAttributeNo(no): moves the position of the current instance to the attribute 
#        with the specified index relative to the containing element. 
#MoveToAttribute(name): moves the position of the current instance to the attribute 
#        with the specified qualified name. 
#MoveToAttributeNs(localName, namespaceURI): moves the position of the current 
#        instance to the attribute with the specified local name and namespace URI. 
#MoveToFirstAttribute: moves the position of the current instance to the first 
#        attribute associated with the current node. 
#MoveToNextAttribute: moves the position of the current instance to the next 
#        attribute associated with the current node. 
#MoveToElement: moves the position of the current instance to the node that contains 
#        the current Attribute node. 

