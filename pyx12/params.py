######################################################################
# Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
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
 2. '~/.pyx12rc' - User's directory
 3. '/usr/local/etc/pyx12.conf' - Site default
 4. self.params - Defaults
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
        """
        Get the value of the parameter specified by option
        @param option: Option name
        @type option: string
        """
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
        """
        Set the value of the parameter specified by option
        @param option: Option name
        @type option: string
        @param value: Parameter value
        @type value: string
        """
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
