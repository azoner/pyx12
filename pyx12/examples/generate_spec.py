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

__version__ = '1.0.0'

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

def save_csv(rows, csv_file):
    import csv
    fields = ['Ordinal', 'Id', 'NodeType', 'Name', 'FormattedName', 'Count', 'Section', 'RelativePath', 'FullPath', 'ParentPath', 'ParentName', 'LoopMaxUse',
              'Usage', 'DataType', 'MinLength', 'MaxLength']
    with open(csv_file, 'wb') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        rows.sort(key=lambda item: item['Ordinal'])
        for row in rows:
            writer.writerow(row)

def save_mapping(rows, json_file):
    sections = sorted(list(set([x['Section'] for x in rows])))
    maps = {}
    with open(json_file, 'w') as fd:
        fd.write('{')
        for s in sections:
            fd.write('"{section}": ['.format(section=s))
            s = [
                {
                    'Id': x['Id'],
                    'Ordinal': x['Ordinal'],
                    'Type': x['DataType'] if 'DataType' in x else None,
                    'FieldName': x['FormattedName'],
                    'X12Path': x['RelativePath'],
                    'FullPath': x['FullPath'],
                    'ParentPath': x['ParentPath'],
                    'ParentName': x['ParentName'],
                    'Usage': x['Usage'],
                    'MaxLength': x['MaxLength'],
            } for x in rows if x['Section'] == s and x['NodeType'] == 'element']
            s.sort(key=lambda item: item['Ordinal'])
            for item in s:
                fitem = json.dumps(item)
                fd.write('\n\t{item},'.format(item=fitem))
            fd.write('\n],\n')
        fd.write('}')

def make_dict(data):
    rows = []
    for k, v in data.items():
        if v['Id'] in ('IEA02', 'GE02', 'SE02', 'ST03'):
            continue
        row = v
        row['FullPath'] = k
        if '2220D' in k and row['Id'].startswith('STC'):
            row['Section'] = 'ServiceLineStatus'
        elif '2220D' in k:
            row['Section'] = 'ServiceLine'
        elif '2200D' in k and row['Id'].startswith('STC'):
            row['Section'] = 'ClaimStatus'
        elif '2200D' in k:
            row['Section'] = 'Claim'
        elif '2000D' in k:
            row['Section'] = 'Patient'
        elif '2000C' in k and row['Id'].startswith('STC'):
            row['Section'] = 'BillingProviderStatus'
        elif '2000C' in k:
            row['Section'] = 'BillingProvider'
        elif '2200B' in k and row['Id'].startswith('STC'):
            row['Section'] = 'InformationReceiverStatus'
        elif '2000A' in k:
            row['Section'] = 'Header'
        else:
            row['Section'] = 'Batch'
        rows.append(row)
    base_paths = {}
    for row in rows:
        section = row['Section']
        if section not in base_paths:
            base_paths[section] = row['ParentPath']
        elif len(base_paths[section]) > len(row['ParentPath']):
            base_paths[section] = row['ParentPath']
    for row in rows:
        basepath = base_paths[row['Section']]
        if row['FullPath'].startswith(basepath):
            row['RelativePath'] = row['FullPath'][len(basepath)+1:]
    for section in list(set([r['Section'] for r in rows])):
        fields = [r for r in rows if r['Section'] == section and r['NodeType'] == 'element']
        fieldnames = [f['FormattedName'] for f in fields]
        duplicate_fieldnames = set([f for f in fieldnames if fieldnames.count(f) > 1])
        for row in [r for r in rows if r['Section'] == section and r['NodeType'] == 'element' and r['FormattedName'] in duplicate_fieldnames]:
            row['FormattedName'] = row['ParentName'] + row['FormattedName']
    return rows

def main():
    """
    Set up environment for processing
    """
    parser = argparse.ArgumentParser(description='Gen X12 Sepcs')
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

    if args.debug:
        logger.setLevel(logging.DEBUG)
        param.set('debug', True)
    if args.verbose > 0:
        logger.setLevel(logging.DEBUG)
    if args.quiet:
        logger.setLevel(logging.ERROR)

    if args.logfile:
        try:
            hdlr = logging.FileHandler(args.logfile)
            hdlr.setFormatter(formatter)
            logger.addHandler(hdlr)
        except IOError:
            logger.exception('Could not open log file: %s' % (args.logfile))

    src_filename = args.input_files[0]
    json_file = os.path.join(os.path.dirname(os.path.abspath(src_filename)), 'node_list.json')
    with open(json_file, 'r') as fd:
        res = json.load(fd)
    rows = make_dict(res)

    csv_file = os.path.join(os.path.dirname(os.path.abspath(src_filename)), 'out.csv')
    save_csv(rows, csv_file)

    json_map_file = os.path.join(os.path.dirname(os.path.abspath(src_filename)), 'map.json')
    save_mapping(rows, json_map_file)

    return True

if __name__ == '__main__':
    sys.exit(not main())
