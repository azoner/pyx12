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
 set(param) - Command line parameters
 '~/.pyx12rc' - User's directory
 '/usr/local/etc/pyx12.conf' - Site default
 self.params - Defaults
"""
import os.path
import ConfigParser
import StringIO

class params:
    def __init__(self, config_file=None):
        default = """
[Main]
map_path=/usr/local/share/pyx12/map
pickle_path=%(map_path)s
exclude_external_codes=
[Validation]
ignore_syntax=False
charset=E
ignore_codes=False
ignore_ext_codes=False
[Output]
skip_html=False
skip_997=False
simple_dtd=http://www.kazoocmh.org/x12simple.dtd
idtag_dtd=http://www.kazoocmh.org/x12idtag.dtd
"""
        self.cfg = ConfigParser.SafeConfigParser()
        self.cfg.readfp(StringIO.StringIO(default))
        if config_file:
            self.cfg.read(['/usr/local/etc/pyx12.conf', \
                os.path.expanduser('~/.pyx12rc'), config_file])
        else:
            self.cfg.read(['/usr/local/etc/pyx12.conf', \
                os.path.expanduser('~/.pyx12rc')])

    def get(self, option):
        for section in self.cfg.sections():
            if self.cfg.has_option(section, option):
                try:
                    return self.cfg.getboolean(section, option)
                except ValueError:
                    try:
                        return self.cfg.get(section, option)
                    except ValueError:
                        pass
        return None

    def set(self, option, value):
        for section in self.cfg.sections():
            if self.cfg.has_option(section, option):
                try:
                    if value is False:
                        self.cfg.set(section, option, 'False')
                    elif value is True:
                        self.cfg.set(section, option, 'True')
                    else:
                        self.cfg.set(section, option, value)
                except:
                    pass

    def __repr__(self):
        fd_out = StringIO.StringIO() 
        self.cfg.write(fd_out)
        return fd_out.getvalue()
