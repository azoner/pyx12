#! /usr/bin/env /usr/local/bin/python
#
#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#                John Holland <jholland@kazoocmh.org> <john@zoner.org>
#
#    All rights reserved.
#
#        Redistribution and use in source and binary forms, with or without modification, 
#        are permitted provided that the following conditions are met:
#
#        1. Redistributions of source code must retain the above copyright notice, this list 
#           of conditions and the following disclaimer. 
#        
#        2. Redistributions in binary form must reproduce the above copyright notice, this 
#           list of conditions and the following disclaimer in the documentation and/or other 
#           materials provided with the distribution. 
#        
#        3. The name of the author may not be used to endorse or promote products derived 
#           from this software without specific prior written permission. 
#
#        THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED 
#        WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
#        MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
#        EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#        EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
#        OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
#        INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
#        CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
#        ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
#        THE POSSIBILITY OF SUCH DAMAGE.

"""
Generate SQL DDL for a table structure fitting a map
"""

import os, os.path
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

TRANS_PRE = 't_'
tbl_stack = [] # tuple(table_name, pk, path)

class SQL_Error(Exception):
    """Class for SQL errors."""

class table:
    def __init__(self, name, pk, path, parent):
        self.name = name
        self.pk = pk
        self.path = path
        self.parent = parent
        self.fields = [] # (name, type)
        self.sub_tables = []

    def __repr__(self):
        str1 = 'CREATE TABLE [%s] ( -- %s\n' % (self.name, self.path)
        str1 += '\t[%s] [int] IDENTITY (1, 1) NOT NULL\n' % (self.pk)
        if self.parent and self.parent.get_pk():
            str1 += ',\t[%s] [int] NOT NULL\n' % (self.parent.get_pk())
        #for (name, type_str) in self.fields:
        #    str1 += ',\t[%s] %s\n' % (name, type_str)
        for table1 in self.sub_tables:
            str1 += table1.__repr__()
        str1 += ') ON [PRIMARY]\nGO\n\n'   
        
        #primary key
        str1 += 'ALTER TABLE [%s] WITH NOCHECK ADD\n' % (self.name)
        str1 += '\tCONSTRAINT [PK_%s] PRIMARY KEY CLUSTERED\n\t(\n\t\t[%s]\n' % (self.name, self.pk)
        str1 += '\t)  ON [PRIMARY]\nGO\n\n'
        
        #foreign keys
        if self.parent and self.parent.get_pk():
            parent_table = self.parent.name
            pk_parent = self.parent.get_pk()
            str1 += 'ALTER TABLE [%s] ADD\n' % (self.name)
            str1 += '\tCONSTRAINT [FK_%s_%s] FOREIGN KEY\n' % (self.name, parent_table)
            str1 += '\t( [%s] )\n' % (pk_parent)
            str1 += '\tREFERENCES [%s] ([%s])\nGO\n' % (parent_table, pk_parent)
        return str1
        
    def get_pk(self):
        return self.pk

    def is_match(self, path):
        return path == self.path

    def is_match_parent(self, path):
        if self.parent:
            return path == self.parent.path
        else:
            return path == '/'

        
def format_name(name):
    return name.replace(' ', '_')
    
