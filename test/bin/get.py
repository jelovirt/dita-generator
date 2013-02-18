#!/usr/bin/python

import httplib
import urllib
import zipfile
from StringIO import StringIO
import sys
import os.path

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def main():
    servers = {
           "production": ("dita-generator-hrd.appspot.com", 80),
           "localhost": ("localhost", 8082)
           }
    targets = {
        "pdf": {
            "output": "pdf-plugin",
            "ot.version": "1.6",
            "pdf.page-size": "210mm 297mm",
            #"pdf.orientation": "landscape",
            "pdf.page-margin-top": "20mm",
            "pdf.page-margin-outside": "20mm",
            "pdf.page-margin-bottom": "20mm",
            "pdf.page-margin-inside": "30mm",
            "pdf.mirror-page-margins": "true",
            #pdf.body-column-count": "2",
            #"pdf.index-column-count": "4",
            "pdf.column-gap": "10mm",
            "pdf.force-page-count": "auto",
            "pdf.chapter-layout": "BASIC",
            "pdf.bookmark-style": "EXPANDED",
            "pdf.toc-maximum-level": "3",
            "pdf.task-label": "YES",
            "pdf.include-related-links": "nofamily",
            
            "pdf.font-family.body": "Sans",
            "pdf.font-size.body": "12pt",
            "pdf.color.body": "black",
            "pdf.start-indent.body": "25pt",
            "pdf.text-align.body": "justify",
            "pdf.line-height.body": "1.8em",
            
            "pdf.font-family.topic": "Serif",
            "pdf.font-size.topic": "18pt",
            "pdf.color.topic": "blue",
            "pdf.font-weight.topic": "bold",
            
            "pdf.font-style.topic.topic.topic": "italic",
            "pdf.start-indent.topic.topic.topic" : "5pt",
            
            "pdf.font-style.section": "italic",
            "pdf.start-indent.section" : "5pt",
            
            "pdf.color.link": "black",
            "pdf.font-style.link": "italic",
            
            "pdf.font-size.note": "10pt",
            "pdf.color.note": "gray",
            "pdf.start-indent.note": "50pt",
            
            "pdf.line-height.pre": "1em",
            
            "pdf.table-numbering": "document",
            "pdf.figure-numbering": "none",
            
            "pdf.text-align": "justify",
            "pdf.dl": "list",
            "pdf.title-numbering": "all",
            "pdf.spacing.before": "10pt",
            "pdf.spacing.after": "10pt",
            "pdf.link-page-number": "true",
            "pdf.table-continued": "true",
            "pdf.formatter": "ah",
            "pdf.override_shell": "true",
            "pdf.header.even": "chapter",
            "pdf.header.odd": "chapter",
            "pdf.drop-folio": "pagenum",
            "id": "com.example.print-pdf",
            "transtype": "print-pdf",
            "plugin-version": "1.0.0"
            },
        "shell": [
            #('version', '1.2'),
            #('file', 'plugin'),
            ('title', 'test'),
            ('owner', 'test'),
            ('output', 'shell'),
            ('type', 'article'),
            ("nested", "true"),
            ('id', 'test'),
            ('att.1.type', 'props'),
            ('att.1.name', 'custom'),
            ('att.1.datatype', 'NMTOKENS'),
            ('att.1.values', 'foo bar baz'),
            ('att.2.type', 'props'),
            ('att.2.name', 'series'),
            ('att.2.datatype', 'NMTOKENS'),
            ('att.2.values', 'consumer'),
            ('subject-scheme', 'true'),
            ("domain", "pr-d"),
            ("domain", "hi-d"),
            ("domain", "xml-d"),
            ("domain", "d4p_formatting-d"),
            ("domain", "d4p_renditionTargetAtt-d")
            ],
        "specialization": [
            #('version', '1.2'),
            #('file', 'plugin'),
            ('title', 'test'),
            ('owner', 'test'),
            ('output', 'specialization'),
            ('root', 'test'),
            ('type', 'concept'),
            ("nested", "true"),
            ('id', 'test'),
            ('att.1.type', 'props'),
            ('att.1.name', 'custom'),
            ('att.1.datatype', 'CDATA'),
            ("domain", "pr-d"),
            ("domain", "hi-d"),
            ("domain", "xml-d"),
            ("domain", "d4p_formatting-d"),
            ("domain", "d4p_renditionTargetAtt-d")
            ]
        }
    i = 1
    server = None
    params = None
    url = None
    handler = list
    try:
        if i == len(sys.argv):
            raise None
        while i < len(sys.argv):
            if sys.argv[i] == "-o":
                i = i + 1
                dir = os.path.abspath(sys.argv[i])
                handler = lambda zip: store(zip, dir)
            elif sys.argv[i] == "-h" or sys.argv[i] == "--help":
                raise None
            elif server is None:
                if not sys.argv[i] in servers:
                    raise None
                server = servers[sys.argv[i]]
            elif params is None:
                if not sys.argv[i] in targets:
                    raise None
                params = targets[sys.argv[i]]
                if sys.argv[i] == "pdf":
                    url = "/generate-plugin"
                else:
                    url = "/generate"
                break
            i = i + 1
    except Exception, e:
        print e
        help()
        exit()
    get(server, handler, params, url)

def help():
    sys.stderr.write("""Usage: get.py [options] environment target

Options:
  -o DIR      output files to plug-ins directory
  -h, --help  print help
Environments:
  localhost   localhost
  production  dita-generator.appspot.com
Targets:
  pdf
  shell
  specialization
""")

def get(server, handler, params, url):
    conn = httplib.HTTPConnection(server[0], server[1])
    conn.request("POST", url, urllib.urlencode(params))
    response = conn.getresponse()
    with zipfile.ZipFile(StringIO(response.read()), "r") as zip:
        handler(zip)
    conn.close()

def list(zip):
    for n in zip.namelist():
        print bcolors.HEADER + n + ":" + bcolors.ENDC
        print zip.open(n).read()

def store(zip, dir):
    for n in zip.namelist():
        #print bcolors.HEADER + os.path.join(dir, n) + ":" + bcolors.ENDC
        src = zip.open(n)
        f = os.path.join(dir, n)
        if not os.path.exists(os.path.dirname(f)):
            os.makedirs(os.path.dirname(f))
        dst = open(f, "w")
        try:
            dst.write(src.read())
        finally:
            src.close()
            dst.close()

if __name__ == "__main__":
    main()
