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
    //seg_data.setValue("TST05-2", "AR");
    cerr << seg_data.getValue("TST02-2") << endl;
    return 1;
}