def gen_sql(map_root, pre):
    """
    iterate through map, generate sql
    """
    global TRANS_PRE
    TRANS_PRE = pre + '_'
    st_loop = table('%s_ST' % (TRANS_PRE), '%s_ST_num' % (TRANS_PRE), '/', None)
    cur_table = st_loop

    for node in map_root:
        path = node.get_path()
        parent = os.path.dirname(path)
        
        if node.id is None:
            continue
        id = node.id
        if id[:3] in ('ISA', 'IEA', 'TA1') or \
            id[:2] in ('GS', 'GE', 'ST', 'SE'):
            continue
        if node.is_map_root():
            continue
        if node.is_loop():
            #pdb.set_trace()
            if node.get_max_repeat() != 1: # Create new table
                # who is parent?
                # same level, then pop to parent and create sub-table
                if cur_table.is_match_parent(parent):
                    cur_table = cur_table.parent
                    table_name = '%s%s_%s' % (TRANS_PRE, node.id, format_name(node.name))
                    pk = '%s_num' % (node.id)
                    cur_table.sub_tables.append(table(table_name, pk, path, cur_table))
                    cur_table = cur_table.sub_tables[-1]

                # cur loop node is child of table
                elif cur_table.is_match(parent):
                    table_name = '%s%s_%s' % (TRANS_PRE, node.id, format_name(node.name))
                    pk = '%s_num' % (node.id)
                    cur_table.sub_tables.append(table(table_name, pk, path, cur_table))
                    cur_table = cur_table.sub_tables[-1]
                
                # cur loop node is up at least one level
                else:
                    # pop stack to parent
                    while cur_table.parent and not cur_table.is_match_parent(parent):
                        cur_table = cur_table.parent
                    
                    table_name = '%s%s_%s' % (TRANS_PRE, node.id, format_name(node.name))
                    pk = '%s_num' % (node.id)
                    cur_table.sub_tables.append(table(table_name, pk, path, cur_table))
                    cur_table = cur_table.sub_tables[-1]
            else:
                table_name = '%s%s_%s' % (TRANS_PRE, node.id, format_name(node.name))
                pk = '%s_num' % (node.id)
                cur_table.sub_tables.append(table(table_name, pk, path, cur_table))
                cur_table = cur_table.sub_tables[-1]
                
        elif node.is_segment():
            # Find parent loop
            while cur_table.parent and not cur_table.is_match_parent(parent):
                cur_table = cur_table.parent

            #if tbl_stack and tbl_stack[-1][2] == node.get_path(): #Repeat of segment
            #    continue
            if node.get_max_repeat() != 1: # Create sub table
                # who is parent
                table_name = '%s%s_%s' % (TRANS_PRE, node.id, format_name(node.name))
                pk = '%s_num' % (node.id)
                cur_table.sub_tables.append(table(table_name, pk, path, cur_table))
                cur_table = cur_table.sub_tables[-1]
        elif node.is_element():
            field_name = '%s_%s' % (node.id, format_name(node.name))
            type = ''
            if node.data_type in ('DT', 'TM'):
                type = ' [datetime]'
            elif node.data_type in ('AN', 'ID'):
                if node.min_len == node.max_len:
                    type = ' [char] (%s)' % (node.max_len)
                else:
                    type = ' [varchar] (%s)' % (node.max_len)
            elif node.data_type == 'N0':
                type = ' [int]'
            elif node.data_type == 'R' or node.data_type[0] == 'N':
                type = ' [float]'
            if type is None:
                raise SQL_Error, 'bad type %s' % (node.data_type)
            type += ' NULL'
            type += '  -- %s(%s, %s)' % (node.data_type, node.min_len, node.max_len)
            cur_table.fields.append((field_name, type))
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
        opts, args = getopt.getopt(sys.argv[1:], 'c:fm:p:qv')
    except getopt.error, msg:
        usage()
        sys.exit(2)
    logger = logging.getLogger('pyx12')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')

    stderr_hdlr = logging.StreamHandler()
    stderr_hdlr.setFormatter(formatter)
    logger.addHandler(stderr_hdlr)

    #param.set_param('map_path', os.path.expanduser('/usr/local/share/pyx12/map'))
    #param.set_param('pickle_path', os.path.expanduser('/tmp'))
    for o, a in opts:
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-f': param.set_param('force_map_load', True)
        if o == '-m': param.set_param('map_path', a)
        if o == '-p': param.set_param('pickle_path', a)
        if o == '-l':
            try:
                hdlr = logging.FileHandler(a)
                hdlr.setFormatter(formatter)
                logger.addHandler(hdlr) 
            except IOError:
                logger.error('Could not open log file: %s' % (a))
        #if o == '-9': target_997 = os.path.splitext(src_filename)[0] + '.997'
    map_path = param.get_param('map_path')

    for map_filename in args:
        try:
            pre = map_filename.split('.')[0]
            sql = gen_sql(pyx12.map_if.map_if(os.path.join(map_path, map_filename), param), pre)
            print sql
        except IOError:
            logger.error('Could not open files')
            usage()
            sys.exit(2)
        except KeyboardInterrupt:
            print "\n[interrupt]"

    return True

#profile.run('x12n_document(src_filename)', 'pyx12.prof')
if __name__ == '__main__':
    sys.exit(not main())

    def pop_to_parent_loop(self, node):
        if node.is_map_root():
            return node
        map_node = node.parent
        if map_node is None:
            raise EngineError, "Node is None: %s" % (node.name)
        while not (map_node.is_loop() or map_node.is_map_root()): 
            map_node = map_node.parent
        if not (map_node.is_loop() or map_node.is_map_root()):
            raise EngineError, "Called pop_to_parent_loop, can't find parent loop"
        return map_node
        

