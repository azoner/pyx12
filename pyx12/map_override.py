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
Apply local overrides to the current map
Overrides defined in a xml document. 
"""

import libxml2
import errors

NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3, 'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8, 'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12}


class map_override:
    def __init__(self, map_root, override_file, icvn, vriic, fic):
        try:
            reader = libxml2.newTextReaderFilename(map_file)
        except:
            raise errors.EngineError, 'Map file not found: %s' % (map_file)
                    
        while reader.Read():
            #processNode(reader)
            if reader.NodeType() == NodeType['element_start'] and reader.Name() == 'version':
             while reader.MoveToNextAttribute():
                    if reader.Name() == 'icvn':
                        icvn = reader.Value()

            if reader.NodeType() == NodeType['element_end'] and reader.Name() == 'version':
                icvn = None

            if reader.NodeType() == NodeType['element_start'] and reader.Name() == 'map':
                file_name = ''
                while reader.MoveToNextAttribute():
                    if reader.Name() == 'vriic':
                        vriic = reader.Value()
                    elif reader.Name() == 'fic':
                        fic = reader.Value()

            if reader.NodeType() == NodeType['element_end'] and reader.Name() == 'map':
                #self.maps.append((icvn, vriic, fic, file_name))
                vriic = None
                fic = None
                file_name = None

            if reader.NodeType() == NodeType['text']:
                file_name = reader.Value()

    def _set_value(self, map_root, path, variable, value):
        pass

    def _append_value(self, map_root, path, variable, value):
        pass

    def _reset_list(self, map_root, path, variable, value):
        pass

