#! /usr/bin/env /usr/local/bin/python

import os.path
import pdb
import sys

import pyx12.error_handler
#from error_handler import ErrorErrhNull
from pyx12.errors import *
import pyx12.map_if
from pyx12.params import params
import pyx12.segment


def donode(node):
    print node.get_path()
    for child in node.children:
        if child.is_loop() or child.is_segment():
            donode(child)

param = params()
param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
param.set('pickle_path', os.path.expanduser('~/src/pyx12/map/'))
map = pyx12.map_if.load_map_file(sys.argv[1], param)
donode(map)
