#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter daemon

Author: Vadim Zaliva <lord@crocodile.org>
'''

import getopt
import sys, os
import string, time
import urllib
import traceback

from xml.dom.minidom import parse, parseString
from ConfigParser import ConfigParser

from boto.connection import SQSConnection
from boto.sqs.message import Message
from boto.exception import SQSError

import fb2tex

MSG_FORMAT_VER=1

# --- Code ---

def usage():
    sys.stderr.write("Usage: fbdaemon.py -c cfgfile [-v]\n")

def main():
      cfgfile = None
      verbose = False
      
      try:
            opts, args = getopt.getopt(sys.argv[1:], "vc:", ["verbose", "cfgfile"])
      except getopt.GetoptError:
            usage()
            sys.exit(2)
      for o, a in opts:
            if o in ("-c", "--cfgfile"):
                  cfgfile = a
            if o in ("-v", "--verbose"):
                  verbose = True

      if len(args) != 0 or cfgfile is None:
            usage()
            sys.exit(2)

      cfg = ConfigParser()
      cfg.read(cfgfile)

      c = SQSConnection(aws_access_key_id=cfg.get('aws','public'), aws_secret_access_key=cfg.get('aws','private'))
      
      qname = cfg.get('queue','name')
      qtimeout = int(cfg.get('queue','timeout'))
      pdelay = int(cfg.get('queue','polling_delay'))
      
      q = c.create_queue(qname)

      while True:
            m = q.read(qtimeout)
            if m==None:
                  time.sleep(pdelay)
            else:
                try:
                    processMessage(m)
                    q.delete_message(m)
                except:
                    print "Error processing message"
                    traceback.print_exc(file=sys.stdout)
                    
def processMessage(m):
    msg = None
    try:
        msg = parseString(m.get_body())
    except:
        print "Invalid message, could not be parsed. Dropping"
        return
        
    root = msg.childNodes[0]
    if root.nodeName != 'fb2pdfjob':
        print "Unknwon XML root element '%s'" % root.nodeName
        return
    v=root.getAttribute('version')
    if not v or int(v)!=MSG_FORMAT_VER: 
        print "Unsupported message format version '%s'" % v
        return

    srcs=root.getElementsByTagName('source')
    if len(srcs)!=1:
        print "Too many sources in the message!"
        return
    src = srcs[0]
    src_url = src.getAttribute('url')
    src_type = src.getAttribute('type')

    results=root.getElementsByTagName('result')
    if len(srcs)!=1:
        print "Too many results in the message!"
        return
    res = results[0]
    res_key = res.getAttribute('key')

    processDocument(src_url, src_type, res_key)

def processDocument(src_url, src_type, res_key):
    tmpdirname = str(int(time.time()))    
    print "Creating dir '%s'" % tmpdirname
    os.mkdir(tmpdirname)
    try:
        fbfilenamebase = os.tempnam(tmpdirname)
        fbfilename = fbfilenamebase + '.fb2'
        print "Downloading '%s' to file '%s'" % (src_url, fbfilename)
        urllib.urlretrieve(src_url, fbfilename)
        texfilename = fbfilenamebase + '.tex'
        fb2tex.fb2tex(fbfilename, texfilename)                
    finally:
        pass
        #TODO: os.remove(tmpdirname)
    

if __name__ == "__main__":
    main()
