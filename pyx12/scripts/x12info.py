#!/usr/bin/env python
import sys
import os
import os.path
import argparse
import logging
import json

libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if os.path.isdir(libpath):
    sys.path.insert(0, libpath)

import pyx12
from pyx12.x12metadata import get_x12file_metadata
#import pyx12.x12file
#import pyx12.error_handler

__author__ = pyx12.__author__
__status__ = pyx12.__status__
__version__ = pyx12.__version__
__date__ = pyx12.__date__

def check_map_path_arg(map_path):
    if not os.path.isdir(map_path):
        raise argparse.ArgumentError(None, "The MAP_PATH '{}' is not a valid directory".format(map_path))
    index_file = 'maps.xml'
    if not os.path.isfile(os.path.join(map_path, index_file)):
        raise argparse.ArgumentError(None,
                    "The MAP_PATH '{}' does not contain the map index file '{}'".format(map_path, index_file))
    return map_path

def main():
    import argparse
    parser = argparse.ArgumentParser(description='X12 File Metatdata')
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--quiet', '-q', action='store_true')
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--eol', '-e', action='store_true', help="Add eol to each segment line")
    parser.add_argument('--inplace', '-i', action='store_true', help="Make changes to files in place")
    parser.add_argument('--fixcounting', '-f', action='store_true', help="Try to fix counting errors")
    #parser.add_argument('--fixwhitespace', '-w', action='store_true', help="Try to fix extra whitespace errors.")
    #parser.add_argument('--output', '-o', action='store', dest="outputfile", default=None, help="Output filename.  Defaults to stdout")
    parser.add_argument('--output-dir', '-t', action='store', dest="outputdirectory", default=None, help="Output directory")
    parser.add_argument('--version', action='version', version='{prog} {version}'.format(prog=parser.prog, version=__version__))
    parser.add_argument('--map-path', '-m', action='store', dest="map_path", default=None, type=check_map_path_arg)
    parser.add_argument('input_files', nargs='*')
    args = parser.parse_args()

    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.addHandler(stdout_hdlr)
    logger.setLevel(logging.INFO)

    param = pyx12.params.params() # args.configfile)
    if args.debug:
        logger.setLevel(logging.DEBUG)
        param.set('debug', True)
    if args.verbose > 0:
        logger.setLevel(logging.DEBUG)
    if args.quiet:
        logger.setLevel(logging.ERROR)
    if args.map_path:
        param.set('map_path', args.map_path)

    for src_filename in args.input_files:
        try:
            (result, headers, node_summary) = get_x12file_metadata(param, src_filename, args.map_path)
            if not result:
                raise pyx12.errors.EngineError()
            res = {
                'headers': headers,
                'nodes': node_summary,
                }
            (basename, ext) = os.path.splitext(src_filename)
            json_filename = '{}.node_list.json'.format(basename)
            if args.outputdirectory:
                json_file = os.path.join(args.outputdirectory , json_filename)
            else:
                json_file = os.path.join(os.path.dirname(os.path.abspath(src_filename)), json_filename)
            with file(json_file, 'w') as fd:
                json.dump(res, fd, indent=4)

        except IOError:
            logger.exception('Could not open files')
            return False
        except KeyboardInterrupt:
            print("\n[interrupt]")
        except Exception as e:
            raise e


if __name__ == '__main__':
    sys.exit(not main())
