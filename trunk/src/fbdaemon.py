#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter daemon

Author: Vadim Zaliva <lord@crocodile.org>
'''

import getopt
import logging, logging.handlers
import sys, os, shutil
import string, time
import urllib
import traceback

from xml.dom.minidom import parse, parseString
from ConfigParser import ConfigParser

from boto.connection import SQSConnection
from boto.connection import S3Connection
from boto.sqs.message import Message
from boto.exception import SQSError
from boto.s3.key import Key

import fb2tex

MSG_FORMAT_VER=2

# --- Defaults ---
logfile = 'fbdaemon.log'
verbosity = logging.NOTSET
log_verbosity = logging.DEBUG

# --- Code ---
class ProcessError:
    def __init__(self, msg):
        self.message = msg
        
    def __str__(self):
        return self.message
        
def usage():
    sys.stderr.write("Usage: fbdaemon.py -c cfgfile [-v]\n")

def parseCommandLineAndReadConfiguration():
    global logfile
    global verbosity
    global log_verbosity
    
    (optlist, arglist) = getopt.getopt(sys.argv[1:], "vc:", ["verbose", "cfgfile="])

    cfgfile = None
    
    for option, argument in optlist:
        if option in ("-v", "--verbose"):
            verbosity = logging.DEBUG
        elif option in ("-c", "--cfgfile"):
            if os.path.isfile(argument):
                cfgfile = argument
            else:
                raise getopt.GetoptError("config file '%s' doesn't exist" % argument)
                
    if cfgfile is None:
        raise getopt.GetoptError("configuration file not specified")

    global cfg
    cfg = ConfigParser()
    cfg.read(cfgfile)
    
    # rotate logs on daily basis
    global logger
    rotatingLog = logging.handlers.TimedRotatingFileHandler(logfile, "D", 1, backupCount=5)
    rotatingLog.setLevel(log_verbosity)
    log_formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    rotatingLog.setFormatter(log_formatter)
    logger=logging.getLogger('fbdaemon')
    logger.addHandler(rotatingLog)
    
    console = logging.StreamHandler()
    console.setLevel(verbosity)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)

def main():
    try:
        global cfg
        parseCommandLineAndReadConfiguration()
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
                except ProcessError, msg:
                    logger.exception(msg)
                    
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

def upload_file(bucket, key, filename):
    global cfg
    c = S3Connection(aws_access_key_id=cfg.get('aws','public'), aws_secret_access_key=cfg.get('aws','private'))
    b = c.create_bucket(bucket)
    k = Key(b)
    k.set_acl('public-read')
    k.key = key
    k.set_contents_from_filename(filename,{'Content-Disposition':'attachement; filename=\"%s\"' % filename})
    #TODO close connection?

def processMessage(m):
    msg = None
    try:
        msg = parseString(m.get_body())
    except:
        logger.debug(m.get_body())
        raise ProcessError("Could not parse the message.")
        
    root = msg.childNodes[0]
    if root.nodeName != 'fb2pdfjob':
        raise ProcessError("Unknwon XML root element '%s'." % root.nodeName)
    v=root.getAttribute('version')
    if not v or int(v)!=MSG_FORMAT_VER: 
        raise ProcessError("Unsupported message format version '%s'." % v)

    srcs=root.getElementsByTagName('source')
    if len(srcs)!=1:
        raise ProcessError("Too many sources in the message.")
    src = srcs[0]
    src_url  = src.getAttribute('url')
    src_type = src.getAttribute('type')
    src_name = src.getAttribute('name')

    results=root.getElementsByTagName('result')
    if len(results)!=1:
        raise ProcessError("Message must contain excactly one 'result' element")
    res_key = results[0].getAttribute('key')

    logs=root.getElementsByTagName('log')
    if len(logs)!=1:
        raise ProcessError("Message must contain excactly one 'result' element")
    log_key = logs[0].getAttribute('key')

    processDocument(str(src_url), str(src_type), str(src_name), str(res_key), str(log_key))

def processDocument(src_url, src_type, src_name, res_key, log_key):
    logger.info("Processing '%s'." % src_name)
    tmpdirname = str(int(time.time()))    
    logger.debug("Creating temporary directory '%s'." % tmpdirname)
    os.mkdir(tmpdirname)
    basedir = os.getcwd()
    bucket='fb2pdf' # TODO: move to cfg
    try:
        os.chdir(tmpdirname)
        fbfilename = src_name + '.fb2'
        logger.info("Downloading '%s' to file '%s'." % (src_url, fbfilename))
        urllib.urlretrieve(src_url, fbfilename)
        texfilename = src_name + '.tex'
        logfilename = src_name + '.txt'
        try:
            fb2tex.fb2tex(fbfilename, texfilename, logfilename)
        except:
            # Conversion error, upload log
            upload_file(bucket, log_key, logfilename)
            raise
        pdffilename = src_name + '.pdf'
        tex2pdf(texfilename, pdffilename)
        # all OK
        # upload PDF 
        upload_file(bucket, res_key, pdffilename)
        # upoad log (log should be uploaded AFTER PDF)
        upload_file(bucket, log_key, logfilename)
    finally:
        os.chdir(basedir)
        pass
        #TODO: os.remove(tmpdirname)

def tex2pdf(texfilename, pdffilename):
    # TODO: specify location to style files
    shutil.copyfile('../../test/verse.sty','./verse.sty')
    shutil.copyfile('../../test/epigraph.sty','./epigraph.sty')
    
    #TODO specify PDF output filename
    rc = os.system("pdflatex -halt-on-error -interaction batchmode -no-shell-escape %s > /dev/null" % texfilename)
    if rc:
        raise "Execution of pdflatex filed with error code %d" % rc
    # Run again, to incorporate TOC
    rc = os.system("pdflatex -halt-on-error -interaction batchmode -no-shell-escape %s > /dev/null" % texfilename)
    if rc:
        raise "Execution of pdflatex filed with error code %d" % rc

    
if __name__ == "__main__":
    sys.exit(main())
