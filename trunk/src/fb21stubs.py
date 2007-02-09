#!/usr/bin/env python

#
# Generated Fri Feb  9 14:42:58 2007 by generateDS.py.
#

import sys
from xml.dom import minidom
from xml.sax import handler, make_parser

import ??? as supermod

class FictionBookSub(supermod.FictionBook):
    def __init__(self, stylesheet=None, description=None, body=None, binary=None):
        supermod.FictionBook.__init__(self, stylesheet, description, body, binary)
supermod.FictionBook.subclass = FictionBookSub
# end class FictionBookSub


class stylesheetSub(supermod.stylesheet):
    def __init__(self, ttype='', valueOf_=''):
        supermod.stylesheet.__init__(self, ttype)
supermod.stylesheet.subclass = stylesheetSub
# end class stylesheetSub


class descriptionSub(supermod.description):
    def __init__(self, title_info=None, src_title_info=None, document_info=None, publish_info=None, custom_info=None, output=None):
        supermod.description.__init__(self, title_info, src_title_info, document_info, publish_info, custom_info, output)
supermod.description.subclass = descriptionSub
# end class descriptionSub


class document_infoSub(supermod.document_info):
    def __init__(self, author=None, program_used=None, date=None, src_url=None, src_ocr=None, id='', version=0.0, history=None):
        supermod.document_info.__init__(self, author, program_used, date, src_url, src_ocr, id, version, history)
supermod.document_info.subclass = document_infoSub
# end class document_infoSub


class publish_infoSub(supermod.publish_info):
    def __init__(self, book_name=None, publisher=None, city=None, year='', isbn=None, sequence=None):
        supermod.publish_info.__init__(self, book_name, publisher, city, year, isbn, sequence)
supermod.publish_info.subclass = publish_infoSub
# end class publish_infoSub


class bodySub(supermod.body):
    def __init__(self, lang='', name='', image=None, title=None, epigraph=None, section=None):
        supermod.body.__init__(self, lang, name, image, title, epigraph, section)
supermod.body.subclass = bodySub
# end class bodySub


class binarySub(supermod.binary):
    def __init__(self, content_type='', id='', valueOf_=''):
        supermod.binary.__init__(self, content_type, id)
supermod.binary.subclass = binarySub
# end class binarySub


class authorTypeSub(supermod.authorType):
    def __init__(self, first_name=None, middle_name=None, last_name=None, nickname=None, home_page=None, email=None, nickname=None, home_page=None, email=None):
        supermod.authorType.__init__(self, first_name, middle_name, last_name, nickname, home_page, email, nickname, home_page, email)
supermod.authorType.subclass = authorTypeSub
# end class authorTypeSub


class textFieldTypeSub(supermod.textFieldType):
    def __init__(self, lang='', valueOf_=''):
        supermod.textFieldType.__init__(self, lang)
supermod.textFieldType.subclass = textFieldTypeSub
# end class textFieldTypeSub


class dateTypeSub(supermod.dateType):
    def __init__(self, lang='', value='', valueOf_=''):
        supermod.dateType.__init__(self, lang, value)
supermod.dateType.subclass = dateTypeSub
# end class dateTypeSub


class titleTypeSub(supermod.titleType):
    def __init__(self, lang='', p=None, empty_line=''):
        supermod.titleType.__init__(self, lang, p, empty_line)
supermod.titleType.subclass = titleTypeSub
# end class titleTypeSub


class imageTypeSub(supermod.imageType):
    def __init__(self, alt='', href='', ttype='', id='', title='', valueOf_=''):
        supermod.imageType.__init__(self, alt, href, ttype, id, title)
supermod.imageType.subclass = imageTypeSub
# end class imageTypeSub


class citeTypeSub(supermod.citeType):
    def __init__(self, lang='', id='', p=None, poem=None, empty_line='', subtitle=None, table=None, text_author=None):
        supermod.citeType.__init__(self, lang, id, p, poem, empty_line, subtitle, table, text_author)
supermod.citeType.subclass = citeTypeSub
# end class citeTypeSub


class poemTypeSub(supermod.poemType):
    def __init__(self, lang='', id='', title=None, epigraph=None, stanza=None, text_author=None, date=None):
        supermod.poemType.__init__(self, lang, id, title, epigraph, stanza, text_author, date)
supermod.poemType.subclass = poemTypeSub
# end class poemTypeSub


class stanzaSub(supermod.stanza):
    def __init__(self, lang='', title=None, subtitle=None, v=None):
        supermod.stanza.__init__(self, lang, title, subtitle, v)
supermod.stanza.subclass = stanzaSub
# end class stanzaSub


