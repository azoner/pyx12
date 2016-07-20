import sys
import os
import os.path
import logging

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

def get_x12file_metadata(param, src_file, map_path=None):
    logger = logging.getLogger('pyx12')
    errh = pyx12.error_handler.errh_null()

    # Get X12 DATA file
    try:
        src = pyx12.x12file.X12Reader(src_file)
    except pyx12.errors.X12Error:
        logger.error('"%s" does not look like an X12 data file' % (src_file))
        return (False, None, None)

    #Get Map of Control Segments
    map_file = 'x12.control.00501.xml' if src.icvn == '00501' else 'x12.control.00401.xml'
    logger.debug('X12 control file: %s' % (map_file))
    control_map = pyx12.map_if.load_map_file(map_file, param, map_path)
    map_index_if = pyx12.map_index.map_index(map_path)
    node = control_map.getnodebypath('/ISA_LOOP/ISA')
    walker = walk_tree()
    icvn = fic = vriic = tspc = None
    cur_map = None  # we do not initially know the X12 transaction type

    isa_data = {}
    node_summary = {}
    node_ordinal = 0
    last_x12_segment_path = None
    for seg in src:
        orig_node = node
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
        if node is None:
            raise pyx12.errors.EngineError("Node not found")
            node = orig_node
        
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
                    node = cur_map.getnodebypath('/ISA_LOOP/GS_LOOP/ST_LOOP/HEADER/BHT')

        if seg.get_seg_id() == 'ISA':
            isa_data = {
                'InterchangeSenderIDQualifier': seg.get_value('ISA05'),
                'InterchangeSenderID': seg.get_value('ISA06'),
                'InterchangeReceiverIDQualifier': seg.get_value('ISA07'),
                'InterchangeReceiverID': seg.get_value('ISA08'),
                'InterchangeDate': seg.get_value('ISA09'),
                'InterchangeTime': seg.get_value('ISA10'),
                'InterchangeControlStandardsIdentifier': seg.get_value('ISA11'),
                'InterchangeControlVersionNumber': seg.get_value('ISA12'),
                'InterchangeControlNumber': seg.get_value('ISA13'),
                'AcknowledgmentRequested': seg.get_value('ISA14'),
                'UsageIndicator': seg.get_value('ISA15'),
                'GSLoops': []
                }
            icvn = isa_data['InterchangeControlVersionNumber']
        elif seg.get_seg_id() == 'IEA':
            isa_data['NumberofIncludedFunctionalGroups'] = seg.get_value('IEA01')
        elif seg.get_seg_id() == 'GS':
            gs_data = {
                'FunctionalGroupHeader': seg.get_value('GS01'),
                'ApplicationSendersCode': seg.get_value('GS02'),
                'ApplicationReceiversCode': seg.get_value('GS03'),
                'FunctionalGroupDate': seg.get_value('GS04'),
                'FunctionalGroupTime': seg.get_value('GS05'),
                'GroupControlNumber': seg.get_value('GS06'),
                'ResponsibleAgencyCode': seg.get_value('GS07'),
                'VersionReleaseIndustryIdentifierCode': seg.get_value('GS08'),
                'STLoops': []
                }
        elif seg.get_seg_id() == 'GE':
            gs_data['NumberofTransactionSetsIncluded'] = seg.get_value('GE01')
            isa_data['GSLoops'].append(gs_data)
        elif seg.get_seg_id() == 'ST':
            st_data = {
                'TransactionSetIdentifierCode': seg.get_value('ST01'),
                'TransactionSetControlNumber': seg.get_value('ST02'),
                'ImplementationConventionReference': seg.get_value('ST03'),
                }
        elif seg.get_seg_id() == 'SE':
            st_data['TransactionSegmentCount'] = seg.get_value('SE01')
            gs_data['STLoops'].append(st_data)
        elif seg.get_seg_id() == 'BHT':
            st_data['HierarchicalStructureCode'] = seg.get_value('BHT01')
            st_data['TransactionSetPurposeCode'] = seg.get_value('BHT02')
            st_data['OriginatorApplicationTransactionIdentifier'] = seg.get_value('BHT03')
            st_data['TransactionSetCreationDate'] = seg.get_value('BHT04')
            st_data['TransactionSetCreationTime'] = seg.get_value('BHT05')
            st_data['ClaimorEncounterIdentifier'] = seg.get_value('BHT06')

        x12path = node.get_path()
        #parent
        if x12path in node_summary:
            node_summary[x12path]['Count'] += 1
            if last_x12_segment_path not in node_summary[x12path]['prefix_nodes']:
                node_summary[x12path]['prefix_nodes'].append(last_x12_segment_path)
        else:
            node_summary[x12path] = {
                'Ordinal': node_ordinal,
                'Count': 1,
                'NodeType': node.base_name,
                'Id': node.id,
                'Name': node.name,
                'ParentName': node.parent.name,
                'LoopMaxUse': node.max_use,
                'ParentPath': node.parent.get_path(),
                'prefix_nodes': [last_x12_segment_path]
            }
            node_ordinal += 1
            
        for (refdes, ele_ord, comp_ord, val) in seg.values_iterator():
            ele_node = node.getnodebypath2(refdes)
            if ele_node.is_composite():
                ele_node = ele_node.get_child_node_by_ordinal(1)
            elepath = ele_node.get_path()

            if elepath in node_summary:
                node_summary[elepath]['Count'] += 1
            else:
                node_summary[elepath] = {
                    'Ordinal': node_ordinal,
                    'Count': 1,
                    'NodeType': ele_node.base_name,
                    'Id': ele_node.id,
                    'Name': ele_node.name,
                    'ParentName': ele_node.parent.name,
                    'ParentPath': ele_node.parent.get_path(),
                    'Usage': ele_node.usage,
                    'DataType': ele_node.data_type,
                    'MinLength': ele_node.min_len,
                    'MaxLength': ele_node.max_len,
                }
                node_ordinal += 1
        last_x12_segment_path = x12path
    return (True, isa_data, node_summary)