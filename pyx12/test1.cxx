#include <string>
#include <iostream>

#include "segment.hxx"

using namespace std;

// most frequently you implement test cases as a free functions
int main()
{
    std::string seg_str("TST*AA*1*Y*BB:5*ZZ");
    cout << seg_str << endl;
    Pyx12::segment seg_data(seg_str, "~", "*", ":");
//    cout << seg_data << endl;
    return 1;
}