class epigraphTypeSub(supermod.epigraphType):
    def __init__(self, id='', p=None, poem=None, cite=None, empty_line='', text_author=None):
        supermod.epigraphType.__init__(self, id, p, poem, cite, empty_line, text_author)
supermod.epigraphType.subclass = epigraphTypeSub
# end class epigraphTypeSub


class annotationTypeSub(supermod.annotationType):
    def __init__(self, lang='', id='', p=None, poem=None, cite=None, subtitle=None, table=None, empty_line=''):
        supermod.annotationType.__init__(self, lang, id, p, poem, cite, subtitle, table, empty_line)
supermod.annotationType.subclass = annotationTypeSub
# end class annotationTypeSub


class sectionTypeSub(supermod.sectionType):
    def __init__(self, lang='', id='', title=None, epigraph=None, image=None, annotation=None, section=None, p=None, poem=None, subtitle=None, cite=None, empty_line='', table=None, p=None, image=None, poem=None, subtitle=None, cite=None, empty_line='', table=None):
        supermod.sectionType.__init__(self, lang, id, title, epigraph, image, annotation, section, p, poem, subtitle, cite, empty_line, table, p, image, poem, subtitle, cite, empty_line, table)
supermod.sectionType.subclass = sectionTypeSub
# end class sectionTypeSub


class styleTypeSub(supermod.styleType):
    def __init__(self, lang='', strong=None, emphasis=None, style=None, a=None, strikethrough=None, sub=None, sup=None, code=None, image=None, mixedclass_=None, content_=None):
        supermod.styleType.__init__(self, mixedclass_, content_)
supermod.styleType.subclass = styleTypeSub
# end class styleTypeSub


class namedStyleTypeSub(supermod.namedStyleType):
    def __init__(self, lang='', name='', strong=None, emphasis=None, style=None, a=None, strikethrough=None, sub=None, sup=None, code=None, image=None, mixedclass_=None, content_=None):
        supermod.namedStyleType.__init__(self, mixedclass_, content_)
supermod.namedStyleType.subclass = namedStyleTypeSub
# end class namedStyleTypeSub


class linkTypeSub(supermod.linkType):
    def __init__(self, href='', ttype='', strong=None, emphasis=None, style=None, strikethrough=None, sub=None, sup=None, code=None, image=None, mixedclass_=None, content_=None):
        supermod.linkType.__init__(self, mixedclass_, content_)
supermod.linkType.subclass = linkTypeSub
# end class linkTypeSub


class styleLinkTypeSub(supermod.styleLinkType):
    def __init__(self, strong=None, emphasis=None, style=None, strikethrough=None, sub=None, sup=None, code=None, image=None, mixedclass_=None, content_=None):
        supermod.styleLinkType.__init__(self, mixedclass_, content_)
supermod.styleLinkType.subclass = styleLinkTypeSub
# end class styleLinkTypeSub


class sequenceTypeSub(supermod.sequenceType):
    def __init__(self, lang='', name='', number=-1, sequence=None):
        supermod.sequenceType.__init__(self, lang, name, number, sequence)
supermod.sequenceType.subclass = sequenceTypeSub
# end class sequenceTypeSub


class tableTypeSub(supermod.tableType):
    def __init__(self, style='', id='', tr=None):
        supermod.tableType.__init__(self, style, id, tr)
supermod.tableType.subclass = tableTypeSub
# end class tableTypeSub


class trSub(supermod.tr):
    def __init__(self, align=None, th=None, td=None):
        supermod.tr.__init__(self, align, th, td)
supermod.tr.subclass = trSub
# end class trSub


class title_infoTypeSub(supermod.title_infoType):
    def __init__(self, genre=None, author=None, book_title=None, annotation=None, keywords=None, date=None, coverpage=None, lang='', src_lang='', translator=None, sequence=None):
        supermod.title_infoType.__init__(self, genre, author, book_title, annotation, keywords, date, coverpage, lang, src_lang, translator, sequence)
supermod.title_infoType.subclass = title_infoTypeSub
# end class title_infoTypeSub


class genreSub(supermod.genre):
    def __init__(self, match=-1, valueOf_=''):
        supermod.genre.__init__(self, match)
supermod.genre.subclass = genreSub
# end class genreSub


class coverpageSub(supermod.coverpage):
    def __init__(self, image=None):
        supermod.coverpage.__init__(self, image)
supermod.coverpage.subclass = coverpageSub
# end class coverpageSub


class shareInstructionTypeSub(supermod.shareInstructionType):
    def __init__(self, include_all=None, price=0.0, mode=None, currency='', part=None, output_document_class=None):
        supermod.shareInstructionType.__init__(self, include_all, price, mode, currency, part, output_document_class)
