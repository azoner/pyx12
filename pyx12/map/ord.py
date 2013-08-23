#! /usr/bin/env python

"""
check ordinal ordering
"""

import os.path
import sys

import pyx12.error_handler
#from error_handler import ErrorErrhNull
import pyx12.map_if
from pyx12.params import params
import pyx12.segment
def donode(node):
    oldpos = 0
    old_path = ''
    old_type = ''
    for child in node.children:
        if child.is_loop() or child.is_segment():
            if child.pos < oldpos:
                #if child.is_loop(): sys.stdout.write('LOOP: ')
                #if child.is_segment(): sys.stdout.write('SEG:  ')
                sys.stdout.write('%s:\t%s\t%s\n' % (old_type, old_path, oldpos))
                sys.stdout.write('%s:\t%s\t%s\n\n' % (child.base_name, child.get_path(), child.pos))
            else:
                oldpos = child.pos
                old_path = child.get_path()
                old_type = child.base_name
        donode(child)

param = params()
param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
map = pyx12.map_if.load_map_file(sys.argv[1], param)
donode(map)
