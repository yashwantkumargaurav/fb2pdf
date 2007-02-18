#!/usr/bin/env python

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

# -- constants --
image_exts = {'image/jpeg':'jpg', 'image/png':'png'}

# --- globals --
enclosures = {}
logfile = 'fb2tex.log'
verbosity = logging.ERROR
log_verbosity = logging.DEBUG

def par(p):
    res = u''
    for s in p:
        if isinstance(s, Tag):
            if s.name == "strong":
                res += u'{\\bf '+ par(s) + u'}'
            elif s.name == "emphasis":
                res += u'{\\it '+ par(s) + u'}'
            elif s.name == "style":
                logging.warning("Unsupported element: %s" % s.name)
                res += "" #TODO
            elif s.name == "a":
                logging.warning("Unsupported element: %s" % s.name)
                res += "" #TODO
            elif s.name == "strikethrough":
                res += u'\\sout{' + par(s) + u'}'
            elif s.name == "sub":
                logging.warning("Unsupported element: %s" % s.name)
                res += "" #TODO
            elif s.name == "sup":
                logging.warning("Unsupported element: %s" % s.name)
                res += "" #TODO
            elif s.name == "code":
                res += u'\n\\begin{verbatim}\n' + _textQuote(_text(s),code=True) + u'\n\\end{verbatim}\n'
            elif s.name == "image":
                logging.warning("Unsupported element: %s" % s.name)
                res += "" #TODO
            elif s.name == "l":
                logging.warning("Unsupported element: %s" % s.name)
                res += "" #TODO
            else:
                logging.error("Unknown paragrpah element: %s" % s.name)
        elif isinstance(s, basestring) or isinstance(s, unicode):
            res += _textQuote(_text(s))
    return res            

def _textQuote(str, code=False):
    ''' Basic paragraph TeX quoting '''
    if len(str)==0:
        return str
    if not code:
        # 'EN DASH' at the beginning of paragraph - russian direct speech
        if ord(str[0])==0x2013:
            str="\\cdash--*" + str[1:]
        # ellipses
        str = string.replace(str,'...','\\ldots')
        # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
        str = string.replace(str,u'\u00ab','<<')
        # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
        str = string.replace(str,u'\u00bb','>>') # replacing with frech/russian equvalent
        # EM-DASH
        str = re.sub(r'(\s)--(\s)','---',str)
        # preserve double quotes
        str = string.replace(str,'"','\\symbol{34}')

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
            logging.error("Unexpected element in _text: '%s'" % x)
    return string.join([convXMLentities(e) for e in  t.contents])

def _uwrite(f, ustr):
    f.write(ustr.encode('utf-8')) 

def fb2tex(infile, outfile):
    f = open(infile, 'r')
    soup = BeautifulStoneSoup(f,selfClosingTags=['empty-line',"image"],convertEntities=[BeautifulStoneSoup.XML_ENTITIES])
    f.close()

    f = open(outfile, 'w')
    f.write("\\documentclass[11pt]{book}\n")
    f.write("\\usepackage{graphicx}\n")
    f.write("\\usepackage{url}\n")
    f.write("\\usepackage{epigraph}\n")
    f.write("\\usepackage{verbatim}\n")
    f.write("\\usepackage{ulem}\n")
    f.write("\\usepackage[utf-8]{inputenc}\n")
    f.write("\\usepackage[russian]{babel}\n")
    # Temporary disabled, since it is causing 'pdfopt' crashes
    #f.write("\\usepackage{hyperref}\n")
    f.write("\\usepackage[papersize={9cm,12cm}, margin=4mm, ignoreall, pdftex]{geometry}\n")
    f.write("\\setcounter{secnumdepth}{-2}\n"); # suppress section numbering

    f.write("\n\\begin{document}\n\n")

    fb = soup.find("fictionbook")
    findEnclosures(fb)
    processDescription(fb.find("description"), f)

    f.write("\\tableofcontents\n");
    
    body=fb.find("body")
    processEpigraphs(body, f)
    processSections(body, f)
    
    f.write("\n\\end{document}\n")
    f.close()

def processSections(b,f):
    ss = b.findAll("section", recursive=False)
    for s in ss:
        processSection(s, f)

def processPoem(p,f):
    f.write('\\begin{verse}\n')
    
    # title (optinal)
    t = p.find("title", recursive=False)
    if t:
        title = getSectionTitle(t)
        if title and len(title):
            f.write("\\poemtitle{")
            _uwrite(f,title)
            f.write("}\n")

    
    # epigraphs (multiple, optional)
    processEpigraphs(p, f)

    # stanza (at least one!) - { title?, subtitle?, v*}
    ss = p.findAll("stanza", recursive=False)
    for s in ss:
        processStanza(s, f)
    
    # text-author (optional)
    # TODO: check, see if there is a better way to list multiple authors
    #    perhaps comma, separated.
    aa = p.findAll("text-author", recursive=False)
    for a in aa:
        author = par(a)
        f.write('\\attrib{')
        _uwrite(f,author)
        f.write("}\n")

    # date
    d = p.find("date", recursive=False)
    if d:
        pdate = _text(d)
        logging.warning("Unsupported element: date")
        #TODO find a nice way to print date
        
    f.write('\\end{verse}\n')

