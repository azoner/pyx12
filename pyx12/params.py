######################################################################
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Holds Run-time Parameters

Order of precedence:
 1. set(param) - Command line parameters
 2. Config file given on command line using -c
 3. '~/.pyx12rc' - User's directory
 4. '/usr/local/etc/pyx12.conf' - Site default
 5. self.params - Defaults
"""
import os.path
#import StringIO
import libxml2

class params:
    def __init__(self, config_file=None):
        self.params = {}
        self.params['map_path'] = '/usr/local/share/pyx12/map'
        self.params['pickle_path'] = '/usr/local/share/pyx12/map'
        self.params['exclude_external_codes'] = None
        self.params['ignore_syntax'] = False
        self.params['charset'] = 'E'
        self.params['ignore_codes'] = False
        self.params['ignore_ext_codes'] = False
        self.params['skip_html'] = False
        self.params['skip_997'] = False
        self.params['simple_dtd'] = 'http://www.kazoocmh.org/x12simple.dtd'
        self.params['idtag_dtd'] = 'http://www.kazoocmh.org/x12idtag.dtd'
        
        self._get_config_file('/usr/local/etc/pyx12.conf')
        self._get_config_file(os.path.expanduser('~/.pyx12rc'))
        if config_file:
            self._get_config_file(config_file)

    def _get_config_file(self, filename):
        if os.path.isfile(filename):
            reader = libxml2.newTextReaderFilename(filename)
            ret = self.reader.Read()
            while ret == 1:
                tmpNodeType = self.reader.NodeType()
                if tmpNodeType == NodeType['element_start']:
                    option = None
                    value = None
                    cur_name = self.reader.Name()
                    if cur_name == 'transaction':
                        base_name = 'transaction'
                    elif cur_name == 'param':
                        base_name = 'param'
                        option = @name
                    elif cur_name == 'type':
                        base_name = 'type'
                elif tmpNodeType == NodeType['element_end']:
                    if option and value is not None:
                        self.params[option] = value
                elif tmpNodeType == NodeType['text']:
                    if cur_name == 'id' and self.base_name == 'transaction':
                        value = self.reader.Value()
                        self.id = self.reader.Value()
                ret = self.reader.Read()

    def get(self, option):
        """
        Get the value of the parameter specified by option
        @param option: Option name
        @type option: string
        """
        if option in self.params.keys():
            return self.params[option]
        else:
            return None

    def set(self, option, value):
        """
        Set the value of the parameter specified by option
        @param option: Option name
        @type option: string
        @param value: Parameter value
        @type value: string
        """
        self.params[option] = value

#    def __repr__(self):
#        pass
