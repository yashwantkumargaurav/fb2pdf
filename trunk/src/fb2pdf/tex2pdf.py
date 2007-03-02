#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter daemon

Author: Vadim Zaliva <lord@crocodile.org>
'''

import sys, os, shutil, logging

# --- Code ---
def tex2pdf(texfilename, pdffilename):
    # Style files located ${sys_prefix}/share/texmf-local/
    shutil.copy(sys.prefix + '/share/texmf-local/verse.sty', "./")
    shutil.copy(sys.prefix + '/share/texmf-local/epigraph.sty', "./")

    logging.getLogger('tex2pdf').debug("Converting TeX to PDF")
    
    #TODO specify PDF output filename
    rc = os.system("pdflatex -halt-on-error -interaction batchmode -no-shell-escape %s > /dev/null" % texfilename)
    if rc:
        raise Exception("Execution of pdflatex failed with error code %d" % rc)
    # Run again, to incorporate TOC
    rc = os.system("pdflatex -halt-on-error -interaction batchmode -no-shell-escape %s > /dev/null" % texfilename)
    if rc:
        raise Exception("Execution of pdflatex failed with error code %d" % rc)

    # Optimize pdf
    logging.getLogger('tex2pdf').debug("Optimzing PDF")
    tmptex=texfilename+".noopt"
    os.rename(texfilename, tmptex)
    rc = os.system("pdfopt %s %s > /dev/null" % (tmptex,texfilename))
    if rc:
        raise Exception("Execution of pdfopt failed with error code %d" % rc)

