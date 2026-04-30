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
from __future__ import annotations
from typing import Any
from os.path import dirname, abspath, join, isdir, isfile, expanduser
import sys
import defusedxml.ElementTree as et
import logging

from pyx12.errors import EngineError


class ParamsBase:
    """
    Base class for parameters
    """

    logger: logging.Logger
    params: dict[str, Any]

    def __init__(self) -> None:
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

    def get(self, option: str) -> Any:
        """
        Get the value of the parameter specified by option
        :param option: Option name
        :type option: string
        """
        if option in self.params:
            return self.params[option]
        else:
            return None

    def set(self, option: str, value: Any) -> None:
        """
        Set the value of the parameter specified by option
        :param option: Option name
        :type option: string
        :param value: Parameter value
        :type value: string
        """
        if value == '':
            self.params[option] = None
        else:
            self.params[option] = value

    def _read_config_file(self, filename: str) -> None:
        """
        Read program configuration from an XML file

        :param filename: XML file
        :type filename: string
        :raises EngineError: If the config file is not found or is unreadable
        :return: None
        """
        if not isfile(filename):
            self.logger.debug(f'Configuration file "{filename}" does not exist')
            raise EngineError(f'Configuration file "{filename}" does not exist')
        try:
            self.logger.debug(f'parsing config file {filename}')
            parser = et.XMLParser(encoding='utf-8')
            t = et.parse(filename, parser=parser)
            for c in t.iter('param'):
                self._set_option(c.get('name'), c.findtext('value'), c.findtext('type'))
        except Exception:
            self.logger.error(f'Read of configuration file "{filename}" failed')
            raise

    def _set_option(self, option: str | None, value: str | None, valtype: str | None) -> None:
        """
        Set the value of the parameter specified by option
        :param option: Option name
        :type option: string
        :param value: Parameter value
        :type value: string
        :param valtype: Parameter type
        :type valtype: string
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
            self.params[option] = value


class ParamsUnix(ParamsBase):
    """
    Read options from XML configuration files
    """
    def __init__(self, config_file: str | None = None) -> None:
        super().__init__()
        config_files = [join(sys.prefix, 'etc/pyx12.conf.xml'),
                        expanduser('~/.pyx12.conf.xml')]
        for filename in config_files:
            if isfile(filename):
                self.logger.debug(f'Read param file: {filename}')
                self._read_config_file(filename)
        if config_file:
            self.logger.debug(f'Read param file: {config_file}')
            self._read_config_file(config_file)
        else:
            self.logger.debug('No config file passed to the constructor')


class ParamsWindows(ParamsBase):
    """
    Read options from XML configuration files
    """
    def __init__(self, config_file: str | None = None) -> None:
        super().__init__()
        config_files = [join(sys.prefix, 'etc/pyx12.conf.xml')]
        for filename in config_files:
            if isfile(filename):
                self.logger.debug(f'Read param file: {filename}')
                self._read_config_file(filename)
        if config_file:
            self.logger.debug(f'Read param file: {config_file}')
            self._read_config_file(config_file)


params: type[ParamsBase] = ParamsWindows if sys.platform == 'win32' else ParamsUnix
