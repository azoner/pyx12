#! /usr/bin/env python

import os.path
import sys
from os.path import abspath, join, dirname, isdir, isfile

import xml.etree.cElementTree as et

def move_to_attrib(etree, ele_name):
    if not etree.get(ele_name):
        v = etree.findtext(ele_name)
        if v is not None:
            etree.set(ele_name, v)
            for x in etree.iterfind(ele_name):
                etree.remove(x)

def do_node(etree):
    move_to_attrib(root, 'name')

    for e in root.iter('loop'):
        print(e.get('xid'))
        move_to_attrib(e, 'name')
        move_to_attrib(e, 'usage')
        move_to_attrib(e, 'pos')
        move_to_attrib(e, 'repeat')
        #do_node(e)
        #if e.text.strip() == '':
        #    e.text = None

    for e in root.iter('segment'):
        print(e.get('xid'))
        move_to_attrib(e, 'name')
        move_to_attrib(e, 'usage')
        move_to_attrib(e, 'pos')
        move_to_attrib(e, 'max_use')
        move_to_attrib(e, 'end_tag')
        #do_node(e)
        #if e.text.strip() == '':
        #    e.text = None

    for e in root.iter('element'):
        print(e.get('xid'))
        move_to_attrib(e, 'name')
        move_to_attrib(e, 'data_ele')
        move_to_attrib(e, 'usage')
        move_to_attrib(e, 'seq')
        move_to_attrib(e, 'repeat')
        if e.text.strip() == '':
            e.text = None
        v = e.find('valid_codes')
        if v is not None:
            k = []
            for c in v.findall('code'):
                k.append(c.text)
                v.remove(c)
            v.set('values', ','.join(k))
            if v.text is not None and v.text.strip() == '':
                v.text = None

    for e in root.iter('composite'):
        print(e.get('xid'))
        move_to_attrib(e, 'name')
        move_to_attrib(e, 'data_ele')
        move_to_attrib(e, 'usage')
        move_to_attrib(e, 'seq')
        move_to_attrib(e, 'repeat')
        if e.text.strip() == '':
            e.text = None

s = '835.5010.X221.A1.xml'
t = '835.5010.X221.A1.v3.xml'
tree = et.parse(s)
root = tree.getroot()

do_node(root)

tree.write(t)