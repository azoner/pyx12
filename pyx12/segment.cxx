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

#include <string>
#include <vector>
#include <iostream>
#include <algorithm>
#include <stdlib.h>

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

Pyx12::element::element(const string& ele_str)
{
    value = ele_str;
}

size_t Pyx12::element::length()
{
    return 1;
}

ostream& Pyx12::element::operator<<(ostream& os)
{
    os << value;
    return os;
}

string Pyx12::element::format()
{
    return value;
}

string Pyx12::element::get_value()
{
    return value;
}

void Pyx12::element::set_value(string ele_str)
{
    value = ele_str;
}

bool Pyx12::element::is_composite()
{
    return false;
}

bool Pyx12::element::is_element()
{
    return true;
}

bool Pyx12::element::is_empty()
{
    if(value.length() != 0)
        return true;
    else
        return false;
}


Pyx12::composite::composite(const string& ele_str, const string& subele_term_)
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

bool Pyx12::composite::not_delim(char c)
{
    if(c != subele_term[0])
        return true;
    else
        return false;
}

bool Pyx12::composite::delim(char c)
{
    if(c == subele_term[0])
        return true;
    else
        return false;
}

vector<string> Pyx12::composite::split(const string& ele_str)
{
    typedef string::const_iterator iter;
    vector<string> ret;

    iter i = ele_str.begin();
    iter j;
    while(i != ele_str.end()) {
        //i = find_if(i, ele_str.end(), Pyx12::composite::not_delim);
        while(i != ele_str.end())
            if((*i) != subele_term[0])
                break;
        j = find(i, ele_str.end(), subele_term[0]);
        //j = find_if(i, ele_str.end(), Pyx12::composite::delim);
        if(i != ele_str.end())
            ret.push_back(string(i, j));
        i = j;
    };
    return ret;
}

size_t Pyx12::composite::length()
{
    return elements.size();
}

ostream& Pyx12::composite::operator<<(ostream& os)
{
    vector<element>::iterator i = elements.begin();
    while(i != elements.end()) {
        os << i->format();
        ++i;
    }
    return os;
}

string Pyx12::composite::format()
{
    return format(subele_term);
}

string Pyx12::composite::format(const string& subele_term_)
{
    typedef vector<element>::iterator iter;
    string term;
    string ret;
    term = subele_term_;
    if(!elements.empty())
        ret += elements[0].format();
    iter i = elements.begin() + 1;
    while(i != elements.end()) {
        ret += term;
        ret += i->format();
    }
    return ret;
}

string Pyx12::composite::get_value()
{
    if(elements.size() == 1)
        return elements[0].get_value();
    else
        throw Pyx12::EngineError("value of composite is undefined");
}

void Pyx12::composite::set_subele_term(const string& subele_term_)
{
    subele_term = subele_term_;
}

bool Pyx12::composite::is_composite()
{
    return true;
}

bool Pyx12::composite::is_element()
{
    return false;
}

bool Pyx12::composite::is_empty()
{
    return elements.empty();
}

Pyx12::element& Pyx12::composite::operator[](size_t i) { 
    return elements[i];
}

const Pyx12::element& Pyx12::composite::operator[](size_t i) const { 
    return elements[i]; 
}

///////////////////////////////////////////////////////////////////////////
//  SEGMENT CLASS
///////////////////////////////////////////////////////////////////////////
Pyx12::segment::segment(const string& seg_str, const string& seg_term_,
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
    cerr << "A1" << endl;;
    if(seg_str.empty())
        throw Pyx12::EngineError("seg_str should not be empty");
    cerr << "A2" << endl;;
    if(seg_str.substr(seg_str.length()-1) == seg_term)
        //elems = split(seg_str.substr(seg_str.begin(), seg_str.end()-1));
        elems = split(seg_str.substr(0, seg_str.length()-1));
    else
        elems = split(seg_str);
    cerr << "A3" << endl;;
    seg_id = elems.front();

    iter i = elems.begin();
    while(i != elems.end()) {
        if(seg_id=="ISA")
            elements.push_back(composite((*i), ele_term));
        else
            elements.push_back(composite((*i), subele_term));
        i++;
    }
}

