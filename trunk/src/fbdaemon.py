#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter daemon

Author: Vadim Zaliva <lord@crocodile.org>
'''

import getopt,sys,string

from boto.connection import SQSConnection
from boto.sqs.message import Message
from boto.exception import SQSError

# --- Constants ---

QUEUE_NAME='fb2pdf'

# --- Code ---

def main():
      c = SQSConnection()
      rs = c.get_all_queues()
      print rs


if __name__ == "__main__":
    main()

