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

#include <string>
#include <vector>
#include <stack>
#include <iostream>
#include <fstream>
#include <ostream>

#define BUFSIZE 8*1024
#define ISA_LEN 106
#define MAX_LINE_LEN 1024
using namespace std;

namespace Pyx12 {
    class x12file {
    private:
        stack<string> loops;
        stack<string> hl_stack;
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

    public:
        x12file(const string& src_filename); //, errh)
        vector<string> next();
        void cleanup();
        void print_seg(vector<string>);
        string format_seg(vector<string>);
    //    ostream& operator<<(ostream&, x12file&);
    };
};
#endif // PYX12_X12FILE_H_
