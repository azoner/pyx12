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
#include <fstream>

#include "x12file.hxx"

//logger = logging.getLogger('pyx12.x12file')

using namespace std;

x12file::x12file(const string& src_filename) //, errh)
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
        
vector<string> x12file::next()
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

    // split composite
    /*
    try {
        for i in xrange(len(seg)))
            if(seg[i].find(subele_term) != -1)
                seg[i] = seg[i].split(subele_term) # Split composite
        if(seg[0] == 'ISA') 
        {
            if(len(seg) != 17)
                raise x12Error, 'The ISA segement must have 16 elements (%s)' % (seg)
            seg[-1] = subele_term
            interchange_control_number = seg[13]
            if(interchange_control_number in isa_ids)
                err_str = 'ISA Interchange Control Number %s not unique within file' \
                    % (interchange_control_number)
                errh.isa_error('025', err_str)
            loops.append(('ISA', interchange_control_number))
            isa_ids.append(interchange_control_number)
            gs_count = 0
            gs_ids = []
            isa_usage = seg[15];
        }
        else if(seg[0] == 'IEA') {
            if(loops[-1][0] != 'ISA' or loops[-1][1] != seg[2])
                err_str = 'IEA id=%s does not match ISA id=%s' % (seg[2], loops[-1][1])
                //errh.isa_error('001', err_str)
            if(atoi(seg[1]) != gs_count)
                err_str = 'IEA count for IEA02=%s is wrong' % (seg[2])
                errh.isa_error('021', err_str)
            del loops[-1]
        }
        else if(seg[0] == 'GS') {
            group_control_number = seg[6]
            if(group_control_number in gs_ids)
                err_str = 'GS Interchange Control Number %s not unique within file' \
                    % (group_control_number)
                errh.gs_error('6', err_str)
            gs_count += 1
            gs_ids.append(group_control_number)
            loops.append(('GS', group_control_number))
            st_count = 0
            st_ids = []
        }
        else if(seg[0] == 'GE') {
            if(loops[-1][0] != 'GS' or loops[-1][1] != seg[2])
                err_str = 'GE id=%s does not match GS id=%s' % (seg[2], loops[-1][1])
                errh.gs_error('4', err_str)
            if(int(seg[1]) != st_count)
                err_str = 'GE count of %s for GE02=%s is wrong. I count %i' \
                    % (seg[1], seg[2], st_count)
                errh.gs_error('5', err_str)
            del loops[-1]
        }
        else if(seg[0] == 'ST') { 
            transaction_control_number = seg[2]
            if(transaction_control_number in st_ids)
                err_str = 'ST Interchange Control Number %s not unique within file' \
                    % (transaction_control_number)
                errh.st_error('23', err_str)
            st_count += 1
            st_ids.append(transaction_control_number)
            loops.append(('ST', transaction_control_number))
            seg_count = 1 
            hl_count = 0
        }
        else if(seg[0] == 'SE') {
            se_trn_control_num = seg[2]
            if(loops[-1][0] != 'ST' or loops[-1][1] != se_trn_control_num)
                err_str = 'SE id=%s does not match ST id=%s' % (se_trn_control_num, loops[-1][1])
                errh.st_error('3', err_str)
            if(int(seg[1]) != seg_count + 1)
                err_str = 'SE count of %s for SE02=%s is wrong. I count %i' \
                    % (seg[1], se_trn_control_num, seg_count + 1)
                errh.st_error('4', err_str)
            del loops[-1]
        }
        else if(seg[0] == 'LS') 
            loops.append(('LS', seg[6]))
        else if(seg[0] == 'LE') 
            del loops[-1]
        else if(seg[0] == 'HL') { 
            seg_count += 1
            hl_count += 1
            if(hl_count != int(seg[1]))
                err_str = 'My HL count %i does not match your HL count %s' \
                    % (hl_count, seg[1])
                errh.seg_error('HL1', err_str)
            if(seg[2] != '')
                parent = int(seg[2])
                if(parent not in hl_stack)
                    hl_stack.append(parent)
                else:
                    if(hl_stack)
                        while hl_stack[-1] != parent)
                            del hl_stack[-1]
        }
        else:
            seg_count += 1;
    }
    catch IndexError {
        err_str = "Expected element not found') %s" % seg
        raise x12Error, err_str
    }
    */
    cur_line += 1;
    return seg;
}

/*    
void x12file::cleanup()
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

list<string> x12file::get_id()
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

void x12file::print_seg(seg)
    sys.stdout.write('%s' % (seg_str(seg, seg_term, ele_term, subele_term, '\n')))

string x12file::format_seg(seg))
    return '%s' % (seg_str(seg, seg_term, ele_term, subele_term, '\n'))

list<string> x12file::get_term()
    return (seg_term, ele_term, subele_term, '\n')
*/
