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

/* Interface to an X12 data file.
 * Efficiently handles large files.
 * Tracks end of explicit loops.
 * Tracks segment/line/loop counts.
 */
 
#include <algorithm>
#include <iterator>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>

#include "x12file.hxx"

//logger = logging.getLogger('pyx12.x12file')

using namespace std;

Pyx12::x12file::x12file(const string& src_filename) //, errh)
/** Initialize the file
 *
 * @param src_file absolute path of source file
 * @type src_file string
 * @param errh L{error_handler.err_handler}
 */
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
        //throw x12Error, err_str
    }
    if(line.size() != ISA_LEN) {
        err_str = "ISA line is only ";
        err_str += line.length();
        err_str += " characters";
        cerr << err_str;
        //#errh.isa_error('ISA4', err_str)
        //throw x12Error, err_str
    }
    seg_term = line.at(line.size()-1); // .data()
    ele_term = line.at(3);
    subele_term = line.at(line.size()-2);
#ifdef DEBUG
    cerr << "seg_term " << seg_term;
    cerr << "ele_term" << ele_term;
    cerr << "subele_term " << subele_term;
    cerr << endl; 
#endif
   
    //buffer = line
    //buffer += fd.read(DEFAULT_BUFSIZE)
    src_fs.seekg(0);
}
        
string Pyx12::x12file::read_seg() {
    string ret("");
    char ch;
    while(!src_fs.eof()) {
        src_fs >> ch;
        if(ch == seg_term)
            return ret;
        if(ch != '\n' && ch != '\r')
            ret.push_back(ch);
    }
}

vector<string> Pyx12::x12file::next() {
    vector<string> seg;
    string line;
    string err_str;
    string group_control_number;
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
    //getline(src_fs, line, seg_term);
    line = x12file::read_seg();
    if(line[line.size()-1] == ele_term)
    {
        err_str = "Segment contains trailing element terminators";
        cerr << err_str << '\n';
        //errh.seg_error('SEG1', err_str, src_line=cur_line+1 )
    }
    Pyx12::segment seg_data(line, seg_term, ele_term, subele_term);
    if(seg_data.get_seg_id()=="ISA") {
        if(seg_data.length() != 16)
            throw x12Error("The ISA segement must have 16 elements");
        //seg[-1] = subele_term
        string interchange_control_number = seg_data.get_value_by_ref_des("ISA13");
        if(find(isa_ids.begin(), isa_ids.end(), interchange_control_number) != isa_ids.end()) {
            err_str = "ISA Interchange Control Number '";
            err_str += interchange_control_number;
            err_str += "' is not unique within file";
            //errh.isa_error("025", err_str)
        }
        loops.push_back(make_pair(string("ISA"), interchange_control_number));
        isa_ids.push_back(interchange_control_number);
        gs_count = 0;
        gs_ids.erase(gs_ids.begin(), gs_ids.end());
        isa_usage = seg_data.get_value_by_ref_des("ISA15");
    }
    else if(seg_data.get_seg_id()=="IEA") {
        if(loops.rbegin()->first != "ISA" 
                || loops.rbegin()->second != seg_data.get_value_by_ref_des("IEA02")) {
            err_str = "IEA id=";
            err_str += seg_data.get_value_by_ref_des("IEA02");
            err_str +=" does not match ISA id=";
            err_str += loops.rbegin()->second;
            //errh.isa_error('001', err_str)
        }
        if(atoi(seg_data.get_value_by_ref_des("IEA02").c_str()) != gs_count) {
            err_str = "IEA count for IEA02=";
            err_str += seg_data.get_value_by_ref_des("IEA02");
            err_str +=" is wrong";
            //errh.isa_error("021", err_str)
        }
        loops.pop_back();
    }
    else if(seg_data.get_seg_id()=="GS") {
        string group_control_number = seg_data.get_value_by_ref_des("GS06");
        if(find(gs_ids.begin(), gs_ids.end(), group_control_number) != gs_ids.end()) {
            err_str = "GS Interchange Control Number ";
            err_str += group_control_number;
            err_str += " not unique within file";
            //errh.gs_error('6', err_str)
        }
        gs_count++;
        gs_ids.push_back(group_control_number);
        loops.push_back(make_pair(string("GS"), group_control_number));
        st_count = 0;
        st_ids.erase(st_ids.begin(), st_ids.end());
    }
    else if(seg_data.get_seg_id()=="GE") {
        string ge_id = seg_data.get_value_by_ref_des("GE02");
        if(loops.rbegin()->first != "GS" 
                || loops.rbegin()->second != ge_id) {
            err_str = "GE id=";
            err_str += ge_id;
            err_str += " does not match GS id=";
            err_str += loops.rbegin()->second;
            //errh.gs_error("4", err_str)
        }
        if(atoi(seg_data.get_value_by_ref_des("GE01").c_str()) != st_count) {
            err_str = "GE count of ";
            err_str += seg_data.get_value_by_ref_des("GE01");
            err_str += " for GE02=" + ge_id;
            err_str += " is wrong. I count ";
            err_str += st_count; // XXX
            //errh.gs_error("5", err_str)
        }
        loops.pop_back();
    }
    else if(seg_data.get_seg_id()=="ST") {
        string transaction_control_number = seg_data.get_value_by_ref_des("ST02");
        if(find(st_ids.begin(), st_ids.end(), transaction_control_number) != st_ids.end()) {
            err_str = "ST Interchange Control Number " + transaction_control_number + " not unique within file";
            //errh.st_error('23', err_str)
        }
        st_count++;
        st_ids.push_back(transaction_control_number);
        loops.push_back(make_pair(string("ST"), transaction_control_number));
        seg_count = 1; 
        hl_count = 0;
    }
    else if(seg_data.get_seg_id()=="SE") {
        string se_trn_control_num = seg_data.get_value_by_ref_des("SE02");
        if(loops.rbegin()->first != "ST" 
                || loops.rbegin()->second != se_trn_control_num) {
            err_str = "SE id=" + se_trn_control_num;
            err_str += " does not match ST id=" + loops.rbegin()->second;
            //errh.st_error("3", err_str)
        }
        if(atoi(seg_data.get_value_by_ref_des("SE01").c_str()) != seg_count + 1) {
            err_str = "SE count of " + seg_data.get_value_by_ref_des("SE01");
            err_str += " for SE02=" + se_trn_control_num + " is wrong. I count "; // + (seg_count + 1); // XX
            //errh.st_error('4', err_str)
        }
        loops.pop_back();
    }
    else if(seg_data.get_seg_id()=="LS") 
        loops.push_back(make_pair(string("LS"), seg_data.get_value_by_ref_des("LS06")));
    else if(seg_data.get_seg_id()=="LE") 
        loops.pop_back();
    else if(seg_data.get_seg_id()=="HL") {
        seg_count++;
        hl_count++;
        if(hl_count != atoi(seg_data.get_value_by_ref_des("HL01").c_str())) {
            //err_str = "My HL count %i does not match your HL count %s' \
            //    % (hl_count, seg[1])
            //errh.seg_error("HL1", err_str)
        }
        if(seg_data.get_value_by_ref_des("HL02") != "") {
            int  hl_parent = atoi(seg_data.get_value_by_ref_des("HL02").c_str());
            while(!hl_stack.empty() && hl_stack.top() != hl_parent)
                hl_stack.pop();
        }
        hl_stack.push(hl_count);
    }
    else
        seg_count++;
    
    //catch IndexError {
    //    err_str = "Expected element not found " + seg.format();
    //    throw x12Error(err_str);
    //}
    cur_line++;
    return seg;
}

