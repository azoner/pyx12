#! /usr/bin/env /usr/local/bin/python

import pyx12.x12file
import pyx12.error_handler
import sys
import getopt
import os.path

"""
Format a X12 document.  If the option -e is used, it adds newlines.
If no source file is given, read from stdin.
If no ouput filename is given with -o,  write to stdout.
"""

def usage():
    sys.stdout.write('x12norm.py %s (%s)\n' % (__version__, __date__))
    sys.stdout.write('usage: x12norm.py [options] source_file\n')
    sys.stdout.write('\noptions:\n')
    sys.stdout.write('  -h         Help\n')
    sys.stdout.write('  -e         Add eol to each segment line\n')
    sys.stdout.write('  -f         Fix.  Try to fix counting errors\n')
    sys.stdout.write('  -o file    Output file.\n')

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hefo:')
    except getopt.error, msg:
        usage()
        return False
    eol = ''
    file_out = None
    fix = False
    for o, a in opts:
        if o == '-h':
            usage()
            return True
        if o == '-e': eol = '\n'
        if o == '-f': fix = True
        if o == '-o': file_out = a

    if file_out:
        fd_out = open(file_out, 'w')
    else:
        fd_out =  sys.stdout
    errh = pyx12.error_handler.errh_null()
    if len(args) > 0:
        file_in = args[0]
        if not os.path.isfile(file_in):
            sys.stderr.write('File %s was not found' % (file_in))
    else:
        file_in = '-'
    src = pyx12.x12file.x12file(file_in, errh)
    for c in src:
        if fix:
            if c[0] == 'IEA' and errh.err_cde == '021':
                c[1] = src.gs_count
            elif c[0] == 'GE' and errh.err_cde == '5':
                c[1] = src.st_count
            elif c[0] == 'SE' and errh.err_cde == '4':
                c[1] = src.seg_count
        fd_out.write(c.format() + eol)
    if eol == '':
        fd_out.write('\n')
    return True

if __name__ == '__main__':
    #if sys.argv[0] == 'x12lintp':
    #    import profile
    #    profile.run('pyx12.x12n_document(src_filename)', 'pyx12.prof')
    #else:
    sys.exit(not main())
