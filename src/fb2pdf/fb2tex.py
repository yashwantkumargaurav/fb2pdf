#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter

Author: Vadim Zaliva <lord@crocodile.org>
'''

import logging
import os
import os.path
import sys
import string
import re
import binascii
from xml.dom.minidom import parse, Node
import pytils.translit

import Image

from exceptions import TemporaryError, PersistentError

parameters = {
    # inputenc option for TeX - should be consistent with output codec
    'inputenc': 'utf-8',

    # codec to use for output - should be consistent with inputenc
    'outcodec': 'utf-8'
}


# -- constants --
image_exts = {'image/jpeg':'jpg', 'image/png':'png'}

section_commands = ['part', 'chapter', 'section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph']


# Following tuples will be examined one by one and applied to the text.
# If head is string (ASCII or unicode) all instances of it would be replaced
# by 2nd element of the tuple.
# If head is compiled regexp, it will be used to substitute all it's instanced
# by 2nd element of the tuple using its .sub() method.
TEXT_PATTERNS = [

    # backslash itself must be represented as \backslash
    # (should go first to avoid escaping backslash in TeX commands
    # produced further down this function)
    ('\\','$\\backslash$'),

    # special chars need to be quoted with backslash
    # (should go after escaping backslash but before any of the
    # other conversions that produce TeX commands that include {})
    (re.compile(r'([\&\$\%\#\_\{\}])'),r'\\\1'),

    # TODO: Fix the following quick ugly hack
    # this is here, because the line above breaks $\backslash$
    # that comes before that, which would break stuff on the above
    # line if it followed it
    (re.compile(r'\\\$\\backslash\\\$'),r'$\\backslash$'),

    # Unicode Character 'EM DASH' (U+2014)
    # used in some documents instead of '-'
    (u'\u2014','---'),

    # 'EN DASH' at the beginning of paragraph - russian direct speech
    (re.compile(r'^\u2013(.*)'), r'\\cdash--*{}\\\1'),

    # ellipses
    ('...', '\\ldots{}'),
    (u'\u2026', '\\ldots{}'),

    # caret
    (re.compile(r'[\^]'), r'\\textasciicircum{}'),

    # tilde
    (re.compile(r'[\~]'), r'\\textasciitilde{}'),

    # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    (u'\u00ab', '<<'),

    # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    # replacing with french/russian equivalent
    (u'\u00bb', '>>'),

    # EN-DASH
    (u'\u2013', '--'),

    # EM-DASH
    (re.compile(r'(\s)--(\s)'), '---'),

    # preserve double quotes
    ('"', '\\symbol{34}'),

    # Fancy quotation marks (sometimes used to denote a quote
    # inside of another quote)
    (u'\u201e', '``'),
    (u'\u201c', "''"),
    (u'\u201f', '``'),
    (u'\u201d', "''"),

    # Broken bar
    (u'\u00A6', '|'),

    # plus-minus
    (u'\u00B1', '$\\pm$'),

    # russian number sign
    (u'\u2116', '\\No{}'),

    # squiare brackets
    ('[', '{[}'),
    (']', '{]}'),

    # Unicode Character 'MIDDLE DOT' (U+00B7)
    (u'\u00B7', '\\textperiodcentered{}'),
    
    # Greek Mu
    (u'\u00B5', '$\\mu$'),

    # Unicode Character 'COMBINING ACUTE ACCENT' (U+0301)
    (re.compile(u'(.)\u0301'), u'\\\'{\\1}'),

    #Unicode Character 'SUPERSCRIPT TWO' (U+00B2)
    (u'\u00B2', '$^2$'),

    #Unicode Character 'SUPERSCRIPT THREE' (U+00B3)    
    (u'\u00B3', '$^3$'),

    # Unicode Character 'INFINITY' (U+221E)
    (u'\u221e','$\\infty$'),
    
]


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
    if not nl:
        return None
    else:
        return nl[0]

def par(p, intitle=False):
    res = u''
    for s in p.childNodes:
        if s.nodeType == Node.ELEMENT_NODE:
            if s.tagName == "strong":
                res += u'{\\bf '+ par(s,intitle) + u'}'
            elif s.tagName == "emphasis":
                res += u'{\\it '+ par(s,intitle) + u'}'
            elif s.tagName == "style":
                logging.getLogger('fb2pdf').warning("Unsupported element: %s" % s.tagName)
                res += "" #TODO
            elif s.tagName == "a":
                if not intitle:
                    href = s.getAttributeNS('http://www.w3.org/1999/xlink','href') or s.getAttribute('href') 
                    if href:
                        if href[0]=='#':
                            res += '\\hyperlink{' + href[1:] + '}{\\underline{' + par(s,intitle) + '}}'
                        else:
                            res += '\\href{' + href + '}{\\underline{' + par(s,intitle) + '}}'
                    else:
                        logging.getLogger('fb2pdf').warning("'a' without 'href'")
                else:
                    res += par(s,intitle)
                res += "" #TODO
            elif s.tagName == "strikethrough":
                res += u'\\sout{' + par(s,intitle) + u'}'
            elif s.tagName == "sub":
                res += u'$_{\\textrm{' + par(s,intitle) + '}}$'
            elif s.tagName == "sup":
                res += u'$^{\\textrm{' + par(s,intitle) + '}}$'
            elif s.tagName == "code":
                res += u'{\\sc' + par(s,intitle) + u'}'
            elif s.tagName == "image":
                if not intitle:
                    res += processInlineImage(s)
                else:
                    # TODO: nicer workaround for issue #44
                    res += "[...]"
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
    if str:
        for (a,b) in TEXT_PATTERNS:
            if isinstance(a,unicode) or isinstance(a,basestring):
                str = string.replace(str,a,b)
            else:
                str = a.sub(b,str)
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
    f.write(ustr.encode(parameters['outcodec'])) 

def _getdir(f):
    (dirname, filename) = os.path.split(f)
    (filebase, fileext) = os.path.splitext(filename)
    if len(dirname) == 0:
        dirname = "."
    return (dirname, filebase)
    
def fb2tex(infile, outfile):
    logging.getLogger('fb2pdf').info("Converting %s" % infile)
    
    f = open(infile, 'r')
    soup = parse(f)
    f.close()

    f = open(outfile, 'w')

    (outdir, outname) = _getdir(outfile)
    
    # laTeX-document header
    f.write("""\\documentclass[12pt,openany]{book}
    \\usepackage{verse}
    \\usepackage{textcomp} 
    \\usepackage[
        colorlinks=true,
        linkcolor=black,
        bookmarks=false,
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
    \\usepackage[%(inputenc)s]{inputenc}
    \\usepackage[russian]{babel}
    \\usepackage{sectsty}
    \\setcounter{secnumdepth}{-2}
    """ % parameters )
    
    #TODO: Instead of selecting font family inside of the document 
    # section, set the defaults for the entire document
    #\renewcommand{\rmdefault}{xxx}
    #\renewcommand{\sfdefault}{xxx}
    #\renewcommand{\ttdefault}{xxx}
    
    f.write("\n\\begin{document}\n\n")
    f.write("\\tolerance=10000\n")
    f.write("\\partfont{\\Large\\raggedright}\n")
    f.write("\\chapterfont{\\large\\raggedright}\n")
    f.write("\\sectionfont{\\raggedright}\n")
    f.write("\\subsectionfont{\\raggedright}\n")
    f.write("\\subsubsectionfont{\\raggedright}\n")
    
    f.write("{\\fontfamily{cmss}\\selectfont\n")

    
    
    fb = soup.documentElement
    if fb.nodeType!=Node.ELEMENT_NODE or fb.tagName != "FictionBook":
        logging.getLogger('fb2pdf').exception("The file does not seems to contain 'fictionbook' root element")
        raise PersistentError("The file does not seems to contain 'fictionbook' root element")
    
    findEnclosures(fb, outdir, outname)
    processDescription(find(fb,"description"), f)

    f.write("\\tableofcontents\n\\newpage\n\n");
    
    body=findAll(fb,"body")
    if not body:
        logging.getLogger('fb2pdf').exception("The file does not seems to contain 'fictionbook/body' element")
        raise PersistentError("The file does not seems to contain 'fictionbook/body' element")
    for b in body:
        processEpigraphs(b, f)
        processSections(b, f, 0)
    
    f.write("}")
    f.write("\n\\end{document}\n")
    f.close()

    logging.getLogger('fb2pdf').info("Conversion successfully finished")

def processSections(b,f,level):
    ss = findAll(b,"section")
    for s in ss:
        processSection(s, f, level)

def processPoem(p,f):
    
    # title (optinal)
    t = find(p,"title")
    if t:
        title = getSectionTitle(t)
        if title:
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
        if title:
            # TODO: implement
            logging.getLogger('fb2pdf').warning("Unsupported element: stanza 'title'")
    
    # subtitle (optional)
    st = find(s,"subtitle")
    if st:
        subtitle = getSectionTitle(st)
        if subtitle:
            # TODO: implement
            logging.getLogger('fb2pdf').warning("Unsupported element: stanza 'subtitle'")

    # 'v' - multiple    
    vv = findAll(s,"v")
    for v in vv:
        vt = par(v)
        if not vt:
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
        if author_name:
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
                _uwrite(f,"\\item\n\\subsection*{%s}\n" % _tocElement(par(x, True), x))
            elif x.tagName=="table":
                logging.getLogger('fb2pdf').warning("Unsupported element: %s" % x.tagName)
                pass # TODO
        elif x.nodeType == Node.TEXT_NODE:
            _uwrite(f,_textQuote(x.data))

    processAuthors(q,f)

    f.write('\\end{quotation}\n')
    
def processSection(s, f, level):
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

    if level>=len(section_commands):
        cmd = "section"
    else:
        cmd = section_commands[level]

    _uwrite(f,"\n\\%s{%s}\n" % (cmd,_tocElement(title, t)))

    processEpigraphs(s, f)
    
    for x in s.childNodes:
        if x.nodeType == Node.ELEMENT_NODE:
            if x.tagName == "section":
                processSection(x,f,level+1)
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
                _uwrite(f,"\\subsection{%s}\n" % _tocElement(par(x, True), x))
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
                    _uwrite(f,"\\subsection*{%s}\n" % _tocElement(par(x, True), x))
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
                res = res + par(x, True)
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
    if not ep:
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
        _uwrite(f,_textQuote(eauthor))
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
        if author_name:
            author_name += " \\and " + authorName(a)
        else:
            author_name = authorName(a)

    # Generate PDF metadata. Must come before \maketitle,
    # because hyperref generates additional metadata there,
    # but Sony Reader seems to only look for the first
    # instance of these attributes.
    if author_name or title:
        f.write("\n\\pdfinfo {\n")

        if author_name:
            f.write("\t/Author (")
            pdf_author_name = ", ".join(author_name.split(" \\and "))
            _uwrite(f,pytils.translit.translify(pdf_author_name))
            f.write(")\n")

        if title:
            f.write("\t/Title (")
            _uwrite(f,pytils.translit.translify(title))
            f.write(")\n")

        f.write("}\n")

    if author_name:
        f.write("\\author{")
        _uwrite(f,author_name)
        f.write("}\n");

    if title:
        _uwrite(f,"\\title{%s}\n" % _tocElement(_textQuote(title), t))

    f.write("\\date{}")

    if author_name or title:
        f.write("\\maketitle\n");

    # cover, optional
    co = find(desc,"coverpage")
    if co:
        images = findAll(co,"image")
        if images:
            #f.write("\\begin{titlepage}\n")
            for image in images:
                f.write(processInlineImage(image))
            #f.write("\\end{titlepage}\n")

    # annotation, optional
    an = find(desc,"annotation")
    if an:
        processAnnotation(f,an)

def findEnclosures(fb, outdir, outname):
    encs = findAll(fb,"binary")
    counter = 0
    for e in encs:
        id=e.getAttribute('id')
        ct=e.getAttribute('content-type')
        global image_exts
        if not image_exts.has_key(ct):
            logging.getLogger('fb2pdf').warning("Unknown content-type '%s' for binary with id %s. Skipping\n" % (ct,id))
            continue
        fname = "enc-%s-%d.%s" % (outname, counter, image_exts[ct])
        counter = counter+1
        fullfname = os.path.join(outdir, fname)
        f = open(fullfname,"wb")
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

