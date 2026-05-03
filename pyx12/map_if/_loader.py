######################################################################
# Copyright (c)
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
"""
load_map_file - parses an X12N IG XML map and returns the root.
"""

from __future__ import annotations

import logging
import os.path
from importlib.resources import files as _res_files
from typing import IO, Any

import defusedxml.ElementTree as et

from ..errors import EngineError
from ._root import map_if


def load_map_file(map_file: str, param: Any, map_path: str | None = None) -> map_if:
    """
    Create the map object from a file

    :param map_file: filename (basename) of the map xml file to load
    :type map_file: string
    :param map_path: Override directory containing map xml files.  If None,
        uses package resource folder
    :type map_path: string
    :rtype: pyx12.map_if
    """
    logger = logging.getLogger("pyx12")
    # Reject any path component in map_file to prevent traversal out of map_path
    if map_file != os.path.basename(map_file) or os.path.isabs(map_file):
        raise EngineError(f"Invalid map file name: {map_file}")
    map_fd: IO[Any]
    if map_path is not None:
        logger.debug(f"Looking for map file '{map_file}' in map_path '{map_path}'")
        if not os.path.isdir(map_path):
            raise OSError(2, "Map path does not exist", map_path)
        full_path = os.path.join(map_path, map_file)
        if not os.path.isfile(full_path):
            raise OSError(2, f"Pyx12 map file '{map_file}' does not exist in map path", map_path)
        map_fd = open(full_path, encoding="utf-8")
    else:
        logger.debug(f"Looking for map file '{map_file}' in package resources")
        map_fd = _res_files("pyx12").joinpath("map", map_file).open("rb")
    with map_fd:
        logger.debug("Create map from %s" % (map_file))
        parser = et.XMLParser(encoding="utf-8")
        etree = et.parse(map_fd, parser=parser)
        return map_if(etree.getroot(), param, map_path)
