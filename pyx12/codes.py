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

class Codes_Error(Exception):
    """Class for code modules errors."""

NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3, \
    'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8, \
    'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12}


class ExternalCodes:
    """
    Name:    ExternalCodes
    Desc:    Validates an ID against an external list of codes
    """

    def __init__(self, base_path, exclude=None):
        """
        Name:    __init__
        Desc:    Initialize the external list of codes
        Params:  
                 exclude - string of external codes to ignore

        self.codes
            <codeset>
                <id>prov_taxonomy</id>
                <name>Provider Taxonomy Code</name>
                <data_ele>127</data_ele>
                <version>
                    <id>1.1</id>
                    <eff_dte>20020101</eff_dte>
                    <exp_dte>20050101</exp_dte>
                    <code>101Y00000N</code>
        self.codes = {id: (eff_dte, exp_dte, [code_values])}
                    map of a tuple of two dates and a list of codes
        """
        
        self.codes = {} 
        code_file = base_path + '/codes.xml'
        pickle_file = '%s.%s' % (os.path.splitext(code_file)[0], 'pkl')
        id = None
        codeset_id = None
        base_name = None
        
        #print exclude
        if exclude is None:
            self.exclude_list = []
        else:
            self.exclude_list = exclude.split(',')

        # init the map of codes from the pickled file codes.pkl
        try:
            if os.stat(code_file)[ST_MTIME] < os.stat(pickle_file)[ST_MTIME]:
                self.codes = cPickle.load(open(pickle_file))
            else: 
                raise Codes_Error, "reload codes"
        except:
            try:
                reader = libxml2.newTextReaderFilename(code_file)
            except:
                raise errors.EngineError, 'Code file not found: %s' % (code_file)
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
                            base_level = reader.Depth()
                            base_name = 'codeset'
                        elif cur_name == 'version':
                            code_list = []
                            eff_dte = None
                            exp_dte = None
                            base_name = 'version'
                    elif reader.NodeType() == NodeType['element_end']:
                        if reader.Name() == 'codeset':
                            self.codes[codeset_id] = (eff_dte, exp_dte, code_list)
                            #del code_list
                            #id = None
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
                            if base_name == 'codeset':
                                codeset_id = reader.Value()
                            id = reader.Value()
                        elif cur_name == 'code':
                            code_list.append(reader.Value())
                        elif cur_name == 'eff_dte':
                            eff_dte = reader.Value()
                        elif cur_name == 'exp_dte':
                            exp_dte = reader.Value()

                    ret = reader.Read()
                    if ret == -1:
                        raise errors.XML_Reader_Error, 'Read Error'
                    elif ret == 0:
                        raise errors.XML_Reader_Error, 'End of Map File'
            except errors.XML_Reader_Error:
                pass
#        try:
#            cPickle.dump(self.codes, open(pickle_file,'w'))
#        except:
#            pass


    def IsValid(self, key, code, check_dte=None):
        """
        Name:    IsValid
        Desc:    Initialize the external list of codes
        Params:  key - the external codeset identifier
                 code - code to be verified
                 check_dte - YYYYMMDD - Date on which to check code validity. eg 20040514
        Returns: True if code is valid, False if not
        """

        #if not given a key, do not flag an error
        if not key:
            raise errors.EngineError, 'bad key %s' % (key)
            #return True
        #check the code against the list indexed by key
        else:
            if key in self.exclude_list:
                return True
            if not self.codes.has_key(key):
                raise errors.EngineError, 'Externel Code "%s" is not defined' % (key)
                
            if check_dte is None:
                code_list = self.codes[key][2]
                if code in code_list:
                    return True
            else:
                if len(check_dte) != 8: 
                    raise errors.EngineError, 'Bad check date %s' & (check_dte)
                dt_check_dte = datetime.date(int(check_dte[:4]), int(check_dte[4:6]), int(check_dte[-2:]))
                eff_dte = self.codes[key][0]
                exp_dte = self.codes[key][1]
                code_list = self.codes[key][2]
                #print eff_dte, exp_dte
                #pdb.set_trace()
                if eff_dte != None:
                    dt_eff_dte = datetime.date(int(eff_dte[:4]), \
                        int(eff_dte[4:6]), int(eff_dte[-2:]))
                else: 
                    dt_eff_dte = dt_check_dte.min
                if exp_dte != None:
                    dt_exp_dte = datetime.date(int(exp_dte[:4]), \
                        int(exp_dte[4:6]), int(exp_dte[-2:]))
                else: 
                    dt_exp_dte = dt_check_dte.max
                if dt_check_dte >= dt_eff_dte and dt_check_dte <= dt_exp_dte:
                    if code in code_list:
                        return True
        return False

    def debug_print(self):
        for key in self.codes.keys():
            print self.codes[key][:10]