def processStanza(s, f):
    # title (optional)
    t = s.find("title", recursive=False)
    if t:
        title = getSectionTitle(t)
        if title and len(title):
            # TODO: implement
            logging.warning("Unsupported element: stanza 'title'")
    
    # subtitle (optional)
    st = s.find("subtitle", recursive=False)
    if st:
        subtitle = getSectionTitle(st)
        if subtitle and len(subtitle):
            # TODO: implement
            logging.warning("Unsupported element: stanza 'subtitle'")

    # 'v' - multiple    
    vv = s.findAll("v", recursive=False)
    for v in vv:
        vt = par(v)
        _uwrite(f,vt)
        f.write(" \\\\\n")
    
def processSection(s, f):
    t = s.find("title", recursive=False)
    if t:
        title = getSectionTitle(t)
    else:
        title = ""

    f.write("\\section{")
    _uwrite(f,title) # TODO quote
    f.write("}\n");

    processEpigraphs(s, f)
    
    for x in s.contents:
        if isinstance(x, Tag):
            if x.name == "section":
                processSection(x,f)
            if x.name == "p":
                _uwrite(f,par(x))
                f.write("\n\n")
            elif x.name == "empty-line":
                f.write("\n\n") # TODO: not sure
            elif x.name == "image":
                logging.warning("Unsupported element: %s" % x.name)
                pass # TODO
            elif x.name == "poem":
                processPoem(x,f)
            elif x.name == "subtitle":
                f.write("\\subsection{")
                _uwrite(f,par(x))
                f.write("}\n")
            elif x.name == "cite":
                logging.warning("Unsupported element: %s" % x.name)
                pass # TODO
            elif x.name == "table":
                logging.warning("Unsupported element: %s" % x.name)
                pass # TODO
            elif x.name!="title" and x.name!="epigraph":
                logging.error("Unknown section element: %s" % x.name)

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
                    f.write("\\subsection*{")
                    _uwrite(f,par(x))
                    f.write("}\n")
                elif x.name == "cite":
                    logging.warning("Unsupported element: %s" % x.name)
                    pass # TODO
                elif x.name == "table":
                    logging.warning("Unsupported element: %s" % x.name)
                    pass # TODO
                else:
                    logging.error("Unknown annotation element: %s" % x.name)
        f.write('\\end{small}\n')
        f.write('\\pagebreak\n')

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
                logging.error("Unknown section title element: %s" % x.name)
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
                logging.warning("Unsupported element: %s" % x.name)
                pass #TODO
            elif x.name != "text-author":
                logging.error("Unknown epigraph element: %s" % x.name)
        
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

def processDescription(desc,f):
    if not desc:
        logging.warning("Missing required 'description' element\n")
        return
    
    # title info, mandatory element
    ti = desc.find("title-info")
    if not ti:
        logging.warning("Missing required 'title-info' element\n")
        return 
    t = ti.find("book-title")
    if t:
        title = _text(t)
    else:
        title = ""
    a = ti.find("author")
    if not a:
        author_name = ""
    else:
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
                
    if author_name:
        f.write("\\author{")
        _uwrite(f,author_name)
        f.write("}\n");

    if title:
        f.write("\\title{")
        _uwrite(f, title)
        f.write("}\n")

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
                processInlineImage(f,image)
            #f.write("\\end{titlepage}\n")

    # annotation, optional
    an = desc.find("annotation")
    if an:
        processAnnotation(f,an)

def findEnclosures(fb):
    encs = fb.findAll("binary", recursive=False)
    for e in encs:
        id=e['id']
        ct=e['content-type']
        global image_exts
        if not image_exts.has_key(ct):
            logging.warning("Unknown content-type '%s' for binary with id %s. Skipping\n" % (ct,id))
            continue
        fname = os.tempnam('.', "enc") + "." + image_exts[ct]
        f=open(fname,"w")
        f.write(binascii.a2b_base64(e.contents[0]))
        f.close()
        global enclosures
        enclosures[id]=(ct, fname)
    
def processInlineImage(f,image):
        global enclosures
        href = image['l:href']
        if not href or href[0]!='#':
            logging.error("Invalid inline image ref '%s'\n" % href)
            return
        href=str(href[1:])
        if not enclosures.has_key(href):
            logging.error("Non-existing image ref '%s'\n" % href)
            return 
        (ct,fname)=enclosures[href]
        f.write("\\includegraphics{%s}\n" % fname)

def usage():
    sys.stderr.write("Usage: fb2tex.py [-v] -f fb2file -o texfile\n")

def parseCommandLine():
    global logfile
    global verbosity
    global log_verbosity
    infile = None
    outfile = None
    
    (optlist, arglist) = getopt.getopt(sys.argv[1:], "vf:o:", ["verbose", "file=", "output="])
    for option, argument in optlist:
        if option in ("-v", "--verbose"):
            verbosity = logging.DEBUG
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
        
    logging.basicConfig(
        level = log_verbosity,
        format = '%(asctime)s %(levelname)-8s %(message)s',
        datefmt = '%a, %d %b %Y %H:%M:%S',
        filename = logfile,
        filemode = 'w'
    )
    
    console = logging.StreamHandler()
    console.setLevel(verbosity)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
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
