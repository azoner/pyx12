#include <string>
#include <iostream>

#include "segment.hxx"

using namespace std;

int main()
{
    std::string seg_str("TST*AA*1*Y*BB:5:4:AA*ZZ~");
    //cout << seg_str << endl;
    Pyx12::Segment seg_data(seg_str, '~', '*', ':');
    cout << seg_data << endl;
    cout << seg_data.getValue("TST01") << endl;
    cout << seg_data.getValue("01") << endl;
    return 1;
}