bool Pyx12::segment::not_delim(char c)
{
    if(c != ele_term[0])
        return true;
    else
        return false;
}

bool Pyx12::segment::delim(char c)
{
    if(c == ele_term[0])
        return true;
    else
        return false;
}

vector<string> Pyx12::segment::split(const string& seg_str)
{
    typedef string::const_iterator iter;
    vector<string> ret;

    iter i = seg_str.begin();
    iter j;
    while(i != seg_str.end()) {
        cerr << "B1" << endl;
        i = find_if(i, seg_str.end(), Pyx12::segment::not_delim);
        //j = find_if(i, seg_str.end(), Pyx12::segment::delim);
        while(i != seg_str.end())
            if((*i++) != ele_term[0])
                break;
        j = find(i, seg_str.end(), ele_term[0]);
        if(i != seg_str.end())
            ret.push_back(string(i, j));
        cerr << string(i, j) << endl;
        i = j;
    }
    cerr << "B2" << endl;
    return ret;
}

ostream& Pyx12::segment::operator<<(ostream& os)
{
    vector<composite>::iterator i = elements.begin();
    while(i != elements.end()) {
        os << i->format(); // XXXXXXXXXXXX
        ++i;
    }
    return os;
}

bool Pyx12::segment::is_empty() {
    return elements.empty();
}

size_t Pyx12::segment::length() {
    return elements.size();
}

void Pyx12::segment::append(const string& ele_str) {
    elements.push_back(composite(ele_str, subele_term));
}

string Pyx12::segment::get_seg_id() {
    return seg_id;
}

string Pyx12::segment::get_value_by_ref_des(const string& ref_des) {
    typedef string::const_iterator iter;
    int ele_idx, comp_idx;

    if(ref_des.substr(0, seg_id.size()) != seg_id)
        throw Pyx12::EngineError("Invalid ref_des: " + ref_des + ", seg_id: " + seg_id);
    string rest(ref_des, seg_id.length(), ref_des.size()-seg_id.length());
    string::size_type dash = ref_des.find('-');
    if(dash == string::npos) {
        ele_idx = atoi(rest.c_str()) - 1;
        comp_idx = 0;
    }
    else {
        ele_idx = atoi(rest.substr(0, dash).c_str()) - 1;
        comp_idx = atoi(rest.substr(dash, rest.size()-dash).c_str()) - 1;
    }
    return elements[ele_idx][comp_idx].get_value();
}

void Pyx12::segment::set_seg_term(const string& seg_term_) {
    seg_term = seg_term_;
}

void Pyx12::segment::set_ele_term(const string& ele_term_) {
    ele_term = ele_term_;
}

void Pyx12::segment::set_subele_term(const string& subele_term_) {
    subele_term = subele_term_;
}

string Pyx12::segment::format() {
    return format(seg_term, ele_term, subele_term);
}

string Pyx12::segment::format(const string& seg_term_, const string& ele_term_, const string& subele_term_) {
    string ret;
    vector<composite>::iterator i = elements.begin();
    while(i != elements.end()) {
        ret += i->format(subele_term_);
        ret += ele_term_;
        ++i;
    }
    return ret;
}

vector<string> Pyx12::segment::format_ele_list(vector<string> str_elems, const string& subele_term_) {
    vector<string> ret;
    vector<composite>::iterator i = elements.begin();
    while(i != elements.end()) {
        ret.push_back(i->format(subele_term_));
        ++i;
    }
    return ret;
}

Pyx12::composite& Pyx12::segment::operator[](size_t i) { 
    return elements[i]; 
}

const Pyx12::composite& Pyx12::segment::operator[](size_t i) const { 
    return elements[i]; 
}

Pyx12::composite& Pyx12::segment::get_item(size_t i) { 
    return elements[i]; 
}

const Pyx12::composite& Pyx12::segment::get_item(size_t i) const { 
    return elements[i];
}

void Pyx12::segment::set_item(size_t i, string val) { 
    elements[i] = composite(val, subele_term);
}
