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

/* Interface to an X12 data file.
 * Efficiently handles large files.
 * Tracks end of explicit loops.
 * Tracks segment/line/loop counts.
 */
 
#include <iterator>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>

#include "x12file.hxx"

//logger = logging.getLogger('pyx12.x12file')

using namespace std;

x12file::x12file(const string& src_filename) //, errh)
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
    cerr << endl; 
#endif
   
    //buffer = line
    //buffer += fd.read(DEFAULT_BUFSIZE)
    src_fs.seekg(0);
}
        
string x12file::read_seg() {
    string ret = "";
    char ch;
    while(!src_fs.eof()) {
        src_fs >> ch;
        if(ch == seg_term)
            return ret;
        if(ch != '\n' && ch != '\r')
            ret.push_back(ch);
    }

vector<string> x12file::next()
{
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
    pyx12::segment seg_data(line);
    switch(seg_data.get_seg_id()) {
        case "ISA":
            if(seg_data.length() != 16)
                raise x12Error, "The ISA segement must have 16 elements";
            //seg[-1] = subele_term
            interchange_control_number = seg_data.get_value_by_ref_des("ISA13");
            if(interchange_control_number in isa_ids)
                err_str = "ISA Interchange Control Number '";
                err_str += interchange_control_number;
                err_str += "' is not unique within file";
                //errh.isa_error("025", err_str)
            loops.push_back(make_pair("ISA", interchange_control_number))
            isa_ids.push_back(interchange_control_number)
            gs_count = 0;
            gs_ids.erase(gs_ids.begin(), gs_ids.end());
            isa_usage = seg_data.get_value_by_ref_des("ISA15");
        case "IEA":
            if(loops.rbegin()->first != "ISA" 
                    || loops.rbegin()->second != seg_data.get_value_by_ref_des("IEA02"))
                err_str = "IEA id=";
                err_str += seg_data.get_value_by_ref_des("IEA02");
                err_str +=" does not match ISA id="l
                err_str += loops.rbegin()->second;
                //errh.isa_error('001', err_str)
            if(atoi(seg[1]) != gs_count)
                err_str = 'IEA count for IEA02=%s is wrong' % (seg[2])
                errh.isa_error('021', err_str)
            loops.erase(loops.rbegin());
        case "GS":
            group_control_number = seg[6]
            if(group_control_number in gs_ids)
                err_str = 'GS Interchange Control Number %s not unique within file' \
                    % (group_control_number)
                errh.gs_error('6', err_str)
            gs_count++;
            gs_ids.push_back(group_control_number)
            loops.push_back(make_pair("GS", group_control_number))
            st_count = 0;
            st_ids.erase(st_ids.begin(), st_ids.end());
        case "GE":
            if(loops[-1][0] != 'GS' || loops[-1][1] != seg[2])
                err_str = 'GE id=%s does not match GS id=%s' % (seg[2], loops[-1][1])
                errh.gs_error('4', err_str)
            if(int(seg[1]) != st_count)
                err_str = 'GE count of %s for GE02=%s is wrong. I count %i' \
                    % (seg[1], seg[2], st_count)
                errh.gs_error('5', err_str)
            loops.erase(loops.rbegin());
        case "ST":
            transaction_control_number = seg[2]
            if(transaction_control_number in st_ids)
                err_str = 'ST Interchange Control Number %s not unique within file' \
                    % (transaction_control_number)
                errh.st_error('23', err_str)
            st_count++;
            st_ids.push_back(transaction_control_number)
            loops.push_back(make_pair("ST", transaction_control_number));
            seg_count = 1 
            hl_count = 0
        case "SE":
            se_trn_control_num = seg[2]
            if(loops[-1][0] != 'ST' || loops[-1][1] != se_trn_control_num)
                err_str = 'SE id=%s does not match ST id=%s' % (se_trn_control_num, loops[-1][1])
                errh.st_error('3', err_str)
            if(int(seg[1]) != seg_count + 1)
                err_str = 'SE count of %s for SE02=%s is wrong. I count %i' \
                    % (seg[1], se_trn_control_num, seg_count + 1)
                errh.st_error('4', err_str)
            loops.erase(loops.rbegin());
        case "LS":
            loops.push_back(make_pair("LS", seg_data.get_value_by_ref_des("LS06")));
        case "LE":
            loops.erase(loops.rbegin());
        case "HL":
            seg_count++;
            hl_count++;
            if(hl_count != int(seg[1]))
                err_str = 'My HL count %i does not match your HL count %s' \
                    % (hl_count, seg[1])
                errh.seg_error('HL1', err_str)
            if(seg[2] != '')
                parent = int(seg[2])
                if(parent not in hl_stack)
                    hl_stack.push_back(parent)
                else:
                    if(hl_stack)
                        while(hl_stack[-1] != parent)
                            hl_stack.erase(hl_stack.rbegin());
        default:
            seg_count++;
    }
    catch IndexError {
        err_str = "Expected element not found') %s" % seg
        raise x12Error, err_str
    }
    cur_line++;
    return seg;
}

/*    
void x12file::cleanup()
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

void x12file::print_seg(seg)
    sys.stdout.write('%s' % (seg_str(seg, seg_term, ele_term, subele_term, '\n')))

string x12file::format_seg(seg))
    return '%s' % (seg_str(seg, seg_term, ele_term, subele_term, '\n'))

list<string> x12file::get_term()
    return (seg_term, ele_term, subele_term, '\n')
*/

string x12file::get_isa_id() const {
    x12file::get_id("ISA");
}

string x12file::get_gs_id() const {
    x12file::get_id("GS");
}

string x12file::get_st_id() const {
    x12file::get_id("ST");
}

string x12file::get_ls_id() const {
    x12file::get_id("LS");
}

string x12file::get_id(string id) const {
    for(list<pair<string,string>>::const_itererator iter = loops.begin();
         iter != loops.end(); ++iter) {
        if(iter->first == id)
            return iter->second;
    }
    return "";
}

list<string> x12file::get_term() const {
    ret = list<string>;
    ret.push_back(seg_term);
    ret.push_back(ele_term);
    ret.push_back(subele_term);
    ret.push_back("\n");
    return ret;
}

/** Get a string representation of the segment
 *
 * @param seg_data pyx12::segment
 * @type src_file string
 * @param errh L{error_handler.err_handler}
 */
string x12file::seg_str(pyx12::segment seg_data, string seg_term, string ele_term,
    string sub_ele_term, string eol="\n") const {
}


