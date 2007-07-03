#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter

Author: Vadim Zaliva <lord@crocodile.org>
'''

__author__ = "Vadim Zaliva"
__copyright__ = "Copyright (C) 2007 Vadim Zaliva"
__version__ = "3.14"

import logging
import os, os.path, sys
import string, re
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

url = 'http://www.codeminders.com/fb2pdf'


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

    # U+2018 LEFT SINGLE QUOTATION MARK
    (u'\u2018', "`"),
    # U+2019 RIGHT SINGLE QUOTATION MARK
    (u'\u2019', "'"),

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

    # Unicode Character 'INFINITY' (U+221E)
    ('*','$\\ast$'),
    
]


# --- globals --
enclosures = {}
notes = []

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

def _translify(s):
    for symb_in, symb_out in pytils.translit.TRANSTABLE:
        s = s.replace(symb_in, symb_out)
    return s

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
                            ltype = s.getAttribute('type')
                            if ltype == "note":
                                res += processFootnote(href,s,intitle)
                            else:
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
                logging.getLogger('fb2pdf').error("Unknown paragraph element: %s" % s.tagName)
        elif s.nodeType == Node.TEXT_NODE:
            res += _textQuote(s.data)
    return res            

def norec(ns,an,defret):
    def decorate(f):
        def new_f(*args, **kwds):
            a0=args[an]
            if a0 in ns:
                #print "recursion detected at '%s' in %s" % (a0, str(ns))
                return defret
            else:
                ns.append(a0)
                x = f(*args, **kwds)
                ns.remove(a0)
                return x
        return new_f
    return decorate

notes_stack=[]    
@norec(notes_stack, 0, "")
def processFootnote(href,s,intitle):
    doc  = s
    while doc.parentNode:
        doc = doc.parentNode

    #TODO: implement footnotes encoded as separate 'body' entities
    e = None
    ss = doc.getElementsByTagName("section")
    for i in ss:
        if i.getAttribute("id")==href[1:]:
            e = i
            break
    if e:
        notes.append(href[1:])
        return u'\\footnote{' + processSection(e, -1) + '}'
    else:
        return  u'\\hyperlink{' + href[1:] + '}{\\underline{' + par(s,intitle) + '}}'

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
    soup.normalize()

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
    _uwrite(f, processDescription(find(fb,"description")))

    f.write("\\tableofcontents\n\\newpage\n\n")
    
    body=findAll(fb,"body")
    if not body:
        logging.getLogger('fb2pdf').exception("The file does not seems to contain 'fictionbook/body' element")
        raise PersistentError("The file does not seems to contain 'fictionbook/body' element")
    for b in body:
        _uwrite(f, processBody(b))

    _uwrite(f,vanitySection())
    
    f.write("}")
    f.write("\n\\end{document}\n")
    f.close()

    logging.getLogger('fb2pdf').info("Conversion successfully finished")

def processBody(b):
    return processEpigraphs(b) + processSections(b, 0)
    
def processSections(b,level):
    return string.join([processSection(s, level) for s in findAll(b,"section") if s.getAttribute('id') not in notes],'')

def processPoem(p):
    res = u''
    # title (optinal)
    t = find(p,"title")
    if t:
        title = getSectionTitle(t)
        if title:
            res += "\\poemtitle{%s}\n" % _tocElement(title, t)
    
    res+='\\begin{verse}\n\n'
    
    # epigraphs (multiple, optional)
    res+=processEpigraphs(p)

    # stanza (at least one!) - { title?, subtitle?, v*}
    res+=string.join([processStanza(s) for s in findAll(p,"stanza")],'')

    res+=processAuthors(p)
    
    # date
    d = find(p, "date")
    if d:
        pdate = _text(d)
        logging.getLogger('fb2pdf').warning("Unsupported element: date")
        #TODO find a nice way to print date
        
    res+='\\end{verse}\n\n'
    return res

def processStanza(s):
    res=u''
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
            res+="\\vspace{12pt}\n"
        else:
            res+=vt + "\\\\\n"
    return res

def processAuthors(q):
    aa = findAll(q,"text-author")
    author_name = ""
    for a in aa:
        if author_name:
            author_name += " \\and " + par(a)
        else:
            author_name = par(a)
            
    if author_name:
        return u"\\author{%s}\n" % author_name
    else:
        return u''

def processCite(q):
    res=u'\\begin{quotation}\n'

    for x in q.childNodes:
        if x.nodeType == Node.ELEMENT_NODE:
            if x.tagName=="p":
                res+=par(x)+"\n\n"
            elif x.tagName=="poem":
                res+=processPoem(x)
            elif x.tagName=="empty-line":
                res+="\\vspace{12pt}\n\n"
            elif x.tagName == "subtitle":
                res+="\\item\n\\subsection*{%s}\n" % _tocElement(par(x, True), x)
            elif x.tagName=="table":
                logging.getLogger('fb2pdf').warning("Unsupported element: %s" % x.tagName)
                pass # TODO
        elif x.nodeType == Node.TEXT_NODE:
            res+=_textQuote(x.data)

    res+=processAuthors(q)
    res+='\\end{quotation}\n'
    return res

def vanitySection():
    res = u"\n\\appendix\n\\pagebreak\n\\section*{PDF Generation}\n"
    res += "Generated on \\textit{\\today} by {\\bf fb2pdf} version \\textit{%s}\n" % (__version__)
    res += '\n\n\\hyperlink{' + url + '}{\\underline{' + url + '}}'
    return res
    
def processSection(s, level):
    res = u''
    if level!=-1:
        pid=s.getAttribute('id')
        if pid:
            res+='\\hypertarget{%s}{}\n' % pid

        t = find(s,"title")
        if t:
            title = getSectionTitle(t)
        else:
            title = ""

        if level>=len(section_commands):
            cmd = "section"
        else:
            cmd = section_commands[level]

        res+="\n\\%s{%s}\n" % (cmd,_tocElement(title, t))
        res+=processEpigraphs(s)

    for x in s.childNodes:
        if x.nodeType == Node.ELEMENT_NODE:
            if x.tagName == "section":
                res+=processSection(x,level+1)
            elif x.tagName == "p":
                pid=x.getAttribute('id')
                if pid:
                    res+='\\hypertarget{%s}{}\n' % pid
                res+=par(x)
                res+="\n\n"
            elif x.tagName == "empty-line":
                res+="\\vspace{12pt}\n\n"
            elif x.tagName == "image":
                res+=processInlineImage(x)
            elif x.tagName == "poem":
                res+=processPoem(x)
            elif x.tagName == "subtitle":
                res+="\\subsection{%s}\n" % _tocElement(par(x, True), x)
            elif x.tagName == "cite":
                res+=processCite(x)
            elif x.tagName == "table":
                logging.getLogger('fb2pdf').warning("Unsupported element: %s" % x.tagName)
                pass # TODO
            elif x.tagName=="title" or x.tagName=="epigraph":
                pass
            else:
                logging.getLogger('fb2pdf').error("Unknown section element: %s" % x.tagName)
    return res

def processAnnotation(an):
    res =u''
    if len(an.childNodes):
        res+='\\section*{}\n'
        res+='\\begin{small}\n'
        for x in an.childNodes:
            if x.nodeType == Node.ELEMENT_NODE:
                if x.tagName == "p":
                    res+=par(x)
                    res+="\n\n"
                elif x.tagName == "empty-line":
                    res+="\n\n" # TODO: not sure
                elif x.tagName == "poem":
                    res+=processPoem(x)
                elif x.tagName == "subtitle":
                    res+="\\subsection*{%s}\n" % _tocElement(par(x, True), x)
                elif x.tagName == "cite":
                    res+=processCite(x)
                elif x.tagName == "table":
                    logging.getLogger('fb2pdf').warning("Unsupported element: %s" % x.tagName)
                    pass # TODO
                else:
                    logging.getLogger('fb2pdf').error("Unknown annotation element: %s" % x.tagName)
        res+='\\end{small}\n'
        res+='\\pagebreak\n\n'
    return res

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

def processEpigraphText(e):
    ''' Epigaph text consists of "p", "empty-line", "poem" and "cite" elements sequence'''
    res = u''
    first = True
    for x in e.childNodes:
        if x.nodeType == Node.ELEMENT_NODE:
            if x.tagName == "p":
                if not first:
                    res+="\\vspace{10pt}"
                else:
                    first = False
                res+=par(x)
            elif x.tagName == "empty-line":
                res+="\\vspace{10pt}"
            elif x.tagName == "poem":
                # TODO: test how verse plays with epigraph evn.
                res+=processPoem(x)
            elif x.tagName == "cite":
                res+=processCite(x)
            elif x.tagName != "text-author":
                logging.getLogger('fb2pdf').error("Unknown epigraph element: %s" % x.tagName)
    return res
        
def processEpigraphs(s):
    ep = findAll(s,"epigraph")
    if not ep:
        return ''
    res = u'\\begin{epigraphs}\n'
    for e in ep:
        res += "\\qitem{"
        res += processEpigraphText(e)
        res += "\\hspace*{\\fill}}%\n" #TODO \hspace is a workaround for #37

        eauthor=""
        ea = find(e,"text-author")
        if ea:
            eauthor=par(ea)
        res += "\t{%s}\n" % eauthor
        
    res+="\\end{epigraphs}\n"
    return res


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

def processDescription(desc):
    if not desc:
        logging.getLogger('fb2pdf').warning("Missing required 'description' element")
        return ''
    # title info, mandatory element
    ti = find(desc,"title-info")
    if not ti:
        logging.getLogger('fb2pdf').warning("Missing required 'title-info' element")
        return ''
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

    res=u''

    # Generate PDF metadata. Must come before \maketitle,
    # because hyperref generates additional metadata there,
    # but Sony Reader seems to only look for the first
    # instance of these attributes.
    if author_name or title:
        res+="\n\\pdfinfo {\n"

        if author_name:
            res+="\t/Author ("
            pdf_author_name = ", ".join(author_name.split(" \\and "))
            res+=pytils.translit.translify(pdf_author_name)
            res+=")\n"

        if title:
            res+="\t/Title ("
            res+=_translify(title)
            res+=")\n"

        res+="}\n"

    if author_name:
        res+="\\author{"
        res+=author_name
        res+="}\n"

    if title:
        res+="\\title{%s}\n" % _tocElement(_textQuote(title), t)

    res+="\\date{}"

    if author_name or title:
        res+="\\maketitle\n"

    # cover, optional
    co = find(desc,"coverpage")
    if co:
        images = findAll(co,"image")
        if images:
            #f.write("\\begin{titlepage}\n")
            for image in images:
                res+=processInlineImage(image)
            #f.write("\\end{titlepage}\n")

    # annotation, optional
    an = find(desc,"annotation")
    if an:
        res+=processAnnotation(an)
    return res

def findEnclosures(fb, outdir, outname):
    encs = findAll(fb,"binary")
    counter = 0
    for e in encs:
        id=e.getAttribute('id')
        ct=e.getAttribute('content-type')
        global image_exts
        if not image_exts.has_key(ct):
            logging.getLogger('fb2pdf').warning("Unknown content-type '%s' for binary with id %s. Skipping" % (ct,id))
            continue
        fname = "enc-%s-%d.%s" % (outname, counter, image_exts[ct])
        counter = counter+1
        fullfname = os.path.join(outdir, fname)
        f = open(fullfname,"wb")
        f.write(binascii.a2b_base64(e.childNodes[0].data))
        f.close()
        try:
            # convert to grayscale, 166dpi (native resolution for Sony Reader)
            Image.open(fullfname).convert("L").save(fullfname, dpi=(166,166))
            #TODO: scale down large images        
            global enclosures
            enclosures[id]=(ct, fname)
        except:
            logging.getLogger('fb2pdf').warning("Error converting enclosure '%s'. Replacing with broken image icon" % id)
            global enclosures
            enclosures[id]=(ct, sys.prefix + '/share/fb2pdf/broken-image.png')
    
def processInlineImage(image):
        global enclosures
        href = image.getAttributeNS('http://www.w3.org/1999/xlink','href')
        if not href or href[0]!='#':
            logging.getLogger('fb2pdf').error("Invalid inline image ref '%s'" % href)
            return ""
        href=str(href[1:])
        if not enclosures.has_key(href):
            logging.getLogger('fb2pdf').error("Non-existing image ref '%s'" % href)
            return ""
        (ct,fname)=enclosures[href]
        return "\\begin{center}\n\\includegraphics{%s}\n\\end{center}\n" % fname

