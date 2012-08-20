#!/usr/bin/env python
import sys
import os
import os.path

libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if os.path.isdir(libpath):
    sys.path.insert(0, libpath)

import pyx12.x12file
import pyx12.error_handler
import sys


def main():
    for src_file in sys.argv[1:]:
        try:
            sys.stdout.write('Source filename: %s\n' % (src_file))
            src = pyx12.x12file.X12Reader(src_file)
            state = ''
            for c in src:
                if c.get_seg_id() == 'ISA':
                    sys.stdout.write('  ISA Sender: "%s"\t' %
                                     (c.get_value('ISA06')))
                    sys.stdout.write('ISA Receiver: "%s"\t' %
                                     (c.get_value('ISA08')))
                    if src.isa_usage == 'P':
                        sys.stdout.write(' PRODUCTION\t')
                    else:
                        sys.stdout.write(' TEST\t')
                    state = ''
                    sys.stdout.write('\n')
                elif c.get_seg_id() == 'GS':
                    sys.stdout.write('  GS Sender: "%s"\t' %
                                     (c.get_value('GS02')))
                    sys.stdout.write('GS Receiver: "%s"\t' %
                                     (c.get_value('GS03')))
                    sys.stdout.write('GS Type: "%s"\t' % (c.get_value('GS08')))
                    state = ''
                    sys.stdout.write('\n')
                elif c.get_seg_id() == 'ST':
                    sys.stdout.write('  ST ID: "%s"\t' % (c.get_value('ST02')))
                    sys.stdout.write('  ST Type: "%s"\t' %
                                     (c.get_value('ST01')))
                    state = ''
                    sys.stdout.write('\n')
                else:
                    state = ''
        except Exception:
            sys.stderr.write('File %s failed.' % (src_file))
            raise

        #self.gs_count = 0
        #self.st_count = 0
        #self.hl_count = 0
        #self.seg_count = 0
        #self.cur_line = 0
        #self.buffer = None


if __name__ == '__main__':
    sys.exit(not main())
