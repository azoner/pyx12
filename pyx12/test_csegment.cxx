// Boost.Test
#include <boost/test/unit_test.hpp>
using boost::unit_test_framework::test_suite;

#include "segment.hxx"

// most frequently you implement test cases as a free functions
void test_simple_identity()
{
    std::string seg_str("TST*AA*1*Y*BB:5*ZZ");
    Pyx12::segment seg_data(seg_str, "~", "*", ":");
    BOOST_CHECK(seg_data.format() == seg_str); 
}

test_suite*
init_unit_test_suite( int, char* [] ) {
    test_suite* test= BOOST_TEST_SUITE( "Segment unit tests" );

    // this example will pass cause we know ahead of time number of expected failures
    test->add( BOOST_TEST_CASE( &test_simple_identity), 0 /* expected one error */ );

    return test;
}
/*
class Simple(unittest.TestCase):

def setUp(self):
seg_str = 'TST*AA*1*Y*BB:5*ZZ'
self.seg = pyx12.segment.segment(seg_str, '~', '*', ':')

def test_simple_is_a(self):
self.failUnless(self.seg[0].is_element())
self.failIf(self.seg[0].is_composite())

def test_simple_len(self):
self.assertEqual(len(self.seg[0]), 1)

def test_simple_indexing(self):
self.assertEqual(self.seg[0][0].get_value(), 'AA')
self.assertEqual(self.seg[1][0].get_value(), '1')
self.assertEqual(self.seg[2][0].get_value(), 'Y')
self.assertEqual(self.seg[2][-1].get_value(), 'Y')
self.failUnlessRaises(IndexError, lambda x: self.seg[0][x].get_value(), 1)
*/
