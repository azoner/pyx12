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
private:
    char seg_term, seg_term_orig;
    char ele_term, ele_term_orig;
    char subele_term, subele_term_orig;
    string seg_id;
    vector<string> elements;

public:
    segment(const string& seg_str, const char seg_term, 
        const char ele_term, const char subele_term);
    string& operator[](size_type i) { return elements[i]; };
    const string& operator[](size_type i) const { return elements[i]; };
    string& get_item(size_type i) { return elements[i]; };
    const string& get_item(size_type i) const { return elements[i]; };
    void set_item(size_type i, string val) { elements[i] = val; };
    void append(string val);
    size_t length();
    string get_seg_id();
    string get_value_by_ref_des(const string& ref_des);
    void set_seg_term(char seg_term);
    void set_ele_term(char ele_term);
    void set_subele_term(char subele_term);
    string format();
    vector<string> format_ele_list(vector<string> str_elems, char subele_term);
    bool is_empty();

    ostream& operator<<(ostream&, segment&);
};



segment::segment(const string& src_filename) //, errh)
{
    //errh = errh
    string line;
    string err_str;
    char c, str[256];

    gs_count = 0;
    st_count = 0;
    hl_count = 0;
    seg_count = 0;
    cur_line = 0;
    src_fs.open(src_filename.c_str());
    src_fs.get(str, ISA_LEN);
    line = str;
    string::size_type idx = 0;
    if(line.substr(0,3) != "ISA") {
        err_str = "First line does not begin with 'ISA') " + line.substr(0,3);
        cerr << err_str;
        //raise x12Error, err_str
    }
    if(line.size() != ISA_LEN) {
        err_str = "ISA line is only ";
        err_str += line.length();
        err_str += " characters";
        cerr << err_str;
        //#errh.isa_error('ISA4', err_str)
        //raise x12Error, err_str
    }
    seg_term = line.at(line.size()-1);
    ele_term = line.at(3);
    subele_term = line.at(line.size()-2);
#ifdef DEBUG
    cerr << "seg_term " << seg_term;
    cerr << "ele_term" << ele_term;
    cerr << "subele_term " << subele_term;
    cerr << "\n"; 
#endif
   
    //buffer = line
    //buffer += fd.read(DEFAULT_BUFSIZE)
    src_fs.seekg(0);
}
        
vector<string> segment::next()
{
    vector<string> seg;
    string line;
    string err_str;
    string group_control_number;
    string::size_type pos;
    //char line_tmp [MAX_LINE_LEN];
    /*
     * void get_chunk(istream& in, string& s, char terminator = '\t')
     * {
     *   s.erase(s.begin(), s.end());
     *     s.reserve(20);
     *       string::value_type ch;
     *         while (in.get(ch) && ch != terminator)
     *             s.insert(s.end(), ch);
     *             }
     *             
     */
    //src_fs.get_line(&line_tmp, MAX_LINE_LEN, seg_term);
    //line += line_tmp;
    getline(src_fs, line, seg_term);
    while(true) {
        // Get first segment in buffer
        while(true) {
            if(line[0] == ' ')
                line.erase(0, 1);
            else
                break;
        }
        while(true) {
            if(line[line.length()-1] == ' ')
                line.erase(line.length()-1);
            else
                break;
        }
        while(pos = line.find('\n') != string::npos) 
            line.erase(pos, pos+1);
        while(pos = line.find('\r') != string::npos) 
            line.erase(pos, pos+1);
        if(line != "")
            break;
    }

    if(line[line.size()-1] == ele_term)
    {
        err_str = "Segment contains trailing element terminators";
        cerr << err_str << '\n';
        //errh.seg_error('SEG1', err_str, src_line=cur_line+1 )
    }
    string::size_type epos;
    pos = 0;
    while(pos != line.length()) {
        epos = line.find(ele_term);
        seg.push_back(line.substr(pos, epos));
        pos = epos + 1;
    };
    cur_line += 1;
    return seg;
}

list<string> segment::get_id()
{
    isa_id = None
    gs_id = None
    st_id = None
    ls_id = None
    for loop in loops)
        if(loop[0] == 'ISA') isa_id = loop[1]
        if(loop[0] == 'GS') gs_id = loop[1]
        if(loop[0] == 'ST') st_id = loop[1]
        if(loop[0] == 'LS') ls_id = loop[1]
    return (isa_id, gs_id, st_id, ls_id, seg_count, cur_line)
}

void segment::print_seg(seg)
    sys.stdout.write('%s' % (seg_str(seg, seg_term, ele_term, subele_term, '\n')))

string segment::format_seg(seg))
    return '%s' % (seg_str(seg, seg_term, ele_term, subele_term, '\n'))

list<string> segment::get_term()
    return (seg_term, ele_term, subele_term, '\n')


