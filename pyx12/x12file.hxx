/*
######################################################################
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
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

#include <fstream>
#include <iostream>
#include <iterator>
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

    /** Interface to an X12 data file.
     * 
     * Efficiently handles large files.
     * Tracks end of explicit loops.
     * Tracks segment/line/loop counts.
     */
    class x12file {
    public:
        x12file(const string& src_filename); //, errh)
        vector<string> next();
        //void cleanup();
        //void print_seg(vector<string>);
        string get_isa_id() const;
        string get_gs_id() const;
        string get_st_id() const;
        string get_ls_id() const;
        int get_seg_count() const {return seg_count;};
        int get_cur_line() const {return cur_line;};
        list<string> get_term() const;
        list<list<string, string, string, string, int> > get_errors() const;
        
    private:
        list<pair<string, string> > loops;
        stack<int> hl_stack;
        int gs_count;
        int st_count;
        int hl_count;
        int seg_count;
        int cur_line;
        list<list<string, string, string, string, int> > err_list;
        //string buffer;
        vector<string> isa_ids, gs_ids, st_ids;
        string isa_usage;
        char seg_term;
        char ele_term;
        char subele_term;
        ifstream src_fs;
        string get_id(string id) const;
        string read_seg();
        void isa_error(const string err_cde, const string err_str);
        void gs_error(const string err_cde, const string err_str);
        void st_error(const string err_cde, const string err_str);
        void seg_error(const string err_cde, const string err_str, const string err_val, const int src_line);
    //    ostream& operator<<(ostream&, x12file&);
    };
/*
    class x12fileIter : public iterator <forward_iterator_tag, pyx12::x12file> {
    }
*/  
};
#endif // PYX12_X12FILE_H_
