#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter daemon

Author: Vadim Zaliva <lord@crocodile.org>
'''

import sys, os, shutil, logging, re

from exceptions import TemporaryError, PersistentError

def QuoteForPOSIX(string):
    '''quote a string so it can be used as an argument in a  posix shell

       According to: http://www.unix.org/single_unix_specification/
          2.2.1 Escape Character (Backslash)

          A backslash that is not quoted shall preserve the literal value
          of the following character, with the exception of a <newline>.

          2.2.2 Single-Quotes

          Enclosing characters in single-quotes ( '' ) shall preserve
          the literal value of each character within the single-quotes.
          A single-quote cannot occur within single-quotes.

      http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/498202
    '''
    return "\\'".join("'" + p + "'" for p in string.split("'"))


# --- Code ---
def tex2pdf(texfilename, pdffilename):
    # Style files located ${sys_prefix}/share/texmf-local/
    shutil.copy(sys.prefix + '/share/texmf-local/verse.sty', "./")
    shutil.copy(sys.prefix + '/share/texmf-local/epigraph.sty', "./")
    for filename in os.listdir(sys.prefix + '/share/fb2pdf/pscyr-fonts'):
        shutil.copyfile(sys.prefix + '/share/fb2pdf/pscyr-fonts/%s' % filename, "./")    

    logging.getLogger('fb2pdf').debug("Converting TeX to PDF")
    
    #TODO specify PDF output filename
    rc = os.system("pdflatex -halt-on-error -interaction batchmode -no-shell-escape %s > /dev/null" % QuoteForPOSIX(texfilename))
    if rc:
        raise PersistentError("Execution of pdflatex failed with error code %d" % rc)
    # Run again, to incorporate TOC
    rc = os.system("pdflatex -halt-on-error -interaction batchmode -no-shell-escape %s > /dev/null" % QuoteForPOSIX(texfilename))
    if rc:
        # Since it is passed first time, second failure considered temporary error
        raise TemporaryError("Execution of pdflatex failed with error code %d" % rc)

    # Optimize pdf
    #logging.getLogger('fb2pdf').debug("Optimzing PDF")
    #tmppdf=pdffilename+".noopt"
    #os.rename(pdffilename, tmppdf)
    #rc = os.system("pdfopt %s %s > /dev/null" % (QuoteForPOSIX(tmppdf),QuoteForPOSIX(pdffilename)))
    #if rc:
    #    raise PersistentError("Execution of pdfopt failed with error code %d" % rc)

