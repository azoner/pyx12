#! /usr/bin/env python
######################################################################
# Copyright (c) 2001-2008 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Generate SQL DDL for a table structure fitting a map
"""

import os, os.path
import string
import sys
import logging
import pdb

# Intrapackage imports
import pyx12
import pyx12.map_if
import pyx12.x12n_document
import pyx12.params

__author__  = pyx12.__author__
__status__  = pyx12.__status__
__version__ = pyx12.__version__
__date__    = pyx12.__date__

tbl_stack = [] # tuple(table_name, pk, path)

class SQL_Error(Exception):
    """Class for SQL errors."""

class table:
    def __init__(self, node_id, node_name, path, parent=None, etype='loop'):
        self.parent = parent
        if self.parent:
            self.root = self.parent.root
        self.name = self.root.unique_tablename(node_id, node_name, path, etype)
        self.pk = '%s_%s_num' % (self.root.prefix, node_id)
        self.path = path
        self.field_prefix = ''
        self.fk_name = self.root.unique_fk_name(path)
        self.fields = [] # (name, etype)
        self.sub_tables = []
        self.root.table_list.append(self.name)

    def __repr__(self):
        str1 = ''
        if self.fk_name:
            str1 += '%s\n' % (self.fk_name)
        for table1 in self.sub_tables:
            str1 += table1.__repr__()
        return str1

    def generate(self):
        str1 = 'CREATE TABLE [%s] ( -- %s\n' % (self.name, self.path)
        str1 += '\t[%s] [int] IDENTITY (1, 1) NOT NULL\n' % (self.pk)
        if self.parent and self.parent.get_pk():
            str1 += ',\t[%s] [int] NOT NULL\n' % (self.parent.get_pk())
        for (name, type_str) in self.fields:
            str1 += ',\t[%s] %s\n' % (name, type_str)
        str1 += ') ON [PRIMARY]\nGO\n\n'   

        #primary key
        str1 += 'ALTER TABLE [%s] WITH NOCHECK ADD\n' % (self.name)
        str1 += '\tCONSTRAINT [PK_%s] PRIMARY KEY CLUSTERED\n\t(\n\t\t[%s]\n' % (self.name, self.pk)
        str1 += '\t)  ON [PRIMARY]\nGO\n\n'
        
        #foreign keys
        if self.parent and self.parent.get_pk():
            if self.fk_name == '':
                raise SQL_Error, 'Bad FK string %s' % (self.name)
            parent_table = self.parent.name
            pk_parent = self.parent.get_pk()
            str1 += 'ALTER TABLE [%s] ADD\n' % (self.name)
            #str1 += '\tCONSTRAINT [FK_%s_%s] FOREIGN KEY\n' % (self.name, parent_table)
            str1 += '\tCONSTRAINT [FK_%s_%s] FOREIGN KEY\n' % (self.root.prefix, self.fk_name)
            str1 += '\t( [%s] )\n' % (pk_parent)
            str1 += '\tREFERENCES [%s] ([%s])\nGO\n\n' % (parent_table, pk_parent)

        for table1 in self.sub_tables:
            str1 += table1.generate()
        
        return str1
        
    def format_name(self, name):
        return name.replace(' ', '_').replace("'", '')

    def get_pk(self):
        return self.pk

    def is_match(self, path):
        return path == self.path

    def is_match_parent(self, path):
        if self.parent:
            return path == self.parent.path
        else:
            return path == '/'

    def _get_unique_field_name(self, id, name):
        field_list = map(lambda x: x[0], self.fields)
        field_name = '%s_%s' % (id, format_name(name))
        if field_name not in field_list:
            return field_name
        field_name = '%s_%s_%s' % (id, self.field_prefix, name)
        idx = 'A'
        while field_name in field_list:
            field_name = '%s_%s_%s' % (id, idx, name)
            idx = chr(ord(idx)+1)
        return field_name
        

class root_table(table):
    def __init__(self, node_id, node_name, path, parent, prefix):
        self.root = self
        self.table_list = []
        self.fk_list = []
        self.prefix = prefix
       # table.__init__(self, node_id, node_name, path, parent)
        
        self.parent = None
        self.name = 'x12_st_loop'
        self.pk = 'st_num'
        self.path = '/'
        self.field_prefix = ''
        self.fk_name = None
        self.fields = [] # (name, type)
        self.sub_tables = []
        self.root.table_list.append(self.name)
        
    def generate(self):
        str1 = ''
        for table1 in self.sub_tables:
            str1 += table1.generate()
        return str1

    def unique_tablename(self, node_id, node_name, path, etype='loop'): 
        clean_name = self.format_name(node_name)
        parents = path[1:].split('/')
        if etype == 'loop' or len(parents) <= 2:
            table_name = ('%s_%s_%s' % (self.prefix, node_id, clean_name))[:120]
        else:
            table_name = ('%s_%s_%s_%s' % (self.prefix, parents[-2], node_id, clean_name))[:120]
            del parents[-1]
            del parents[-1]
        i = 1
        while table_name in self.table_list:
            table_name = ('%s_%s_%s_%s' % (self.prefix, string.join(parents[:-i], '_'), \
                node_id, clean_name))[:120]
            i += 1
            #pdb.set_trace()
            #raise SQL_Error, 'Duplicate Table Name %s' % (table_name)
        return table_name

    def unique_fk_name(self, path):
        fmt_path = string.join(path.split('/'), '_')
        fk1 = fmt_path
        idx = 'A'
        while fk1 in self.fk_list:
            fk1 = fmt_path + '_' + idx
            idx = chr(ord(idx)+1)
        self.fk_list.append(fk1)
        return fk1


def format_name(name):
    return name.replace(' ', '_').replace("'", '')

def gen_sql(map_root, prefix):
    """
    iterate through map, generate sql
    """
    st_loop = root_table('ST', 'ST LOOP', '/', None, prefix)
    cur_table = st_loop

    for node in map_root:
        path = node.get_path()
        parent = os.path.dirname(path)
        
        if node.id is None:
            continue
        if node.id[:3] in ('ISA', 'IEA', 'TA1') or \
            node.id[:2] in ('GS', 'GE', 'ST', 'SE'):
            continue
        if node.is_map_root():
            continue
        if node.is_loop():
            #pdb.set_trace()
            if node.get_max_repeat() != 1: # Create new table
                # who is parent?
                # same level, then pop to parent and create sub-table
                if cur_table.is_match_parent(parent):
                    if cur_table.parent:
                        cur_table = cur_table.parent
                    cur_table.sub_tables.append(table(node.id, node.name, path, cur_table))
                    cur_table = cur_table.sub_tables[-1]
                    cur_table.fk_name = cur_table.root.unique_fk_name(\
                        string.join(path.split('/'), '_'))

                # cur loop node is child of table
                elif cur_table.is_match(parent):
                    cur_table.sub_tables.append(table(node.id, node.name, path, cur_table))
                    cur_table = cur_table.sub_tables[-1]
                
                # cur loop node is up at least one level
                else:
                    # pop stack to parent
                    while cur_table.parent and not cur_table.is_match_parent(parent):
                        cur_table = cur_table.parent
                    cur_table.sub_tables.append(table(node.id, node.name, path, cur_table))
                    cur_table = cur_table.sub_tables[-1]
            else:
                cur_table.sub_tables.append(table(node.id, node.name, path, cur_table))
                cur_table = cur_table.sub_tables[-1]
                
        elif node.is_segment():
            cur_table.field_prefix = '' #%s' % (node.id)
            if node.children[0].is_element() \
                and node.children[0].data_type == 'ID' \
                and node.children[0].valid_codes:
                cur_table.field_prefix = '%s' % (node.children[0].valid_codes[0])
            # Find parent loop
            #pdb.set_trace()
            while cur_table.parent and cur_table.is_match_parent(parent):
                cur_table = cur_table.parent

            #if tbl_stack and tbl_stack[-1][2] == node.get_path(): #Repeat of segment
            #    continue
            if node.get_max_repeat() != 1: # Create sub table
                # who is parent
                parent_id = parent.split('/')[-1]
                cur_table.sub_tables.append(table(node.id, node.name, path, cur_table, 'segment'))
                cur_table = cur_table.sub_tables[-1]
        elif node.is_element():
            if node.usage == 'N':
                continue
            #field_name = '%s_%s_%s' % (node.id, cur_table.field_prefix, format_name(node.name))
            vtype = ''
            if node.data_type in ('DT', 'TM'):
                vtype = ' [datetime]'
            elif node.data_type in ('AN', 'ID'):
                if node.min_len == node.max_len:
                    vtype = ' [char] (%s)' % (node.max_len)
                else:
                    vtype = ' [varchar] (%s)' % (node.max_len)
            elif node.data_type == 'N0':
                vtype = ' [int]'
            elif node.data_type == 'R' or node.data_type[0] == 'N':
                vtype = ' [float]'
            if vtype is None:
                raise SQL_Error, 'bad type %s' % (node.data_type)
            vtype += ' NULL'
            vtype += '  -- %s(%s, %s)' % (node.data_type, node.min_len, node.max_len)
            field_name = cur_table._get_unique_field_name(node.id, \
                format_name(node.name))
            cur_table.fields.append((field_name, vtype))
        elif node.is_composite():
            pass
    return st_loop

   
def usage():
    sys.stdout.write('x12sql.py %s (%s)\n' % (__version__, __date__))
    sys.stdout.write('usage: x12sql.py [options] source_files\n')
    sys.stdout.write('\noptions:\n')
    sys.stdout.write('  -m <path>  Path to map files\n')
    sys.stdout.write('  -p <path>  Path to to pickle files\n')
    sys.stdout.write('  -q         Quiet output\n')
    sys.stdout.write('  -v         Verbose output\n')
    
def main():
    """
    Set up environment for processing
    """
    import getopt
    param = pyx12.params.params()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:f:m:p:qv')
    except getopt.error, msg:
        usage()
        return False
    logger = logging.getLogger('pyx12')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')

    stderr_hdlr = logging.StreamHandler()
    stderr_hdlr.setFormatter(formatter)
    logger.addHandler(stderr_hdlr)

    prefix = None
    for o, a in opts:
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-m': param.set('map_path', a)
        if o == '-p': param.set('pickle_path', a)
        if o == '-f': prefix = a
        if o == '-l':
            try:
                hdlr = logging.FileHandler(a)
                hdlr.setFormatter(formatter)
                logger.addHandler(hdlr) 
            except IOError:
                logger.error('Could not open log file: %s' % (a))
        #if o == '-9': target_997 = os.path.splitext(src_filename)[0] + '.997'
    map_path = param.get('map_path')

    for map_filename in args:
        try:
            (map_path, map_file) = os.path.split(os.path.abspath(map_filename))
            if os.path.isfile(os.path.join(map_path, map_file)):
                param.set('map_path', map_path)
            if not prefix:
                prefix = map_file.split('.')[0]
            sql = gen_sql(pyx12.map_if.map_if(os.path.join(map_path, map_file), param), prefix)
            print sql.generate()
            #print sql
        except IOError:
            logger.error('Could not open files')
            usage()
            return False
        except KeyboardInterrupt:
            print "\n[interrupt]"

    return True

#profile.run('x12n_document(src_filename)', 'pyx12.prof')
if __name__ == '__main__':
    sys.exit(not main())

