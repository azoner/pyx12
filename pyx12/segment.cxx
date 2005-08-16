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

#include <string>
#include <vector>
#include <iostream>
#include <algorithm>
#include <stdlib.h>

#include "segment.hxx"
#include "errors.hxx"

/** Implements an interface to a x12 segment.
 *
 * A segment is comprised of a segment identifier and a sequence of elements.
 * An element can be a simple element or a composite.  A simple element is
 * treated as a composite element with one sub-element.
 *
 * All indexing is zero based.
*/ 
using namespace std;

///////////////////////////////////////////////////////////////////////////
//  ELEMENT CLASS
//
//  Encapsulates an X12 Element.  String values
///////////////////////////////////////////////////////////////////////////
Pyx12::Element::Element() {}

Pyx12::Element::Element(const string& ele_str)
{
    value = ele_str;
}

size_t
Pyx12::Element::length() const
{
    return 1;
}

string
Pyx12::Element::format()
{
    return value;
}

string
Pyx12::Element::getValue()
{
    return value;
}

void
Pyx12::Element::setValue(const string& ele_str)
{
    value = ele_str;
}

bool
Pyx12::Element::isComposite()
{
    return false;
}

bool
Pyx12::Element::isElement()
{
    return true;
}

bool
Pyx12::Element::isEmpty()
{
    if(value.length() != 0)
        return true;
    else
        return false;
}



///////////////////////////////////////////////////////////////////////////
//  COMPOSITE CLASS
//
//  Encapsulates an X12 Composite. Contains X12 Elements.
///////////////////////////////////////////////////////////////////////////
Pyx12::Composite::Composite() {}

Pyx12::Composite::Composite(const string& ele_str, const char subele_term_)
{
    typedef vector<string>::const_iterator iter;
    subele_term = subele_term_;
    subele_term_orig = subele_term_;
    vector<string> elems = split(ele_str);
    iter i = elems.begin();
    while(i != elems.end())
    {
        elements.push_back(Element((*i)));
        ++i;
    }
}

/*
bool 
Pyx12::Composite::not_delim(char c)
{
    if(c != subele_term[0])
        return true;
    else
        return false;
}

bool 
Pyx12::Composite::delim(char c)
{
    if(c == subele_term[0])
        return true;
    else
        return false;
}
*/

vector<string>
Pyx12::Composite::split(const string& ele_str)
{
    typedef string::const_iterator iter;
    vector<string> ret;

    iter i = ele_str.begin();
    while(i != ele_str.end())
    {
        i = find_if(i, ele_str.end(), Pyx12::IsNotDelim(subele_term));
        iter j = find_if(i, ele_str.end(), Pyx12::IsDelim(subele_term));
        if(i != ele_str.end())
            ret.push_back(string(i, j));
        i = j;
    };
    return ret;
}

Pyx12::CompElements_sz
Pyx12::Composite::length() const
{
    return elements.size();
}

string
Pyx12::Composite::format()
{
    return format(subele_term);
}

string
Pyx12::Composite::format(const char subele_term_)
{
    typedef Pyx12::CompElements::iterator iter;
    string ret;
    iter i = elements.begin();
    while(i != elements.end()) {
        ret += i->format();
        ret += subele_term_;
        ++i;
    }
    while(ret.length() > 0 && 
            ret.substr(ret.length()-1) == string(1, subele_term_))
        ret.erase(ret.length()-1);
        //ret = ret.substr(0, ret.length()-1);
    return ret;
}

Pyx12::Element
Pyx12::Composite::getElement(int comp_idx)
{
    if(comp_idx == -1)
        return elements[0];
    else
    {
        if(elements.end() <= elements.begin() + comp_idx)
            return Pyx12::Element("");
        return elements[comp_idx];
    }
}

string
Pyx12::Composite::getValue()
{
    if(elements.size() == 1)
        return elements[0].getValue();
    else
        throw Pyx12::EngineError("value of Composite is undefined");
}

/** Set the value of an element or subelement identified by the
 *      Reference Designator.
 *
 *   @param comp_des Element position
 *   @param val New value
 */
