import unittest

import pyx12.error_handler
import pyx12.map_if
import pyx12.params
import pyx12.path
import pyx12.segment

class LoadAllMapsNoErrors(unittest.TestCase):

    def test_load_834(self):
        param = pyx12.params.params()
        map = pyx12.map_if.load_map_file('834.5010.X220.A1.xml', param)

    def test_load_837p(self):
        param = pyx12.params.params()
        map = pyx12.map_if.load_map_file('837.5010.X222.A1.xml', param)


    
