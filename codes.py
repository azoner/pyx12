#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
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


"""
External Codes interface
"""

import os, os.path
#import sys
import cPickle
import libxml2
import datetime 
import pdb
from stat import ST_MTIME
from stat import ST_SIZE

# Intrapackage imports
import errors

NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3, \
    'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8, \
    'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12}


class ExternalCodes:
    """
    Name:    ExternalCodes
    Desc:    Validates an ID against an external list of codes
    """

    def __init__(self):
        """
        Name:    __init__
        Desc:    Initialize the external list of codes
        Params:  
        """
        
        self.codes = {} # {code_type: [(code_values, eff_dte, exp_dte)]}
        code_file = 'map/codes.xml'
        pickle_file = '%s.%s' % (os.path.splitext(code_file)[0], 'pkl')
        id = None
        
        # init the map of codes from the pickled file codes.pkl
        try:
            if os.stat(code_file)[ST_MTIME] < os.stat(pickle_file)[ST_MTIME]:
                self.codes = cPickle.load(open(pickle_file))
            else: 
                raise "reload codes"
        except:
            try:
                reader = libxml2.newTextReaderFilename(code_file)
            except:
                raise errors.x12Error, 'Code file not found: %s' % (code_file)
            try:
                ret = reader.Read()
                if ret == -1:
                    raise errors.XML_Reader_Error, 'Read Error'
                elif ret == 0:
                    raise errors.XML_Reader_Error, 'End of Map File'
                while ret == 1:
                    #print 'map_if', reader.NodeType(), reader.Depth(), reader.Name()
                    if reader.NodeType() == NodeType['element_start']:
                        cur_name = reader.Name()
                        if cur_name == 'codeset':
                            code_list = []
                            base_level = reader.Depth()
                        elif cur_name == 'version':
                            pass
                    elif reader.NodeType() == NodeType['element_end']:
                        if reader.Name() == 'codeset':
                            self.codes[id] = code_list
                            #del code_list
                            id = None
#                       if reader.Depth() <= base_level:
#                           ret = reader.Read()
#                            if ret == -1:
#                               raise errors.XML_Reader_Error, 'Read Error'
#                            elif ret == 0:
#                               raise errors.XML_Reader_Error, 'End of Map File'
#                            break
                        cur_name = ''
                    elif reader.NodeType() == NodeType['text'] and base_level + 1 <= reader.Depth():
                        if cur_name == 'id':
                            id = reader.Value()
                        elif cur_name == 'code':
                            eff_dte = None
                            exp_dte = None
                            code_val = reader.Value()
                            if reader.HasAttributes():
                                print 'yes'
                                reader.MoveToFirstAttribute()
                                while reader.MoveToNextAttribute():
                                    if code_val == '101Y00000N': print reader.Name(), reader.Value()
                                    if reader.Name() == 'eff_dte': eff_dte = reader.Value()
                                    elif reader.Name() == 'exp_dte': exp_dte = reader.Value()
                                code_list.append((code_val, eff_dte, exp_dte))
                                #reader.GetAttributeNo(0), reader.GetAttributeNo(1)))
                                #reader.GetAttribute('eff_dte'), reader.GetAttribute('exp_dte')))

                    ret = reader.Read()
                    if ret == -1:
                        raise errors.XML_Reader_Error, 'Read Error'
                    elif ret == 0:
                        raise errors.XML_Reader_Error, 'End of Map File'
            except errors.XML_Reader_Error:
                pass
        try:
            pass
            #cPickle.dump(self.codes,open(pickle_file,'w'))
        except:
            pass


    def IsValid(self, key, code, check_dte):
        """
        Name:    IsValid
        Desc:    Initialize the external list of codes
        Params:  key - the external codeset identifier
                 code - code to be verified
                 check_dte - YYYYMMDD - Date on which to check code validity. eg 20040514
        Returns: 1 if code is valid, 0 if not
        """

        #if not given a key, do not flag an error
        if not key:
            return True
        #check the code against the list indexed by key
        else:
            if len(check_dte) != 8: raise errors.EngineError, 'Bad check date %s' & (check_dte)
            dt_check_dte = datetime.date(int(check_dte[:4]), int(check_dte[4:6]), int(check_dte[-2:]))
            if not key in self.codes.keys():
                raise errors.EngineError, 'Enternel Code %s is not defined' % (key)
            #if not code in self.codes[key]:
            for code_tuple in self.codes[key]:
                if code == code_tuple[0]:
                    print code_tuple
                    if code_tuple[1] != None:
                        dt_eff_dte = datetime.date(int(code_tuple[1][:4]), \
                            int(code_tuple[1][4:6]), int(code_tuple[1][-2:]))
                    else: dt_eff_dte = dt_check_dte.min
                    if code_tuple[2] != None:
                        dt_exp_dte = datetime.date(int(code_tuple[2][:4]), \
                            int(code_tuple[2][4:6]), int(code_tuple[2][-2:]))
                    else: dt_exp_dte= dt_check_dte.max
                    if dt_check_dte >= dt_eff_dte and dt_check_dte <= dt_exp_dte:
                        return True
                return False
        return True

    def debug_print(self):
        for key in self.codes.keys():
            print self.codes[key][:10]

