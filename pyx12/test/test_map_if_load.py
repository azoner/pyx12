import unittest

import pyx12.error_handler
import pyx12.map_if
import pyx12.params
import pyx12.path
import pyx12.segment

class LoadAllMapsNoErrors(unittest.TestCase):

    def test_load_maps(self):
        param = pyx12.params.params()
        maps = [
            '270.4010.X092.A1.xml',
            '271.4010.X092.A1.xml',
            '276.4010.X093.A1.xml',
            '277.4010.X093.A1.xml',
            '277.5010.X212.xml',
            '277.5010.X214.xml',
            '277U.4010.X070.xml',
            '278.4010.X094.27.A1.xml',
            '278.4010.X094.A1.xml',
            '820.4010.X061.A1.xml',
            '820.5010.X218.v2.xml',
            '820.5010.X218.xml',
            '830.4010.PS.xml',
            '834.4010.X095.A1.xml',
            '834.5010.X220.A1.v2.xml',
            '834.5010.X220.A1.xml',
            '835.4010.X091.A1.xml',
            '835.5010.X221.A1.v2.xml',
            '835.5010.X221.A1.xml',
            '837.4010.X096.A1.xml',
            '837.4010.X097.A1.xml',
            '837.4010.X098.A1.xml',
            '837.5010.X222.A1.xml',
            '837Q3.I.5010.X223.A1.v2.xml',
            '837Q3.I.5010.X223.A1.xml',
            '997.4010.xml',
            '999.5010.xml',
            '999.5010X231.A1.xml',
        ]
        for map in maps:
            try:
                map = pyx12.map_if.load_map_file(map, param)
            except:
                print(map)
                raise

