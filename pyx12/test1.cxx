#include <string>
#include <iostream>

#include "segment.hxx"

using namespace std;

int main()
{
    std::string seg_str("TST*AA:1*1:2:3*Y~");
    //cout << seg_str << endl;
    Pyx12::Segment seg_data(seg_str, '~', '*', ':');
    cerr << seg_data << endl;
    seg_data.setValue("TST05-2", "AR");
    //cerr << "TEST1: After set" << endl;
    cerr << seg_data << endl;
    //cerr << "TEST1: ostream" << endl;
    cerr << seg_data.format() << endl;
    //cerr << "TEST1: After format" << endl;
    return 1;
}
