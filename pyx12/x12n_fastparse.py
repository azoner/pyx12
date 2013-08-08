#####################################################################
# Copyright Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Parse a ANSI X12N data file.  Validate against a map and codeset values.
"""

#import os
#import os.path
import logging
import pprint

# Intrapackage imports
import pyx12.error_handler
#import pyx12.error_debug
import pyx12.errors
import pyx12.map_index
import pyx12.map_if
import pyx12.x12file
from pyx12.map_walker import walk_tree


def apply_loop_count(orig_node, new_map):
    """
    Apply loop counts to current map
    """
    logger = logging.getLogger('pyx12')
    ct_list = []
    orig_node.get_counts_list(ct_list)
    for (path, ct) in ct_list:
        try:
            curnode = new_map.getnodebypath(path)
            curnode.set_cur_count(ct)
        except pyx12.errors.EngineError:
            logger.error('getnodebypath failed:  path "%s" not found' % path)


def reset_isa_counts(cur_map):
    cur_map.getnodebypath('/ISA_LOOP').set_cur_count(1)
    cur_map.getnodebypath('/ISA_LOOP/ISA').set_cur_count(1)


def reset_gs_counts(cur_map):
    cur_map.getnodebypath('/ISA_LOOP/GS_LOOP').reset_cur_count()
    cur_map.getnodebypath('/ISA_LOOP/GS_LOOP').set_cur_count(1)
    cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS').set_cur_count(1)


def x12n_fastparser(param, src_file):
    """
    Primary X12 validation function
    @param param: pyx12.param instance
    @param src_file: Source document
    @type src_file: string
    @rtype: boolean
    """
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
    control_map = pyx12.map_if.load_map_file(map_file, param)
    map_index_if = pyx12.map_index.map_index()
    node = control_map.getnodebypath('/ISA_LOOP/ISA')
    walker = walk_tree()
    icvn = fic = vriic = tspc = None

    walk_history = {}
    pp = pprint.PrettyPrinter(indent=4)
    for seg in src:
        #find node
        orig_node = node

        if seg.get_seg_id() == 'ISA':
            node = control_map.getnodebypath('/ISA_LOOP/ISA')
        elif seg.get_seg_id() == 'GS':
            node = control_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
        else:
            try:
                start_path = node.get_path()
                seg_key = seg.seg_id
                hkey = start_path + '__' + seg_key
                if hkey in walk_history:
                    node = walk_history[hkey]['node']
                    walk_history[hkey]['count'] += 1
                else:
                    (node, pop_loops, push_loops) = walker.walk(node, seg, errh,
                                                            src.get_seg_count(), src.get_cur_line(), src.get_ls_id())
                    new_path = node.get_path()
                    #if walk_history[hkey]['newpath'] != new_path:
                    #    raise Exception('Saved newpath "{}" is not walked path "{}"'.format(walk_history[hkey]['newpath'], new_path))
                    walk_history[hkey] = {'newpath': new_path, 'count': 1, 'node': node}
            except pyx12.errors.EngineError:
                logger.error('Source file line %i' % (src.get_cur_line()))
                raise
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
                        raise pyx12.errors.EngineError("Map not found.  icvn=%s, fic=%s, vriic=%s" %
                                                       (icvn, fic, vriic))
                    cur_map = pyx12.map_if.load_map_file(map_file, param)
                    if cur_map.id == '837':
                        src.check_837_lx = True
                    else:
                        src.check_837_lx = False
                    logger.debug('Map file: %s' % (map_file))
                    apply_loop_count(orig_node, cur_map)
                    reset_isa_counts(cur_map)
                reset_gs_counts(cur_map)
                node = cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/GS')
            elif seg.get_seg_id() == 'GE':
                pass
            elif seg.get_seg_id() == 'ST':
                pass
            elif seg.get_seg_id() == 'SE':
                pass
            else:
                pass

    src.cleanup()  # Catch any skipped loop trailers
    pp.pprint(walk_history)

    del node
    del src
    del control_map
    del cur_map
