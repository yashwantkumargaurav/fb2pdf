#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter daemon

Author: Vadim Zaliva <lord@crocodile.org>
'''

import sys, os, shutil, logging

from exceptions import TemporaryError, PersistentError

# --- Code ---
def tex2pdf(texfilename, pdffilename):
    # Style files located ${sys_prefix}/share/texmf-local/
    shutil.copy(sys.prefix + '/share/texmf-local/verse.sty', "./")
    shutil.copy(sys.prefix + '/share/texmf-local/epigraph.sty', "./")

    logging.getLogger('fb2pdf').debug("Converting TeX to PDF")
    
    #TODO specify PDF output filename
    rc = os.system("pdflatex -halt-on-error -interaction batchmode -no-shell-escape %s > /dev/null" % texfilename)
    if rc:
        raise PersistentError("Execution of pdflatex failed with error code %d" % rc)
    # Run again, to incorporate TOC
    rc = os.system("pdflatex -halt-on-error -interaction batchmode -no-shell-escape %s > /dev/null" % texfilename)
    if rc:
        # Since it is passed first time, second failure considered temporary error
        raise TemporaryError("Execution of pdflatex failed with error code %d" % rc)

    # Optimize pdf
    logging.getLogger('fb2pdf').debug("Optimzing PDF")
    tmppdf=pdffilename+".noopt"
    os.rename(pdffilename, tmppdf)
    rc = os.system("pdfopt %s %s > /dev/null" % (tmppdf,pdffilename))
    if rc:
        raise PersistentError("Execution of pdfopt failed with error code %d" % rc)

