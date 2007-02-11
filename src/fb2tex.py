#!/usr/bin/env python

'''
FictionBook2 -> TeX converter

Author: Vadim Zaliva <lord@crocodile.org>
'''

import getopt, sys, string

from BeautifulSoup import BeautifulStoneSoup, Tag

def processStyle(f, s):
    if s.name == "strong":
        pass
    elif s.name == "emphasis":
        f.write("\\emph{")
        _uwrite(f,_pQuote(_text(s)))
        f.write("}")
    elif s.name == "style":
        pass #TODO
    elif s.name == "a":
        pass #TODO
    elif s.name == "strikethrough":
        f.write("\\sout{")
        _uwrite(f,_pQuote(_text(s)))
        f.write("}")
    elif s.name == "sub":
        pass #TODO
    elif s.name == "sup":
        pass #TODO
    elif s.name == "code":
        f.write("\n\\begin{verbatim}\n")
        _uwrite(f,_pQuote(_text(s)))
        f.write("\n\\end{verbatim}\n")
    elif s.name == "image":
        pass #TODO

def _pQuote(str):
    ''' Basic paragraph TeX quoting '''
    if len(str)==0:
        return str
    # 'EN DASH' at the beginning of paragrapg - russian direct speach
    if ord(str[0])==8211:
        str="\\cdash--*" + str[1:]
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
    title = ""
    if t:
        for tx in t:
            if isinstance(tx, Tag):
                if tx.name == "p":
                    if len(title):
                        title = title + "\\\\" + _text(tx)
                    else:
                        title = _text(tx)
                elif tx.name == "empty-line":
                    if len(title):
                        title = title + "\\\\"

    # TODO: epigraphs
    f.write("\\section{")
    _uwrite(f,title) # TODO quote
    f.write("}\n");
                        
    for x in s.contents:
        if isinstance(x, Tag):
            if x.name == "section":
                processSection(x,f)
            if x.name == "p":
                if len(x.contents) and isinstance(x.contents[0], Tag):
                    processStyle(f, x.contents[0])
                else:
                    _uwrite(f,_pQuote(_text(x)))
                f.write("\n\n")
            elif x.name == "empty-line":
                f.write("\n\n") # TODO: not sure

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
