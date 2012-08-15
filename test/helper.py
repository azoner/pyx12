import unittest
import pdb


def get_testcases(ns):
    ret = []
    ns_dict = ns.__dict__
    for key in ns_dict.keys():
        try:
            if issubclass(ns_dict[key], unittest.TestCase):
                ret.append(ns_dict[key].__name__)
        except:
            pass
    ret.sort()
    return ret


def print_testcases(ns):
    for t in get_testcases(ns):
        print t


def get_suite(ns, args):
    if args:
        suite = unittest.TestSuite()
        ns_dict = ns.__dict__
        tests = get_testcases(ns)
        for arg in args:
            if arg in tests:
                suite.addTest(unittest.makeSuite(ns_dict[arg]))
        return suite
    else:
        suite = unittest.defaultTestLoader.loadTestsFromModule(ns)
        return suite
