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
#include <algorithm>

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

ostream& element::operator<<(ostream& os)
{
    os << value;
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

void element::set_value(string ele_str)
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
        return true;
    else
        return false;
}


composite::composite(const string& ele_str, const string& subele_term_)
{
    typedef vector<string>::const_iterator iter;
    subele_term = subele_term_;
    subele_term_orig = subele_term_;
    vector<string> elems = split(ele_str);
    iter i = elems.begin();
    while(i != elems.end()) {
        elements.push_back(element((*i)));
    }
}

/*
bool composite::not_delim(char c)
{
    if(c != subele_term[0])
        return true;
    else
        return false;
}

bool composite::delim(char c)
{
    if(c == subele_term[0])
        return true;
    else
        return false;
}
*/

vector<string> composite::split(const string& ele_str)
{
    typedef string::const_iterator iter;
    vector<string> ret;

    iter i = ele_str.begin();
    iter j;
    while(i != ele_str.end()) {
        //i = find_if(i, ele_str.end(), composite::not_delim);
        while(i != ele_str.end())
            if((*i) != subele_term[0])
                break;
        j = find(i, ele_str.end(), subele_term[0]);
        //j = find_if(i, ele_str.end(), composite::delim);
        if(i != ele_str.end())
            ret.push_back(string(i, j));
        i = j;
    };
    return ret;
}

size_t composite::length()
{
    return elements.size();
}

ostream& composite::operator<<(ostream& os)
{
    vector<element>::iterator i = elements.begin();
    while(i != elements.end()) {
        os << i->format();
        ++i;
    }
    return os;
}

string composite::format()
{
    return format(subele_term);
}

string composite::format(const string& subele_term_)
{
    typedef vector<element>::iterator iter;
    string term;
    string ret;
    term = subele_term_;
    if(!elements.empty())
        ret.append(elements[0].format());
    iter i = elements.begin() + 1;
    while(i != elements.end()) {
        ret += term;
        ret += i->format();
    }
    return ret;
}

string composite::get_value()
{
    if(elements.size() == 1)
        return elements[0].get_value();
    else
        throw Pyx12Errors::EngineError("value of composite is undefined");
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


segment::segment(const string& seg_str, const string& seg_term_,
        const string& ele_term_, const string& subele_term_)
{
    typedef vector<string>::const_iterator iter;
    vector<string> elems;
    seg_term = seg_term_;
    seg_term_orig = subele_term_;
    ele_term = ele_term_;
    ele_term_orig = ele_term_;
    subele_term = subele_term_;
    subele_term_orig = subele_term_;
    //seg_id = '';
    if(seg_str.empty())
        throw Pyx12Errors::EngineError("seg_str should not be empty");
    if(seg_str.substr(seg_str.length()-1) == seg_term)
        //elems = split(seg_str.substr(seg_str.begin(), seg_str.end()-1));
        elems = split(seg_str.substr(0, seg_str.length()-1));
    else
        elems = split(seg_str);
    seg_id = elems.front();

    iter i = elems.begin();
    while(i != elems.end()) {
        if(seg_id=="ISA")
            elements.push_back(composite((*i), ele_term));
        else
            elements.push_back(composite((*i), subele_term));
    }
}
/*
bool segment::not_delim(char c)
{
    if(c != ele_term[0])
        return true;
    else
        return false;
}

bool segment::delim(char c)
{
    if(c == ele_term[0])
        return true;
    else
        return false;
}
*/
vector<string> segment::split(const string& seg_str)
{
    typedef string::const_iterator iter;
    vector<string> ret;

    iter i = seg_str.begin();
    iter j;
    while(i != seg_str.end()) {
        //i = find_if(i, seg_str.end(), segment::not_delim);
        //j = find_if(i, seg_str.end(), segment::delim);
        while(i != seg_str.end())
            if((*i) != ele_term[0])
                break;
        j = find(i, seg_str.end(), ele_term[0]);
        if(i != seg_str.end())
            ret.push_back(string(i, j));
        i = j;
    }
    return ret;
}

ostream& segment::operator<<(ostream& os)
{
    vector<composite>::iterator i = elements.begin();
    while(i != elements.end()) {
        os << i->format(); // XXXXXXXXXXXX
        ++i;
    }
    return os;
}

bool segment::is_empty()
{
    return elements.empty();
}

size_t segment::length()
{
    return elements.size();
}

void segment::append(const string& ele_str)
{
    elements.push_back(composite(ele_str, subele_term));
}

string get_seg_id()
{
    return seg_id;
}

string get_value_by_ref_des(const string& ref_des)
{
    typedef string::const_iterator iter;
    int ele_idx, comp_idx;

    if(ref_des.substr(0, seg_id.size()) != seg_id):
        throw Pyx12Errors::EngineError("Invalid ref_des: " + ref_des + ", seg_id: " + seg_id);
    string rest = ref_des.substr(seg_id.length(), ref_des.size()-seg_id.length());
    size_t dash = find(ref_des.begin(), ref_des.end(), '-');
    if(dash == -1) {
        ele_idx = int(rest) -1;
        comp_idx = 0;
    }
    else {
        ele_idx = int(rest.substr(0, dash)) -1;
        comp_idx = int(rest.substr(dash, rest.size()-dash)) -1;
    }
    return elements[ele_idx][comp_idx].get_value();
}

void set_seg_term(const string& seg_term_) {
    seg_term = seg_term_;
}

void set_ele_term(const string& ele_term_) {
    ele_term = ele_term_;
}

void set_subele_term(const string& subele_term_) {
    subele_term = subele_term_;
}

string format() {
    format(seg_term, ele_term, subele_term);
}

string format(const string& seg_term_, const string& ele_term_, const string& subele_term_) {
    string ret;
    vector<composite>::iterator i = elements.begin();
    while(i != elements.end()) {
        ret += i->format(subele_term_);
        ret += ele_term_;
        ++i;
    }
    return ret;
}

vector<string> format_ele_list(vector<string> str_elems, const string& subele_term_) {
    vector<string> ret;
    vector<composite>::iterator i = elements.begin();
    while(i != elements.end()) {
        ret.append(i->format(subele_term_) + ele_term_);
        ++i;
    }
    return ret;
}