/*    
void Pyx12::x12file::cleanup()
// At EOF, check for missing end segments
{
    if(loops)
        for (seg, id) in loops.reverse()) 
            if(loops[-1][0] == 'ST')
                err_str = 'ST id=%s was not closed with a SE' % (id)
                errh.st_error('3', err_str)
                errh.close_st_loop(None, None, self)
            elif(loops[-1][0] == 'GS')
                err_str = 'GS id=%s was not closed with a GE' % (id)
                errh.gs_error('3', err_str)
                errh.close_gs_loop(None, None, self)
            elif(loops[-1][0] == 'ISA')
                err_str = 'ISA id=%s was not closed with a IEA' % (id)
                errh.isa_error('023', err_str)
                errh.close_isa_loop(None, None, self)
} 

void Pyx12::x12file::print_seg(seg)
    sys.stdout.write('%s' % (seg_str(seg, seg_term, ele_term, subele_term, '\n')))

string Pyx12::x12file::format_seg(seg))
    return '%s' % (seg_str(seg, seg_term, ele_term, subele_term, '\n'))

list<string> Pyx12::x12file::get_term()
    return (seg_term, ele_term, subele_term, '\n')
*/

string Pyx12::x12file::get_isa_id() const {
    x12file::get_id("ISA");
}

string Pyx12::x12file::get_gs_id() const {
    x12file::get_id("GS");
}

string Pyx12::x12file::get_st_id() const {
    x12file::get_id("ST");
}

string Pyx12::x12file::get_ls_id() const {
    x12file::get_id("LS");
}

string Pyx12::x12file::get_id(string id) const {
    for(list<pair<string,string> >::const_itererator iter = loops.begin();
         iter != loops.end(); ++iter) {
        if(iter->first == id)
            return iter->second;
    }
    return "";
}

list<string> Pyx12::x12file::get_term() const {
    list<string> ret;
    ret.push_back(seg_term);
    ret.push_back(ele_term);
    ret.push_back(subele_term);
    ret.push_back("\n");
    return ret;
}

void Pyx12::x12file::isa_error(const string err_cde, const string err_str) {
    list<string, string, string> tmp;
    tmp.push_back("isa");
    tmp.push_back(err_cde);
    tmp.push_back(err_str);
    err_list.push_back(tmp)
}

void Pyx12::x12file::gs_error(const string err_cde, const string err_str) {
    list<string, string, string> tmp;
    tmp.push_back("gs");
    tmp.push_back(err_cde);
    tmp.push_back(err_str);
    err_list.push_back(tmp)
}

void Pyx12::x12file::st_error(const string err_cde, const string err_str) {
    list<string, string, string> tmp;
    tmp.push_back("st");
    tmp.push_back(err_cde);
    tmp.push_back(err_str);
    err_list.push_back(tmp)
}

void Pyx12::x12file::seg_error(const string err_cde, 
        const string err_str, const string err_val, const int src_line) {
    list<string, string, string, string, int> tmp;
    tmp.push_back("seg");
    tmp.push_back(err_cde);
    tmp.push_back(err_str);
    tmp.push_back(err_val);
    tmp.push_back(src_line);
    err_list.push_back(tmp)
}


/** Get a string representation of the segment
 *
 * @param seg_data Pyx12::segment
 * @type src_file string
 * @param errh L{error_handler.err_handler}
 */
/*
string Pyx12::x12file::seg_str(Pyx12::segment seg_data, string seg_term, string ele_term,
    string sub_ele_term, string eol="\n") const {
}
*/

