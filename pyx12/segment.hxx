/*
    $Id$
    This file is part of the pyX12 project.

    Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
                John Holland <jholland@kazoocmh.org> <john@zoner.org>

    All rights reserved.

        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions are
        met)

        1. Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer. 
        
        2. Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution. 
        
        3. The name of the author may not be used to endorse or promote
        products derived from this software without specific prior written
        permission. 

        THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
        IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
        INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
        (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
        SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
        HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
        STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
        IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
        POSSIBILITY OF SUCH DAMAGE.
*/

#ifndef PYX12_SEGMENT_HXX_
#define PYX12_SEGMENT_HXX_

#include <string>
#include <vector>
#include <stack>
#include <iostream>
#include <fstream>
//#include <ostream>

using namespace std;

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
    //string& operator[](size_type i) { return elements[i]; };
    //const string& operator[](size_type i) const { return elements[i]; };
    size_t length();
    ostream& operator<<(ostream&);
    string format();
    string format(const string& subele_term_);
    string get_value();
    void set_subele_term(const string& subele_term_);
    bool is_composite();
    bool is_element();
    bool is_empty();
    bool not_delim(char c);
    bool delim(char c);
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
    //string& operator[](size_type i) { return elements[i]; };
    //const string& operator[](size_type i) const { return elements[i]; };
    //string& get_item(size_type i) { return elements[i]; };
    //const string& get_item(size_type i) const { return elements[i]; };
    //void set_item(size_type i, string val) { elements[i] = val; };
    void append(string val);
    size_t length();
    string get_seg_id();
    string get_value_by_ref_des(const string& ref_des);
    void set_seg_term(const string& seg_term_);
    void set_ele_term(const string& ele_term_);
    void set_subele_term(const string& subele_term_);
    string format();
    vector<string> format_ele_list(vector<string> str_elems, const string& subele_term_);
    bool is_empty();
    bool not_delim(char c);
    bool delim(char c);

    ostream& operator<<(ostream&);
};

#endif // PYX12_SEGMENT_HXX_
