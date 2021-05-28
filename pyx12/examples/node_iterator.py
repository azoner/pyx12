#!/usr/bin/env python
import sys
import os
import os.path
import logging
import argparse
import json

libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if os.path.isdir(libpath):
    sys.path.insert(0, libpath)

# Intrapackage imports
import pyx12.error_handler
import pyx12.errors
import pyx12.map_index
import pyx12.map_if
import pyx12.params
import pyx12.x12file
from pyx12.map_walker import walk_tree

__version__ = '1.0.0'

def x12n_iterator(param, src_file, map_path=None):
    logger = logging.getLogger('pyx12')
    errh = pyx12.error_handler.errh_null()

    # Get X12 DATA file
    try:
        src = pyx12.x12file.X12Reader(src_file)
    except pyx12.errors.X12Error:
        logger.error('"%s" does not look like an X12 data file' % (src_file))
        return False

    #Get Map of Control Segments
    map_file = 'x12.control.00501.xml' if src.icvn == '00501' else 'x12.control.00401.xml'
    logger.debug('X12 control file: %s' % (map_file))
    control_map = pyx12.map_if.load_map_file(map_file, param, map_path)
    map_index_if = pyx12.map_index.map_index(map_path)
    node = control_map.getnodebypath('/ISA_LOOP/ISA')
    walker = walk_tree()
    icvn = fic = vriic = tspc = None
    cur_map = None  # we do not initially know the X12 transaction type

    res = {}
    res_ordinal = 0
    last_x12_segment_path = None
    for seg in src:
        #find node
        orig_node = node

        if False:
            print('--------------------------------------------')
            print(seg)
            print('--------------------------------------------')
            # reset to control map for ISA and GS loops
            print('------- counters before --------')
            print((walker.counter._dict))
        if seg.get_seg_id() == 'ISA':
            node = control_map.getnodebypath('/ISA_LOOP/ISA')
            walker.forceWalkCounterToLoopStart('/ISA_LOOP', '/ISA_LOOP/ISA')
        elif seg.get_seg_id() == 'GS':
            node = control_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
            walker.forceWalkCounterToLoopStart('/ISA_LOOP/GS_LOOP', '/ISA_LOOP/GS_LOOP/GS')
        else:
            # from the current node, find the map node matching the segment
            # keep track of the loops traversed
            try:
                (node, pop_loops, push_loops) = walker.walk(node, seg, errh, src.get_seg_count(), src.get_cur_line(), src.get_ls_id())
            except pyx12.errors.EngineError:
                logger.error('Source file line %i' % (src.get_cur_line()))
                raise

        if False:
            print('------- counters after --------')
            print((walker.counter._dict))
        if node is None:
            node = orig_node
        else:
            if seg.get_seg_id() == 'ISA':
                icvn = seg.get_value('ISA12')
            elif seg.get_seg_id() == 'IEA':
                pass
            elif seg.get_seg_id() == 'GS':
                fic = seg.get_value('GS01')
                vriic = seg.get_value('GS08')
                map_file_new = map_index_if.get_filename(icvn, vriic, fic)
                if map_file != map_file_new:
                    map_file = map_file_new
                    if map_file is None:
                        err_str = "Map not found.  icvn={}, fic={}, vriic={}".format(icvn, fic, vriic)
                        raise pyx12.errors.EngineError(err_str)
                    cur_map = pyx12.map_if.load_map_file(map_file, param, map_path)
                    src.check_837_lx = True if cur_map.id == '837' else False
                    logger.debug('Map file: %s' % (map_file))
                node = cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
                pass
            elif seg.get_seg_id() == 'BHT':
                # special case for 4010 837P
                if vriic in ('004010X094', '004010X094A1'):
                    tspc = seg.get_value('BHT02')
                    logger.debug('icvn=%s, fic=%s, vriic=%s, tspc=%s' %
                                 (icvn, fic, vriic, tspc))
                    map_file_new = map_index_if.get_filename(icvn, vriic, fic, tspc)
                    logger.debug('New map file: %s' % (map_file_new))
                    if map_file != map_file_new:
                        map_file = map_file_new
                        if map_file is None:
                            err_str = "Map not found.  icvn={}, fic={}, vriic={}, tspc={}".format(
                                        icvn, fic, vriic, tspc)
                            raise pyx12.errors.EngineError(err_str)
                        cur_map = pyx12.map_if.load_map_file(map_file, param, map_path)
                        src.check_837_lx = True if cur_map.id == '837' else False
                        logger.debug('Map file: %s' % (map_file))
                        #apply_loop_count(node, cur_map)
                        node = cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BHT')
            #elif seg.get_seg_id() == 'GE':
            #    pass
            #elif seg.get_seg_id() == 'ST':
            #    pass
            #elif seg.get_seg_id() == 'SE':
            #    pass
            else:
                pass

        x12path = node.get_path()
        #parent
        if x12path in res:
            res[x12path]['Count'] += 1
            if last_x12_segment_path not in res[x12path]['prefix_nodes']:
                res[x12path]['prefix_nodes'].append(last_x12_segment_path)
        else:
            res[x12path] = {
                'Ordinal': res_ordinal,
                'Count': 1,
                'NodeType': node.base_name,
                'Id': node.id,
                'Name': node.name,
                'FormattedName': clean_name(node.name),
                'ParentName': clean_name(node.parent.name),
                'LoopMaxUse': node.max_use,
                'ParentPath': node.parent.get_path(),
                'prefix_nodes': [last_x12_segment_path]
            }
            res_ordinal += 1

        for (refdes, ele_ord, comp_ord, val) in seg.values_iterator():
            elepath = node.parent.get_path() + '/' + refdes
            if elepath in res:
                res[elepath]['Count'] += 1
            else:
                ele_node = node.getnodebypath2(refdes)
                #node.get_child_node_by_ordinal(
                res[elepath] = {
                    'Ordinal': res_ordinal,
                    'Count': 1,
                    'NodeType': ele_node.base_name,
                    'Id': ele_node.id,
                    'Name': ele_node.name,
                    'FormattedName': clean_name(ele_node.name),
                    'ParentName': clean_name(ele_node.parent.name),
                    #'max_use': ele_node.max_use,
                    'ParentPath': ele_node.parent.get_path(),
                    'Usage': ele_node.usage,
                    'DataType': ele_node.data_type,
                    'MinLength': ele_node.min_len,
                    'MaxLength': ele_node.max_len,
                }
                res_ordinal += 1

            #print (refdes, val)
        last_x12_segment_path = x12path

    del node
    del src
    del control_map
    try:
        del cur_map
    except UnboundLocalError:
        pass
    return res

