#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter daemon

Author: Vadim Zaliva <lord@crocodile.org>
'''

import getopt
import logging, logging.handlers
import sys, os, os.path, shutil
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

from daemon import createDaemon

import fb2tex

_MSG_FORMAT_VER=2

# --- Defaults ---

pidfile='/var/run/updater.pid'
logfile = '/var/log/fbdaemon.log'
log_verbosity = logging.INFO
logger = None

# --- Code ---
class ProcessError:
    def __init__(self, msg):
        self.message = msg
        
    def __str__(self):
        return self.message
        
def usage():
    sys.stderr.write("Usage: fbdaemon.py -c cfgfile [-p pidfile] [-v] [-d]\n")

def parseCommandLineAndReadConfiguration():
    global logfile
    global log_verbosity
    
    (optlist, arglist) = getopt.getopt(sys.argv[1:], "vdc:p:l:", ["verbose", "daemon", "cfgfile=", "pidfile=","logfile="])

    cfgfile = None
    do_daemon = False
    
    for option, argument in optlist:
        if option in ("-d", "--daemon"):
            do_daemon = True
        if option in ("-v", "--verbose"):
            log_verbosity = logging.DEBUG
        elif option in ("-c", "--cfgfile"):
            if os.path.isfile(argument):
                cfgfile = argument
            else:
                raise getopt.GetoptError("config file '%s' doesn't exist" % argument)
        elif option in ("-p", "--pidfile"):
            global pidfile
            pidfile = argument
        elif option in ("-l", "--logfile"):
            global logfile
            logfile = argument
                
    if cfgfile is None:
        raise getopt.GetoptError("configuration file not specified")

    if do_daemon:
        # Detach
        createDaemon()

        # change process name, important for init.d script on Linux
        if os.path.exists('/lib/libc.so.6'):
            libc = dl.open('/lib/libc.so.6')
            libc.call('prctl', 15, 'updater', 0, 0, 0)
        
        # write PID file
        p = open(pidfile, "w")
        p.write("%s\n" % os.getpid())
        p.close()

    global cfg
    cfg = ConfigParser()
    cfg.read(cfgfile)
    
    # rotate logs on daily basis
    global logger
    rotatingLog = logging.handlers.TimedRotatingFileHandler(logfile, "D", 1, backupCount=5)
    log_formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    rotatingLog.setFormatter(log_formatter)
    logger=logging.getLogger('fbdaemon')
    logger.addHandler(rotatingLog)

    if not do_daemon:
        console = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console.setFormatter(formatter)
        logger.addHandler(console)

    logger.setLevel(log_verbosity)


def main():
    try:
        global cfg
        global logger
        parseCommandLineAndReadConfiguration()

        logger.info("Starting")
            
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
    k.key = key
    k.set_contents_from_filename(filename,{'Content-Disposition':'attachment; filename=\"%s\"' % filename})
    k.set_acl('public-read')
    #TODO close connection?

def processMessage(m):
    logger.debug("Received new task")
    msg = None
    try:
        msg = parseString(m.get_body())
    except:
        logger.exception("Error parsing message body")
        logger.debug(m.get_body())
        raise ProcessError("Could not parse the message.")
        
    root = msg.childNodes[0]
    if root.nodeName != 'fb2pdfjob':
        raise ProcessError("Unknown XML root element '%s'." % root.nodeName)
    v=root.getAttribute('version')
    if not v or int(v)!=_MSG_FORMAT_VER: 
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
        raise ProcessError("Message must contain exactly one 'result' element")
    res_key = results[0].getAttribute('key')

    logs=root.getElementsByTagName('log')
    if len(logs)!=1:
        raise ProcessError("Message must contain exactly one 'result' element")
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
        logger.debug("Downloading '%s' to file '%s'." % (src_url, fbfilename))
        urllib.urlretrieve(src_url, fbfilename)
        texfilename = src_name + '.tex'
        logfilename = src_name + '.txt'
        try:
            logger.debug("Converting to TeX")
            fb2tex.fb2tex(fbfilename, texfilename, logfilename)
        except:
            # Conversion error, upload log
            logger.exception("Error converting to TeX")
            upload_file(bucket, log_key, logfilename)
            raise
        pdffilename = src_name + '.pdf'
        logger.debug("Converting to PDF")
        tex2pdf(texfilename, pdffilename)
        # all OK
        # upload PDF 
        logger.debug("Uploading PDF to S3")
        upload_file(bucket, res_key, pdffilename)
        # upoad log (log should be uploaded AFTER PDF)
        logger.debug("Uploading log to S3")
        upload_file(bucket, log_key, logfilename)
    finally:
        logger.debug("Removing temp files")
        os.chdir(basedir)
        # remove temp files
        for f in os.listdir(tmpdirname):
            os.remove("%s/%s" % (tmpdirname,f))
        os.rmdir(tmpdirname)

def tex2pdf(texfilename, pdffilename):
    # TODO: specify location to style files
    shutil.copyfile('../../test/verse.sty','./verse.sty')
    shutil.copyfile('../../test/epigraph.sty','./epigraph.sty')
    
    #TODO specify PDF output filename
    rc = os.system("pdflatex -halt-on-error -interaction batchmode -no-shell-escape %s > /dev/null" % texfilename)
    if rc:
        raise "Execution of pdflatex failed with error code %d" % rc
    # Run again, to incorporate TOC
    rc = os.system("pdflatex -halt-on-error -interaction batchmode -no-shell-escape %s > /dev/null" % texfilename)
    if rc:
        raise "Execution of pdflatex failed with error code %d" % rc

    
if __name__ == "__main__":
    sys.exit(main())
