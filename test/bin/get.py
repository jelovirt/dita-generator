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
           "production": ("dita-generator.appspot.com", 80),
           "localhost": ("localhost", 8082)
           }
    i = 1
    server = None
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
            else:
                server = servers[sys.argv[i]]
                break
            i = i + 1
    except:
        help()
        exit()
    get(server, handler)

def help():
    sys.stderr.write("""Usage: get.py [options] environment\n
Options:
  -o DIR      output files to plug-ins directory
  -h, --help  print help\n""")

def get(server, handler):
    params = {
            "output": "pdf-plugin",
            "ot.version": "1.5.4",
            "pdf.page-size": "210mm 297mm",
            "pdf.orientation": "landscape",
            "pdf.page-margin-top": "10mm",
            "pdf.page-margin-outside": "10mm",
            "pdf.page-margin-bottom": "10mm",
            "pdf.page-margin-inside": "20mm",
            "pdf.mirror-page-margins": "true",
            "pdf.body-column-count": "2",
            "pdf.index-column-count": "4",
            "pdf.column-gap": "16pt",
            "pdf.force-page-count": "auto",
            "pdf.chapter-layout": "BASIC",
            "pdf.bookmark-style": "EXPANDED",
            "pdf.toc-maximum-level": "3",
            "pdf.task-label": "YES",
            "pdf.include-related-links": "nofamily",
            "pdf.font-family": "Serif",
            "pdf.default-font-size": "10pt",
            "pdf.color": "black",
            "pdf.side-col-width": "20pt",
            "pdf.link-color": "inherit",
            "pdf.text-align": "justify",
            "pdf.dl": "html",
            "id": "com.example.print-pdf",
            "transtype": "print-pdf",
            "plugin-version": "1.0.0"
            }
    conn = httplib.HTTPConnection(server[0], server[1])
    conn.request("POST", "/generate-plugin", urllib.urlencode(params))
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