supermod.shareInstructionType.subclass = shareInstructionTypeSub
# end class shareInstructionTypeSub


class partShareInstructionTypeSub(supermod.partShareInstructionType):
    def __init__(self, include=None, href='', ttype='', valueOf_=''):
        supermod.partShareInstructionType.__init__(self, include, href, ttype)
supermod.partShareInstructionType.subclass = partShareInstructionTypeSub
# end class partShareInstructionTypeSub


class outPutDocumentTypeSub(supermod.outPutDocumentType):
    def __init__(self, price=0.0, create=None, name='', part=None):
        supermod.outPutDocumentType.__init__(self, price, create, name, part)
supermod.outPutDocumentType.subclass = outPutDocumentTypeSub
# end class outPutDocumentTypeSub


class tdTypeSub(supermod.tdType):
    def __init__(self, rowspan=-1, colspan=-1, align=None, style_attr='', id='', lang='', strong=None, emphasis=None, style=None, a=None, strikethrough=None, sub=None, sup=None, code=None, image=None, valueOf_='', mixedclass_=None, content_=None):
        supermod.tdType.__init__(self, mixedclass_, content_)
supermod.tdType.subclass = tdTypeSub
# end class tdTypeSub


class inlineImageTypeSub(supermod.inlineImageType):
    def __init__(self, alt='', href='', ttype='', valueOf_=''):
        supermod.inlineImageType.__init__(self, alt, href, ttype)
supermod.inlineImageType.subclass = inlineImageTypeSub
# end class inlineImageTypeSub


class pTypeSub(supermod.pType):
    def __init__(self, id='', style_attr='', lang='', strong=None, emphasis=None, style=None, a=None, strikethrough=None, sub=None, sup=None, code=None, image=None, valueOf_='', mixedclass_=None, content_=None):
        supermod.pType.__init__(self, mixedclass_, content_)
supermod.pType.subclass = pTypeSub
# end class pTypeSub


class custom_infoSub(supermod.custom_info):
    def __init__(self, info_type='', lang='', valueOf_=''):
        supermod.custom_info.__init__(self, info_type, lang)
supermod.custom_info.subclass = custom_infoSub
# end class custom_infoSub



#
# SAX handler used to determine the top level element.
#
class SaxSelectorHandler(handler.ContentHandler):
    def __init__(self):
        self.topElementName = None
    def getTopElementName(self):
        return self.topElementName
    def startElement(self, name, attrs):
        self.topElementName = name
        raise StopIteration


def parseSelect(inFileName):
    infile = file(inFileName, 'r')
    topElementName = None
    parser = make_parser()
    documentHandler = SaxSelectorHandler()
    parser.setContentHandler(documentHandler)
    try:
        try:
            parser.parse(infile)
        except StopIteration:
            topElementName = documentHandler.getTopElementName()
        if topElementName is None:
            raise RuntimeError, 'no top level element'
        topElementName = topElementName.replace('-', '_').replace(':', '_')
        if topElementName not in supermod.__dict__:
            raise RuntimeError, 'no class for top element: %s' % topElementName
        topElement = supermod.__dict__[topElementName]
        infile.seek(0)
        doc = minidom.parse(infile)
    finally:
        infile.close()
    rootNode = doc.childNodes[0]
    rootObj = topElement.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0)
    return rootObj


def saxParse(inFileName):
    parser = make_parser()
    documentHandler = supermod.SaxFictionbookHandler()
    parser.setDocumentHandler(documentHandler)
    parser.parse('file:%s' % inFileName)
    rootObj = documentHandler.getRoot()
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0)
    return rootObj


def saxParseString(inString):
    parser = make_parser()
    documentHandler = supermod.SaxContentHandler()
    parser.setDocumentHandler(documentHandler)
    parser.feed(inString)
    parser.close()
    rootObj = documentHandler.getRoot()
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0)
    return rootObj


def parse(inFilename):
    doc = minidom.parse(inFilename)
    rootNode = doc.documentElement
    rootObj = supermod.FictionBook.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="FictionBook")
    doc = None
    return rootObj


def parseString(inString):
    doc = minidom.parseString(inString)
    rootNode = doc.documentElement
    rootObj = supermod.FictionBook.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="FictionBook")
    return rootObj


def parseLiteral(inFilename):
    doc = minidom.parse(inFilename)
    rootNode = doc.documentElement
    rootObj = supermod.FictionBook.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('from ??? import *\n\n')
    sys.stdout.write('rootObj = FictionBook(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="FictionBook")
    sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""

def usage():
    print USAGE_TEXT
    sys.exit(-1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    root = parse(infilename)


if __name__ == '__main__':
    main()
    #import pdb
    #pdb.run('main()')


