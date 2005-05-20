#! /usr/bin/env /usr/local/bin/python

import pyx12
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

__author__  = pyx12.__author__
__status__  = pyx12.__status__
__version__ = pyx12.__version__
__date__    = pyx12.__date__

def usage():
    pgm_nme = os.path.basename(sys.argv[0])
    sys.stdout.write('%s %s (%s)\n' % (pgm_nme, __version__, __date__))
    sys.stdout.write('usage: %s [options] source_file\n' % (pgm_nme))
    sys.stdout.write('\noptions:\n')
    sys.stdout.write('  -h         Help\n')
    sys.stdout.write('  -d         Debug mode\n')
    sys.stdout.write('  -e         Add eol to each segment line\n')
    sys.stdout.write('  -f         Fix.  Try to fix counting errors\n')
    sys.stdout.write('  -o file    Output file.\n')

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dhefo:')
    except getopt.error, msg:
        usage()
        return False
    debug = False
    eol = ''
    file_out = None
    fix = False
    for o, a in opts:
        if o == '-h':
            usage()
            return True
        if o == '-d': debug = True
        if o == '-e': eol = '\n'
        if o == '-f': fix = True
        if o == '-o': file_out = a

    if not debug:
        try:
            import psyco
            psyco.full()
        except ImportError:
            pass

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
    for seg_data in src:
        if fix:
            if seg_data.get_seg_id() == 'IEA' and errh.err_cde == '021':
                seg_data.set('IEA01', src.gs_count)
            elif seg_data.get_seg_id() == 'GE' and errh.err_cde == '5':
                seg_data.set('GE01', src.st_count)
            elif seg_data.get_seg_id() == 'SE' and errh.err_cde == '4':
                seg_data.set('SE01', src.seg_count)
            elif seg_data.get_seg_id() == 'HL' and errh.err_cde == 'HL1':
                seg_data.set('HL01', src.hl_count)
        fd_out.write(seg_data.format() + eol)
    if eol == '':
        fd_out.write('\n')
    return True

if __name__ == '__main__':
    #if sys.argv[0] == 'x12normp':
    #    import profile
    #    profile.run('pyx12.x12n_document(src_filename)', 'pyx12.prof')
    #else:
    sys.exit(not main())
