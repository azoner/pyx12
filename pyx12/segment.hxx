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

#ifndef PYX12_SEGMENT_HXX_
#define PYX12_SEGMENT_HXX_

#include <string>
#include <vector>
#include <stack>
#include <iostream>
#include <fstream>
#include <cstddef>
#include <memory>
#include <algorithm>

//#include <ostream>

using namespace std;

namespace Pyx12 {
    class element {
    private:
        string value;
        
    public:
        element(const string& ele_str);
        size_t length();
        ostream& operator<<(ostream&);
        string format();
        string get_value();
        void set_value(string ele_str);
        bool is_composite();
        bool is_element();
        bool is_empty();
    };


    class composite {
    private:
        vector<element> elements;
        string subele_term, subele_term_orig;
        vector<string> split(const string& ele_str);

    public:
        composite(const string& ele_str, const string& subele_term_);
        element& operator[](size_t);
        const element& operator[](size_t) const;
        size_t length();
        ostream& operator<<(ostream&);
        string format();
        string format(const string& subele_term_);
        string get_value();
        void set_subele_term(const string& subele_term_);
        bool is_composite();
        bool is_element();
        bool is_empty();
        //bool not_delim(char c);
        //bool delim(char c);
    };


    class segment {
    private:
        string seg_term, seg_term_orig;
        string ele_term, ele_term_orig;
        string subele_term, subele_term_orig;
        string seg_id;
        vector<composite> elements;
        vector<string> split(const string& ele_str);

    public:
        segment(const string& seg_str, const string& seg_term_, 
            const string& ele_term_, const string& subele_term_);
        composite& operator[](size_t i);
        const composite& operator[](size_t i) const;
        composite& get_item(size_t i);
        const composite& get_item(size_t i) const;
        void set_item(size_t i, string val);
        void append(const string& ele_str);
        size_t length();
        string get_seg_id();
        string get_value_by_ref_des(const string& ref_des);
        void set_seg_term(const string& seg_term_);
        void set_ele_term(const string& ele_term_);
        void set_subele_term(const string& subele_term_);
        string format();
        string format(const string& seg_term_, const string& ele_term_, const string& subele_term_);
        vector<string> format_ele_list(vector<string> str_elems, const string& subele_term_);
        bool is_empty();
        //bool not_delim(char c);
        //bool delim(char c);

        ostream& operator<<(ostream&);
    };
}
#endif // PYX12_SEGMENT_HXX_
