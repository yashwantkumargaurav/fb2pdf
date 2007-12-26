#!/usr/bin/env python

'''
FB2 Merge utility. Merges two or more FB2 files

Author: Vadim Zaliva <lord@crocodile.org>
'''

__author__ = "Vadim Zaliva"
__copyright__ = "Copyright (C) 2007 Vadim Zaliva"
__version__ = "0.1"

import os, os.path, sys, traceback
import string, re
import binascii
from xml.dom.minidom import parse, Node
import getopt
from sets import Set

verbose = False

def _text(t):
    res = ""
    for x in t.childNodes:
        if x.nodeType == Node.TEXT_NODE:
            res += x.data
        else:
            raise Exception("Expected TEXT, got " + x.tagName)
    return res

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

def getTitleInfo(doc):
    fb = doc.documentElement
    desc = find(fb,"description")
    # desc is mandatory
    ti = find(desc,"title-info")
    # title-info is mandatroy
    return ti

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

def getAuthors(doc):
    ti = getTitleInfo(doc)
    aa = findAll(ti,"author")
    authors = map(authorName,aa)
    return authors


def prefixId(e,i):
    for x in e.childNodes:
        if x.nodeType == Node.ELEMENT_NODE:
            id=x.getAttribute('id')
            if id:
                x.setAttribute('id',i+':'+id)
            href = x.getAttributeNS('http://www.w3.org/1999/xlink','href')
            if href and href[0]=='#':
                x.setAttributeNS('http://www.w3.org/1999/xlink','href','#'+i+':'+href[1:])
            href=x.getAttribute('href')
            if href and href[0]=='#':
                x.setAttribute('href','#'+i+':'+href[1:])
            prefixId(x,i)

def fbmerge(infiles, outfile, author, title):
    src=[]
    for fn in infiles:
        if verbose:
            sys.stderr.write("Loading %s\n" % fn)
        f = open(fn, 'r')
        soup = parse(f)
        f.close()
        soup.normalize()
        fb = soup.documentElement
        if fb.nodeType!=Node.ELEMENT_NODE or fb.tagName != "FictionBook":
            sys.stderr.write("The file %s does not seems to contain 'fictionbook' root element\n" % fn)
            return 10
        src.append(soup)

    if not author:
        # build composite author name
        bookauthors=map(Set,map(getAuthors,src))
        authors=reduce(lambda x,y: x.union(y),bookauthors, Set())
        author=string.join(authors,',')

    if not title:
        title = 'Antology'

    i=0
    for s in src:
        prefixId(s.documentElement, str(i))
        i=i+1

    f = open(outfile, 'w')
    f.close()
    return 0


def usage():
    sys.stderr.write("Usage: fbmegge.py [-v] -o outfile fb2file1 fb2file2 [fb2fileN...]\n")

def parseCommandLine():
    infiles = []
    outfile = None
    global verbose
    verbose = False
    author = None
    title = None
    
    (optlist, arglist) = getopt.getopt(sys.argv[1:], "vo:a:t:", ["verbose", "output=","author=","title="])
    for option, argument in optlist:
        if option in ("-v", "--verbose"):
            verbose = True
        elif option in ("-o", "--output"):
            outfile = argument
        elif option in ("-a", "--author"):
            author = argument
        elif option in ("-t", "--title"):
            title = argument

    if outfile == None:
        raise getopt.GetoptError("output file not specified")

    for filename in arglist:
        if os.path.isfile(filename):
            infiles.append(filename)
        else:
            raise getopt.GetoptError("input file '%s' doesn't exist" % filename)

    if len(infiles) <2:
        raise getopt.GetoptError("Not enough input files specified")
        
    return (infiles, outfile, author, title)

def main():
    try:
        (infiles, outfile, author, title) = parseCommandLine()
        return fbmerge(infiles, outfile, author, title)
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
