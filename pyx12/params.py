######################################################################
# Copyright (c)
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Holds Run-time Parameters

Order of precedence:
 1. set(param) - Command line parameters
 2. Config files as constructor parameters
 3. self.params - Defaults
"""
from os.path import dirname, abspath, join, isdir, isfile, expanduser
import sys
import xml.etree.cElementTree as et
import logging

from pyx12.errors import EngineError


class ParamsBase(object):
    """
    Base class for parameters
    """
    def __init__(self):
        self.logger = logging.getLogger('pyx12.params')
        self.params = {}
        #First, try relative path
        base_dir = dirname(dirname(abspath(sys.argv[0])))
        map_path = join(base_dir, 'map')
        #Then look in standard installation location
        if not isdir(map_path):
            map_path = join(sys.prefix, 'share', 'pyx12', 'map')
        self.params['map_path'] = map_path
        self.params['exclude_external_codes'] = None
        self.params['charset'] = 'E'
        self.params['simple_dtd'] = ''
        self.params['xmlout'] = 'simple'

    def get(self, option):
        """
        Get the value of the parameter specified by option
        @param option: Option name
        @type option: string
        """
        if option in list(self.params.keys()):
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
        if value == '':
            self.params[option] = None
        else:
            self.params[option] = value

    def _read_config_file(self, filename):
        """
        Read program configuration from an XML file

        @param filename: XML file
        @type filename: string
        @raise EngineError: If the config file is not found or is unreadable
        @return: None
        """
        if not isfile(filename):
            self.logger.debug('Configuration file "%s" does not exist' %
                              filename)
            raise EngineError('Configuration file "%s" does not exist' %
                              (filename))
        try:
            self.logger.debug('parsing config file %s' % (filename))
            t = et.parse(filename)
            for c in t.iter('param'):
                option = c.get('name')
                value = c.findtext('value')
                valtype = c.findtext('type')
                self._set_option(option, value, valtype)
        except Exception:
            self.logger.error('Read of configuration file "%s" failed' %
                              (filename))
            raise

    def _set_option(self, option, value, valtype):
        """
        Set the value of the parameter specified by option
        @param option: Option name
        @type option: string
        @param value: Parameter value
        @type value: string
        @param valtype: Parameter type
        @type valtype: string
        """
        if option is None or option == '':
            return
        if value == '':
            value = None
        if valtype == 'boolean':
            if value in ('False', 'F'):
                self.params[option] = False
            else:
                self.params[option] = True
        else:
            try:
                if self.params[option] != value:
                    self.params[option] = value
                    #self.logger.debug('Params: option "%s": "%s"' % \
                    #    (option, self.params[option]))
            except Exception:
                self.params[option] = value
                #self.logger.debug('Params: option "%s": "%s"' % \
                #   (option, self.params[option]))
        #self.logger.debug('Params: option "%s": "%s"' % \
        #    (option, self.params[option]))


class ParamsUnix(ParamsBase):
    """
    Read options from XML configuration files
    """
    def __init__(self, config_file=None):
        ParamsBase.__init__(self)
        config_files = [join(sys.prefix, 'etc/pyx12.conf.xml'),
                        expanduser('~/.pyx12.conf.xml')]
        for filename in config_files:
            if isfile(filename):
                self.logger.debug('Read param file: %s' % (filename))
                self._read_config_file(filename)
        if config_file:
            self.logger.debug('Read param file: %s' % (filename))
            self._read_config_file(config_file)
        else:
            self.logger.debug('No config file passed to the constructor')


class ParamsWindows(ParamsBase):
    """
    Read options from XML configuration files
    """
    def __init__(self, config_file=None):
        ParamsBase.__init__(self)
        config_files = [join(sys.prefix, 'etc/pyx12.conf.xml')]
        for filename in config_files:
            if isfile(filename):
                self.logger.debug('Read param file: %s' % (filename))
                self._read_config_file(filename)
        if config_file:
            self.logger.debug('Read param file: %s' % (filename))
            self._read_config_file(config_file)

if sys.platform == 'win32':
    params = ParamsWindows
else:
    params = ParamsUnix