/*
void
Pyx12::Composite::setValue(const string& comp_des, const string& val)
{
    Pyx12::CompElements_sz comp_idx = atoi(comp_des);
    while(elements.size() <= comp_idx) 
        elements.push_back(Pyx12::Element(""));
    elements[comp_idx] = Pyx12::Element(val);
}
*/

/** Set the value of an element or subelement identified by the position.
 *
 *   @param comp_idx Element position
 *   @param val New value
 */
void
Pyx12::Composite::setValue(const Pyx12::CompElements_sz comp_idx, const string& val)
{
    while(elements.size() <= comp_idx)
        elements.push_back(Pyx12::Element(""));
    elements[comp_idx] = Pyx12::Element(val);
}

void
Pyx12::Composite::setSubeleTerm(const char subele_term_)
    
{
    subele_term = subele_term_;
}

bool
Pyx12::Composite::isComposite()
{
    return true;
}

bool
Pyx12::Composite::isElement()
{
    return false;
}

bool
Pyx12::Composite::isEmpty()
{
    return elements.empty();
}

Pyx12::Element&
Pyx12::Composite::operator[](Pyx12::CompElements_sz i)
{
    return elements[i];
}

const Pyx12::Element&
Pyx12::Composite::operator[](Pyx12::CompElements_sz i) const
{
    return elements[i]; 
}

///////////////////////////////////////////////////////////////////////////
//  SEGMENT CLASS
//
//  Encapsulates an X12 segment.  Contains Composites.
///////////////////////////////////////////////////////////////////////////

Pyx12::Segment::Segment() {}

Pyx12::Segment::Segment(const string& seg_str, const char seg_term_ = '~',
        const char ele_term_ = '*', const char subele_term_ = ':')
{
    typedef vector<string>::const_iterator iter;
    vector<string> elems;
    seg_term = seg_term_;
    seg_term_orig = seg_term_;
    ele_term = ele_term_;
    ele_term_orig = ele_term_;
    subele_term = subele_term_;
    subele_term_orig = subele_term_;
    //seg_id = '';
    if(seg_str.empty())
        throw Pyx12::EngineError("seg_str should not be empty");
    if(seg_str.substr(seg_str.length()-1) == string(1, seg_term))
        //elems = split(seg_str.substr(seg_str.begin(), seg_str.end()-1));
        elems = split(seg_str.substr(0, seg_str.length()-1));
    else
        elems = split(seg_str);
    seg_id = elems.front();

    iter i = elems.begin() + 1;
    while(i != elems.end()){
        if(seg_id=="ISA")
            // Special handling for ISA segment
            // guarantee subele_term will not be matched
            elements.push_back(Composite((*i), ele_term));
        else
            elements.push_back(Composite((*i), subele_term));
        i++;
    }
}

/*
bool
Pyx12::Segment::not_delim(char c)
{
    if(c != ele_term[0])
        return true;
    else
        return false;
}

bool
Pyx12::Segment::delim(char c)
{
    if(c == ele_term[0])
        return true;
    else
        return false;
}
*/

vector<string>
Pyx12::Segment::split(const string& seg_str)
{
    typedef string::const_iterator iter;
    vector<string> ret;

    iter i = seg_str.begin();
    while(i != seg_str.end())
    {
        i = find_if(i, seg_str.end(), Pyx12::IsNotDelim(ele_term));
        iter j = find_if(i, seg_str.end(), Pyx12::IsDelim(ele_term));
        if(i != seg_str.end())
            ret.push_back(string(i, j));
        i = j;
    };
    return ret;
}

/** Is the segment empty?
 */
bool
Pyx12::Segment::isEmpty()
{
    return elements.empty();
}

/** Is the segment ID look valid?
 */
bool
Pyx12::Segment::isSegIdValid()
{
    if(seg_id == "" || seg_id.length() < 2 || seg_id.length() > 3)
        return false;
    else
        return true;
}

/** How many elements are in this segment?
 */
Pyx12::SegComposites_sz
Pyx12::Segment::length() const
{
    return elements.size();
}

/** Append a new composite to the segment
 */
