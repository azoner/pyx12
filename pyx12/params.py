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
Holds Run-time Parameters
Order of precedence:
 set_params(param) - Command line parameters
 '~/.pyx12rc' - User's directory
 '/usr/local/etc/pyx12.conf' - Site default
 self.params - Defaults
"""
import os.path
import ConfigParser

class params:
    def __init__(self):
        self.params = {
            'charset': 'E', 
            'checkdate': None, 
            'ignore_codes': False,
            'ignore_ext_codes': False, 
            'skip_html': False, 
            'skip_997': False,
            'ignore_syntax': False,
            'map_path': '/usr/local/share/pyx12/map',
            'exclude_external_codes': ''
            }
        self.params['pickle_path'] = self.params['map_path']
        self.cfg = ConfigParser.SafeConfigParser()
        self.cfg.read(['/usr/local/etc/pyx12.conf', os.path.expanduser('~/.pyx12rc')])

        self._set_cfg_option('Main', 'map_path')
        self._set_cfg_option('Main', 'pickle_path')
        self._set_cfg_option('Main', 'exclude_external_codes')
        self._set_cfg_option('Validation', 'charset')
        self._set_cfg_option_boolean('Validation', 'ignore_syntax')
        self._set_cfg_option_boolean('Validation', 'ignore_codes')
        self._set_cfg_option_boolean('Validation', 'ignore_ext_codes')
        self._set_cfg_option_boolean('Output', 'skip_html')
        self._set_cfg_option_boolean('Output', 'skip_997')
        self._set_cfg_option('Output', 'simple_dtd')
        self._set_cfg_option('Output', 'idtag_dtd')
       
    def _set_cfg_option(self, section, option):
        if self.cfg.has_section(section):
            if self.cfg.has_option(section, option):
                try:
                    self.params[option] = self.cfg.get(section, option)
                except:
                    pass
        
    def _set_cfg_option_boolean(self, section, option):
        if self.cfg.has_section(section):
            if self.cfg.has_option(section, option):
                try:
                    self.params[option] = self.cfg.getboolean(section, option)
                except:
                    pass

    def get_param(self, param_str):
        if param_str in self.params.keys():
            return self.params[param_str]
        else:
            return None

    def set_param(self, param_str, value):
        self.params[param_str] = value

    def __repr__(self):
        res = ''
        for key in self.params.keys():
            res += '%s=%s\n' % (key, self.params[key])
        return res
