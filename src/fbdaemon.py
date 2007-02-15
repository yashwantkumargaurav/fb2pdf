#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter daemon

Author: Vadim Zaliva <lord@crocodile.org>
'''

import getopt,sys,string,time

from ConfigParser import ConfigParser

from boto.connection import SQSConnection
from boto.sqs.message import Message
from boto.exception import SQSError

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
                  print m

if __name__ == "__main__":
    main()

