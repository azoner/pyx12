/*
######################################################################
# Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

$Id$
*/

#ifndef PYX12_X12FILE_H_
#define PYX12_X12FILE_H_

#include <iostream>
#include <fstream>
#include <list>
#include <stack>
#include <string>
#include <utility>
#include <vector>
//#include <ostream>

#include "segment.hxx"

#define BUFSIZE 8*1024
#define ISA_LEN 106
#define MAX_LINE_LEN 1024
using namespace std;

namespace Pyx12 {
    class x12file {
    private:
        list<pair<string, string>> loops;
        stack<int> hl_stack;
        int gs_count;
        int st_count;
        int hl_count;
        int seg_count;
        int cur_line;
        //string buffer;
        vector<string> isa_ids, gs_ids, st_ids;
        string isa_usage;
        char seg_term;
        char ele_term;
        char subele_term;
        ifstream src_fs;
        get_id(string id) const;

    public:
        x12file(const string& src_filename); //, errh)
        vector<string> next();
        void cleanup();
        void print_seg(vector<string>);
        string get_isa_id() const;
        string get_gs_id() const;
        string get_st_id() const;
        string get_ls_id() const;
        int get_seg_count() const;
        int get_cur_line() const;
        list<string> get_term() const;
        string seg_str(pyx12::segment seg_data, string seg_term, string ele_term, 
            string sub_ele_term, string eol='\n') const;
        
    //    ostream& operator<<(ostream&, x12file&);
    };
};
#endif // PYX12_X12FILE_H_
