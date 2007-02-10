'''
FictionBook2 module
'''

import sys, string
from xml.sax import handler, parse

class Book(handler.ContentHandler):

    # callbacks

    def start_FictionBook_body(self, attrs):
        print "start_FictionBook"

    def end_FictionBook_body(self):
        print "end_FictionBook"

    # Implementation

    def __init__(self):
        self.path = []

    def parseFile(self, fname):
        inFile = open(fname, 'r')
        parse(inFile, self)
        inFile.close()

    def callHandler(self, *args):
        prefix = args[0]
        args = args[1:]
        methodname = prefix + "_" + string.join(self.path,"_")
        try:
            method = getattr(self, methodname)
            if len(args):
                method(args)
            else:
                method()
        except AttributeError:
            pass
        
    # ContentHadler callbacks

    def startElement(self, name, attrs):
        self.path.append(name)
        self.callHandler("start", attrs)
        
    def endElement(self, name):
        self.callHandler("end")
        self.path.pop()

    def characters( self, content):
        pass
        #self.callHandler("chars", content)


