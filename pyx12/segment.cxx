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

#include <string>
#include <vector>
#include <iostream>
#include <fstream>

#include "segment.hxx"
#include "errors.hxx"

/*
 * Implements an interface to a x12 segment.
 *
 * A segment is comprised of a segment identifier and a sequence of elements.
 * An element can be a simple element or a composite.  A simple element is
 * treated as a composite element with one sub-element.
 *
 * All indexing is zero based.
*/ 

using namespace std;

element::element(const string& ele_str)
{
    value = ele_str;
}

size_t element::length()
{
    return 1;
}

ostream& element::operator<<(ostream& os, element& ele)
{
    os << ele;
    return os;
}

string element::format()
{
    return value;
}

string element::get_value()
{
    return value;
}

void element::set_value(string, ele_str)
{
    value = ele_str;
}

bool element::is_composite()
{
    return false;
}

bool element::is_element()
{
    return true;
}

bool element::is_empty()
{
    if(value.length() != 0)
        return true
    else
        return false
}


composite::composite(const string& ele_str, const string& subele_term_)
{
    subele_term = subele_term_;
    subele_term_orig = subele_term_;
    elements = split(ele_str);
}

bool composite::not_delim(char c)
{
    if(c != subele_term)
        return true;
    else
        return false;
}

bool composite::delim(char c)
{
    if(c == subele_term)
        return true;
    else
        return false;
}

vector<string> composite::split(const string& ele_str)
{
    typedef string::const_iterator iter;
    vector<string> ret;

    iter i = string.begin();
    while(i != str.end()) {
        i = find_if(i, str.end(), not_delim);
        j = find_if(i, str.end(), delim);
        if(i != str.end())
            ret = push_back(string(i, j));
        i = j;
    }
    return ret;
}

size_t composite::length()
{
    return elements.length();
}

ostream& composite::operator<<(ostream& os, composite& comp)
{
    for(vector<string> size_type i = 0; i != comp.size(), ++i)
        os << i->value; // XXXXXXXXXXXX
    return os;
}

string composite::format(char subele_term_='')
{
    char term;
    string ret;
    if(subele_term_ == '')
        term = subele_term;
    else
        term = subele_term_;
    if(!elements.empty())
        ret.append(elements[0].format())
    iter i = elements.begin() + 1;
    while(i != str.end()) {
        ret.append(term);
        ret.append(i->format());
    }
    return ret;
}

string composite::get_value()
{
    if(elements.length() == 1)
        return elements[0].get_value();
    else
        throw Pyx12Errors::IndexError("value of composite is undefined");
}

void composite::set_subele_term(const string& subele_term_)
{
    subele_term = subele_term_;
}

bool composite::is_composite()
{
    return true;
}

bool composite::is_element()
{
    return false;
}

bool composite::is_empty()
{
    return elements.empty();
}


class segment {
    vector<string> elements;

public:
    void append(string val);
    size_t length();
    string get_seg_id();
    string get_value_by_ref_des(const string& ref_des);
    void set_seg_term(char seg_term);
    void set_ele_term(char ele_term);
    void set_subele_term(char subele_term);
    string format();
    vector<string> format_ele_list(vector<string> str_elems, char subele_term);
};



segment::segment(const string& seg_str, const char seg_term_,
        const char ele_term_, const char subele_term_);
{
    typedef string::const_iterator iter;
    seg_term = seg_term_;
    seg_term_orig = subele_term_;
    ele_term = ele_term_;
    ele_term_orig = ele_term_;
    subele_term = subele_term_;
    subele_term_orig = subele_term_;
    seg_id = '';
    if(seg_str.empty())
        throw Errors::EngineError("seg_str should not be empty");
    if(seg_str.substr(seg_str.length()-1) == seg_term)
        seg_str.erase(seg_str.rbegin()) // strip trailing seg_term
    vector<string> elems = split(seg_str);
    seg_id = elems.front();

    iter i = elems.begin();
    while(i != elems.end()) {
        if(seg_id=="ISA")
            elements.push_back(composite((*i), ele_term));
        else
            elements.push_back(composite((*i), subele_term));
    }
    return ret;
}

bool composite::not_delim(char c)
{
    if(c != ele_term)
        return true;
    else
        return false;
}

bool composite::delim(char c)
{
    if(c == ele_term)
        return true;
    else
        return false;
}

vector<string> segment::split(const string& seg_str)
{
    typedef string::const_iterator iter;
    vector<string> ret;

    iter i = seg_str.begin();
    while(i != seg_str.end()) {
        i = find_if(i, str.end(), not_delim);
        j = find_if(i, str.end(), delim);
        if(i != str.end())
            ret.push_back(string(i, j));
        i = j;
    }
    return ret;
}

ostream& segment::operator<<(ostream& os, segment& seg)
{
    for(vector<string> size_type i = 0; i != seg.size(), ++i)
        os << i->value; // XXXXXXXXXXXX
    return os;
}

bool composite::is_empty()
{
    return elements.empty();
}