def clean_name(name):
    return name.replace(' ', '').replace('/', '').replace("'", '')

def check_map_path_arg(map_path):
    if not os.path.isdir(map_path):
        raise argparse.ArgumentError(None, "The MAP_PATH '{}' is not a valid directory".format(map_path))
    index_file = 'maps.xml'
    if not os.path.isfile(os.path.join(map_path, index_file)):
        raise argparse.ArgumentError(None,
                    "The MAP_PATH '{}' does not contain the map index file '{}'".format(map_path, index_file))
    return map_path

def main():
    """
    Set up environment for processing
    """
    parser = argparse.ArgumentParser(description='X12 Validation')
    parser.add_argument('--config-file', '-c', action='store',
                        dest="configfile", default=None)
    parser.add_argument(
        '--log-file', '-l', action='store', dest="logfile", default=None)
    parser.add_argument('--map-path', '-m', action='store', dest="map_path", default=None, type=check_map_path_arg)
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--quiet', '-q', action='store_true')
    parser.add_argument('--html', '-H', action='store_true')
    parser.add_argument('--version', action='version', version='{prog} {version}'.format(prog=parser.prog, version=__version__))
    parser.add_argument('input_files', nargs='*')
    args = parser.parse_args()

    logger = logging.getLogger('pyx12')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.addHandler(stdout_hdlr)
    logger.setLevel(logging.INFO)

    param = pyx12.params.params(args.configfile)
    if args.debug:
        logger.setLevel(logging.DEBUG)
        param.set('debug', True)
    if args.verbose > 0:
        logger.setLevel(logging.DEBUG)
    if args.quiet:
        logger.setLevel(logging.ERROR)
    if args.map_path:
        param.set('map_path', args.map_path)

    if args.logfile:
        try:
            hdlr = logging.FileHandler(args.logfile)
            hdlr.setFormatter(formatter)
            logger.addHandler(hdlr)
        except IOError:
            logger.exception('Could not open log file: %s' % (args.logfile))

    for src_filename in args.input_files:
        try:
            if not os.path.isfile(src_filename):
                logger.error('Could not open file "%s"' % (src_filename))
                continue
            res = x12n_iterator(param=param, src_file=src_filename, map_path=args.map_path)
            json_file = os.path.join(os.path.dirname(os.path.abspath(src_filename)), 'node_list.json')
            with open(json_file, 'w') as fd:
                json.dump(res, fd, indent=4)

        except IOError:
            logger.exception('Could not open files')
            return False
        except KeyboardInterrupt:
            print("\n[interrupt]")
        #except Exception as e:
        #    raise e
    return True

if __name__ == '__main__':
    sys.exit(not main())
