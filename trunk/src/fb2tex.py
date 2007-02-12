#!/usr/bin/env python

'''
FictionBook2 -> TeX converter

Author: Vadim Zaliva <lord@crocodile.org>
'''

import getopt, sys, string, re

from BeautifulSoup import BeautifulStoneSoup, Tag

def p(x):
    if len(x.contents) and isinstance(x.contents[0], Tag):
        return style(x.contents[0])
    else:
        return _textQuote(_text(x))

def style(s):
    if s.name == "strong":
        return u'{\\bf '+ _textQuote(_text(s)) + u'}'
    elif s.name == "emphasis":
        return u'{\\it '+ _textQuote(_text(s)) + u'}'
    elif s.name == "style":
        pass #TODO
    elif s.name == "a":
        pass #TODO
    elif s.name == "strikethrough":
        return u'\\sout{' + _textQuote(_text(s)) + u'}'
    elif s.name == "sub":
        pass #TODO
    elif s.name == "sup":
        pass #TODO
    elif s.name == "code":
        return u'\n\\begin{verbatim}\n' + _textQuote(_text(s),code=True) + u'\n\\end{verbatim}\n'
    elif s.name == "image":
        pass #TODO

def _textQuote(str, code=False):
    ''' Basic paragraph TeX quoting '''
    if len(str)==0:
        return str
    if not code:
        # 'EN DASH' at the beginning of paragrapg - russian direct speach
        if ord(str[0])==8211:
            str="\\cdash--*" + str[1:]
        # ellipses
        str = string.replace(str,'...','\\ldots')
        # em-dash
        str = re.sub(r'(\s)--(\s)','---',str)

    return str

def _text(t):
    return string.join(t.contents)

def _uwrite(f, ustr):
    f.write(ustr.encode('utf-8')) 

def fb2tex(infile, outfile):
    f = open(infile, 'r')
    soup = BeautifulStoneSoup(f,selfClosingTags=['empty-line'])
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
    f.write("\\usepackage[papersize={9cm,12cm}, margin=4mm, ignoreall, pdftex]{geometry}\n")
    f.write("\\setcounter{secnumdepth}{-2}\n"); # supress section numbering
    f.write("\n\\begin{document}\n\n")

    fb = soup.find("fictionbook")
    processTitleAndAuthor(fb,f)
    processSections(fb.find("body"), f)
    
    f.write("\\tableofcontents\n"); #TODO: move to beginning, make hyperlined index.
    f.write("\n\\end{document}\n")
    f.close()

def processSections(b,f):
    ss = b.findAll("section", recursive=False)
    for s in ss:
        processSection(s, f)

def processSection(s, f):
    t = s.find("title", recursive=False)
    if t:
        title = getSectionTitle(t)
    else:
        t = ""

    f.write("\\section{")
    _uwrite(f,title) # TODO quote
    f.write("}\n");

    processEpigraphs(f,s)
    
    for x in s.contents:
        if isinstance(x, Tag):
            if x.name == "section":
                processSection(x,f)
            if x.name == "p":
                _uwrite(f,p(x))
                f.write("\n\n")
            elif x.name == "empty-line":
                f.write("\n\n") # TODO: not sure


def getSectionTitle(t):
    ''' Section title consists of "p" and "empty-line" elements sequence'''
    first = True
    res = u''
    for x in t:
        if isinstance(x, Tag):
            if x.name == "p":
                if not first:
                    res = res + u"\\linebreak"
                else:
                    first = False
                res = res + p(x)
            elif x.name == "empty-line":
                if not first:
                    res = res + u"\\linebreak"
    return res

def processEpigraphText(f,e):
    first = True
    ''' Epigaph text consists of "p", "empty-line", "poem" and "cite" elements sequence'''
    for x in e.contents:
        if isinstance(x, Tag):
            if x.name == "p":
                if not first:
                    f.write("\\linebreak")
                else:
                    first = False
                _uwrite(f,p(x))
            elif x.name == "empty-line":
                if not first:
                    f.write("\\linebreak")
            elif x.name == "poem":
                pass #TODO
            elif x.name == "cite":
                pass #TODO
        
def processEpigraphs(f,s):
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
        

def processTitleAndAuthor(fb,f):

    #TODO: body/title
    desc = fb.find("description")
    if not desc:
        return
    ti = fb.find("title-info")
    if not ti:
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

    if author_name or title:
        f.write("\\maketitle\n");

    # TODO: PDF info generation temporaty disabled. It seems that
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

    fb2tex(infile, outfile)

if __name__ == "__main__":
    main()