void
Pyx12::Segment::append(const string& ele_str)
{
    elements.push_back(Composite(ele_str, subele_term));
}

/** Get the segment ID
 */
string
Pyx12::Segment::getSegId()
{
    return seg_id;
}

/** Get the value of the composite by Reference Designator
 */
string
Pyx12::Segment::getValue(const string& ref_des)
{
    Pyx12::Composite comp_data = getComposite(ref_des);
    return comp_data.format();
 /*
    typedef string::const_iterator iter;
    Pyx12::SegComposites_sz ele_idx, comp_idx;

    if(ref_des.substr(0, seg_id.size()) != seg_id)
        throw Pyx12::EngineError("Invalid ref_des: " + ref_des + ", seg_id: " + seg_id);
    string rest(ref_des, seg_id.length(), ref_des.size()-seg_id.length());
    string::size_type dash = ref_des.find('-');
    if(dash == string::npos)
    {
        ele_idx = atoi(rest.c_str()) - 1;
        comp_idx = 0;
    }
    else
    {
        ele_idx = atoi(rest.substr(0, dash).c_str()) - 1;
        comp_idx = atoi(rest.substr(dash, rest.size()-dash).c_str()) - 1;
    }
    return elements[ele_idx][comp_idx].getValue();
*/
}

/** Get the segment delimiter
 */
void
Pyx12::Segment::setSegTerm(const char seg_term_)
{
    seg_term = seg_term_;
}

/** Get the element delimiter
 */
void
Pyx12::Segment::setEleTerm(const char ele_term_)
{
    ele_term = ele_term_;
}

/** Get the sub-element delimiter
 */
void
Pyx12::Segment::setSubeleTerm(const char subele_term_)
{
    subele_term = subele_term_;
}

string
Pyx12::Segment::format()
{
    return format(this->seg_term, this->ele_term, this->subele_term);
}

string
Pyx12::Segment::format(const char seg_term_, const char ele_term_, const char subele_term_)
{
    string ret = seg_id + ele_term_;
    //Pyx12::SegComposites::iterator i = elements.begin();
    for(Pyx12::SegComposites::iterator i = elements.begin();
            i != elements.end(); ++i) {
        ret += i->format(subele_term_);
        ret += ele_term_;
        //cerr << "ret: " << ret << endl;
    }
    //Strip trailing element delimiter
    while(ret.length() > 0 && 
            ret.substr(ret.length()-1) == string(1, ele_term_))
        ret.erase(ret.length()-1);
    ret += seg_term_; // Add segment delimiter
    //cerr << ret << endl;
    return ret;
}

/** Modifies the parameter str_elems, appending formatted composites.
 * Strips trailing empty composites
 *
 * @param str_elems vector to modify
 */
void
Pyx12::Segment::format_ele_list(vector<string> str_elems)
{
    format_ele_list(str_elems, subele_term);
}

/** Modifies the parameter str_elems, appending formatted composites.
 * Strips trailing empty composites
 *
 * @param str_elems vector to modify
 * @param subele_term_ Sub-element terminator to use
 */
void
Pyx12::Segment::format_ele_list(vector<string> str_elems, const char subele_term_)
{
   // vector<string> ret;
    Pyx12::SegComposites::iterator last_it;
    Pyx12::SegComposites::iterator i = elements.begin();
    // Find last non-empty composite
    while(i != elements.end()) {
        if(!i->isEmpty())
            last_it = i;
        ++i;
    }
    i = elements.begin();
    while(i != last_it) {  //elements.end()) {
        str_elems.push_back(i->format(subele_term_));
        ++i;
    }
    //return ret;
}

Pyx12::Composite&
Pyx12::Segment::operator[](Pyx12::SegComposites_sz i)
{
    return elements[i]; 
}

const Pyx12::Composite&
Pyx12::Segment::operator[](Pyx12::SegComposites_sz i) const
{
    return elements[i]; 
}

/** Set the value of an element or subelement identified by the
 *      Reference Designator.
 *
 *   @param ref_des X12 Reference Designator
 *   @param val New value
 */
