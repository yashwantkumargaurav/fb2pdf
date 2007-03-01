#!/usr/bin/env python2.4

'''
FictionBook2 -> TeX converter daemon

Author: Vadim Zaliva <lord@crocodile.org>
'''

import sys, os, os.path, shutil
import string, time
import urllib

from xml.dom.minidom import parse, parseString

from boto.connection import S3Connection
from boto.s3.key import Key

import fb2tex

_MSG_FORMAT_VER=2

# --- Code ---
class ProcessError:
    def __init__(self, msg):
        self.message = msg
        
    def __str__(self):
        return self.message
        
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
    logging.getLogger('tex2pdf').debug("Received new task")
    msg = None
    try:
        msg = parseString(m.get_body())
    except:
        logging.getLogger('tex2pdf').exception("Error parsing message body")
        logging.getLogger('tex2pdf').debug(m.get_body())
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
    logging.getLogger('tex2pdf').info("Processing '%s'." % src_name)
    tmpdirname = str(int(time.time()))    
    logging.getLogger('tex2pdf').debug("Creating temporary directory '%s'." % tmpdirname)
    os.mkdir(tmpdirname)
    basedir = os.getcwd()
    bucket='fb2pdf' # TODO: move to cfg
    try:
        os.chdir(tmpdirname)
        fbfilename = src_name + '.fb2'
        logging.getLogger('tex2pdf').debug("Downloading '%s' to file '%s'." % (src_url, fbfilename))
        urllib.urlretrieve(src_url, fbfilename)
        texfilename = src_name + '.tex'
        logfilename = src_name + '.txt'
        try:
            logging.getLogger('tex2pdf').debug("Converting to TeX")
            fb2tex.fb2tex(fbfilename, texfilename, logfilename)
        except:
            # Conversion error, upload log
            logging.getLogger('tex2pdf').exception("Error converting to TeX")
            upload_file(bucket, log_key, logfilename)
            raise
        pdffilename = src_name + '.pdf'
        logging.getLogger('tex2pdf').debug("Converting to PDF")
        tex2pdf(texfilename, pdffilename)
        # all OK
        # upload PDF 
        logging.getLogger('tex2pdf').debug("Uploading PDF to S3")
        upload_file(bucket, res_key, pdffilename)
        # upoad log (log should be uploaded AFTER PDF)
        logging.getLogger('tex2pdf').debug("Uploading log to S3")
        upload_file(bucket, log_key, logfilename)
    finally:
        logging.getLogger('tex2pdf').debug("Removing temp files")
        os.chdir(basedir)
        # remove temp files
        for f in os.listdir(tmpdirname):
            os.remove("%s/%s" % (tmpdirname,f))
        os.rmdir(tmpdirname)

def tex2pdf(texfilename, pdffilename):
    # Style files located ${sys_prefix}/share/texmf-local/

    logging.getLogger('tex2pdf').debug("Converting TeX to PDF")
    
    #TODO specify PDF output filename
    rc = os.system("pdflatex -halt-on-error -interaction batchmode -no-shell-escape %s > /dev/null" % texfilename)
    if rc:
        raise "Execution of pdflatex failed with error code %d" % rc
    # Run again, to incorporate TOC
    rc = os.system("pdflatex -halt-on-error -interaction batchmode -no-shell-escape %s > /dev/null" % texfilename)
    if rc:
        raise "Execution of pdflatex failed with error code %d" % rc

    # Optimize pdf
    logging.getLogger('tex2pdf').debug("Optimzing PDF")
    tmptex=texfilename+".noopt"
    os.rename(texfilename, tmptex)
    rc = os.system("pdfopt %s %s > /dev/null" % (tmptex,texfilename))
    if rc:
        raise "Execution of pdfopt failed with error code %d" % rc

