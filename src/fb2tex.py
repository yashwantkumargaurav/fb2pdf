#!/usr/bin/env python

'''
FictionBook2 -> TeX converter

Author: Vadim Zaliva <lord@crocodile.org>
'''


import getopt, sys

import fictionbook

def usage():
    sys.stderr.write("Usage: fb2tex.py -f fb2file -o texfile\n")

def main():

    infile = None
    outfile = None
    verbose = False
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vf:o:", ["verbose", "file", "output"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-f", "--file"):
            infile = a
        if o in ("-o", "--output"):
            outfile = a
        if o in ("-v", "--verbose"):
            verbose = True

    if len(args) != 0 or infile is None or outfile is None:
        usage()
        sys.exit(2)

    fb = fictionbook.TexFBook(outfile)
    fb.parseFile(infile)

if __name__ == "__main__":
    main()
