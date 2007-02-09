#!/usr/bin/env python

#
# Generated Fri Feb  9 14:42:57 2007 by generateDS.py.
#

import sys
import getopt
from xml.dom import minidom
from xml.dom import Node

#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Support/utility functions.
#

def showIndent(outfile, level):
    for idx in range(level):
        outfile.write('    ')

def quote_xml(inStr):
    s1 = inStr
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('"', '&quot;')
    return s1

def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(outfile, level, name)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (self.name, self.value, self.name))
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write('MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write('MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write('MixedContainer(%d, %d, "%s",\n' % \
                (self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


#
# Data representation classes.
#

class FictionBook:
    subclass = None
    def __init__(self, stylesheet=None, description=None, body=None, binary=None):
        if stylesheet is None:
            self.stylesheet = []
        else:
            self.stylesheet = stylesheet
        self.description = description
        if body is None:
            self.body = []
        else:
            self.body = body
        if binary is None:
            self.binary = []
        else:
            self.binary = binary
    def factory(*args_, **kwargs_):
        if FictionBook.subclass:
            return FictionBook.subclass(*args_, **kwargs_)
        else:
            return FictionBook(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getStylesheet(self): return self.stylesheet
    def setStylesheet(self, stylesheet): self.stylesheet = stylesheet
    def addStylesheet(self, value): self.stylesheet.append(value)
    def insertStylesheet(self, index, value): self.stylesheet[index] = value
    def getDescription(self): return self.description
    def setDescription(self, description): self.description = description
    def getBody(self): return self.body
    def setBody(self, body): self.body = body
    def addBody(self, value): self.body.append(value)
    def insertBody(self, index, value): self.body[index] = value
    def getBinary(self): return self.binary
    def setBinary(self, binary): self.binary = binary
    def addBinary(self, value): self.binary.append(value)
    def insertBinary(self, index, value): self.binary[index] = value
    def export(self, outfile, level, name_='FictionBook'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='FictionBook'):
        pass
    def exportChildren(self, outfile, level, name_='FictionBook'):
        for stylesheet_ in self.getStylesheet():
            stylesheet_.export(outfile, level)
        if self.description:
            self.description.export(outfile, level)
        for body_ in self.getBody():
            body_.export(outfile, level)
        for binary_ in self.getBinary():
            binary_.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='FictionBook'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('stylesheet=[\n')
        level += 1
        for stylesheet in self.stylesheet:
            showIndent(outfile, level)
            outfile.write('stylesheet(\n')
            stylesheet.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.description:
            showIndent(outfile, level)
            outfile.write('description=description(\n')
            self.description.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('body=[\n')
        level += 1
        for body in self.body:
            showIndent(outfile, level)
            outfile.write('body(\n')
            body.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('binary=[\n')
        level += 1
        for binary in self.binary:
            showIndent(outfile, level)
            outfile.write('binary(\n')
            binary.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'stylesheet':
            obj_ = stylesheet.factory()
            obj_.build(child_)
            self.stylesheet.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'description':
            obj_ = description.factory()
            obj_.build(child_)
            self.setDescription(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'body':
            obj_ = body.factory()
            obj_.build(child_)
            self.body.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'binary':
            obj_ = binary.factory()
            obj_.build(child_)
            self.binary.append(obj_)
# end class FictionBook


class stylesheet:
    subclass = None
    def __init__(self, ttype='', valueOf_=''):
        self.ttype = ttype
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if stylesheet.subclass:
            return stylesheet.subclass(*args_, **kwargs_)
        else:
            return stylesheet(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='stylesheet'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='stylesheet')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='stylesheet'):
        outfile.write(' type="%s"' % (self.getType(), ))
    def exportChildren(self, outfile, level, name_='stylesheet'):
        outfile.write(self.valueOf_)
    def exportLiteral(self, outfile, level, name_='stylesheet'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('ttype = "%s",\n' % (self.getType(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('type'):
            self.ttype = attrs.get('type').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class stylesheet


class description:
    subclass = None
    def __init__(self, title_info=None, src_title_info=None, document_info=None, publish_info=None, custom_info=None, output=None):
        self.title_info = title_info
        self.src_title_info = src_title_info
        self.document_info = document_info
        self.publish_info = publish_info
        if custom_info is None:
            self.custom_info = []
        else:
            self.custom_info = custom_info
        if output is None:
            self.output = []
        else:
            self.output = output
    def factory(*args_, **kwargs_):
        if description.subclass:
            return description.subclass(*args_, **kwargs_)
        else:
            return description(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getTitle_info(self): return self.title_info
    def setTitle_info(self, title_info): self.title_info = title_info
    def getSrc_title_info(self): return self.src_title_info
    def setSrc_title_info(self, src_title_info): self.src_title_info = src_title_info
    def getDocument_info(self): return self.document_info
    def setDocument_info(self, document_info): self.document_info = document_info
    def getPublish_info(self): return self.publish_info
    def setPublish_info(self, publish_info): self.publish_info = publish_info
    def getCustom_info(self): return self.custom_info
    def setCustom_info(self, custom_info): self.custom_info = custom_info
    def addCustom_info(self, value): self.custom_info.append(value)
    def insertCustom_info(self, index, value): self.custom_info[index] = value
    def getOutput(self): return self.output
    def setOutput(self, output): self.output = output
    def addOutput(self, value): self.output.append(value)
    def insertOutput(self, index, value): self.output[index] = value
    def export(self, outfile, level, name_='description'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='description'):
        pass
    def exportChildren(self, outfile, level, name_='description'):
        if self.title_info:
            self.title_info.export(outfile, level, name_='title-info')
        if self.src_title_info:
            self.src_title_info.export(outfile, level, name_='src-title-info')
        if self.document_info:
            self.document_info.export(outfile, level)
        if self.publish_info:
            self.publish_info.export(outfile, level)
        for custom_info_ in self.getCustom_info():
            custom_info_.export(outfile, level)
        for output_ in self.getOutput():
            output_.export(outfile, level, name_='output')
    def exportLiteral(self, outfile, level, name_='description'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.title_info:
            showIndent(outfile, level)
            outfile.write('title_info=title_infoType(\n')
            self.title_info.exportLiteral(outfile, level, name_='title_info')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.src_title_info:
            showIndent(outfile, level)
            outfile.write('src_title_info=title_infoType(\n')
            self.src_title_info.exportLiteral(outfile, level, name_='src_title_info')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.document_info:
            showIndent(outfile, level)
            outfile.write('document_info=document_info(\n')
            self.document_info.exportLiteral(outfile, level, name_='document_info')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.publish_info:
            showIndent(outfile, level)
            outfile.write('publish_info=publish_info(\n')
            self.publish_info.exportLiteral(outfile, level, name_='publish_info')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('custom_info=[\n')
        level += 1
        for custom_info in self.custom_info:
            showIndent(outfile, level)
            outfile.write('custom_info(\n')
            custom_info.exportLiteral(outfile, level, name_='custom_info')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('output=[\n')
        level += 1
        for output in self.output:
            showIndent(outfile, level)
            outfile.write('shareInstructionType(\n')
            output.exportLiteral(outfile, level, name_='output')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'title-info':
            obj_ = title_infoType.factory()
            obj_.build(child_)
            self.setTitle_info(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'src-title-info':
            obj_ = title_infoType.factory()
            obj_.build(child_)
            self.setSrc_title_info(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'document-info':
            obj_ = document_info.factory()
            obj_.build(child_)
            self.setDocument_info(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'publish-info':
            obj_ = publish_info.factory()
            obj_.build(child_)
            self.setPublish_info(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'custom-info':
            obj_ = custom_info.factory()
            obj_.build(child_)
            self.custom_info.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'output':
            obj_ = shareInstructionType.factory()
            obj_.build(child_)
            self.output.append(obj_)
# end class description


class document_info:
    subclass = None
    def __init__(self, author=None, program_used=None, date=None, src_url=None, src_ocr=None, id='', version=0.0, history=None):
        if author is None:
            self.author = []
        else:
            self.author = author
        self.program_used = program_used
        self.date = date
        if src_url is None:
            self.src_url = []
        else:
            self.src_url = src_url
        self.src_ocr = src_ocr
        self.id = id
        self.version = version
        self.history = history
    def factory(*args_, **kwargs_):
        if document_info.subclass:
            return document_info.subclass(*args_, **kwargs_)
        else:
            return document_info(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getAuthor(self): return self.author
    def setAuthor(self, author): self.author = author
    def addAuthor(self, value): self.author.append(value)
    def insertAuthor(self, index, value): self.author[index] = value
    def getProgram_used(self): return self.program_used
    def setProgram_used(self, program_used): self.program_used = program_used
    def getDate(self): return self.date
    def setDate(self, date): self.date = date
    def getSrc_url(self): return self.src_url
    def setSrc_url(self, src_url): self.src_url = src_url
    def addSrc_url(self, value): self.src_url.append(value)
    def insertSrc_url(self, index, value): self.src_url[index] = value
    def getSrc_ocr(self): return self.src_ocr
    def setSrc_ocr(self, src_ocr): self.src_ocr = src_ocr
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def getVersion(self): return self.version
    def setVersion(self, version): self.version = version
    def getHistory(self): return self.history
    def setHistory(self, history): self.history = history
    def export(self, outfile, level, name_='document-info'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='document-info'):
        pass
    def exportChildren(self, outfile, level, name_='document-info'):
        for author_ in self.getAuthor():
            author_.export(outfile, level, name_='author')
        if self.program_used:
            self.program_used.export(outfile, level, name_='program-used')
        if self.date:
            self.date.export(outfile, level, name_='date')
        for src_url_ in self.getSrc_url():
            showIndent(outfile, level)
            outfile.write('<src-url>%s</src-url>\n' % quote_xml(src_url_))
        if self.src_ocr:
            self.src_ocr.export(outfile, level, name_='src-ocr')
        showIndent(outfile, level)
        outfile.write('<id>%s</id>\n' % quote_xml(self.getId()))
        showIndent(outfile, level)
        outfile.write('<version>%f</version>\n' % self.getVersion())
        if self.history:
            self.history.export(outfile, level, name_='history')
    def exportLiteral(self, outfile, level, name_='document-info'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('author=[\n')
        level += 1
        for author in self.author:
            showIndent(outfile, level)
            outfile.write('authorType(\n')
            author.exportLiteral(outfile, level, name_='author')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.program_used:
            showIndent(outfile, level)
            outfile.write('program_used=textFieldType(\n')
            self.program_used.exportLiteral(outfile, level, name_='program_used')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.date:
            showIndent(outfile, level)
            outfile.write('date=dateType(\n')
            self.date.exportLiteral(outfile, level, name_='date')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('src_url=[\n')
        level += 1
        for src_url in self.src_url:
            showIndent(outfile, level)
            outfile.write('%s,\n' % quote_python(src_url))
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.src_ocr:
            showIndent(outfile, level)
            outfile.write('src_ocr=textFieldType(\n')
            self.src_ocr.exportLiteral(outfile, level, name_='src_ocr')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('id=%s,\n' % quote_python(self.getId()))
        showIndent(outfile, level)
        outfile.write('version=%f,\n' % self.getVersion())
        if self.history:
            showIndent(outfile, level)
            outfile.write('history=annotationType(\n')
            self.history.exportLiteral(outfile, level, name_='history')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'author':
            obj_ = authorType.factory()
            obj_.build(child_)
            self.author.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'program-used':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setProgram_used(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'date':
            obj_ = dateType.factory()
            obj_.build(child_)
            self.setDate(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'src-url':
            src_url_ = ''
            for text__content_ in child_.childNodes:
                src_url_ += text__content_.nodeValue
            self.src_url.append(src_url_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'src-ocr':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setSrc_ocr(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'id':
            id_ = ''
            for text__content_ in child_.childNodes:
                id_ += text__content_.nodeValue
            id_ = ' '.join(id_.split())
            self.id = id_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'version':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    fval_ = float(sval_)
                except ValueError:
                    raise ValueError('requires float (or double) -- %s' % child_.toxml())
                self.version = fval_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'history':
            obj_ = annotationType.factory()
            obj_.build(child_)
            self.setHistory(obj_)
# end class document_info


class publish_info:
    subclass = None
    def __init__(self, book_name=None, publisher=None, city=None, year='', isbn=None, sequence=None):
        self.book_name = book_name
        self.publisher = publisher
        self.city = city
        self.year = year
        self.isbn = isbn
        if sequence is None:
            self.sequence = []
        else:
            self.sequence = sequence
    def factory(*args_, **kwargs_):
        if publish_info.subclass:
            return publish_info.subclass(*args_, **kwargs_)
        else:
            return publish_info(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getBook_name(self): return self.book_name
    def setBook_name(self, book_name): self.book_name = book_name
    def getPublisher(self): return self.publisher
    def setPublisher(self, publisher): self.publisher = publisher
    def getCity(self): return self.city
    def setCity(self, city): self.city = city
    def getYear(self): return self.year
    def setYear(self, year): self.year = year
    def getIsbn(self): return self.isbn
    def setIsbn(self, isbn): self.isbn = isbn
    def getSequence(self): return self.sequence
    def setSequence(self, sequence): self.sequence = sequence
    def addSequence(self, value): self.sequence.append(value)
    def insertSequence(self, index, value): self.sequence[index] = value
    def export(self, outfile, level, name_='publish-info'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='publish-info'):
        pass
    def exportChildren(self, outfile, level, name_='publish-info'):
        if self.book_name:
            self.book_name.export(outfile, level, name_='book-name')
        if self.publisher:
            self.publisher.export(outfile, level, name_='publisher')
        if self.city:
            self.city.export(outfile, level, name_='city')
        showIndent(outfile, level)
        outfile.write('<year>%s</year>\n' % quote_xml(self.getYear()))
        if self.isbn:
            self.isbn.export(outfile, level, name_='isbn')
        for sequence_ in self.getSequence():
            sequence_.export(outfile, level, name_='sequence')
    def exportLiteral(self, outfile, level, name_='publish-info'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.book_name:
            showIndent(outfile, level)
            outfile.write('book_name=textFieldType(\n')
            self.book_name.exportLiteral(outfile, level, name_='book_name')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.publisher:
            showIndent(outfile, level)
            outfile.write('publisher=textFieldType(\n')
            self.publisher.exportLiteral(outfile, level, name_='publisher')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.city:
            showIndent(outfile, level)
            outfile.write('city=textFieldType(\n')
            self.city.exportLiteral(outfile, level, name_='city')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('year=%s,\n' % quote_python(self.getYear()))
        if self.isbn:
            showIndent(outfile, level)
            outfile.write('isbn=textFieldType(\n')
            self.isbn.exportLiteral(outfile, level, name_='isbn')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('sequence=[\n')
        level += 1
        for sequence in self.sequence:
            showIndent(outfile, level)
            outfile.write('sequenceType(\n')
            sequence.exportLiteral(outfile, level, name_='sequence')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'book-name':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setBook_name(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'publisher':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setPublisher(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'city':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setCity(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'year':
            year_ = ''
            for text__content_ in child_.childNodes:
                year_ += text__content_.nodeValue
            self.year = year_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'isbn':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setIsbn(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sequence':
            obj_ = sequenceType.factory()
            obj_.build(child_)
            self.sequence.append(obj_)
# end class publish_info


class body:
    subclass = None
    def __init__(self, lang='', name='', image=None, title=None, epigraph=None, section=None):
        self.lang = lang
        self.name = name
        self.image = image
        self.title = title
        if epigraph is None:
            self.epigraph = []
        else:
            self.epigraph = epigraph
        if section is None:
            self.section = []
        else:
            self.section = section
    def factory(*args_, **kwargs_):
        if body.subclass:
            return body.subclass(*args_, **kwargs_)
        else:
            return body(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getImage(self): return self.image
    def setImage(self, image): self.image = image
    def getTitle(self): return self.title
    def setTitle(self, title): self.title = title
    def getEpigraph(self): return self.epigraph
    def setEpigraph(self, epigraph): self.epigraph = epigraph
    def addEpigraph(self, value): self.epigraph.append(value)
    def insertEpigraph(self, index, value): self.epigraph[index] = value
    def getSection(self): return self.section
    def setSection(self, section): self.section = section
    def addSection(self, value): self.section.append(value)
    def insertSection(self, index, value): self.section[index] = value
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def getName(self): return self.name
    def setName(self, name): self.name = name
    def export(self, outfile, level, name_='body'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='body')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='body'):
        if self.getLang() is not None:
            outfile.write(' lang="%s"' % (self.getLang(), ))
        if self.getName() is not None:
            outfile.write(' name="%s"' % (self.getName(), ))
    def exportChildren(self, outfile, level, name_='body'):
        if self.image:
            self.image.export(outfile, level, name_='image')
        if self.title:
            self.title.export(outfile, level, name_='title')
        for epigraph_ in self.getEpigraph():
            epigraph_.export(outfile, level, name_='epigraph')
        for section_ in self.getSection():
            section_.export(outfile, level, name_='section')
    def exportLiteral(self, outfile, level, name_='body'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('lang = "%s",\n' % (self.getLang(),))
        showIndent(outfile, level)
        outfile.write('name = "%s",\n' % (self.getName(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.image:
            showIndent(outfile, level)
            outfile.write('image=imageType(\n')
            self.image.exportLiteral(outfile, level, name_='image')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.title:
            showIndent(outfile, level)
            outfile.write('title=titleType(\n')
            self.title.exportLiteral(outfile, level, name_='title')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('epigraph=[\n')
        level += 1
        for epigraph in self.epigraph:
            showIndent(outfile, level)
            outfile.write('epigraphType(\n')
            epigraph.exportLiteral(outfile, level, name_='epigraph')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('section=[\n')
        level += 1
        for section in self.section:
            showIndent(outfile, level)
            outfile.write('sectionType(\n')
            section.exportLiteral(outfile, level, name_='section')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('lang'):
            self.lang = attrs.get('lang').value
        if attrs.get('name'):
            self.name = attrs.get('name').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'image':
            obj_ = imageType.factory()
            obj_.build(child_)
            self.setImage(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'title':
            obj_ = titleType.factory()
            obj_.build(child_)
            self.setTitle(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'epigraph':
            obj_ = epigraphType.factory()
            obj_.build(child_)
            self.epigraph.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'section':
            obj_ = sectionType.factory()
            obj_.build(child_)
            self.section.append(obj_)
# end class body


class binary(base64Binary):
    subclass = None
    def __init__(self, content_type='', id='', valueOf_=''):
        self.content_type = content_type
        self.id = id
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if binary.subclass:
            return binary.subclass(*args_, **kwargs_)
        else:
            return binary(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getContent_type(self): return self.content_type
    def setContent_type(self, content_type): self.content_type = content_type
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='binary'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='binary')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='binary'):
        outfile.write(' content-type="%s"' % (self.getContent_type(), ))
        outfile.write(' id="%s"' % (self.getId(), ))
        base64Binary.exportAttributes(self, outfile, level, name_='binary')
    def exportChildren(self, outfile, level, name_='binary'):
        base64Binary.exportChildren(self, outfile, level, name_)
        outfile.write(self.valueOf_)
    def exportLiteral(self, outfile, level, name_='binary'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('content_type = "%s",\n' % (self.getContent_type(),))
        showIndent(outfile, level)
        outfile.write('id = "%s",\n' % (self.getId(),))
        base64Binary.exportLiteralAttributes(self, outfile, level, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
        base64Binary.exportLiteralChildren(self, outfile, level, name_)
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('content-type'):
            self.content_type = attrs.get('content-type').value
        if attrs.get('id'):
            self.id = attrs.get('id').value
        base64Binary.buildAttributes(self, attrs)
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class binary


class authorType:
    subclass = None
    def __init__(self, first_name=None, middle_name=None, last_name=None, nickname=None, home_page=None, email=None, nickname=None, home_page=None, email=None):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.nickname = nickname
        if home_page is None:
            self.home_page = []
        else:
            self.home_page = home_page
        if email is None:
            self.email = []
        else:
            self.email = email
        self.nickname = nickname
        if home_page is None:
            self.home_page = []
        else:
            self.home_page = home_page
        if email is None:
            self.email = []
        else:
            self.email = email
    def factory(*args_, **kwargs_):
        if authorType.subclass:
            return authorType.subclass(*args_, **kwargs_)
        else:
            return authorType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getFirst_name(self): return self.first_name
    def setFirst_name(self, first_name): self.first_name = first_name
    def getMiddle_name(self): return self.middle_name
    def setMiddle_name(self, middle_name): self.middle_name = middle_name
    def getLast_name(self): return self.last_name
    def setLast_name(self, last_name): self.last_name = last_name
    def getNickname(self): return self.nickname
    def setNickname(self, nickname): self.nickname = nickname
    def getHome_page(self): return self.home_page
    def setHome_page(self, home_page): self.home_page = home_page
    def addHome_page(self, value): self.home_page.append(value)
    def insertHome_page(self, index, value): self.home_page[index] = value
    def getEmail(self): return self.email
    def setEmail(self, email): self.email = email
    def addEmail(self, value): self.email.append(value)
    def insertEmail(self, index, value): self.email[index] = value
    def getNickname(self): return self.nickname
    def setNickname(self, nickname): self.nickname = nickname
    def getHome_page(self): return self.home_page
    def setHome_page(self, home_page): self.home_page = home_page
    def addHome_page(self, value): self.home_page.append(value)
    def insertHome_page(self, index, value): self.home_page[index] = value
    def getEmail(self): return self.email
    def setEmail(self, email): self.email = email
    def addEmail(self, value): self.email.append(value)
    def insertEmail(self, index, value): self.email[index] = value
    def export(self, outfile, level, name_='authorType'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='authorType'):
        pass
    def exportChildren(self, outfile, level, name_='authorType'):
        if self.first_name:
            self.first_name.export(outfile, level, name_='first-name')
        if self.middle_name:
            self.middle_name.export(outfile, level, name_='middle-name')
        if self.last_name:
            self.last_name.export(outfile, level, name_='last-name')
        if self.nickname:
            self.nickname.export(outfile, level, name_='nickname')
        for home_page_ in self.getHome_page():
            showIndent(outfile, level)
            outfile.write('<home-page>%s</home-page>\n' % quote_xml(home_page_))
        for email_ in self.getEmail():
            showIndent(outfile, level)
            outfile.write('<email>%s</email>\n' % quote_xml(email_))
        if self.nickname:
            self.nickname.export(outfile, level, name_='nickname')
        for home_page_ in self.getHome_page():
            showIndent(outfile, level)
            outfile.write('<home-page>%s</home-page>\n' % quote_xml(home_page_))
        for email_ in self.getEmail():
            showIndent(outfile, level)
            outfile.write('<email>%s</email>\n' % quote_xml(email_))
    def exportLiteral(self, outfile, level, name_='authorType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.first_name:
            showIndent(outfile, level)
            outfile.write('first_name=textFieldType(\n')
            self.first_name.exportLiteral(outfile, level, name_='first_name')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.middle_name:
            showIndent(outfile, level)
            outfile.write('middle_name=textFieldType(\n')
            self.middle_name.exportLiteral(outfile, level, name_='middle_name')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.last_name:
            showIndent(outfile, level)
            outfile.write('last_name=textFieldType(\n')
            self.last_name.exportLiteral(outfile, level, name_='last_name')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.nickname:
            showIndent(outfile, level)
            outfile.write('nickname=textFieldType(\n')
            self.nickname.exportLiteral(outfile, level, name_='nickname')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('home_page=[\n')
        level += 1
        for home_page in self.home_page:
            showIndent(outfile, level)
            outfile.write('%s,\n' % quote_python(home_page))
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('email=[\n')
        level += 1
        for email in self.email:
            showIndent(outfile, level)
            outfile.write('%s,\n' % quote_python(email))
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.nickname:
            showIndent(outfile, level)
            outfile.write('nickname=textFieldType(\n')
            self.nickname.exportLiteral(outfile, level, name_='nickname')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('home_page=[\n')
        level += 1
        for home_page in self.home_page:
            showIndent(outfile, level)
            outfile.write('%s,\n' % quote_python(home_page))
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('email=[\n')
        level += 1
        for email in self.email:
            showIndent(outfile, level)
            outfile.write('%s,\n' % quote_python(email))
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'first-name':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setFirst_name(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'middle-name':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setMiddle_name(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'last-name':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setLast_name(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'nickname':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setNickname(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'home-page':
            home_page_ = ''
            for text__content_ in child_.childNodes:
                home_page_ += text__content_.nodeValue
            self.home_page.append(home_page_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'email':
            email_ = ''
            for text__content_ in child_.childNodes:
                email_ += text__content_.nodeValue
            self.email.append(email_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'nickname':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setNickname(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'home-page':
            home_page_ = ''
            for text__content_ in child_.childNodes:
                home_page_ += text__content_.nodeValue
            self.home_page.append(home_page_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'email':
            email_ = ''
            for text__content_ in child_.childNodes:
                email_ += text__content_.nodeValue
            self.email.append(email_)
# end class authorType


class textFieldType:
    subclass = None
    def __init__(self, lang='', valueOf_=''):
        self.lang = lang
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if textFieldType.subclass:
            return textFieldType.subclass(*args_, **kwargs_)
        else:
            return textFieldType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='textFieldType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='textFieldType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='textFieldType'):
        if self.getLang() is not None:
            outfile.write(' lang="%s"' % (self.getLang(), ))
    def exportChildren(self, outfile, level, name_='textFieldType'):
        outfile.write(self.valueOf_)
    def exportLiteral(self, outfile, level, name_='textFieldType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('lang = "%s",\n' % (self.getLang(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('lang'):
            self.lang = attrs.get('lang').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class textFieldType


class dateType:
    subclass = None
    def __init__(self, lang='', value='', valueOf_=''):
        self.lang = lang
        self.value = value
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if dateType.subclass:
            return dateType.subclass(*args_, **kwargs_)
        else:
            return dateType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def getValue(self): return self.value
    def setValue(self, value): self.value = value
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='dateType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='dateType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='dateType'):
        if self.getLang() is not None:
            outfile.write(' lang="%s"' % (self.getLang(), ))
        if self.getValue() is not None:
            outfile.write(' value="%s"' % (self.getValue(), ))
    def exportChildren(self, outfile, level, name_='dateType'):
        outfile.write(self.valueOf_)
    def exportLiteral(self, outfile, level, name_='dateType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('lang = "%s",\n' % (self.getLang(),))
        showIndent(outfile, level)
        outfile.write('value = "%s",\n' % (self.getValue(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('lang'):
            self.lang = attrs.get('lang').value
        if attrs.get('value'):
            self.value = attrs.get('value').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class dateType


class titleType:
    subclass = None
    def __init__(self, lang='', p=None, empty_line=''):
        self.lang = lang
        self.p = p
        self.empty_line = empty_line
    def factory(*args_, **kwargs_):
        if titleType.subclass:
            return titleType.subclass(*args_, **kwargs_)
        else:
            return titleType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getP(self): return self.p
    def setP(self, p): self.p = p
    def getEmpty_line(self): return self.empty_line
    def setEmpty_line(self, empty_line): self.empty_line = empty_line
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def export(self, outfile, level, name_='titleType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='titleType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='titleType'):
        if self.getLang() is not None:
            outfile.write(' lang="%s"' % (self.getLang(), ))
    def exportChildren(self, outfile, level, name_='titleType'):
        if self.p:
            self.p.export(outfile, level, name_='p')
        showIndent(outfile, level)
        outfile.write('<empty-line>%s</empty-line>\n' % quote_xml(self.getEmpty_line()))
    def exportLiteral(self, outfile, level, name_='titleType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('lang = "%s",\n' % (self.getLang(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.p:
            showIndent(outfile, level)
            outfile.write('p=pType(\n')
            self.p.exportLiteral(outfile, level, name_='p')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('empty_line=%s,\n' % quote_python(self.getEmpty_line()))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('lang'):
            self.lang = attrs.get('lang').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'p':
            obj_ = pType.factory()
            obj_.build(child_)
            self.setP(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'empty-line':
            empty_line_ = ''
            for text__content_ in child_.childNodes:
                empty_line_ += text__content_.nodeValue
            self.empty_line = empty_line_
# end class titleType


class empty_line:
    subclass = None
    def __init__(self, valueOf_=''):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if empty_line.subclass:
            return empty_line.subclass(*args_, **kwargs_)
        else:
            return empty_line(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='empty-line'):
        showIndent(outfile, level)
        outfile.write('<%s>' % name_)
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='empty-line'):
        pass
    def exportChildren(self, outfile, level, name_='empty-line'):
        outfile.write(self.valueOf_)
    def exportLiteral(self, outfile, level, name_='empty-line'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class empty_line


class imageType:
    subclass = None
    def __init__(self, alt='', href='', ttype='', id='', title='', valueOf_=''):
        self.alt = alt
        self.href = href
        self.ttype = ttype
        self.id = id
        self.title = title
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if imageType.subclass:
            return imageType.subclass(*args_, **kwargs_)
        else:
            return imageType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getAlt(self): return self.alt
    def setAlt(self, alt): self.alt = alt
    def getHref(self): return self.href
    def setHref(self, href): self.href = href
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def getTitle(self): return self.title
    def setTitle(self, title): self.title = title
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='imageType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='imageType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='imageType'):
        if self.getAlt() is not None:
            outfile.write(' alt="%s"' % (self.getAlt(), ))
        if self.getHref() is not None:
            outfile.write(' href="%s"' % (self.getHref(), ))
        if self.getType() is not None:
            outfile.write(' type="%s"' % (self.getType(), ))
        if self.getId() is not None:
            outfile.write(' id="%s"' % (self.getId(), ))
        if self.getTitle() is not None:
            outfile.write(' title="%s"' % (self.getTitle(), ))
    def exportChildren(self, outfile, level, name_='imageType'):
        outfile.write(self.valueOf_)
    def exportLiteral(self, outfile, level, name_='imageType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('alt = "%s",\n' % (self.getAlt(),))
        showIndent(outfile, level)
        outfile.write('href = "%s",\n' % (self.getHref(),))
        showIndent(outfile, level)
        outfile.write('ttype = "%s",\n' % (self.getType(),))
        showIndent(outfile, level)
        outfile.write('id = "%s",\n' % (self.getId(),))
        showIndent(outfile, level)
        outfile.write('title = "%s",\n' % (self.getTitle(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('alt'):
            self.alt = attrs.get('alt').value
        if attrs.get('href'):
            self.href = attrs.get('href').value
        if attrs.get('type'):
            self.ttype = attrs.get('type').value
        if attrs.get('id'):
            self.id = attrs.get('id').value
        if attrs.get('title'):
            self.title = attrs.get('title').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class imageType


class citeType:
    subclass = None
    def __init__(self, lang='', id='', p=None, poem=None, empty_line='', subtitle=None, table=None, text_author=None):
        self.lang = lang
        self.id = id
        self.p = p
        self.poem = poem
        self.empty_line = empty_line
        self.subtitle = subtitle
        self.table = table
        if text_author is None:
            self.text_author = []
        else:
            self.text_author = text_author
    def factory(*args_, **kwargs_):
        if citeType.subclass:
            return citeType.subclass(*args_, **kwargs_)
        else:
            return citeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getP(self): return self.p
    def setP(self, p): self.p = p
    def getPoem(self): return self.poem
    def setPoem(self, poem): self.poem = poem
    def getEmpty_line(self): return self.empty_line
    def setEmpty_line(self, empty_line): self.empty_line = empty_line
    def getSubtitle(self): return self.subtitle
    def setSubtitle(self, subtitle): self.subtitle = subtitle
    def getTable(self): return self.table
    def setTable(self, table): self.table = table
    def getText_author(self): return self.text_author
    def setText_author(self, text_author): self.text_author = text_author
    def addText_author(self, value): self.text_author.append(value)
    def insertText_author(self, index, value): self.text_author[index] = value
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def export(self, outfile, level, name_='citeType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='citeType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='citeType'):
        if self.getLang() is not None:
            outfile.write(' lang="%s"' % (self.getLang(), ))
        if self.getId() is not None:
            outfile.write(' id="%s"' % (self.getId(), ))
    def exportChildren(self, outfile, level, name_='citeType'):
        if self.p:
            self.p.export(outfile, level, name_='p')
        if self.poem:
            self.poem.export(outfile, level, name_='poem')
        showIndent(outfile, level)
        outfile.write('<empty-line>%s</empty-line>\n' % quote_xml(self.getEmpty_line()))
        if self.subtitle:
            self.subtitle.export(outfile, level, name_='subtitle')
        if self.table:
            self.table.export(outfile, level, name_='table')
        for text_author_ in self.getText_author():
            text_author_.export(outfile, level, name_='text_author')
    def exportLiteral(self, outfile, level, name_='citeType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('lang = "%s",\n' % (self.getLang(),))
        showIndent(outfile, level)
        outfile.write('id = "%s",\n' % (self.getId(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.p:
            showIndent(outfile, level)
            outfile.write('p=pType(\n')
            self.p.exportLiteral(outfile, level, name_='p')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.poem:
            showIndent(outfile, level)
            outfile.write('poem=poemType(\n')
            self.poem.exportLiteral(outfile, level, name_='poem')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('empty_line=%s,\n' % quote_python(self.getEmpty_line()))
        if self.subtitle:
            showIndent(outfile, level)
            outfile.write('subtitle=pType(\n')
            self.subtitle.exportLiteral(outfile, level, name_='subtitle')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.table:
            showIndent(outfile, level)
            outfile.write('table=tableType(\n')
            self.table.exportLiteral(outfile, level, name_='table')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('text_author=[\n')
        level += 1
        for text_author in self.text_author:
            showIndent(outfile, level)
            outfile.write('pType(\n')
            text_author.exportLiteral(outfile, level, name_='text_author')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('lang'):
            self.lang = attrs.get('lang').value
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'p':
            obj_ = pType.factory()
            obj_.build(child_)
            self.setP(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'poem':
            obj_ = poemType.factory()
            obj_.build(child_)
            self.setPoem(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'empty-line':
            empty_line_ = ''
            for text__content_ in child_.childNodes:
                empty_line_ += text__content_.nodeValue
            self.empty_line = empty_line_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'subtitle':
            obj_ = pType.factory()
            obj_.build(child_)
            self.setSubtitle(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'table':
            obj_ = tableType.factory()
            obj_.build(child_)
            self.setTable(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'text-author':
            obj_ = pType.factory()
            obj_.build(child_)
            self.text_author.append(obj_)
# end class citeType


class poemType:
    subclass = None
    def __init__(self, lang='', id='', title=None, epigraph=None, stanza=None, text_author=None, date=None):
        self.lang = lang
        self.id = id
        self.title = title
        if epigraph is None:
            self.epigraph = []
        else:
            self.epigraph = epigraph
        if stanza is None:
            self.stanza = []
        else:
            self.stanza = stanza
        if text_author is None:
            self.text_author = []
        else:
            self.text_author = text_author
        self.date = date
    def factory(*args_, **kwargs_):
        if poemType.subclass:
            return poemType.subclass(*args_, **kwargs_)
        else:
            return poemType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getTitle(self): return self.title
    def setTitle(self, title): self.title = title
    def getEpigraph(self): return self.epigraph
    def setEpigraph(self, epigraph): self.epigraph = epigraph
    def addEpigraph(self, value): self.epigraph.append(value)
    def insertEpigraph(self, index, value): self.epigraph[index] = value
    def getStanza(self): return self.stanza
    def setStanza(self, stanza): self.stanza = stanza
    def addStanza(self, value): self.stanza.append(value)
    def insertStanza(self, index, value): self.stanza[index] = value
    def getText_author(self): return self.text_author
    def setText_author(self, text_author): self.text_author = text_author
    def addText_author(self, value): self.text_author.append(value)
    def insertText_author(self, index, value): self.text_author[index] = value
    def getDate(self): return self.date
    def setDate(self, date): self.date = date
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def export(self, outfile, level, name_='poemType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='poemType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='poemType'):
        if self.getLang() is not None:
            outfile.write(' lang="%s"' % (self.getLang(), ))
        if self.getId() is not None:
            outfile.write(' id="%s"' % (self.getId(), ))
    def exportChildren(self, outfile, level, name_='poemType'):
        if self.title:
            self.title.export(outfile, level, name_='title')
        for epigraph_ in self.getEpigraph():
            epigraph_.export(outfile, level, name_='epigraph')
        for stanza_ in self.getStanza():
            stanza_.export(outfile, level)
        for text_author_ in self.getText_author():
            text_author_.export(outfile, level, name_='text_author')
        if self.date:
            self.date.export(outfile, level, name_='date')
    def exportLiteral(self, outfile, level, name_='poemType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('lang = "%s",\n' % (self.getLang(),))
        showIndent(outfile, level)
        outfile.write('id = "%s",\n' % (self.getId(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.title:
            showIndent(outfile, level)
            outfile.write('title=titleType(\n')
            self.title.exportLiteral(outfile, level, name_='title')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('epigraph=[\n')
        level += 1
        for epigraph in self.epigraph:
            showIndent(outfile, level)
            outfile.write('epigraphType(\n')
            epigraph.exportLiteral(outfile, level, name_='epigraph')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('stanza=[\n')
        level += 1
        for stanza in self.stanza:
            showIndent(outfile, level)
            outfile.write('stanza(\n')
            stanza.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('text_author=[\n')
        level += 1
        for text_author in self.text_author:
            showIndent(outfile, level)
            outfile.write('pType(\n')
            text_author.exportLiteral(outfile, level, name_='text_author')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.date:
            showIndent(outfile, level)
            outfile.write('date=dateType(\n')
            self.date.exportLiteral(outfile, level, name_='date')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('lang'):
            self.lang = attrs.get('lang').value
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'title':
            obj_ = titleType.factory()
            obj_.build(child_)
            self.setTitle(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'epigraph':
            obj_ = epigraphType.factory()
            obj_.build(child_)
            self.epigraph.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'stanza':
            obj_ = stanza.factory()
            obj_.build(child_)
            self.stanza.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'text-author':
            obj_ = pType.factory()
            obj_.build(child_)
            self.text_author.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'date':
            obj_ = dateType.factory()
            obj_.build(child_)
            self.setDate(obj_)
# end class poemType


class stanza:
    subclass = None
    def __init__(self, lang='', title=None, subtitle=None, v=None):
        self.lang = lang
        self.title = title
        self.subtitle = subtitle
        if v is None:
            self.v = []
        else:
            self.v = v
    def factory(*args_, **kwargs_):
        if stanza.subclass:
            return stanza.subclass(*args_, **kwargs_)
        else:
            return stanza(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getTitle(self): return self.title
    def setTitle(self, title): self.title = title
    def getSubtitle(self): return self.subtitle
    def setSubtitle(self, subtitle): self.subtitle = subtitle
    def getV(self): return self.v
    def setV(self, v): self.v = v
    def addV(self, value): self.v.append(value)
    def insertV(self, index, value): self.v[index] = value
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def export(self, outfile, level, name_='stanza'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='stanza')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='stanza'):
        if self.getLang() is not None:
            outfile.write(' lang="%s"' % (self.getLang(), ))
    def exportChildren(self, outfile, level, name_='stanza'):
        if self.title:
            self.title.export(outfile, level, name_='title')
        if self.subtitle:
            self.subtitle.export(outfile, level, name_='subtitle')
        for v_ in self.getV():
            v_.export(outfile, level, name_='v')
    def exportLiteral(self, outfile, level, name_='stanza'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('lang = "%s",\n' % (self.getLang(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.title:
            showIndent(outfile, level)
            outfile.write('title=titleType(\n')
            self.title.exportLiteral(outfile, level, name_='title')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.subtitle:
            showIndent(outfile, level)
            outfile.write('subtitle=pType(\n')
            self.subtitle.exportLiteral(outfile, level, name_='subtitle')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('v=[\n')
        level += 1
        for v in self.v:
            showIndent(outfile, level)
            outfile.write('pType(\n')
            v.exportLiteral(outfile, level, name_='v')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('lang'):
            self.lang = attrs.get('lang').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'title':
            obj_ = titleType.factory()
            obj_.build(child_)
            self.setTitle(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'subtitle':
            obj_ = pType.factory()
            obj_.build(child_)
            self.setSubtitle(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'v':
            obj_ = pType.factory()
            obj_.build(child_)
            self.v.append(obj_)
# end class stanza


class epigraphType:
    subclass = None
    def __init__(self, id='', p=None, poem=None, cite=None, empty_line='', text_author=None):
        self.id = id
        self.p = p
        self.poem = poem
        self.cite = cite
        self.empty_line = empty_line
        if text_author is None:
            self.text_author = []
        else:
            self.text_author = text_author
    def factory(*args_, **kwargs_):
        if epigraphType.subclass:
            return epigraphType.subclass(*args_, **kwargs_)
        else:
            return epigraphType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getP(self): return self.p
    def setP(self, p): self.p = p
    def getPoem(self): return self.poem
    def setPoem(self, poem): self.poem = poem
    def getCite(self): return self.cite
    def setCite(self, cite): self.cite = cite
    def getEmpty_line(self): return self.empty_line
    def setEmpty_line(self, empty_line): self.empty_line = empty_line
    def getText_author(self): return self.text_author
    def setText_author(self, text_author): self.text_author = text_author
    def addText_author(self, value): self.text_author.append(value)
    def insertText_author(self, index, value): self.text_author[index] = value
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def export(self, outfile, level, name_='epigraphType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='epigraphType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='epigraphType'):
        if self.getId() is not None:
            outfile.write(' id="%s"' % (self.getId(), ))
    def exportChildren(self, outfile, level, name_='epigraphType'):
        if self.p:
            self.p.export(outfile, level, name_='p')
        if self.poem:
            self.poem.export(outfile, level, name_='poem')
        if self.cite:
            self.cite.export(outfile, level, name_='cite')
        showIndent(outfile, level)
        outfile.write('<empty-line>%s</empty-line>\n' % quote_xml(self.getEmpty_line()))
        for text_author_ in self.getText_author():
            text_author_.export(outfile, level, name_='text_author')
    def exportLiteral(self, outfile, level, name_='epigraphType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('id = "%s",\n' % (self.getId(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.p:
            showIndent(outfile, level)
            outfile.write('p=pType(\n')
            self.p.exportLiteral(outfile, level, name_='p')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.poem:
            showIndent(outfile, level)
            outfile.write('poem=poemType(\n')
            self.poem.exportLiteral(outfile, level, name_='poem')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.cite:
            showIndent(outfile, level)
            outfile.write('cite=citeType(\n')
            self.cite.exportLiteral(outfile, level, name_='cite')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('empty_line=%s,\n' % quote_python(self.getEmpty_line()))
        showIndent(outfile, level)
        outfile.write('text_author=[\n')
        level += 1
        for text_author in self.text_author:
            showIndent(outfile, level)
            outfile.write('pType(\n')
            text_author.exportLiteral(outfile, level, name_='text_author')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'p':
            obj_ = pType.factory()
            obj_.build(child_)
            self.setP(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'poem':
            obj_ = poemType.factory()
            obj_.build(child_)
            self.setPoem(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'cite':
            obj_ = citeType.factory()
            obj_.build(child_)
            self.setCite(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'empty-line':
            empty_line_ = ''
            for text__content_ in child_.childNodes:
                empty_line_ += text__content_.nodeValue
            self.empty_line = empty_line_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'text-author':
            obj_ = pType.factory()
            obj_.build(child_)
            self.text_author.append(obj_)
# end class epigraphType


class annotationType:
    subclass = None
    def __init__(self, lang='', id='', p=None, poem=None, cite=None, subtitle=None, table=None, empty_line=''):
        self.lang = lang
        self.id = id
        self.p = p
        self.poem = poem
        self.cite = cite
        self.subtitle = subtitle
        self.table = table
        self.empty_line = empty_line
    def factory(*args_, **kwargs_):
        if annotationType.subclass:
            return annotationType.subclass(*args_, **kwargs_)
        else:
            return annotationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getP(self): return self.p
    def setP(self, p): self.p = p
    def getPoem(self): return self.poem
    def setPoem(self, poem): self.poem = poem
    def getCite(self): return self.cite
    def setCite(self, cite): self.cite = cite
    def getSubtitle(self): return self.subtitle
    def setSubtitle(self, subtitle): self.subtitle = subtitle
    def getTable(self): return self.table
    def setTable(self, table): self.table = table
    def getEmpty_line(self): return self.empty_line
    def setEmpty_line(self, empty_line): self.empty_line = empty_line
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def export(self, outfile, level, name_='annotationType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='annotationType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='annotationType'):
        if self.getLang() is not None:
            outfile.write(' lang="%s"' % (self.getLang(), ))
        if self.getId() is not None:
            outfile.write(' id="%s"' % (self.getId(), ))
    def exportChildren(self, outfile, level, name_='annotationType'):
        if self.p:
            self.p.export(outfile, level, name_='p')
        if self.poem:
            self.poem.export(outfile, level, name_='poem')
        if self.cite:
            self.cite.export(outfile, level, name_='cite')
        if self.subtitle:
            self.subtitle.export(outfile, level, name_='subtitle')
        if self.table:
            self.table.export(outfile, level, name_='table')
        showIndent(outfile, level)
        outfile.write('<empty-line>%s</empty-line>\n' % quote_xml(self.getEmpty_line()))
    def exportLiteral(self, outfile, level, name_='annotationType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('lang = "%s",\n' % (self.getLang(),))
        showIndent(outfile, level)
        outfile.write('id = "%s",\n' % (self.getId(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.p:
            showIndent(outfile, level)
            outfile.write('p=pType(\n')
            self.p.exportLiteral(outfile, level, name_='p')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.poem:
            showIndent(outfile, level)
            outfile.write('poem=poemType(\n')
            self.poem.exportLiteral(outfile, level, name_='poem')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.cite:
            showIndent(outfile, level)
            outfile.write('cite=citeType(\n')
            self.cite.exportLiteral(outfile, level, name_='cite')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.subtitle:
            showIndent(outfile, level)
            outfile.write('subtitle=pType(\n')
            self.subtitle.exportLiteral(outfile, level, name_='subtitle')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.table:
            showIndent(outfile, level)
            outfile.write('table=tableType(\n')
            self.table.exportLiteral(outfile, level, name_='table')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('empty_line=%s,\n' % quote_python(self.getEmpty_line()))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('lang'):
            self.lang = attrs.get('lang').value
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'p':
            obj_ = pType.factory()
            obj_.build(child_)
            self.setP(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'poem':
            obj_ = poemType.factory()
            obj_.build(child_)
            self.setPoem(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'cite':
            obj_ = citeType.factory()
            obj_.build(child_)
            self.setCite(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'subtitle':
            obj_ = pType.factory()
            obj_.build(child_)
            self.setSubtitle(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'table':
            obj_ = tableType.factory()
            obj_.build(child_)
            self.setTable(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'empty-line':
            empty_line_ = ''
            for text__content_ in child_.childNodes:
                empty_line_ += text__content_.nodeValue
            self.empty_line = empty_line_
# end class annotationType


class sectionType:
    subclass = None
    def __init__(self, lang='', id='', title=None, epigraph=None, image=None, annotation=None, section=None, p=None, poem=None, subtitle=None, cite=None, empty_line='', table=None, p=None, image=None, poem=None, subtitle=None, cite=None, empty_line='', table=None):
        self.lang = lang
        self.id = id
        self.title = title
        if epigraph is None:
            self.epigraph = []
        else:
            self.epigraph = epigraph
        self.image = image
        self.annotation = annotation
        if section is None:
            self.section = []
        else:
            self.section = section
        self.p = p
        self.poem = poem
        self.subtitle = subtitle
        self.cite = cite
        self.empty_line = empty_line
        self.table = table
        self.p = p
        self.image = image
        self.poem = poem
        self.subtitle = subtitle
        self.cite = cite
        self.empty_line = empty_line
        self.table = table
    def factory(*args_, **kwargs_):
        if sectionType.subclass:
            return sectionType.subclass(*args_, **kwargs_)
        else:
            return sectionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getTitle(self): return self.title
    def setTitle(self, title): self.title = title
    def getEpigraph(self): return self.epigraph
    def setEpigraph(self, epigraph): self.epigraph = epigraph
    def addEpigraph(self, value): self.epigraph.append(value)
    def insertEpigraph(self, index, value): self.epigraph[index] = value
    def getImage(self): return self.image
    def setImage(self, image): self.image = image
    def getAnnotation(self): return self.annotation
    def setAnnotation(self, annotation): self.annotation = annotation
    def getSection(self): return self.section
    def setSection(self, section): self.section = section
    def addSection(self, value): self.section.append(value)
    def insertSection(self, index, value): self.section[index] = value
    def getP(self): return self.p
    def setP(self, p): self.p = p
    def getPoem(self): return self.poem
    def setPoem(self, poem): self.poem = poem
    def getSubtitle(self): return self.subtitle
    def setSubtitle(self, subtitle): self.subtitle = subtitle
    def getCite(self): return self.cite
    def setCite(self, cite): self.cite = cite
    def getEmpty_line(self): return self.empty_line
    def setEmpty_line(self, empty_line): self.empty_line = empty_line
    def getTable(self): return self.table
    def setTable(self, table): self.table = table
    def getP(self): return self.p
    def setP(self, p): self.p = p
    def getImage(self): return self.image
    def setImage(self, image): self.image = image
    def getPoem(self): return self.poem
    def setPoem(self, poem): self.poem = poem
    def getSubtitle(self): return self.subtitle
    def setSubtitle(self, subtitle): self.subtitle = subtitle
    def getCite(self): return self.cite
    def setCite(self, cite): self.cite = cite
    def getEmpty_line(self): return self.empty_line
    def setEmpty_line(self, empty_line): self.empty_line = empty_line
    def getTable(self): return self.table
    def setTable(self, table): self.table = table
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def export(self, outfile, level, name_='sectionType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='sectionType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='sectionType'):
        if self.getLang() is not None:
            outfile.write(' lang="%s"' % (self.getLang(), ))
        if self.getId() is not None:
            outfile.write(' id="%s"' % (self.getId(), ))
    def exportChildren(self, outfile, level, name_='sectionType'):
        if self.title:
            self.title.export(outfile, level, name_='title')
        for epigraph_ in self.getEpigraph():
            epigraph_.export(outfile, level, name_='epigraph')
        if self.image:
            self.image.export(outfile, level, name_='image')
        if self.annotation:
            self.annotation.export(outfile, level, name_='annotation')
        for section_ in self.getSection():
            section_.export(outfile, level, name_='section')
        if self.p:
            self.p.export(outfile, level, name_='p')
        if self.poem:
            self.poem.export(outfile, level, name_='poem')
        if self.subtitle:
            self.subtitle.export(outfile, level, name_='subtitle')
        if self.cite:
            self.cite.export(outfile, level, name_='cite')
        showIndent(outfile, level)
        outfile.write('<empty-line>%s</empty-line>\n' % quote_xml(self.getEmpty_line()))
        if self.table:
            self.table.export(outfile, level, name_='table')
        if self.p:
            self.p.export(outfile, level, name_='p')
        if self.image:
            self.image.export(outfile, level, name_='image')
        if self.poem:
            self.poem.export(outfile, level, name_='poem')
        if self.subtitle:
            self.subtitle.export(outfile, level, name_='subtitle')
        if self.cite:
            self.cite.export(outfile, level, name_='cite')
        showIndent(outfile, level)
        outfile.write('<empty-line>%s</empty-line>\n' % quote_xml(self.getEmpty_line()))
        if self.table:
            self.table.export(outfile, level, name_='table')
    def exportLiteral(self, outfile, level, name_='sectionType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('lang = "%s",\n' % (self.getLang(),))
        showIndent(outfile, level)
        outfile.write('id = "%s",\n' % (self.getId(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.title:
            showIndent(outfile, level)
            outfile.write('title=titleType(\n')
            self.title.exportLiteral(outfile, level, name_='title')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('epigraph=[\n')
        level += 1
        for epigraph in self.epigraph:
            showIndent(outfile, level)
            outfile.write('epigraphType(\n')
            epigraph.exportLiteral(outfile, level, name_='epigraph')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.image:
            showIndent(outfile, level)
            outfile.write('image=imageType(\n')
            self.image.exportLiteral(outfile, level, name_='image')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.annotation:
            showIndent(outfile, level)
            outfile.write('annotation=annotationType(\n')
            self.annotation.exportLiteral(outfile, level, name_='annotation')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('section=[\n')
        level += 1
        for section in self.section:
            showIndent(outfile, level)
            outfile.write('sectionType(\n')
            section.exportLiteral(outfile, level, name_='section')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.p:
            showIndent(outfile, level)
            outfile.write('p=pType(\n')
            self.p.exportLiteral(outfile, level, name_='p')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.poem:
            showIndent(outfile, level)
            outfile.write('poem=poemType(\n')
            self.poem.exportLiteral(outfile, level, name_='poem')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.subtitle:
            showIndent(outfile, level)
            outfile.write('subtitle=pType(\n')
            self.subtitle.exportLiteral(outfile, level, name_='subtitle')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.cite:
            showIndent(outfile, level)
            outfile.write('cite=citeType(\n')
            self.cite.exportLiteral(outfile, level, name_='cite')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('empty_line=%s,\n' % quote_python(self.getEmpty_line()))
        if self.table:
            showIndent(outfile, level)
            outfile.write('table=tableType(\n')
            self.table.exportLiteral(outfile, level, name_='table')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.p:
            showIndent(outfile, level)
            outfile.write('p=pType(\n')
            self.p.exportLiteral(outfile, level, name_='p')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.image:
            showIndent(outfile, level)
            outfile.write('image=imageType(\n')
            self.image.exportLiteral(outfile, level, name_='image')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.poem:
            showIndent(outfile, level)
            outfile.write('poem=poemType(\n')
            self.poem.exportLiteral(outfile, level, name_='poem')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.subtitle:
            showIndent(outfile, level)
            outfile.write('subtitle=pType(\n')
            self.subtitle.exportLiteral(outfile, level, name_='subtitle')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.cite:
            showIndent(outfile, level)
            outfile.write('cite=citeType(\n')
            self.cite.exportLiteral(outfile, level, name_='cite')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('empty_line=%s,\n' % quote_python(self.getEmpty_line()))
        if self.table:
            showIndent(outfile, level)
            outfile.write('table=tableType(\n')
            self.table.exportLiteral(outfile, level, name_='table')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('lang'):
            self.lang = attrs.get('lang').value
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'title':
            obj_ = titleType.factory()
            obj_.build(child_)
            self.setTitle(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'epigraph':
            obj_ = epigraphType.factory()
            obj_.build(child_)
            self.epigraph.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'image':
            obj_ = imageType.factory()
            obj_.build(child_)
            self.setImage(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'annotation':
            obj_ = annotationType.factory()
            obj_.build(child_)
            self.setAnnotation(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'section':
            obj_ = sectionType.factory()
            obj_.build(child_)
            self.section.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'p':
            obj_ = pType.factory()
            obj_.build(child_)
            self.setP(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'poem':
            obj_ = poemType.factory()
            obj_.build(child_)
            self.setPoem(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'subtitle':
            obj_ = pType.factory()
            obj_.build(child_)
            self.setSubtitle(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'cite':
            obj_ = citeType.factory()
            obj_.build(child_)
            self.setCite(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'empty-line':
            empty_line_ = ''
            for text__content_ in child_.childNodes:
                empty_line_ += text__content_.nodeValue
            self.empty_line = empty_line_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'table':
            obj_ = tableType.factory()
            obj_.build(child_)
            self.setTable(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'p':
            obj_ = pType.factory()
            obj_.build(child_)
            self.setP(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'image':
            obj_ = imageType.factory()
            obj_.build(child_)
            self.setImage(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'poem':
            obj_ = poemType.factory()
            obj_.build(child_)
            self.setPoem(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'subtitle':
            obj_ = pType.factory()
            obj_.build(child_)
            self.setSubtitle(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'cite':
            obj_ = citeType.factory()
            obj_.build(child_)
            self.setCite(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'empty-line':
            empty_line_ = ''
            for text__content_ in child_.childNodes:
                empty_line_ += text__content_.nodeValue
            self.empty_line = empty_line_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'table':
            obj_ = tableType.factory()
            obj_.build(child_)
            self.setTable(obj_)
# end class sectionType


class styleType:
    subclass = None
    def __init__(self, lang='', strong=None, emphasis=None, style=None, a=None, strikethrough=None, sub=None, sup=None, code=None, image=None, mixedclass_=None, content_=None):
        self.lang = lang
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if styleType.subclass:
            return styleType.subclass(*args_, **kwargs_)
        else:
            return styleType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getStrong(self): return self.strong
    def setStrong(self, strong): self.strong = strong
    def getEmphasis(self): return self.emphasis
    def setEmphasis(self, emphasis): self.emphasis = emphasis
    def getStyle(self): return self.style
    def setStyle(self, style): self.style = style
    def getA(self): return self.a
    def setA(self, a): self.a = a
    def getStrikethrough(self): return self.strikethrough
    def setStrikethrough(self, strikethrough): self.strikethrough = strikethrough
    def getSub(self): return self.sub
    def setSub(self, sub): self.sub = sub
    def getSup(self): return self.sup
    def setSup(self, sup): self.sup = sup
    def getCode(self): return self.code
    def setCode(self, code): self.code = code
    def getImage(self): return self.image
    def setImage(self, image): self.image = image
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def export(self, outfile, level, name_='styleType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='styleType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='styleType'):
        if self.getLang() is not None:
            outfile.write(' lang="%s"' % (self.getLang(), ))
    def exportChildren(self, outfile, level, name_='styleType'):
        for item_ in self.content_:
            item_.export(outfile, level, name_)
    def exportLiteral(self, outfile, level, name_='styleType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('lang = "%s",\n' % (self.getLang(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('lang'):
            self.lang = attrs.get('lang').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'strong':
            childobj_ = styleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'strong', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'emphasis':
            childobj_ = styleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'emphasis', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'style':
            childobj_ = namedStyleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'style', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'a':
            childobj_ = linkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'a', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'strikethrough':
            childobj_ = styleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'strikethrough', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sub':
            childobj_ = styleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sub', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sup':
            childobj_ = styleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sup', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'code':
            childobj_ = styleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'code', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'image':
            childobj_ = inlineImageType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'image', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class styleType


class namedStyleType:
    subclass = None
    def __init__(self, lang='', name='', strong=None, emphasis=None, style=None, a=None, strikethrough=None, sub=None, sup=None, code=None, image=None, mixedclass_=None, content_=None):
        self.lang = lang
        self.name = name
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if namedStyleType.subclass:
            return namedStyleType.subclass(*args_, **kwargs_)
        else:
            return namedStyleType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getStrong(self): return self.strong
    def setStrong(self, strong): self.strong = strong
    def getEmphasis(self): return self.emphasis
    def setEmphasis(self, emphasis): self.emphasis = emphasis
    def getStyle(self): return self.style
    def setStyle(self, style): self.style = style
    def getA(self): return self.a
    def setA(self, a): self.a = a
    def getStrikethrough(self): return self.strikethrough
    def setStrikethrough(self, strikethrough): self.strikethrough = strikethrough
    def getSub(self): return self.sub
    def setSub(self, sub): self.sub = sub
    def getSup(self): return self.sup
    def setSup(self, sup): self.sup = sup
    def getCode(self): return self.code
    def setCode(self, code): self.code = code
    def getImage(self): return self.image
    def setImage(self, image): self.image = image
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def getName(self): return self.name
    def setName(self, name): self.name = name
    def export(self, outfile, level, name_='namedStyleType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='namedStyleType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='namedStyleType'):
        if self.getLang() is not None:
            outfile.write(' lang="%s"' % (self.getLang(), ))
        outfile.write(' name="%s"' % (self.getName(), ))
    def exportChildren(self, outfile, level, name_='namedStyleType'):
        for item_ in self.content_:
            item_.export(outfile, level, name_)
    def exportLiteral(self, outfile, level, name_='namedStyleType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('lang = "%s",\n' % (self.getLang(),))
        showIndent(outfile, level)
        outfile.write('name = "%s",\n' % (self.getName(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('lang'):
            self.lang = attrs.get('lang').value
        if attrs.get('name'):
            self.name = attrs.get('name').value
            self.name = ' '.join(self.name.split())
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'strong':
            childobj_ = styleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'strong', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'emphasis':
            childobj_ = styleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'emphasis', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'style':
            childobj_ = namedStyleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'style', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'a':
            childobj_ = linkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'a', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'strikethrough':
            childobj_ = styleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'strikethrough', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sub':
            childobj_ = styleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sub', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sup':
            childobj_ = styleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sup', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'code':
            childobj_ = styleType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'code', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'image':
            childobj_ = inlineImageType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'image', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class namedStyleType


class linkType:
    subclass = None
    def __init__(self, href='', ttype='', strong=None, emphasis=None, style=None, strikethrough=None, sub=None, sup=None, code=None, image=None, mixedclass_=None, content_=None):
        self.href = href
        self.ttype = ttype
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if linkType.subclass:
            return linkType.subclass(*args_, **kwargs_)
        else:
            return linkType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getStrong(self): return self.strong
    def setStrong(self, strong): self.strong = strong
    def getEmphasis(self): return self.emphasis
    def setEmphasis(self, emphasis): self.emphasis = emphasis
    def getStyle(self): return self.style
    def setStyle(self, style): self.style = style
    def getStrikethrough(self): return self.strikethrough
    def setStrikethrough(self, strikethrough): self.strikethrough = strikethrough
    def getSub(self): return self.sub
    def setSub(self, sub): self.sub = sub
    def getSup(self): return self.sup
    def setSup(self, sup): self.sup = sup
    def getCode(self): return self.code
    def setCode(self, code): self.code = code
    def getImage(self): return self.image
    def setImage(self, image): self.image = image
    def getHref(self): return self.href
    def setHref(self, href): self.href = href
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
    def export(self, outfile, level, name_='linkType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='linkType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='linkType'):
        outfile.write(' href="%s"' % (self.getHref(), ))
        if self.getType() is not None:
            outfile.write(' type="%s"' % (self.getType(), ))
    def exportChildren(self, outfile, level, name_='linkType'):
        for item_ in self.content_:
            item_.export(outfile, level, name_)
    def exportLiteral(self, outfile, level, name_='linkType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('href = "%s",\n' % (self.getHref(),))
        showIndent(outfile, level)
        outfile.write('ttype = "%s",\n' % (self.getType(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('href'):
            self.href = attrs.get('href').value
        if attrs.get('type'):
            self.ttype = attrs.get('type').value
            self.ttype = ' '.join(self.ttype.split())
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'strong':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'strong', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'emphasis':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'emphasis', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'style':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'style', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'strikethrough':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'strikethrough', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sub':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sub', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sup':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sup', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'code':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'code', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'image':
            childobj_ = inlineImageType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'image', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class linkType


class styleLinkType:
    subclass = None
    def __init__(self, strong=None, emphasis=None, style=None, strikethrough=None, sub=None, sup=None, code=None, image=None, mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if styleLinkType.subclass:
            return styleLinkType.subclass(*args_, **kwargs_)
        else:
            return styleLinkType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getStrong(self): return self.strong
    def setStrong(self, strong): self.strong = strong
    def getEmphasis(self): return self.emphasis
    def setEmphasis(self, emphasis): self.emphasis = emphasis
    def getStyle(self): return self.style
    def setStyle(self, style): self.style = style
    def getStrikethrough(self): return self.strikethrough
    def setStrikethrough(self, strikethrough): self.strikethrough = strikethrough
    def getSub(self): return self.sub
    def setSub(self, sub): self.sub = sub
    def getSup(self): return self.sup
    def setSup(self, sup): self.sup = sup
    def getCode(self): return self.code
    def setCode(self, code): self.code = code
    def getImage(self): return self.image
    def setImage(self, image): self.image = image
    def export(self, outfile, level, name_='styleLinkType'):
        showIndent(outfile, level)
        outfile.write('<%s>' % name_)
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='styleLinkType'):
        pass
    def exportChildren(self, outfile, level, name_='styleLinkType'):
        for item_ in self.content_:
            item_.export(outfile, level, name_)
    def exportLiteral(self, outfile, level, name_='styleLinkType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('content_ = [\n')
        for item_ in self.content_:
            item_.exportLiteral(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'strong':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'strong', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'emphasis':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'emphasis', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'style':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'style', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'strikethrough':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'strikethrough', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sub':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sub', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sup':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'sup', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'code':
            childobj_ = styleLinkType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'code', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'image':
            childobj_ = inlineImageType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'image', childobj_)
            self.content_.append(obj_)
        elif child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
# end class styleLinkType


class sequenceType:
    subclass = None
    def __init__(self, lang='', name='', number=-1, sequence=None):
        self.lang = lang
        self.name = name
        self.number = number
        if sequence is None:
            self.sequence = []
        else:
            self.sequence = sequence
    def factory(*args_, **kwargs_):
        if sequenceType.subclass:
            return sequenceType.subclass(*args_, **kwargs_)
        else:
            return sequenceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getSequence(self): return self.sequence
    def setSequence(self, sequence): self.sequence = sequence
    def addSequence(self, value): self.sequence.append(value)
    def insertSequence(self, index, value): self.sequence[index] = value
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def getName(self): return self.name
    def setName(self, name): self.name = name
    def getNumber(self): return self.number
    def setNumber(self, number): self.number = number
    def export(self, outfile, level, name_='sequenceType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='sequenceType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='sequenceType'):
        if self.getLang() is not None:
            outfile.write(' lang="%s"' % (self.getLang(), ))
        outfile.write(' name="%s"' % (self.getName(), ))
        if self.getNumber() is not None:
            outfile.write(' number="%s"' % (self.getNumber(), ))
    def exportChildren(self, outfile, level, name_='sequenceType'):
        for sequence_ in self.getSequence():
            sequence_.export(outfile, level, name_='sequence')
    def exportLiteral(self, outfile, level, name_='sequenceType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('lang = "%s",\n' % (self.getLang(),))
        showIndent(outfile, level)
        outfile.write('name = "%s",\n' % (self.getName(),))
        showIndent(outfile, level)
        outfile.write('number = "%s",\n' % (self.getNumber(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('sequence=[\n')
        level += 1
        for sequence in self.sequence:
            showIndent(outfile, level)
            outfile.write('sequenceType(\n')
            sequence.exportLiteral(outfile, level, name_='sequence')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('lang'):
            self.lang = attrs.get('lang').value
        if attrs.get('name'):
            self.name = attrs.get('name').value
        if attrs.get('number'):
            try:
                self.number = int(attrs.get('number').value)
            except ValueError:
                raise ValueError('Bad integer attribute (number)')
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sequence':
            obj_ = sequenceType.factory()
            obj_.build(child_)
            self.sequence.append(obj_)
# end class sequenceType


class tableType:
    subclass = None
    def __init__(self, style='', id='', tr=None):
        self.style = style
        self.id = id
        if tr is None:
            self.tr = []
        else:
            self.tr = tr
    def factory(*args_, **kwargs_):
        if tableType.subclass:
            return tableType.subclass(*args_, **kwargs_)
        else:
            return tableType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getTr(self): return self.tr
    def setTr(self, tr): self.tr = tr
    def addTr(self, value): self.tr.append(value)
    def insertTr(self, index, value): self.tr[index] = value
    def getStyle(self): return self.style
    def setStyle(self, style): self.style = style
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def export(self, outfile, level, name_='tableType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='tableType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='tableType'):
        if self.getStyle() is not None:
            outfile.write(' style="%s"' % (self.getStyle(), ))
        if self.getId() is not None:
            outfile.write(' id="%s"' % (self.getId(), ))
    def exportChildren(self, outfile, level, name_='tableType'):
        for tr_ in self.getTr():
            tr_.export(outfile, level)
    def exportLiteral(self, outfile, level, name_='tableType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('style = "%s",\n' % (self.getStyle(),))
        showIndent(outfile, level)
        outfile.write('id = "%s",\n' % (self.getId(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('tr=[\n')
        level += 1
        for tr in self.tr:
            showIndent(outfile, level)
            outfile.write('tr(\n')
            tr.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('style'):
            self.style = attrs.get('style').value
        if attrs.get('id'):
            self.id = attrs.get('id').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'tr':
            obj_ = tr.factory()
            obj_.build(child_)
            self.tr.append(obj_)
# end class tableType


class tr:
    subclass = None
    def __init__(self, align=None, th=None, td=None):
        self.align = align
        self.th = th
        self.td = td
    def factory(*args_, **kwargs_):
        if tr.subclass:
            return tr.subclass(*args_, **kwargs_)
        else:
            return tr(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getTh(self): return self.th
    def setTh(self, th): self.th = th
    def getTd(self): return self.td
    def setTd(self, td): self.td = td
    def getAlign(self): return self.align
    def setAlign(self, align): self.align = align
    def export(self, outfile, level, name_='tr'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='tr')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='tr'):
        if self.getAlign() is not None:
            outfile.write(' align="%s"' % (self.getAlign(), ))
    def exportChildren(self, outfile, level, name_='tr'):
        if self.th:
            self.th.export(outfile, level, name_='th')
        if self.td:
            self.td.export(outfile, level, name_='td')
    def exportLiteral(self, outfile, level, name_='tr'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('align = "%s",\n' % (self.getAlign(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.th:
            showIndent(outfile, level)
            outfile.write('th=tdType(\n')
            self.th.exportLiteral(outfile, level, name_='th')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.td:
            showIndent(outfile, level)
            outfile.write('td=tdType(\n')
            self.td.exportLiteral(outfile, level, name_='td')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('align'):
            self.align = attrs.get('align').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'th':
            obj_ = tdType.factory()
            obj_.build(child_)
            self.setTh(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'td':
            obj_ = tdType.factory()
            obj_.build(child_)
            self.setTd(obj_)
# end class tr


class title_infoType:
    subclass = None
    def __init__(self, genre=None, author=None, book_title=None, annotation=None, keywords=None, date=None, coverpage=None, lang='', src_lang='', translator=None, sequence=None):
        if genre is None:
            self.genre = []
        else:
            self.genre = genre
        if author is None:
            self.author = []
        else:
            self.author = author
        self.book_title = book_title
        self.annotation = annotation
        self.keywords = keywords
        self.date = date
        self.coverpage = coverpage
        self.lang = lang
        self.src_lang = src_lang
        if translator is None:
            self.translator = []
        else:
            self.translator = translator
        if sequence is None:
            self.sequence = []
        else:
            self.sequence = sequence
    def factory(*args_, **kwargs_):
        if title_infoType.subclass:
            return title_infoType.subclass(*args_, **kwargs_)
        else:
            return title_infoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getGenre(self): return self.genre
    def setGenre(self, genre): self.genre = genre
    def addGenre(self, value): self.genre.append(value)
    def insertGenre(self, index, value): self.genre[index] = value
    def getAuthor(self): return self.author
    def setAuthor(self, author): self.author = author
    def addAuthor(self, value): self.author.append(value)
    def insertAuthor(self, index, value): self.author[index] = value
    def getBook_title(self): return self.book_title
    def setBook_title(self, book_title): self.book_title = book_title
    def getAnnotation(self): return self.annotation
    def setAnnotation(self, annotation): self.annotation = annotation
    def getKeywords(self): return self.keywords
    def setKeywords(self, keywords): self.keywords = keywords
    def getDate(self): return self.date
    def setDate(self, date): self.date = date
    def getCoverpage(self): return self.coverpage
    def setCoverpage(self, coverpage): self.coverpage = coverpage
    def getLang(self): return self.lang
    def setLang(self, lang): self.lang = lang
    def getSrc_lang(self): return self.src_lang
    def setSrc_lang(self, src_lang): self.src_lang = src_lang
    def getTranslator(self): return self.translator
    def setTranslator(self, translator): self.translator = translator
    def addTranslator(self, value): self.translator.append(value)
    def insertTranslator(self, index, value): self.translator[index] = value
    def getSequence(self): return self.sequence
    def setSequence(self, sequence): self.sequence = sequence
    def addSequence(self, value): self.sequence.append(value)
    def insertSequence(self, index, value): self.sequence[index] = value
    def export(self, outfile, level, name_='title-infoType'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='title-infoType'):
        pass
    def exportChildren(self, outfile, level, name_='title-infoType'):
        for genre_ in self.getGenre():
            genre_.export(outfile, level)
        for author_ in self.getAuthor():
            author_.export(outfile, level)
        if self.book_title:
            self.book_title.export(outfile, level, name_='book-title')
        if self.annotation:
            self.annotation.export(outfile, level, name_='annotation')
        if self.keywords:
            self.keywords.export(outfile, level, name_='keywords')
        if self.date:
            self.date.export(outfile, level, name_='date')
        if self.coverpage:
            self.coverpage.export(outfile, level)
        showIndent(outfile, level)
        outfile.write('<lang>%s</lang>\n' % quote_xml(self.getLang()))
        showIndent(outfile, level)
        outfile.write('<src-lang>%s</src-lang>\n' % quote_xml(self.getSrc_lang()))
        for translator_ in self.getTranslator():
            translator_.export(outfile, level, name_='translator')
        for sequence_ in self.getSequence():
            sequence_.export(outfile, level, name_='sequence')
    def exportLiteral(self, outfile, level, name_='title-infoType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('genre=[\n')
        level += 1
        for genre in self.genre:
            showIndent(outfile, level)
            outfile.write('genre(\n')
            genre.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('author=[\n')
        level += 1
        for author in self.author:
            showIndent(outfile, level)
            outfile.write('author(\n')
            author.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.book_title:
            showIndent(outfile, level)
            outfile.write('book_title=textFieldType(\n')
            self.book_title.exportLiteral(outfile, level, name_='book_title')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.annotation:
            showIndent(outfile, level)
            outfile.write('annotation=annotationType(\n')
            self.annotation.exportLiteral(outfile, level, name_='annotation')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.keywords:
            showIndent(outfile, level)
            outfile.write('keywords=textFieldType(\n')
            self.keywords.exportLiteral(outfile, level, name_='keywords')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.date:
            showIndent(outfile, level)
            outfile.write('date=dateType(\n')
            self.date.exportLiteral(outfile, level, name_='date')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.coverpage:
            showIndent(outfile, level)
            outfile.write('coverpage=coverpage(\n')
            self.coverpage.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('lang=%s,\n' % quote_python(self.getLang()))
        showIndent(outfile, level)
        outfile.write('src_lang=%s,\n' % quote_python(self.getSrc_lang()))
        showIndent(outfile, level)
        outfile.write('translator=[\n')
        level += 1
        for translator in self.translator:
            showIndent(outfile, level)
            outfile.write('authorType(\n')
            translator.exportLiteral(outfile, level, name_='translator')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('sequence=[\n')
        level += 1
        for sequence in self.sequence:
            showIndent(outfile, level)
            outfile.write('sequenceType(\n')
            sequence.exportLiteral(outfile, level, name_='sequence')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'genre':
            obj_ = genre.factory()
            obj_.build(child_)
            self.genre.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'author':
            obj_ = author.factory()
            obj_.build(child_)
            self.author.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'book-title':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setBook_title(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'annotation':
            obj_ = annotationType.factory()
            obj_.build(child_)
            self.setAnnotation(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'keywords':
            obj_ = textFieldType.factory()
            obj_.build(child_)
            self.setKeywords(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'date':
            obj_ = dateType.factory()
            obj_.build(child_)
            self.setDate(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'coverpage':
            obj_ = coverpage.factory()
            obj_.build(child_)
            self.setCoverpage(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'lang':
            lang_ = ''
            for text__content_ in child_.childNodes:
                lang_ += text__content_.nodeValue
            self.lang = lang_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'src-lang':
            src_lang_ = ''
            for text__content_ in child_.childNodes:
                src_lang_ += text__content_.nodeValue
            self.src_lang = src_lang_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'translator':
            obj_ = authorType.factory()
            obj_.build(child_)
            self.translator.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sequence':
            obj_ = sequenceType.factory()
            obj_.build(child_)
            self.sequence.append(obj_)
# end class title_infoType


class genre(genreType):
    subclass = None
    def __init__(self, match=-1, valueOf_=''):
        self.match = match
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if genre.subclass:
            return genre.subclass(*args_, **kwargs_)
        else:
            return genre(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getMatch(self): return self.match
    def setMatch(self, match): self.match = match
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='genre'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='genre')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='genre'):
        if self.getMatch() is not None:
            outfile.write(' match="%s"' % (self.getMatch(), ))
        genreType.exportAttributes(self, outfile, level, name_='genre')
    def exportChildren(self, outfile, level, name_='genre'):
        genreType.exportChildren(self, outfile, level, name_)
        outfile.write(self.valueOf_)
    def exportLiteral(self, outfile, level, name_='genre'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('match = "%s",\n' % (self.getMatch(),))
        genreType.exportLiteralAttributes(self, outfile, level, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
        genreType.exportLiteralChildren(self, outfile, level, name_)
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('match'):
            try:
                self.match = int(attrs.get('match').value)
            except ValueError:
                raise ValueError('Bad integer attribute (match)')
        genreType.buildAttributes(self, attrs)
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class genre


class author(authorType):
    subclass = None
    def __init__(self, first_name=None, middle_name=None, last_name=None, nickname=None, home_page=None, email=None, nickname=None, home_page=None, email=None, valueOf_=''):
        authorType.__init__(self, first_name, middle_name, last_name, nickname, home_page, email, nickname, home_page, email)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if author.subclass:
            return author.subclass(*args_, **kwargs_)
        else:
            return author(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='author'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='author'):
        authorType.exportAttributes(self, outfile, level, name_='author')
    def exportChildren(self, outfile, level, name_='author'):
        authorType.exportChildren(self, outfile, level, name_)
    def exportLiteral(self, outfile, level, name_='author'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
        authorType.exportLiteralAttributes(self, outfile, level, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
        authorType.exportLiteralChildren(self, outfile, level, name_)
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        authorType.buildAttributes(self, attrs)
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
        authorType.buildChildren(self, child_, nodeName_)
# end class author


class coverpage:
    subclass = None
    def __init__(self, image=None):
        if image is None:
            self.image = []
        else:
            self.image = image
    def factory(*args_, **kwargs_):
        if coverpage.subclass:
            return coverpage.subclass(*args_, **kwargs_)
        else:
            return coverpage(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getImage(self): return self.image
    def setImage(self, image): self.image = image
    def addImage(self, value): self.image.append(value)
    def insertImage(self, index, value): self.image[index] = value
    def export(self, outfile, level, name_='coverpage'):
        showIndent(outfile, level)
        outfile.write('<%s>\n' % name_)
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='coverpage'):
        pass
    def exportChildren(self, outfile, level, name_='coverpage'):
        for image_ in self.getImage():
            image_.export(outfile, level, name_='image')
    def exportLiteral(self, outfile, level, name_='coverpage'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('image=[\n')
        level += 1
        for image in self.image:
            showIndent(outfile, level)
            outfile.write('inlineImageType(\n')
            image.exportLiteral(outfile, level, name_='image')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'image':
            obj_ = inlineImageType.factory()
            obj_.build(child_)
            self.image.append(obj_)
# end class coverpage


class shareInstructionType:
    subclass = None
    def __init__(self, include_all=None, price=0.0, mode=None, currency='', part=None, output_document_class=None):
        self.include_all = include_all
        self.price = price
        self.mode = mode
        self.currency = currency
        self.part = part
        self.output_document_class = output_document_class
    def factory(*args_, **kwargs_):
        if shareInstructionType.subclass:
            return shareInstructionType.subclass(*args_, **kwargs_)
        else:
            return shareInstructionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getPart(self): return self.part
    def setPart(self, part): self.part = part
    def getOutput_document_class(self): return self.output_document_class
    def setOutput_document_class(self, output_document_class): self.output_document_class = output_document_class
    def getInclude_all(self): return self.include_all
    def setInclude_all(self, include_all): self.include_all = include_all
    def getPrice(self): return self.price
    def setPrice(self, price): self.price = price
    def getMode(self): return self.mode
    def setMode(self, mode): self.mode = mode
    def getCurrency(self): return self.currency
    def setCurrency(self, currency): self.currency = currency
    def export(self, outfile, level, name_='shareInstructionType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='shareInstructionType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='shareInstructionType'):
        outfile.write(' include-all="%s"' % (self.getInclude_all(), ))
        if self.getPrice() is not None:
            outfile.write(' price="%s"' % (self.getPrice(), ))
        outfile.write(' mode="%s"' % (self.getMode(), ))
        if self.getCurrency() is not None:
            outfile.write(' currency="%s"' % (self.getCurrency(), ))
    def exportChildren(self, outfile, level, name_='shareInstructionType'):
        if self.part:
            self.part.export(outfile, level, name_='part')
        if self.output_document_class:
            self.output_document_class.export(outfile, level, name_='output-document-class')
    def exportLiteral(self, outfile, level, name_='shareInstructionType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('include_all = "%s",\n' % (self.getInclude_all(),))
        showIndent(outfile, level)
        outfile.write('price = "%s",\n' % (self.getPrice(),))
        showIndent(outfile, level)
        outfile.write('mode = "%s",\n' % (self.getMode(),))
        showIndent(outfile, level)
        outfile.write('currency = "%s",\n' % (self.getCurrency(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.part:
            showIndent(outfile, level)
            outfile.write('part=partShareInstructionType(\n')
            self.part.exportLiteral(outfile, level, name_='part')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.output_document_class:
            showIndent(outfile, level)
            outfile.write('output_document_class=outPutDocumentType(\n')
            self.output_document_class.exportLiteral(outfile, level, name_='output_document_class')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('include-all'):
            self.include_all = attrs.get('include-all').value
        if attrs.get('price'):
            try:
                self.price = float(attrs.get('price').value)
            except:
                raise ValueError('Bad float/double attribute (price)')
        if attrs.get('mode'):
            self.mode = attrs.get('mode').value
        if attrs.get('currency'):
            self.currency = attrs.get('currency').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'part':
            obj_ = partShareInstructionType.factory()
            obj_.build(child_)
            self.setPart(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'output-document-class':
            obj_ = outPutDocumentType.factory()
            obj_.build(child_)
            self.setOutput_document_class(obj_)
# end class shareInstructionType


class partShareInstructionType:
    subclass = None
    def __init__(self, include=None, href='', ttype='', valueOf_=''):
        self.include = include
        self.href = href
        self.ttype = ttype
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if partShareInstructionType.subclass:
            return partShareInstructionType.subclass(*args_, **kwargs_)
        else:
            return partShareInstructionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getInclude(self): return self.include
    def setInclude(self, include): self.include = include
    def getHref(self): return self.href
    def setHref(self, href): self.href = href
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='partShareInstructionType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='partShareInstructionType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='partShareInstructionType'):
        outfile.write(' include="%s"' % (self.getInclude(), ))
        outfile.write(' href="%s"' % (self.getHref(), ))
        if self.getType() is not None:
            outfile.write(' type="%s"' % (self.getType(), ))
    def exportChildren(self, outfile, level, name_='partShareInstructionType'):
        outfile.write(self.valueOf_)
    def exportLiteral(self, outfile, level, name_='partShareInstructionType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('include = "%s",\n' % (self.getInclude(),))
        showIndent(outfile, level)
        outfile.write('href = "%s",\n' % (self.getHref(),))
        showIndent(outfile, level)
        outfile.write('ttype = "%s",\n' % (self.getType(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('include'):
            self.include = attrs.get('include').value
        if attrs.get('href'):
            self.href = attrs.get('href').value
        if attrs.get('type'):
            self.ttype = attrs.get('type').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class partShareInstructionType


class outPutDocumentType:
    subclass = None
    def __init__(self, price=0.0, create=None, name='', part=None):
        self.price = price
        self.create = create
        self.name = name
        self.part = part
    def factory(*args_, **kwargs_):
        if outPutDocumentType.subclass:
            return outPutDocumentType.subclass(*args_, **kwargs_)
        else:
            return outPutDocumentType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getPart(self): return self.part
    def setPart(self, part): self.part = part
    def getPrice(self): return self.price
    def setPrice(self, price): self.price = price
    def getCreate(self): return self.create
    def setCreate(self, create): self.create = create
    def getName(self): return self.name
    def setName(self, name): self.name = name
    def export(self, outfile, level, name_='outPutDocumentType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='outPutDocumentType')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='outPutDocumentType'):
        if self.getPrice() is not None:
            outfile.write(' price="%s"' % (self.getPrice(), ))
        if self.getCreate() is not None:
            outfile.write(' create="%s"' % (self.getCreate(), ))
        outfile.write(' name="%s"' % (self.getName(), ))
    def exportChildren(self, outfile, level, name_='outPutDocumentType'):
        if self.part:
            self.part.export(outfile, level, name_='part')
    def exportLiteral(self, outfile, level, name_='outPutDocumentType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('price = "%s",\n' % (self.getPrice(),))
        showIndent(outfile, level)
        outfile.write('create = "%s",\n' % (self.getCreate(),))
        showIndent(outfile, level)
        outfile.write('name = "%s",\n' % (self.getName(),))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.part:
            showIndent(outfile, level)
            outfile.write('part=partShareInstructionType(\n')
            self.part.exportLiteral(outfile, level, name_='part')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('price'):
            try:
                self.price = float(attrs.get('price').value)
            except:
                raise ValueError('Bad float/double attribute (price)')
        if attrs.get('create'):
            self.create = attrs.get('create').value
        if attrs.get('name'):
            self.name = attrs.get('name').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'part':
            obj_ = partShareInstructionType.factory()
            obj_.build(child_)
            self.setPart(obj_)
# end class outPutDocumentType


class tdType(styleType):
    subclass = None
    def __init__(self, rowspan=-1, colspan=-1, align=None, style_attr='', id='', lang='', strong=None, emphasis=None, style=None, a=None, strikethrough=None, sub=None, sup=None, code=None, image=None, valueOf_='', mixedclass_=None, content_=None):
        styleType.__init__(self, mixedclass_, content_)
        self.rowspan = rowspan
        self.colspan = colspan
        self.align = align
        self.style_attr = style_attr
        self.id = id
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if tdType.subclass:
            return tdType.subclass(*args_, **kwargs_)
        else:
            return tdType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getRowspan(self): return self.rowspan
    def setRowspan(self, rowspan): self.rowspan = rowspan
    def getColspan(self): return self.colspan
    def setColspan(self, colspan): self.colspan = colspan
    def getAlign(self): return self.align
    def setAlign(self, align): self.align = align
    def getStyle_attr(self): return self.style_attr
    def setStyle_attr(self, style_attr): self.style_attr = style_attr
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='tdType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='tdType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='tdType'):
        if self.getRowspan() is not None:
            outfile.write(' rowspan="%s"' % (self.getRowspan(), ))
        if self.getColspan() is not None:
            outfile.write(' colspan="%s"' % (self.getColspan(), ))
        if self.getAlign() is not None:
            outfile.write(' align="%s"' % (self.getAlign(), ))
        if self.getStyle_attr() is not None:
            outfile.write(' style_attr="%s"' % (self.getStyle_attr(), ))
        if self.getId() is not None:
            outfile.write(' id="%s"' % (self.getId(), ))
        styleType.exportAttributes(self, outfile, level, name_='tdType')
    def exportChildren(self, outfile, level, name_='tdType'):
        styleType.exportChildren(self, outfile, level, name_)
    def exportLiteral(self, outfile, level, name_='tdType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('rowspan = "%s",\n' % (self.getRowspan(),))
        showIndent(outfile, level)
        outfile.write('colspan = "%s",\n' % (self.getColspan(),))
        showIndent(outfile, level)
        outfile.write('align = "%s",\n' % (self.getAlign(),))
        showIndent(outfile, level)
        outfile.write('style_attr = "%s",\n' % (self.getStyle_attr(),))
        showIndent(outfile, level)
        outfile.write('id = "%s",\n' % (self.getId(),))
        styleType.exportLiteralAttributes(self, outfile, level, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
        styleType.exportLiteralChildren(self, outfile, level, name_)
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('rowspan'):
            try:
                self.rowspan = int(attrs.get('rowspan').value)
            except ValueError:
                raise ValueError('Bad integer attribute (rowspan)')
        if attrs.get('colspan'):
            try:
                self.colspan = int(attrs.get('colspan').value)
            except ValueError:
                raise ValueError('Bad integer attribute (colspan)')
        if attrs.get('align'):
            self.align = attrs.get('align').value
        if attrs.get('style_attr'):
            self.style_attr = attrs.get('style_attr').value
        if attrs.get('id'):
            self.id = attrs.get('id').value
        styleType.buildAttributes(self, attrs)
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
        styleType.buildChildren(self, child_, nodeName_)
# end class tdType


class inlineImageType:
    subclass = None
    def __init__(self, alt='', href='', ttype='', valueOf_=''):
        self.alt = alt
        self.href = href
        self.ttype = ttype
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if inlineImageType.subclass:
            return inlineImageType.subclass(*args_, **kwargs_)
        else:
            return inlineImageType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getAlt(self): return self.alt
    def setAlt(self, alt): self.alt = alt
    def getHref(self): return self.href
    def setHref(self, href): self.href = href
    def getType(self): return self.ttype
    def setType(self, ttype): self.ttype = ttype
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='inlineImageType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='inlineImageType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='inlineImageType'):
        if self.getAlt() is not None:
            outfile.write(' alt="%s"' % (self.getAlt(), ))
        if self.getHref() is not None:
            outfile.write(' href="%s"' % (self.getHref(), ))
        if self.getType() is not None:
            outfile.write(' type="%s"' % (self.getType(), ))
    def exportChildren(self, outfile, level, name_='inlineImageType'):
        outfile.write(self.valueOf_)
    def exportLiteral(self, outfile, level, name_='inlineImageType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('alt = "%s",\n' % (self.getAlt(),))
        showIndent(outfile, level)
        outfile.write('href = "%s",\n' % (self.getHref(),))
        showIndent(outfile, level)
        outfile.write('ttype = "%s",\n' % (self.getType(),))
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('alt'):
            self.alt = attrs.get('alt').value
        if attrs.get('href'):
            self.href = attrs.get('href').value
        if attrs.get('type'):
            self.ttype = attrs.get('type').value
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class inlineImageType


class pType(styleType):
    subclass = None
    def __init__(self, id='', style_attr='', lang='', strong=None, emphasis=None, style=None, a=None, strikethrough=None, sub=None, sup=None, code=None, image=None, valueOf_='', mixedclass_=None, content_=None):
        styleType.__init__(self, mixedclass_, content_)
        self.id = id
        self.style_attr = style_attr
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
    def factory(*args_, **kwargs_):
        if pType.subclass:
            return pType.subclass(*args_, **kwargs_)
        else:
            return pType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getId(self): return self.id
    def setId(self, id): self.id = id
    def getStyle_attr(self): return self.style_attr
    def setStyle_attr(self, style_attr): self.style_attr = style_attr
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='pType'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='pType')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='pType'):
        if self.getId() is not None:
            outfile.write(' id="%s"' % (self.getId(), ))
        if self.getStyle_attr() is not None:
            outfile.write(' style_attr="%s"' % (self.getStyle_attr(), ))
        styleType.exportAttributes(self, outfile, level, name_='pType')
    def exportChildren(self, outfile, level, name_='pType'):
        styleType.exportChildren(self, outfile, level, name_)
    def exportLiteral(self, outfile, level, name_='pType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('id = "%s",\n' % (self.getId(),))
        showIndent(outfile, level)
        outfile.write('style_attr = "%s",\n' % (self.getStyle_attr(),))
        styleType.exportLiteralAttributes(self, outfile, level, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
        styleType.exportLiteralChildren(self, outfile, level, name_)
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('id'):
            self.id = attrs.get('id').value
        if attrs.get('style_attr'):
            self.style_attr = attrs.get('style_attr').value
        styleType.buildAttributes(self, attrs)
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.nodeValue)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
        styleType.buildChildren(self, child_, nodeName_)
# end class pType


class custom_info(textFieldType):
    subclass = None
    def __init__(self, info_type='', lang='', valueOf_=''):
        textFieldType.__init__(self, lang)
        self.info_type = info_type
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if custom_info.subclass:
            return custom_info.subclass(*args_, **kwargs_)
        else:
            return custom_info(*args_, **kwargs_)
    factory = staticmethod(factory)
    def getInfo_type(self): return self.info_type
    def setInfo_type(self, info_type): self.info_type = info_type
    def getValueOf_(self): return self.valueOf_
    def setValueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, name_='custom-info'):
        showIndent(outfile, level)
        outfile.write('<%s' % (name_, ))
        self.exportAttributes(outfile, level, name_='custom-info')
        outfile.write('>')
        self.exportChildren(outfile, level + 1, name_)
        outfile.write('</%s>\n' % name_)
    def exportAttributes(self, outfile, level, name_='custom-info'):
        outfile.write(' info-type="%s"' % (self.getInfo_type(), ))
        textFieldType.exportAttributes(self, outfile, level, name_='custom-info')
    def exportChildren(self, outfile, level, name_='custom-info'):
        textFieldType.exportChildren(self, outfile, level, name_)
        outfile.write(self.valueOf_)
    def exportLiteral(self, outfile, level, name_='custom-info'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('info_type = "%s",\n' % (self.getInfo_type(),))
        textFieldType.exportLiteralAttributes(self, outfile, level, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('valueOf_ = "%s",\n' % (self.valueOf_,))
        textFieldType.exportLiteralChildren(self, outfile, level, name_)
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        if attrs.get('info-type'):
            self.info_type = attrs.get('info-type').value
        textFieldType.buildAttributes(self, attrs)
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
# end class custom_info


from xml.sax import handler, make_parser

class SaxStackElement:
    def __init__(self, name='', obj=None):
        self.name = name
        self.obj = obj
        self.content = ''

#
# SAX handler
#
class SaxFictionbookHandler(handler.ContentHandler):
    def __init__(self):
        self.stack = []
        self.root = None

    def getRoot(self):
        return self.root

    def setDocumentLocator(self, locator):
        self.locator = locator
    
    def showError(self, msg):
        print '*** (showError):', msg
        sys.exit(-1)

    def startElement(self, name, attrs):
        done = 0
        if name == 'FictionBook':
            obj = FictionBook.factory()
            stackObj = SaxStackElement('FictionBook', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'stylesheet':
            obj = stylesheet.factory()
            val = attrs.get('type', None)
            if val is not None:
                obj.setType(val)
            stackObj = SaxStackElement('stylesheet', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'description':
            obj = description.factory()
            stackObj = SaxStackElement('description', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'title-info':
            obj = title_infoType.factory()
            stackObj = SaxStackElement('title_info', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'src-title-info':
            obj = title_infoType.factory()
            stackObj = SaxStackElement('src_title_info', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'document-info':
            obj = document_info.factory()
            stackObj = SaxStackElement('document_info', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'author':
            obj = authorType.factory()
            stackObj = SaxStackElement('author', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'program-used':
            obj = textFieldType.factory()
            stackObj = SaxStackElement('program_used', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'date':
            obj = dateType.factory()
            stackObj = SaxStackElement('date', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'src-url':
            stackObj = SaxStackElement('src_url', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'src-ocr':
            obj = textFieldType.factory()
            stackObj = SaxStackElement('src_ocr', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'id':
            stackObj = SaxStackElement('id', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'version':
            stackObj = SaxStackElement('version', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'history':
            obj = annotationType.factory()
            stackObj = SaxStackElement('history', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'publish-info':
            obj = publish_info.factory()
            stackObj = SaxStackElement('publish_info', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'book-name':
            obj = textFieldType.factory()
            stackObj = SaxStackElement('book_name', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'publisher':
            obj = textFieldType.factory()
            stackObj = SaxStackElement('publisher', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'city':
            obj = textFieldType.factory()
            stackObj = SaxStackElement('city', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'year':
            stackObj = SaxStackElement('year', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'isbn':
            obj = textFieldType.factory()
            stackObj = SaxStackElement('isbn', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'sequence':
            obj = sequenceType.factory()
            stackObj = SaxStackElement('sequence', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'custom-info':
            obj = custom_info.factory()
            val = attrs.get('info-type', None)
            if val is not None:
                obj.setInfo-type(val)
            stackObj = SaxStackElement('custom_info', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'output':
            obj = shareInstructionType.factory()
            stackObj = SaxStackElement('output', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'body':
            obj = body.factory()
            val = attrs.get('lang', None)
            if val is not None:
                obj.setLang(val)
            val = attrs.get('name', None)
            if val is not None:
                obj.setName(val)
            stackObj = SaxStackElement('body', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'image':
            obj = imageType.factory()
            stackObj = SaxStackElement('image', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'title':
            obj = titleType.factory()
            stackObj = SaxStackElement('title', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'epigraph':
            obj = epigraphType.factory()
            stackObj = SaxStackElement('epigraph', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'section':
            obj = sectionType.factory()
            stackObj = SaxStackElement('section', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'binary':
            obj = binary.factory()
            val = attrs.get('content-type', None)
            if val is not None:
                obj.setContent-type(val)
            val = attrs.get('id', None)
            if val is not None:
                obj.setId(val)
            stackObj = SaxStackElement('binary', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'first-name':
            obj = textFieldType.factory()
            stackObj = SaxStackElement('first_name', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'middle-name':
            obj = textFieldType.factory()
            stackObj = SaxStackElement('middle_name', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'last-name':
            obj = textFieldType.factory()
            stackObj = SaxStackElement('last_name', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'nickname':
            obj = textFieldType.factory()
            stackObj = SaxStackElement('nickname', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'home-page':
            stackObj = SaxStackElement('home_page', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'email':
            stackObj = SaxStackElement('email', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'p':
            obj = pType.factory()
            stackObj = SaxStackElement('p', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'empty-line':
            stackObj = SaxStackElement('empty_line', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'poem':
            obj = poemType.factory()
            stackObj = SaxStackElement('poem', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'subtitle':
            obj = pType.factory()
            stackObj = SaxStackElement('subtitle', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'table':
            obj = tableType.factory()
            stackObj = SaxStackElement('table', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'text-author':
            obj = pType.factory()
            stackObj = SaxStackElement('text_author', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'stanza':
            obj = stanza.factory()
            val = attrs.get('lang', None)
            if val is not None:
                obj.setLang(val)
            stackObj = SaxStackElement('stanza', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'v':
            obj = pType.factory()
            stackObj = SaxStackElement('v', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'cite':
            obj = citeType.factory()
            stackObj = SaxStackElement('cite', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'annotation':
            obj = annotationType.factory()
            stackObj = SaxStackElement('annotation', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'strong':
            obj = styleType.factory()
            stackObj = SaxStackElement('strong', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'emphasis':
            obj = styleType.factory()
            stackObj = SaxStackElement('emphasis', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'style':
            obj = namedStyleType.factory()
            stackObj = SaxStackElement('style', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'a':
            obj = linkType.factory()
            stackObj = SaxStackElement('a', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'strikethrough':
            obj = styleType.factory()
            stackObj = SaxStackElement('strikethrough', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'sub':
            obj = styleType.factory()
            stackObj = SaxStackElement('sub', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'sup':
            obj = styleType.factory()
            stackObj = SaxStackElement('sup', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'code':
            obj = styleType.factory()
            stackObj = SaxStackElement('code', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'tr':
            obj = tr.factory()
            val = attrs.get('align', None)
            if val is not None:
                obj.setAlign(val)
            stackObj = SaxStackElement('tr', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'th':
            obj = tdType.factory()
            stackObj = SaxStackElement('th', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'td':
            obj = tdType.factory()
            stackObj = SaxStackElement('td', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'genre':
            obj = genre.factory()
            val = attrs.get('match', None)
            if val is not None:
                try:
                    obj.setMatch(int(val))
                except:
                    self.reportError('"match" attribute must be integer')
            stackObj = SaxStackElement('genre', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'book-title':
            obj = textFieldType.factory()
            stackObj = SaxStackElement('book_title', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'keywords':
            obj = textFieldType.factory()
            stackObj = SaxStackElement('keywords', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'coverpage':
            obj = coverpage.factory()
            stackObj = SaxStackElement('coverpage', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'lang':
            stackObj = SaxStackElement('lang', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'src-lang':
            stackObj = SaxStackElement('src_lang', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'translator':
            obj = authorType.factory()
            stackObj = SaxStackElement('translator', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'part':
            obj = partShareInstructionType.factory()
            stackObj = SaxStackElement('part', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'output-document-class':
            obj = outPutDocumentType.factory()
            stackObj = SaxStackElement('output_document_class', obj)
            self.stack.append(stackObj)
            done = 1
        if not done:
            self.reportError('"%s" element not allowed here.' % name)

    def endElement(self, name):
        done = 0
        if name == 'FictionBook':
            if len(self.stack) == 1:
                self.root = self.stack[-1].obj
                self.stack.pop()
                done = 1
        elif name == 'stylesheet':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addStylesheet(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'description':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setDescription(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'title-info':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setTitle_info(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'src-title-info':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setSrc_title_info(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'document-info':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setDocument_info(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'author':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addAuthor(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'program-used':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setProgram_used(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'date':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setDate(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'src-url':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.addSrc_url(content)
                self.stack.pop()
                done = 1
        elif name == 'src-ocr':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setSrc_ocr(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'id':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setId(content)
                self.stack.pop()
                done = 1
        elif name == 'version':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                if content:
                    try:
                        content = float(content)
                    except:
                        self.reportError('"version" must be float -- content: %s' % content)
                else:
                    content = -1
                self.stack[-2].obj.setVersion(content)
                self.stack.pop()
                done = 1
        elif name == 'history':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setHistory(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'publish-info':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setPublish_info(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'book-name':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setBook_name(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'publisher':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setPublisher(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'city':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setCity(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'year':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setYear(content)
                self.stack.pop()
                done = 1
        elif name == 'isbn':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setIsbn(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'sequence':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addSequence(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'custom-info':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addCustom_info(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'output':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addOutput(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'body':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addBody(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'image':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setImage(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'title':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setTitle(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'epigraph':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addEpigraph(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'section':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addSection(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'binary':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addBinary(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'first-name':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setFirst_name(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'middle-name':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setMiddle_name(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'last-name':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setLast_name(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'nickname':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setNickname(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'home-page':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.addHome_page(content)
                self.stack.pop()
                done = 1
        elif name == 'email':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.addEmail(content)
                self.stack.pop()
                done = 1
        elif name == 'p':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setP(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'empty-line':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setEmpty_line(content)
                self.stack.pop()
                done = 1
        elif name == 'poem':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setPoem(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'subtitle':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setSubtitle(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'table':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setTable(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'text-author':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addText_author(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'stanza':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addStanza(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'v':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addV(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'cite':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setCite(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'annotation':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setAnnotation(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'strong':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setStrong(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'emphasis':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setEmphasis(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'style':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setStyle(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'a':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setA(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'strikethrough':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setStrikethrough(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'sub':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setSub(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'sup':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setSup(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'code':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setCode(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'tr':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addTr(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'th':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setTh(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'td':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setTd(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'genre':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addGenre(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'book-title':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setBook_title(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'keywords':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setKeywords(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'coverpage':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setCoverpage(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'lang':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setLang(content)
                self.stack.pop()
                done = 1
        elif name == 'src-lang':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.setSrc_lang(content)
                self.stack.pop()
                done = 1
        elif name == 'translator':
            if len(self.stack) >= 2:
                self.stack[-2].obj.addTranslator(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'part':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setPart(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'output-document-class':
            if len(self.stack) >= 2:
                self.stack[-2].obj.setOutput_document_class(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        if not done:
            self.reportError('"%s" element not allowed here.' % name)

    def characters(self, chrs, start, end):
        if len(self.stack) > 0:
            self.stack[-1].content += chrs[start:end]

    def reportError(self, mesg):
        locator = self.locator
        sys.stderr.write('Doc: %s  Line: %d  Column: %d\n' % \
            (locator.getSystemId(), locator.getLineNumber(), 
            locator.getColumnNumber() + 1))
        sys.stderr.write(mesg)
        sys.stderr.write('\n')
        sys.exit(-1)
        #raise RuntimeError

USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
Options:
    -s        Use the SAX parser, not the minidom parser.
"""

def usage():
    print USAGE_TEXT
    sys.exit(-1)


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
        if topElementName not in globals():
            raise RuntimeError, 'no class for top element: %s' % topElementName
        topElement = globals()[topElementName]
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
    documentHandler = SaxFictionbookHandler()
    parser.setDocumentHandler(documentHandler)
    parser.parse('file:%s' % inFileName)
    root = documentHandler.getRoot()
    sys.stdout.write('<?xml version="1.0" ?>\n')
    root.export(sys.stdout, 0)
    return root


def saxParseString(inString):
    parser = make_parser()
    documentHandler = SaxFictionbookHandler()
    parser.setDocumentHandler(documentHandler)
    parser.feed(inString)
    parser.close()
    rootObj = documentHandler.getRoot()
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0)
    return rootObj


def parse(inFileName):
    doc = minidom.parse(inFileName)
    rootNode = doc.documentElement
    rootObj = FictionBook.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="FictionBook")
    return rootObj


def parseString(inString):
    doc = minidom.parseString(inString)
    rootNode = doc.documentElement
    rootObj = FictionBook.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="FictionBook")
    return rootObj


def parseLiteral(inFileName):
    doc = minidom.parse(inFileName)
    rootNode = doc.documentElement
    rootObj = FictionBook.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('from fb21 import *\n\n')
    sys.stdout.write('rootObj = FictionBook(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="FictionBook")
    sys.stdout.write(')\n')
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == '-s':
        saxParse(args[1])
    elif len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    main()
    #import pdb
    #pdb.run('main()')

