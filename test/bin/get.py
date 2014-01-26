#!/usr/bin/python

import httplib
import urllib
import zipfile
from StringIO import StringIO
import sys
import os.path
import json
import logging

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
    json_targets = {
        "shell": {
              "domain": [
                "pr-d",
                "hi-d"
              ],
              "custom_domain": [{
                "id": "legal",
                "title": "Legal"
              }],
              "title": "test",
              "subject_scheme": True,
              "plugin_name": "test",
              "nested": True,
              "stylesheet": [],
              "attrs": [
                {
                  "values": [
                    "foo",
                    "bar",
                    "baz"
                  ],
                  "type": "props",
                  "name": "custom"
                },
                {
                  "values": ["consumer"],
                  "type": "props",
                  "name": "series"
                }
              ],
              "file": "test",
              "owner": "test",
              "output": "shell",
              "type": "concept",
              "id": "test",
              "version": "1.2"
            },
        "specialization": {
              "domain": [
                "pr-d",
                "hi-d",
                "xml-d",
                "d4p_formatting-d",
                "d4p_renditionTargetAtt-d"
              ],
              "custom_domain": [],
              "title": "test",
              "subject_scheme": False,
              "type": "concept",
              "plugin_name": "test",
              "nested": True,
              "stylesheet": [],
              "attrs": [{
                "values": [],
                "type": "props",
                "name": "custom"
              }],
              "file": "test",
              "owner": "test",
              "output": "specialization",
              "root": "test",
              "id": "test",
              "version": "1.2"
            },
        "pdf": {
            "id": "com.example.print-pdf",
            "ot_version": "1.8",
            "plugin_version": "1.0.0",
            "transtype": "print-pdf",
            "configuration": {
                "style": {
                    "body": {
                      "font-size": "12pt",
                      "start-indent": "25pt",
                      "color": "black",
                      "font-family": "Sans",
                      "line-height": "1.8em",
                      "text-align": "justify"
                    },
                    "pre": {
                        "line-height": "1em"
                    },
                    "dl": {
                      "dl-type": "list",
                      "background-color": "pink"
                    },
                    "topic.topic.topic": {
                      "font-style": "italic",
                      "start-indent": "5pt"
                    },
                    "section": {
                      "font-style": "italic",
                      "start-indent": "5pt"
                    },
                    "note": {
                      "color": "gray",
                      "font-size": "10pt",
                      "start-indent": "50pt",
                      "icon": "icon"
                    },
                    "topic.topic": {
                        "title-numbering": "true"
                    },
                    "topic": {
                      "color": "blue",
                      "title-numbering": "true",
                      "font-size": "18pt",
                      "font-weight": "bold",
                      "font-family": "Serif"
                    },
                    "link": {
                      "color": "black",
                      "link-url": "true",
                      "font-style": "italic",
                      "link-page-number": "true"
                    },
                    "fig": {
                      "background-color": "yellow",
                      "caption-number": "none"
                    },
                    "table": {
                      "background-color": "cyan",
                      "caption-number": "document"
                    },
                    "codeblock": {
                        "background-color": "silver"
                    }
                },
                "bookmark_style": "EXPANDED",
                "page_size": [
                    "210mm",
                    "297mm"
                ],
                "include_related_links": "nofamily",
                "page_number": "chapter-page",
                "formatter": "ah",
                "override_shell": True,
                "column_gap": "10mm",
                "table_continued": True,
                "title_numbering": "all",
                "cover_image_metadata": "cover-image",
                "page_margins": {
                    "top": "20mm",
                    "inside": "30mm",
                    "outside": "20mm",
                    "bottom": "20mm"
                },
                "force_page_count": "auto",
                "header": {
                    "even": ["chapter"],
                    "odd": ["chapter"]
                },
                "chapter_layout": "BASIC",
                "footer": {
                    "even": ["pagenum"],
                    "odd": ["pagenum"]
                },
                "mirror_page_margins": True,
                "task_label": True,
                "toc_maximum_level": 3
            }
        }
    }
    form_targets = {
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
            "pdf.title-numbering.topic": "true",
            
            "pdf.title-numbering.topic.topic": "true",

            "pdf.font-style.topic.topic.topic": "italic",
            "pdf.start-indent.topic.topic.topic" : "5pt",

            "pdf.font-style.topic.topic.topic.topic": "italic",

            "pdf.font-style.section": "italic",
            "pdf.start-indent.section" : "5pt",
            
            "pdf.color.link": "black",
            "pdf.font-style.link": "italic",
            "pdf.link-page-number.link": "true",
            "pdf.link-url.link": "true",
            
            "pdf.font-size.note": "10pt",
            "pdf.color.note": "gray",
            "pdf.start-indent.note": "50pt",
            "pdf.icon.note": "icon",
            
            "pdf.line-height.pre": "1em",
            
            "pdf.dl-type.dl": "list",
            "pdf.background-color.dl": "pink",
            
            "pdf.background-color.codeblock": "silver",
            
            "pdf.caption-number.table": "document",
            "pdf.background-color.table": "cyan",
            
            "pdf.caption-number.fig": "none",
            "pdf.background-color.fig": "yellow",

            "pdf.cover_image_metadata": "cover-image",

            "pdf.text-align": "justify",
            #"pdf.dl": "list",
            "pdf.title-numbering": "all",
            "pdf.spacing.before": "10pt",
            "pdf.spacing.after": "10pt",
            #"pdf.link-page-number": "true",
            "pdf.table-continued": "true",
            "pdf.formatter": "ah",
            "pdf.override_shell": "true",
            "pdf.header.even": "chapter",
            "pdf.header.odd": "chapter",
            "pdf.page-number": "chapter-page",
            "pdf.drop-folio": "pagenum",
            "id": "com.example.print-pdf",
            "transtype": "print-pdf",
            "plugin-version": "1.0.0"
            },
        "empty": [
            ('output', 'shell'),
            ('id', 'test'),
            ('owner', 'test'),
            ('title', 'test')
            ],
        "shell": [
            ('version', '1.2'),
            #('file', 'plugin'),
            ('title', 'test'),
            ('owner', 'test'),
            ('output', 'shell'),
            #('type', 'article'),
            ('type', 'concept'),
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
            
            ('dom.1.id', 'legal'),
            ('dom.1.title', 'Legal'),
            #('dom.2.id', 'safety'),
            #('dom.2.title', 'Safety'),
            
            ('subject-scheme', 'true'),
            ("domain", "pr-d"),
            ("domain", "hi-d")
            #("domain", "xml-d"),
            #("domain", "d4p_formatting-d"),
            #("domain", "d4p_renditionTargetAtt-d")
            ],
        "specialization": [
            ('version', '1.2'),
            #('file', 'plugin'),
            ('title', 'test'),
            ('owner', 'test'),
            ('output', 'specialization'),
            ('root', 'test'),
            ('type', 'topic'),
            #("nested", "true"),
            ('id', 'test'),
            ('att.1.type', 'props'),
            ('att.1.name', 'custom'),
            ('att.1.datatype', 'CDATA'),
            #("domain", "pr-d"),
            ("domain", "hi-d"),
            #("domain", "xml-d"),
            #("domain", "d4p_formatting-d"),
            #("domain", "d4p_renditionTargetAtt-d")
            ]
        }
    i = 1
    server = None
    params = None
    url = None
    targets = form_targets
    function = get
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
            elif sys.argv[i] == "-f" or sys.argv[i] == "--form":
                targets = form_targets
                function = get
            elif sys.argv[i] == "-j" or sys.argv[i] == "--json":
                targets = json_targets
                function = post
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
    function(server, handler, params, url)

def help():
    sys.stderr.write("""Usage: get.py [options] environment target

Options:
  -o DIR      output files to plug-ins directory
  -h, --help  print help
  -f, --form  use form API
  -j, --json  use JSON API
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

def post(server, handler, params, url):
    conn = httplib.HTTPConnection(server[0], server[1])
    conn.set_debuglevel(1)
    conn.request("POST", url, json.dumps(params), {"Content-Type": "application/json"})
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
