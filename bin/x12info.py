#! /usr/bin/env /usr/local/bin/python

import pyx12.x12file
import pyx12.error_handler
import sys

def main():
    for src_file in sys.argv[1:]:
        try:
            sys.stdout.write('Source filename: %s\n' % (src_file))
            errh = pyx12.error_handler.err_handler()
            src = pyx12.x12file.x12file(src_file, errh)
            state = ''
            for c in src:
                if c.get_seg_id() == 'ISA':
                    sys.stdout.write('ISA Sender: "%s"\t' % (c[6]))
                    sys.stdout.write('ISA Receiver: "%s"\t' % (c[8]))
                    if src.isa_usage == 'P':
                        sys.stdout.write(' PRODUCTION\t') 
                    else:
                        sys.stdout.write(' TEST\t') 
                    state = ''
                    sys.stdout.write('\n')
                elif c.get_seg_id() == 'GS':
                    sys.stdout.write('  GS Sender: "%s"\t' % (c[2]))
                    sys.stdout.write('GS Receiver: "%s"\t' % (c[3]))
                    state = ''
                    sys.stdout.write('\n')
                elif c.get_seg_id() == 'ST':
                    sys.stdout.write('  ST ID: "%s"\t' % (c[1]))
                    state = ''
                    sys.stdout.write('\n')
                else:
                    state = ''
        except:
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