void
Pyx12::Segment::setValue(const string& ref_des, const string& val)
{
    //pair<Pyx12::SegComposites_sz, Pyx12::CompElements_sz> idx = parseRefDes(ref_des);
    //Pyx12::SegComposites_sz ele_idx = idx.first;
    //Pyx12::CompElements_sz comp_idx = idx.second;
    pair<int, int> idx = parseRefDes(ref_des);
    int ele_idx = idx.first;
    int comp_idx = idx.second;
    while(elements.end() <= elements.begin() + ele_idx) 
        elements.push_back(Pyx12::Composite("", subele_term));
    if(comp_idx == -1) {
        elements[ele_idx] = Pyx12::Composite(val, subele_term);
    }
    else 
        elements[ele_idx].setValue(comp_idx, val);
}

Pyx12::Composite
Pyx12::Segment::getComposite(const string& ref_des)
{
    pair<int, int> idx = parseRefDes(ref_des);
    int ele_idx = idx.first;
    //pair<Pyx12::SegComposites_sz, Pyx12::CompElements_sz> idx = parseRefDes(ref_des);
    //Pyx12::SegComposites_sz ele_idx = idx.first;
    if(elements.end() <= elements.begin() + ele_idx)
        //throw Pyx12::EngineError("Invalid RefDes" + ref_des);
        return Pyx12::Composite("", subele_term);
    return elements[ele_idx];
}

/*
const Pyx12::Composite&
Pyx12::Segment::getComposite(const string& ref_des) const
{
    pair<Pyx12::SegComposites_sz, Pyx12::CompElements_sz> idx = parseRefDes(ref_des);
    Pyx12::SegComposites_sz ele_idx = idx.first;
    if(ele_idx >= elements.size())
        throw Pyx12::EngineError("Invalid RefDes" + ref_des);
    return elements[ele_idx];
}
*/

Pyx12::Element
Pyx12::Segment::getElement(const string& ref_des)
{
    //pair<Pyx12::SegComposites_sz, Pyx12::CompElements_sz> idx = parseRefDes(ref_des);
    //Pyx12::SegComposites_sz ele_idx = idx.first;
    //Pyx12::CompElements_sz comp_idx = idx.second;
    pair<int, int> idx = parseRefDes(ref_des);
    int ele_idx = idx.first;
    int comp_idx = idx.second;
    if(elements.end() <= elements.begin() + ele_idx)
        return Pyx12::Element("");
        //throw Pyx12::EngineError("Invalid RefDes" + ref_des);
    return elements[ele_idx].getElement(comp_idx);
    /*
    if(comp_idx == -1)
        return elements[ele_idx][0];
    else
    {
        if(elements[ele_idx].end() <= elements[ele_idx].begin() + comp_idx)
            return Pyx12::Element("");
            //throw Pyx12::EngineError("Invalid RefDes" + ref_des);
        return elements[ele_idx][comp_idx];
    }
    */
}

/*
const Pyx12::Element&
Pyx12::Segment::getElement(const string& ref_des) const
{
    pair<Pyx12::SegComposites_sz, Pyx12::CompElements_sz> idx = parseRefDes(ref_des);
    Pyx12::SegComposites_sz ele_idx = idx.first;
    Pyx12::CompElements_sz comp_idx = idx.second;
    if(ele_idx >= length())
        throw Pyx12::EngineError("Invalid RefDes" + ref_des);
    if(comp_idx == 0)
        return elements[ele_idx][0];
    else
    {
        if(comp_idx >= elements[ele_idx].length())
            throw Pyx12::EngineError("Invalid RefDes" + ref_des);
        return elements[ele_idx][comp_idx];
    }
}
*/


/** Get the element and sub-element indexes.
 *
 * @param ref_des X12 Reference Designator
 * @exception EngineError If the given ref_des does not match the segment ID
 *   or if the indexes are not valid integers
 * @return pair<Pyx12::SegComposites_sz, Pyx12::CompElements_sz>
 *
 * Format of ref_des: 
 *   - a simple element: TST02
 *   - a composite: TST03 where TST03 is a composite
 *   - a sub-element: TST03-2
 *   - or any of the above with the segment ID omitted (02, 03, 03-1)
 */
