#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter

Author: Vadim Zaliva <lord@crocodile.org>
'''

import getopt
import logging
import traceback
import os
import sys
import string
import re
import binascii

from BeautifulSoup import BeautifulStoneSoup, Tag, NavigableString
import Image

# -- constants --
image_exts = {'image/jpeg':'jpg', 'image/png':'png'}

# --- globals --
enclosures = {}
logfile = 'fb2tex.log'

def par(p):
    res = u''
    for s in p:
        if isinstance(s, Tag):
            if s.name == "strong":
                res += u'{\\bf '+ par(s) + u'}'
            elif s.name == "emphasis":
                res += u'{\\it '+ par(s) + u'}'
            elif s.name == "style":
                flogger.warning("Unsupported element: %s" % s.name)
                res += "" #TODO
            elif s.name == "a":
                href=s.get('l:href')
                if href:
                    if href[0]=='#':
                        res += '\\hyperlink{' + href[1:] + '}{\\underline{' + _textQuote(_text(s)) + '}}'
                    else:
                        res += '\\href{' + href + '}{\\underline{' + _textQuote(_text(s)) + '}}'
                else:
                    print s
                    flogger.warning("'a' without 'href'")
                res += "" #TODO
            elif s.name == "strikethrough":
                res += u'\\sout{' + par(s) + u'}'
            elif s.name == "sub":
                res += u'$_{\\textrm{' + par(s) + '}}$'
            elif s.name == "sup":
                res += u'$^{\\textrm{' + par(s) + '}}$'
            elif s.name == "code":
                res += u'\n\\begin{verbatim}\n' + _textQuote(_text(s),code=True) + u'\n\\end{verbatim}\n'
            elif s.name == "image":
                res += processInlineImage(s)
            elif s.name == "l":
                flogger.warning("Unsupported element: %s" % s.name)
                res += "" #TODO
            else:
                flogger.error("Unknown paragrpah element: %s" % s.name)
        elif isinstance(s, basestring) or isinstance(s, unicode):
            res += _textQuote(_text(s))
    return res            

def _textQuote(str, code=False):
    ''' Basic paragraph TeX quoting '''
    if len(str)==0:
        return str
    if not code:
        # backslash itself must be represented as \backslash
        # (should go first to avoid escaping backslash in TeX commands
        # produced further down this function)
        str = string.replace(str,'\\','\\backslash\\,')
        # special chars need to be quoted with backslash
        # (should go after escaping backslash but before any of the
        # other conversions that produce TeX commands that include {})
        str = re.sub(r'([\&\$\%\#\_\{\}])',r'\\\1',str)
        
        # 'EN DASH' at the beginning of paragraph - russian direct speech
        if ord(str[0])==0x2013:
            str="\\cdash--*" + str[1:]
        # ellipses
        str = string.replace(str,'...','\\ldots')
        # caret
        str = string.replace(str,'\^','\\textasciicircum')
        # tilde
        str = string.replace(str,'\~','\\textasciitilde')
        # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
        str = string.replace(str,u'\u00ab','<<')
        # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
        str = string.replace(str,u'\u00bb','>>') # replacing with french/russian equivalent
        # EM-DASH
        str = re.sub(r'(\s)--(\s)','---',str)
        # preserve double quotes
        str = string.replace(str,'"','\\symbol{34}')
        # Fancy quotation marks (sometimes used to denote a quote
        # inside of another quote)
        str = string.replace(str,u'\u201e','``')
        str = string.replace(str,u'\u201c',"''")
        
    return str

def convXMLentities(s):
    #TODO: proper conversion
    return s.replace('&lt;','<') \
           .replace('&gt;','>') \
           .replace('&amp;','&')
           
def _text(t):
    if isinstance(t, basestring) or isinstance(t, unicode):
        return convXMLentities(unicode(t))
    
    # Temporary check. TODO: remove
    for x in t.contents:
        if not isinstance(x, basestring) and not isinstance(x, unicode):
            flogger.error("Unexpected element in _text: '%s'" % x)
    return string.join([convXMLentities(e) for e in  t.contents])

def _escapeSpace(t):
    return re.sub(r'([ ])+',r'\\ ', t)

def _pdfString(p):
    res = ''
    for s in p:
        res = res + _text(s)
    return res.encode('utf-8', 'replace')

def _uwrite(f, ustr):
    f.write(ustr.encode('utf-8')) 

def _getdir(f):
    l = string.rsplit(f,"/",1)
    if len(l)==2:
        return l[0]
    else:
        return "."
    
def fb2tex(infile, outfile, logfilename=None):

    flogger.info("Converting %s to %s" % (infile,outfile))

    if logfilename:
        initLog(logfilename, logging.DEBUG)
    flogger.info("Converting %s" % infile)
        
    f = open(infile, 'r')
    soup = BeautifulStoneSoup(f,selfClosingTags=['empty-line',"image"],convertEntities=[BeautifulStoneSoup.XML_ENTITIES])
    f.close()

    f = open(outfile, 'w')

    outdir=_getdir(outfile)
    
    # laTeX-document header
    f.write("""\\documentclass[12pt,openany]{book}
    \\usepackage[
        colorlinks=true,
        linkcolor=black,
        bookmarks=true,
        bookmarksnumbered=true,
        hypertexnames=false,
        plainpages=false,
        pdfpagelabels,
        unicode
    ]{hyperref}
    \\usepackage[
        papersize={90.6mm,122.4mm},
        margin=1mm,
        ignoreall,
        pdftex
    ]{geometry}
    \\usepackage{graphicx}
    \\usepackage{url}
    \\usepackage{epigraph}
    \\usepackage{verbatim}
    \\usepackage{ulem}
    \\usepackage[utf-8]{inputenc}
    \\usepackage[russian]{babel}
    \\setcounter{secnumdepth}{-2}
    """)
    
    #TODO: Instead of selecting font family inside of the document 
    # section, set the defaults for the entire document
    #\renewcommand{\rmdefault}{xxx}
    #\renewcommand{\sfdefault}{xxx}
    #\renewcommand{\ttdefault}{xxx}
    
    f.write("\n\\begin{document}\n\n")
    f.write("{\\fontfamily{cmss}\\selectfont\n")
    fb = soup.find("fictionbook")
    
    findEnclosures(fb,outdir)
    processDescription(fb.find("description"), f)

    f.write("\\tableofcontents\n\\newpage\n\n");
    
    body=fb.find("body")
    processEpigraphs(body, f)
    processSections(body, f)
    
    f.write("}")
    f.write("\n\\end{document}\n")
    f.close()

    flogger.info("Conversion successfully finished")

def processSections(b,f):
    ss = b.findAll("section", recursive=False)
    for s in ss:
        processSection(s, f)

def processPoem(p,f):
    f.write('\\begin{verse}\n\n')
    
    # title (optinal)
    t = p.find("title", recursive=False)
    if t:
        title = getSectionTitle(t)
        if title and len(title):
            f.write("\\poemtitle{\\texorpdfstring{")
            _uwrite(f,_escapeSpace(title))
            f.write("}{%s}}\n" % _pdfString(title))

    
    # epigraphs (multiple, optional)
    processEpigraphs(p, f)

    # stanza (at least one!) - { title?, subtitle?, v*}
    ss = p.findAll("stanza", recursive=False)
    for s in ss:
        processStanza(s, f)

    processAuthors(p,f)
    
    # date
    d = p.find("date", recursive=False)
    if d:
        pdate = _text(d)
        flogger.warning("Unsupported element: date")
        #TODO find a nice way to print date
        
    f.write('\\end{verse}\n\n')

def processStanza(s, f):
    # title (optional)
    t = s.find("title", recursive=False)
    if t:
        title = getSectionTitle(t)
        if title and len(title):
            # TODO: implement
            flogger.warning("Unsupported element: stanza 'title'")
    
    # subtitle (optional)
    st = s.find("subtitle", recursive=False)
    if st:
        subtitle = getSectionTitle(st)
        if subtitle and len(subtitle):
            # TODO: implement
            flogger.warning("Unsupported element: stanza 'subtitle'")

    # 'v' - multiple    
    vv = s.findAll("v", recursive=False)
    for v in vv:
        vt = par(v)
        _uwrite(f,vt)
        f.write(" \\\\\n")


def processAuthors(q,f):
    aa = q.findAll("text-author")
    author_name = ""
    for a in aa:
        if len(author_name):
            author_name += " \\and " + _textQuote(_text(a))
        else:
            author_name = _textQuote(_text(a))
            
    if author_name:
        f.write("\\author{")
        _uwrite(f,author_name)
        f.write("}\n");


def processCite(q,f):
    f.write('\\begin{quotation}\n')

    for x in q:
        if isinstance(x, Tag):
            if x.name=="p":
                _uwrite(f,par(x))
                f.write("\n\n")
            elif x.name=="poem":
                processPoem(x,f)
            elif x.name=="empty-line":
                f.write("\\vspace{10mm}\n\n")
            elif x.name == "subtitle":
                f.write("\\subsection*{\\texorpdfstring{")
                _uwrite(f,_escapeSpace(par(x)))
                f.write("}{%s}}\n\n" % _pdfString(x))
            elif x.name=="table":
                flogger.warning("Unsupported element: %s" % x.name)
                pass # TODO
        elif isinstance(x, basestring) or isinstance(x, unicode):
            _uwrite(f,_textQuote(_text(x)))

    processAuthors(q,f)

    f.write('\\end{quotation}\n')
    
def processSection(s, f):
    t = s.find("title", recursive=False)
    if t:
        title = getSectionTitle(t)
    else:
        title = ""

    f.write("\n\\section{\\texorpdfstring{")
    _uwrite(f,_escapeSpace(title)) # TODO quote
    f.write("}{%s}}\n\n" % _pdfString(title));

    processEpigraphs(s, f)
    
    for x in s.contents:
        if isinstance(x, Tag):
            if x.name == "section":
                processSection(x,f)
            if x.name == "p":
                pid=x.get('id')
                if pid:
                    f.write('\\hypertarget{')
                    _uwrite(f,pid)
                    f.write('}{}\n')
                _uwrite(f,par(x))
                f.write("\n\n")
            elif x.name == "empty-line":
                f.write("\\vspace{10mm}\n\n")
            elif x.name == "image":
                f.write(processInlineImage(x))
            elif x.name == "poem":
                processPoem(x,f)
            elif x.name == "subtitle":
                f.write("\\subsection{\\texorpdfstring{")
                _uwrite(f,_escapeSpace(par(x)))
                f.write("}{%s}}\n" % _pdfString(x))
            elif x.name == "cite":
                processCite(x,f)
            elif x.name == "table":
                flogger.warning("Unsupported element: %s" % x.name)
                pass # TODO
            elif x.name!="title" and x.name!="epigraph":
                flogger.error("Unknown section element: %s" % x.name)

def processAnnotation(f, an):
    if len(an):
        f.write('\\section*{}\n')
        f.write('\\begin{small}\n')
        for x in an:
            if isinstance(x, Tag):
                if x.name == "p":
                    _uwrite(f,par(x))
                    f.write("\n\n")
                elif x.name == "empty-line":
                    f.write("\n\n") # TODO: not sure
                elif x.name == "poem":
                    processPoem(x,f)
                elif x.name == "subtitle":
                    f.write("\\subsection*{\\texorpdfstring{")
                    _uwrite(f,_escapeSpace(par(x)))
                    f.write("}{%s}}\n" % _pdfString(x))
                elif x.name == "cite":
                    processCite(x,f)
                elif x.name == "table":
                    flogger.warning("Unsupported element: %s" % x.name)
                    pass # TODO
                else:
                    flogger.error("Unknown annotation element: %s" % x.name)
        f.write('\\end{small}\n')
        f.write('\\pagebreak\n\n')

def getSectionTitle(t):
    ''' Section title consists of "p" and "empty-line" elements sequence'''
    first = True
    res = u''
    for x in t:
        if isinstance(x, Tag):
            if x.name == "p":
                if not first:
                    res = res + u"\\\\"
                else:
                    first = False
                res = res + par(x)
            elif x.name == "empty-line":
                if not first:
                    res = res + u"\\\\"
            else:
                flogger.error("Unknown section title element: %s" % x.name)
    return res

def processEpigraphText(f,e):
    first = True
    ''' Epigaph text consists of "p", "empty-line", "poem" and "cite" elements sequence'''
    i=0
    for x in e.contents:
        i=i+1
        if isinstance(x, Tag):
            if x.name == "p":
                if not first:
                    f.write("\\\\")
                else:
                    first = False
                _uwrite(f,par(x))
            elif x.name == "empty-line":
                if not first and i!=len(e.contents):
                    # not first, not last
                    f.write("\\\\")
            elif x.name == "poem":
                # TODO: test how verse plays with epigraph evn.
                processPoem(x,f)
            elif x.name == "cite":
                processCite(x,f)
            elif x.name != "text-author":
                flogger.error("Unknown epigraph element: %s" % x.name)
        
def processEpigraphs(s,f):
    ep = s.findAll("epigraph", recursive=False)
    if len(ep)==0:
        return
    f.write("\\begin{epigraphs}\n")
    for e in ep:
        f.write("\\qitem{")
        processEpigraphText(f, e)
        f.write(" }%\n")

        eauthor=""
        ea=e.find("text-author")
        if ea:
            eauthor=_text(ea)
        f.write("\t{")
        _uwrite(f,eauthor)
        f.write("}\n")
        
    f.write("\\end{epigraphs}\n")


def authorName(a):
    fn = a.find("first-name")
    if fn:
        author_name = _text(fn)
    else:
        author_name = ""
    mn = a.find("middle-name")
    if mn:
        if author_name:
            author_name = author_name + " " + _text(mn)
        else:
            author_name = _text(mn)
    ln = a.find("last-name")
    if ln:
        if author_name:
            author_name = author_name + " " + _text(ln)
        else:
            author_name = _text(ln)
    return author_name

def processDescription(desc,f):
    if not desc:
        flogger.warning("Missing required 'description' element\n")
        return
    
    # title info, mandatory element
    ti = desc.find("title-info")
    if not ti:
        flogger.warning("Missing required 'title-info' element\n")
        return 
    t = ti.find("book-title")
    if t:
        title = _text(t)
    else:
        title = ""

    # authors
    aa = ti.findAll("author")
    author_name = ""
    for a in aa:
        if len(author_name):
            author_name += " \\and " + authorName(a)
        else:
            author_name = authorName(a)
            
    if author_name:
        f.write("\\author{")
        _uwrite(f,author_name)
        f.write("}\n");

    if title:
        f.write("\\title{\\texorpdfstring{")
        _uwrite(f, _escapeSpace(title))
        f.write("}{%s}}\n" % _pdfString(title))

    f.write("\\date{}")

    if author_name or title:
        f.write("\\maketitle\n");

    # TODO: PDF info generation temporary disabled. It seems that
    # non ASCII characters are not allowed there!
    if False and (author_name or title):
        f.write("\n\\pdfinfo {\n")

        if author_name:
            f.write("\t/Title (")
            _uwrite(f,author_name) #TODO quoting, at least brackets
            f.write(")\n")

        if title:
            f.write("\t/Author (")
            _uwrite(f,title) #TODO quoting, at least brackets
            f.write(")\n")

        f.write("}\n")

    # cover, optional
    co = desc.find("coverpage")
    if co:
        images = co.findAll("image", recursive=False)
        if len(images):
            #f.write("\\begin{titlepage}\n")
            for image in images:
                f.write(processInlineImage(image))
            #f.write("\\end{titlepage}\n")

    # annotation, optional
    an = desc.find("annotation")
    if an:
        processAnnotation(f,an)

def findEnclosures(fb,outdir):
    encs = fb.findAll("binary", recursive=False)
    for e in encs:
        id=e['id']
        ct=e['content-type']
        global image_exts
        if not image_exts.has_key(ct):
            flogger.warning("Unknown content-type '%s' for binary with id %s. Skipping\n" % (ct,id))
            continue
        fname = os.tempnam(".", "enc") + "." + image_exts[ct]
        fullfname = outdir + "/" + fname
        f = open(fullfname,"w")
        f.write(binascii.a2b_base64(e.contents[0]))
        f.close()
        # convert to grayscale, 166dpi (native resolution for Sony Reader)
        Image.open(fullfname).convert("L").save(fullfname, dpi=(166,166))
        #TODO: scale down large images        
        global enclosures
        enclosures[id]=(ct, fname)
    
def processInlineImage(image):
        global enclosures
        href = image.get('l:href')
        if not href or href[0]!='#':
            flogger.error("Invalid inline image ref '%s'\n" % href)
            return ""
        href=str(href[1:])
        if not enclosures.has_key(href):
            flogger.error("Non-existing image ref '%s'\n" % href)
            return ""
        (ct,fname)=enclosures[href]
        return "\\begin{center}\n\\includegraphics{%s}\n\\end{center}\n" % fname

def usage():
    sys.stderr.write("Usage: fb2tex.py [-v] -f fb2file -o texfile\n")

def initLog(logfilename, log_verbosity):
    hdlr = logging.FileHandler(logfilename)
    formatter = logging.Formatter('%(asctime)s [%(process)d.%(thread)d] %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    
    global flogger
    flogger = logging.getLogger('fb2tex')
    flogger.addHandler(hdlr)
    flogger.setLevel(log_verbosity)


def parseCommandLine():
    infile = None
    outfile = None

    log_verbosity = logging.INFO
    
    (optlist, arglist) = getopt.getopt(sys.argv[1:], "vf:o:", ["verbose", "file=", "output="])
    for option, argument in optlist:
        if option in ("-v", "--verbose"):
            log_verbosity = logging.DEBUG
        elif option in ("-f", "--file"):
            if os.path.isfile(argument):
                infile = argument
            else:
                raise getopt.GetoptError("input file '%s' doesn't exist" % argument)
        elif option in ("-o", "--output"):
            outfile = argument
            
    if infile == None:
        raise getopt.GetoptError("input file not specified")
    if outfile == None:
        raise getopt.GetoptError("output file not specified")

    # file log
    initLog(logfile, log_verbosity)

    # console log
    console = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    flogger.addHandler(console)
    
    return (infile, outfile)

def main():
    try:
        (infile, outfile) = parseCommandLine()
        fb2tex(infile, outfile)
    except getopt.GetoptError, msg:
        if len(sys.argv[1:]) > 0:
            print >>sys.stderr, "Error: %s\n" % msg
        else:
            usage()
        return 2
    except:
        info = sys.exc_info()
        traceback.print_exc()
        return 3

if __name__ == "__main__":
    sys.exit(main())
