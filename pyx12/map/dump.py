#! /usr/bin/env python

import os.path
import sys

import pyx12.error_handler
import pyx12.map_if
import pyx12.segment
from pyx12.params import params


def donode(node):
    print(node.get_path())
    for child in node.children:
        if child.is_loop() or child.is_segment():
            donode(child)


param = params()
param.set("map_path", os.path.expanduser("~/src/pyx12/map/"))
map = pyx12.map_if.load_map_file(sys.argv[1], param)
donode(map)
