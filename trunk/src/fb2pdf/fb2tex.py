#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter

Author: Vadim Zaliva <lord@crocodile.org>
'''

import logging
import os
import sys
import string
import re
import binascii
from xml.dom.minidom import parse, Node

import Image

from exceptions import TemporaryError, PersistentError


# -- constants --
image_exts = {'image/jpeg':'jpg', 'image/png':'png'}

# --- globals --
enclosures = {}

def findAll(elem, what):
    res = []
    for x in elem.childNodes:
        if x.nodeType == Node.ELEMENT_NODE and x.tagName==what:
            res.append(x)

    return res

def find(elem, what):
    nl=elem.getElementsByTagName(what)
    if nl is None or len(nl)==0:
        return None
    else:
        return nl[0]

def par(p, allowhref=True):
    res = u''
    for s in p.childNodes:
        if s.nodeType == Node.ELEMENT_NODE:
            if s.tagName == "strong":
                res += u'{\\bf '+ par(s,allowhref) + u'}'
            elif s.tagName == "emphasis":
                res += u'{\\it '+ par(s,allowhref) + u'}'
            elif s.tagName == "style":
                logging.getLogger('fb2pdf').warning("Unsupported element: %s" % s.tagName)
                res += "" #TODO
            elif s.tagName == "a":
                if allowhref:
                    href = s.getAttributeNS('http://www.w3.org/1999/xlink','href')
                    if href:
                        if href[0]=='#':
                            res += '\\hyperlink{' + href[1:] + '}{\\underline{' + par(s,allowhref) + '}}'
                        else:
                            res += '\\href{' + href + '}{\\underline{' + par(s,allowhref) + '}}'
                    else:
                        logging.getLogger('fb2pdf').warning("'a' without 'href'")
                else:
                    res += par(s,allowhref)
                res += "" #TODO
            elif s.tagName == "strikethrough":
                res += u'\\sout{' + par(s,allowhref) + u'}'
            elif s.tagName == "sub":
                res += u'$_{\\textrm{' + par(s,allowhref) + '}}$'
            elif s.tagName == "sup":
                res += u'$^{\\textrm{' + par(s,allowhref) + '}}$'
            elif s.tagName == "code":
                res += u'{\\sc' + par(s,allowhref) + u'}'
            elif s.tagName == "image":
                res += processInlineImage(s)
            elif s.tagName == "l":
                logging.getLogger('fb2pdf').warning("Unsupported element: %s" % s.tagName)
                res += "" #TODO
            else:
                logging.getLogger('fb2pdf').error("Unknown paragrpah element: %s" % s.tagName)
        elif s.nodeType == Node.TEXT_NODE:
            res += _textQuote(s.data)
    return res            

def _textQuote(str):
    ''' Basic paragraph TeX quoting '''
    if len(str)==0:
        return str
    # backslash itself must be represented as \backslash
    # (should go first to avoid escaping backslash in TeX commands
    # produced further down this function)
    str = string.replace(str,'\\','$\\backslash$')
    # special chars need to be quoted with backslash
    # (should go after escaping backslash but before any of the
    # other conversions that produce TeX commands that include {})
    str = re.sub(r'([\&\$\%\#\_\{\}])',r'\\\1',str)
    # TODO: Fix the following quick ugly hack
    # this is here, because the line above breaks $\backslash$
    # that comes before that, which would break stuff on the above
    # line if it followed it
    str = re.sub(r'\\\$\\backslash\\\$',r'$\\backslash$',str)

    # Unicode Character 'EM DASH' (U+2014)
    # used in some documents instead of '-'
    str = string.replace(str,u'\u2014','---')
    # 'EN DASH' at the beginning of paragraph - russian direct speech
    if ord(str[0])==0x2013:
        str="\\cdash--*\\," + str[1:]
    # ellipses
    str = string.replace(str,'...','\\ldots\\,')
    str = string.replace(str,u'\u2026','\\ldots\\,')
    # caret
    str = re.sub(r'[\^]',r'\\textasciicircum\\,',str)
    # tilde
    str = re.sub(r'[\~]',r'\\textasciitilde\\,',str)
    # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    str = string.replace(str,u'\u00ab','<<')
    # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    str = string.replace(str,u'\u00bb','>>') # replacing with french/russian equivalent
    # EN-DASH
    str = string.replace(str,u'\u2013','--')
    # EM-DASH
    str = re.sub(r'(\s)--(\s)','---',str)
    # preserve double quotes
    str = string.replace(str,'"','\\symbol{34}')
    # Fancy quotation marks (sometimes used to denote a quote
    # inside of another quote)
    str = string.replace(str,u'\u201e','``')
    str = string.replace(str,u'\u201c',"''")
    str = string.replace(str,u'\u201f','``')
    str = string.replace(str,u'\u201d',"''")
    # Broken bar
    str = string.replace(str,u'\u00A6','|')
    # plus-minus
    str = string.replace(str,u'\u00B1','$\\pm$')
    # russian number sign
    str = string.replace(str,u'\u2116','\\No\\,')
    # squiare brackets
    str = string.replace(str,'[','{[}')
    str = string.replace(str,']','{]}')
    # Unicode Character 'MIDDLE DOT' (U+00B7)
    str = string.replace(str,u'\u00B7','\\textperiodcentered\\,')
    # Greek Mu
    str = string.replace(str,u'\u00B5','$\\mu$')

        
    return str

def _text(t):
    res = ""
    for x in t.childNodes:
        if x.nodeType == Node.TEXT_NODE:
            res += x.data
        else:
            raise Exception("Expected TEXT, got " + x.tagName)

    return res

def _escapeSpace(t):
    return re.sub(r'([ ])+',r'\\ ', unicode(t))

def _pdfString(t):
    if t.nodeType == Node.ELEMENT_NODE:
        res = []
        for e in t.childNodes:
            res.append(_pdfString(e))
        return " ".join(res)
    elif t.nodeType == Node.TEXT_NODE:
        return t.data.strip()
        
    return u'' # empty section titles seem to be popular for some reason

def _tocElement(title, t):
    """
    Takes quoted string 'title' and node 't' and returns a string
    suitable for using in the section title or any other place which will
    get included in the TOC of the PDF document.
    """
    #res = u'\\texorpdfstring{%s}{%s}' % (_escapeSpace(title), _pdfString(t))
    res = _escapeSpace(title)
    return res

def _uwrite(f, ustr):
    f.write(ustr.encode('utf-8')) 

def _getdir(f):
    l = string.rsplit(f,"/",1)
    if len(l)==2:
        return l[0]
    else:
        return "."
    
def fb2tex(infile, outfile):
    logging.getLogger('fb2pdf').info("Converting %s" % infile)
    
    f = open(infile, 'r')
    soup = parse(f)
    f.close()

    f = open(outfile, 'w')

    outdir=_getdir(outfile)
    
    # laTeX-document header
    f.write("""\\documentclass[12pt,openany]{book}
    \\usepackage{textcomp} 
    \\usepackage[
        colorlinks=true,
        linkcolor=black,
        bookmarks=true,
        bookmarksnumbered=true,
        hypertexnames=false,
        plainpages=false,
        pdfpagelabels,
        unicode=true
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
    
    fb = soup.documentElement
    if fb.nodeType!=Node.ELEMENT_NODE or fb.tagName != "FictionBook":
        logging.getLogger('fb2pdf').exception("The file does not seems to contain 'fictionbook' root element")
        raise PersistentError("The file does not seems to contain 'fictionbook' root element")
    
    findEnclosures(fb,outdir)
    processDescription(find(fb,"description"), f)

    f.write("\\tableofcontents\n\\newpage\n\n");
    
    body=findAll(fb,"body")
    if not body or len(body)==0:
        logging.getLogger('fb2pdf').exception("The file does not seems to contain 'fictionbook/body' element")
        raise PersistentError("The file does not seems to contain 'fictionbook/body' element")
    for b in body:
        processEpigraphs(b, f)
        processSections(b, f)
    
    f.write("}")
    f.write("\n\\end{document}\n")
    f.close()

    logging.getLogger('fb2pdf').info("Conversion successfully finished")

def processSections(b,f):
    ss = findAll(b,"section")
    for s in ss:
        processSection(s, f)

def processPoem(p,f):
    
    # title (optinal)
    t = find(p,"title")
    if t:
        title = getSectionTitle(t)
        if title and len(title):
            _uwrite(f,"\\poemtitle{%s}\n" % _tocElement(title, t))
    
    f.write('\\begin{verse}\n\n')
    
    # epigraphs (multiple, optional)
    processEpigraphs(p, f)

    # stanza (at least one!) - { title?, subtitle?, v*}
    ss = findAll(p,"stanza")
    for s in ss:
        processStanza(s, f)

    processAuthors(p,f)
    
    # date
    d = find(p, "date")
    if d:
        pdate = _text(d)
        logging.getLogger('fb2pdf').warning("Unsupported element: date")
        #TODO find a nice way to print date
        
    f.write('\\end{verse}\n\n')

def processStanza(s, f):
    # title (optional)
    t = find(s,"title")
    if t:
        title = getSectionTitle(t)
        if title and len(title):
            # TODO: implement
            logging.getLogger('fb2pdf').warning("Unsupported element: stanza 'title'")
    
    # subtitle (optional)
    st = find(s,"subtitle")
    if st:
        subtitle = getSectionTitle(st)
        if subtitle and len(subtitle):
            # TODO: implement
            logging.getLogger('fb2pdf').warning("Unsupported element: stanza 'subtitle'")

    # 'v' - multiple    
    vv = findAll(s,"v")
    for v in vv:
        vt = par(v)
        if len(vt)==0:
            # TODO: use \vgap from verse package
            vt="\\vspace{12pt}\n"
            _uwrite(f,vt)
        else:
            _uwrite(f,vt)
            f.write("\\\\\n")


def processAuthors(q,f):
    aa = findAll(q,"text-author")
    author_name = ""
    for a in aa:
        if len(author_name):
            author_name += " \\and " + par(a)
        else:
            author_name = par(a)
            
    if author_name:
        f.write("\\author{")
        _uwrite(f,author_name)
        f.write("}\n");


def processCite(q,f):
    f.write('\\begin{quotation}\n')

    for x in q.childNodes:
        if x.nodeType == Node.ELEMENT_NODE:
            if x.tagName=="p":
                _uwrite(f,par(x))
                f.write("\n\n")
            elif x.tagName=="poem":
                processPoem(x,f)
            elif x.tagName=="empty-line":
                f.write("\\vspace{12pt}\n\n")
            elif x.tagName == "subtitle":
                _uwrite(f,"\\item\n\\subsection*{%s}\n" % _tocElement(par(x, False), x))
            elif x.tagName=="table":
                logging.getLogger('fb2pdf').warning("Unsupported element: %s" % x.tagName)
                pass # TODO
        elif x.nodeType == Node.TEXT_NODE:
            _uwrite(f,_textQuote(x.data))

    processAuthors(q,f)

    f.write('\\end{quotation}\n')
    
def processSection(s, f):
    pid=s.getAttribute('id')
    if pid:
        f.write('\\hypertarget{')
        _uwrite(f,pid)
        f.write('}{}\n')
    
    t = find(s,"title")
    if t:
        title = getSectionTitle(t)
    else:
        title = ""
    _uwrite(f,"\n\\section{%s}\n" % _tocElement(title, t))

    processEpigraphs(s, f)
    
    for x in s.childNodes:
        if x.nodeType == Node.ELEMENT_NODE:
            if x.tagName == "section":
                processSection(x,f)
            elif x.tagName == "p":
                pid=x.getAttribute('id')
                if pid:
                    f.write('\\hypertarget{')
                    _uwrite(f,pid)
                    f.write('}{}\n')
                _uwrite(f,par(x))
                f.write("\n\n")
            elif x.tagName == "empty-line":
                f.write("\\vspace{12pt}\n\n")
            elif x.tagName == "image":
                f.write(processInlineImage(x))
            elif x.tagName == "poem":
                processPoem(x,f)
            elif x.tagName == "subtitle":
                _uwrite(f,"\\subsection{%s}\n" % _tocElement(par(x, False), x))
            elif x.tagName == "cite":
                processCite(x,f)
            elif x.tagName == "table":
                logging.getLogger('fb2pdf').warning("Unsupported element: %s" % x.tagName)
                pass # TODO
            elif x.tagName=="title" or x.tagName=="epigraph":
                pass
            else:
                logging.getLogger('fb2pdf').error("Unknown section element: %s" % x.tagName)

def processAnnotation(f, an):
    if len(an.childNodes):
        f.write('\\section*{}\n')
        f.write('\\begin{small}\n')
        for x in an.childNodes:
            if x.nodeType == Node.ELEMENT_NODE:
                if x.tagName == "p":
                    _uwrite(f,par(x))
                    f.write("\n\n")
                elif x.tagName == "empty-line":
                    f.write("\n\n") # TODO: not sure
                elif x.tagName == "poem":
                    processPoem(x,f)
                elif x.tagName == "subtitle":
                    _uwrite(f,"\\subsection*{%s}\n" % _tocElement(par(x, False), x))
                elif x.tagName == "cite":
                    processCite(x,f)
                elif x.tagName == "table":
                    logging.getLogger('fb2pdf').warning("Unsupported element: %s" % x.tagName)
                    pass # TODO
                else:
                    logging.getLogger('fb2pdf').error("Unknown annotation element: %s" % x.tagName)
        f.write('\\end{small}\n')
        f.write('\\pagebreak\n\n')

def getSectionTitle(t):
    ''' Section title consists of "p" and "empty-line" elements sequence'''
    first = True
    res = u''
    for x in t.childNodes:
        if x.nodeType == Node.ELEMENT_NODE:
            if x.tagName == "p":
                if not first:
                    res = res + u"\\\\"
                else:
                    first = False
                res = res + par(x, False)
            elif x.tagName == "empty-line":
                res = res + u"\\vspace{10pt}"
            else:
                logging.getLogger('fb2pdf').error("Unknown section title element: %s" % x.tagName)
    return res

def processEpigraphText(f,e):
    first = True
    ''' Epigaph text consists of "p", "empty-line", "poem" and "cite" elements sequence'''
    for x in e.childNodes:
        if x.nodeType == Node.ELEMENT_NODE:
            if x.tagName == "p":
                if not first:
                    f.write("\\vspace{10pt}")
                else:
                    first = False
                _uwrite(f,par(x))
            elif x.tagName == "empty-line":
                f.write("\\vspace{10pt}")
            elif x.tagName == "poem":
                # TODO: test how verse plays with epigraph evn.
                processPoem(x,f)
            elif x.tagName == "cite":
                processCite(x,f)
            elif x.tagName != "text-author":
                logging.getLogger('fb2pdf').error("Unknown epigraph element: %s" % x.tagName)
        
def processEpigraphs(s,f):
    ep = findAll(s,"epigraph")
    if len(ep)==0:
        return
    f.write("\\begin{epigraphs}\n")
    for e in ep:
        f.write("\\qitem{")
        processEpigraphText(f, e)
        f.write("\\hspace*{\\fill}}%\n") #TODO \hspace is a workaround for #37

        eauthor=""
        ea=find(e,"text-author")
        if ea:
            eauthor=_text(ea)
        f.write("\t{")
        _uwrite(f,eauthor)
        f.write("}\n")
        
    f.write("\\end{epigraphs}\n")


def authorName(a):
    fn = find(a,"first-name")
    if fn:
        author_name = _text(fn)
    else:
        author_name = ""
    mn = find(a,"middle-name")
    if mn:
        if author_name:
            author_name = author_name + " " + _text(mn)
        else:
            author_name = _text(mn)
    ln = find(a,"last-name")
    if ln:
        if author_name:
            author_name = author_name + " " + _text(ln)
        else:
            author_name = _text(ln)
    return author_name

def processDescription(desc,f):
    if not desc:
        logging.getLogger('fb2pdf').warning("Missing required 'description' element\n")
        return
    
    # title info, mandatory element
    ti = find(desc,"title-info")
    if not ti:
        logging.getLogger('fb2pdf').warning("Missing required 'title-info' element\n")
        return 
    t = find(ti,"book-title")
    if t:
        title = _text(t)
    else:
        title = ""

    # authors
    aa = findAll(ti,"author")
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
        _uwrite(f,"\\title{%s}\n" % _tocElement(_textQuote(title), t))

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
    co = find(desc,"coverpage")
    if co:
        images = findAll(co,"image")
        if len(images):
            #f.write("\\begin{titlepage}\n")
            for image in images:
                f.write(processInlineImage(image))
            #f.write("\\end{titlepage}\n")

    # annotation, optional
    an = find(desc,"annotation")
    if an:
        processAnnotation(f,an)

def findEnclosures(fb,outdir):
    encs = findAll(fb,"binary")
    for e in encs:
        id=e.getAttribute('id')
        ct=e.getAttribute('content-type')
        global image_exts
        if not image_exts.has_key(ct):
            logging.getLogger('fb2pdf').warning("Unknown content-type '%s' for binary with id %s. Skipping\n" % (ct,id))
            continue
        fname = os.tempnam(".", "enc") + "." + image_exts[ct]
        fullfname = outdir + "/" + fname
        f = open(fullfname,"w")
        f.write(binascii.a2b_base64(e.childNodes[0].data))
        f.close()
        # convert to grayscale, 166dpi (native resolution for Sony Reader)
        Image.open(fullfname).convert("L").save(fullfname, dpi=(166,166))
        #TODO: scale down large images        
        global enclosures
        enclosures[id]=(ct, fname)
    
def processInlineImage(image):
        global enclosures
        href = image.getAttributeNS('http://www.w3.org/1999/xlink','href')
        if not href or href[0]!='#':
            logging.getLogger('fb2pdf').error("Invalid inline image ref '%s'\n" % href)
            return ""
        href=str(href[1:])
        if not enclosures.has_key(href):
            logging.getLogger('fb2pdf').error("Non-existing image ref '%s'\n" % href)
            return ""
        (ct,fname)=enclosures[href]
        return "\\begin{center}\n\\includegraphics{%s}\n\\end{center}\n" % fname

