#! /usr/bin/env /usr/local/bin/python

import pyx12.x12file
import pyx12.error_handler
import sys

def main():
    for src_file in sys.argv[1:]:
        try:
            sys.stdout.write('Source filename: %s\n' % (src_file))
            errh = pyx12.error_handler.err_handler()
            fd = open(src_file, 'r')
            src = pyx12.x12file.x12file(fd, errh)
            state = ''
            for c in src:
                if c[0] == 'ISA':
                    sys.stdout.write('ISA From: %s\n' % (c[6]))
                    sys.stdout.write('ISA To: %s\n' % (c[8]))
                    if src.isa_usage == 'P':
                        sys.stdout.write('PRODUCTION\n') 
                    else:
                        sys.stdout.write('TEST\n') 
                    state = ''
                elif c[0] == 'GS':
                    sys.stdout.write('GS From: %s\n' % (c[2]))
                    sys.stdout.write('GS To: %s\n' % (c[3]))
                    state = ''
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
