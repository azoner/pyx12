#!/usr/bin/env python
import glob
import json
import logging
import os
import os.path
import argparse
import sys

libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if os.path.isdir(libpath):
    sys.path.insert(0, libpath)

import pyx12
import pyx12.errors
import pyx12.params
from pyx12.x12metadata import get_x12file_metadata

__author__ = pyx12.__author__
__status__ = pyx12.__status__
__version__ = pyx12.__version__
__date__ = pyx12.__date__

def check_map_path_arg(map_path):
    if not os.path.isdir(map_path):
        raise argparse.ArgumentTypeError(f"MAP_PATH '{map_path}' is not a valid directory")
    index_file = 'maps.xml'
    if not os.path.isfile(os.path.join(map_path, index_file)):
        raise argparse.ArgumentTypeError(
            f"MAP_PATH '{map_path}' does not contain the map index file '{index_file}'"
        )
    return map_path

def main():
    parser = argparse.ArgumentParser(description='X12 File Metadata')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--quiet', '-q', action='store_true')
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--eol', '-e', action='store_true', help='Add eol to each segment line')
    parser.add_argument('--inplace', '-i', action='store_true', help='Make changes to files in place')
    parser.add_argument('--fixcounting', '-f', action='store_true', help='Try to fix counting errors')
    parser.add_argument('--output-dir', '-t', action='store', dest='outputdirectory', default=None,
                        help='Output directory')
    parser.add_argument('--map-path', '-m', action='store', dest='map_path', default=None,
                        type=check_map_path_arg)
    parser.add_argument('--version', action='version', version=f'{parser.prog} {__version__}')
    parser.add_argument('input_files', nargs='*')
    args = parser.parse_args()

    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.addHandler(stdout_hdlr)
    logger.setLevel(logging.INFO)

    param = pyx12.params.params()
    if args.debug:
        logger.setLevel(logging.DEBUG)
        param.set('debug', True)
    if args.verbose > 0:
        logger.setLevel(logging.DEBUG)
    if args.quiet:
        logger.setLevel(logging.ERROR)
    if args.map_path:
        param.set('map_path', args.map_path)

    for fn in args.input_files:
        for src_filename in glob.iglob(fn):
            try:
                logger.debug(f'Processing {src_filename}')
                (result, headers, node_summary) = get_x12file_metadata(param, src_filename, args.map_path)
                if not result:
                    raise pyx12.errors.EngineError()
                res = {'headers': headers, 'nodes': node_summary}
                stem = os.path.splitext(os.path.basename(src_filename))[0]
                out_dir = args.outputdirectory or os.path.dirname(os.path.abspath(src_filename))
                json_file = os.path.join(out_dir, f'{stem}.node_list.json')
                with open(json_file, 'w', encoding='utf-8') as fd:
                    json.dump(res, fd, indent=4)
            except OSError:
                logger.exception('Could not open files')
                return False
            except KeyboardInterrupt:
                print('\n[interrupt]')
    return True

if __name__ == '__main__':
    sys.exit(not main())
