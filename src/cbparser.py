'''
SAX-based parser with python method callbas
'''

import sys, string
from xml.sax import handler, parse
from functional import flatten

class XMLCbParser(handler.ContentHandler):

    def __init__(self):
        self._path = []

    def parseFile(self, fname):
        inFile = open(fname, 'r')
        parse(inFile, self)
        inFile.close()

    def _callHandler(self, *args):
        prefix = args[0]
        args = args[1:]
        methodname = prefix + "_" + string.join(self._path,"_")
        method = None
        try:
            method = getattr(self, methodname)
        except AttributeError:
            pass
        if method:
            if len(args):
                method(*args)
            else:
                method()

    def _quoteName(self, name):
        return string.replace(name,"-","__")
    
    # ContentHadler callbacks

    def startElement(self, name, attrs):
        self._path.append(self._quoteName(name))
        self._callHandler("start", attrs)
        
    def endElement(self, name):
        self._callHandler("end")
        self._path.pop()

    def characters(self, content):
        if type(content) == list or type(content) is tuple:
            v = string.join(flatten(content))
        else:
            v = content
        self._callHandler("chars", v)


