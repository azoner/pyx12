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

#ifndef PYX12_X12FILE_H_
#define PYX12_X12FILE_H_

#include <string>
#include <vector>
#include <stack>
#include <iostream>
#include <fstream>
#include <ostream>

#define BUFSIZE 8*1024
#define ISA_LEN 106
#define MAX_LINE_LEN 1024
using namespace std;

namespace Pyx12 {
    class x12file {
    private:
        stack<string> loops;
        stack<string> hl_stack;
        int gs_count;
        int st_count;
        int hl_count;
        int seg_count;
        int cur_line;
        //string buffer;
        vector<string> isa_ids, gs_ids, st_ids;
        string isa_usage;
        char seg_term;
        char ele_term;
        char subele_term;
        ifstream src_fs;

    public:
        x12file(const string& src_filename); //, errh)
        vector<string> next();
        void cleanup();
        void print_seg(vector<string>);
        string format_seg(vector<string>);
    //    ostream& operator<<(ostream&, x12file&);
    };
};
#endif // PYX12_X12FILE_H_
