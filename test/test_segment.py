#! /usr/bin/env /usr/local/bin/python

import unittest

import pyx12.segment

class Identity(unittest.TestCase):

    #def setUp(self):

    def test_identity(self):
        seg_str = 'TST&AA!1!1&BB!5'
        seg = pyx12.segment.segment(seg_str, '+', '&', '!')
        self.assertEqual(seg_str+'+\n', seg.__repr__())
        self.assertEqual(seg.get_seg_id(), 'TST')
                    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Identity))
    return suite

#if __name__ == "__main__":
#    unittest.main()
unittest.TextTestRunner(verbosity=2).run(suite())


