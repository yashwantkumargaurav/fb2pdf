#!/usr/bin/env python2.4

'''
Simple Tool to clear queue

Author: Vadim Zaliva <lord@crocodile.org>
'''

import getopt,sys,string,time

from ConfigParser import ConfigParser

from boto.connection import SQSConnection
from boto.sqs.message import Message
from boto.exception import SQSError

# --- Code ---

def usage():
    sys.stderr.write("Usage: queue_clear.py [-v] -c cfgfile\n")

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
      q = c.create_queue(qname)
      print "Queue created. Clearning..."
      n=q.clear()
      print "Queue cleared. %d messages dropped." % n
      c.delete_queue(q)
      print "Queue deleted."

if __name__ == "__main__":
    main()