/*
pair<Pyx12::SegComposites_sz, Pyx12::CompElements_sz>
Pyx12::Segment::parseRefDes(const std::string& ref_des)
{
    typedef string::const_iterator iter;
    Pyx12::SegComposites_sz ele_idx;
    Pyx12::CompElements_sz comp_idx;
    if(ref_des=="")
        throw Pyx12::EngineError("Blank Reference Designator");
    //if(ref_des.substr(0, seg_id.size()) != seg_id)
    //    throw Pyx12::EngineError("Invalid ref_des: " + ref_des + ", seg_id: " + seg_id);
    string rest;
    if(isalpha(ref_des[0])) {
        if(ref_des.substr(0, seg_id.length()) != seg_id)
            throw Pyx12::EngineError("Invalid Reference Designator: " 
                    + ref_des + ", seg_id: " + seg_id);
        rest = ref_des.substr(seg_id.length(), ref_des.size()-seg_id.length());
    }
    else {
        rest = ref_des;
    }
    string::size_type dash = ref_des.find('-');
    if(dash == string::npos) {
        ele_idx = atoi(rest.c_str()) - 1;
        comp_idx = 0;
    }
    else {
        ele_idx = atoi(rest.substr(0, dash).c_str()) - 1;
        comp_idx = atoi(rest.substr(dash, rest.size()-dash).c_str()) - 1;
    }
    //cerr << ref_des << '\t' << ele_idx << '\t' << comp_idx << '\n';
    return make_pair(ele_idx, comp_idx);
}
*/

/** Get the element and sub-element indexes.
 *
 * @param ref_des X12 Reference Designator
 * @exception EngineError If the given ref_des does not match the segment ID
 *   or if the indexes are not valid integers
 * @return pair<int, int>
 *
 * Format of ref_des: 
 *   - a simple element: TST02
 *   - a composite: TST03 where TST03 is a composite
 *   - a sub-element: TST03-2
 *   - or any of the above with the segment ID omitted (02, 03, 03-1)
 */
pair<int, int>
Pyx12::Segment::parseRefDes(const std::string& ref_des)
{
    typedef string::const_iterator iter;
    if(ref_des=="")
        throw Pyx12::EngineError("Blank Reference Designator");
    //if(ref_des.substr(0, seg_id.size()) != seg_id)
    //    throw Pyx12::EngineError("Invalid ref_des: " + ref_des + ", seg_id: " + seg_id);
    string rest;
    if(isalpha(ref_des[0])) {
        if(ref_des.substr(0, seg_id.length()) != seg_id)
            throw Pyx12::EngineError("Invalid Reference Designator: " 
                    + ref_des + ", seg_id: " + seg_id);
        rest = ref_des.substr(seg_id.length(), ref_des.size()-seg_id.length());
    }
    else {
        rest = ref_des;
    }
    int ele_idx, comp_idx;
    string::size_type dash = ref_des.find('-');
    if(dash == string::npos) {
        ele_idx = atoi(rest.c_str()) - 1;
        comp_idx = -1;
    }
    else {
        ele_idx = atoi(rest.substr(0, dash).c_str()) - 1;
        comp_idx = atoi(rest.substr(dash, rest.size()-dash).c_str()) - 1;
    }
    //cerr << ref_des << '\t' << ele_idx << '\t' << comp_idx << '\n';
    return make_pair(ele_idx, comp_idx);
}

ostream &
Pyx12::operator << (ostream & out, Pyx12::Element & e)
{
    out << e.value;
    return out;
}

ostream &
Pyx12::operator << (ostream & out, Pyx12::Composite & c)
{
    Pyx12::CompElements::iterator i = c.elements.begin();
    while(i != c.elements.end()) {
        out << i->format();
        ++i;
    }
    return out;
}

ostream &
Pyx12::operator << (ostream & out, Pyx12::Segment & seg)
{
    out << seg.format();
    //SegComposites::iterator i = seg.elements.begin();
    //while(i != seg.elements.end())
    //{
    //    out << i->format(); // XXXXXXXXXXXX
    //    ++i;
    //}
    return out;
}

