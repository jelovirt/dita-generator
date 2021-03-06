#!/usr/bin/env python
# -*- coding: UTF-8; indent-tabs-mode:nil; tab-width:4 -*-
# This file is part of DITA DTD Generator.
#
# Copyright 2010 Jarno Elovirta <http://www.elovirta.com/>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#from google.appengine.dist import use_library
#use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
import os.path
import ditagen
import sys
import ditagen.dita
import ditagen.dtdgen
from ditagen.dita import CustomDomain
import ditagen.dita.v1_1
import ditagen.dita.v1_2
import ditagen.dita.d4p
import ditagen.generator
import ditagen.pdf_generator
from ditagen.generator import Version
import re
import logging
import json
import conf


class MainHandler(webapp.RequestHandler):

    titles = {
      "shell": "Shell DTD",
      "specialization": "Specialization DTD",
      "attribute": "Attribute Specialization DTD",
      "pdf-plugin": "PDF plug-in",
    }

    def get(self):
        path_args = [a.strip() for a in self.request.path.split("/")[1:]]
        template_values = {
            #"advanced": self.request.get("debug") == "true",
            "advanced": False,
            "version": "1.2",
            "revision": conf.revision,
            "revision_short": conf.revision_short
        }
        template_file = "index.html"
        
        if len(path_args) > 0 and path_args[0] == "advanced":
            template_values["advanced"] = True
            path_args = path_args[1:]

        __idx = 0
        for a in path_args:
            if a == "":
                pass
            elif __idx == 0:
                # legacy
                if a in ("plugin", "pdf-plugin"):
                    self.redirect("http://dita-generator.elovirta.com/", permanent=True)
                    return
                if a in ("shell", "specialization", "attribute"):
                    template_values["output"] = a
                    template_values["title"] = "%s" % self.titles[path_args[__idx]]
                    template_values["output_title"] = self.titles[path_args[__idx]].lower()
                    template_values["generate_url"] = "/generate"
                    template_file = a + ".html"
                elif a in ("pdf-plugin"):
                    template_values["output"] = a
                    template_values["title"] = "DITA-OT %s" % self.titles[path_args[__idx]]
                    template_values["output_title"] = self.titles[path_args[__idx]].lower()
                    template_values["generate_url"] = "/generate-plugin"
                    template_values["styles"] = ditagen.pdf_generator.styles
                    template_values["css"] = "pdf.css"
                    template_file = a + ".html"
                else:
                    self.response.set_status(404)
                    self.response.headers["Content-Type"] = "text/plain; charset=UTF-8"
                    self.response.out.write("Unrecognized output type " + a)
                    return
            #elif __idx == 1:
                #if a in ("1.1", "1.2"):
                #    template_values["version"] = a
                #else:
                #    self.response.set_status(404)
                #    self.response.headers["Content-Type"] = "text/plain; charset=UTF-8"
                #    self.response.out.write("Unrecognized DITA version " + a)
                #    return
            __idx += 1
        
        path = os.path.join(os.path.dirname(__file__), template_file)
        self.response.out.write(template.render(path, template_values))
        #path = os.path.join(os.path.split(__file__)[0], 'app.yaml')


class GenerateHandler(webapp.RequestHandler):

    def post(self):
        if self.request.headers["Content-Type"].split(";")[0] == "application/json":
            try:
                __args = json.loads(self.request.body)
                #logging.info(json.dumps(__args))
            except Exception:
                self.error(500)
                raise
            self.process(__args)
        else:
            self.get()

    def get(self):
        try:
            __args = self.read_arguments()
            #logging.info(json.dumps(__args))
        except Exception:
            self.error(500)
            raise
        self.process(__args)

    def process(self, __args):
        __version = __args["version"] #"1.2"
        __dita_gen = ditagen.generator.PluginGenerator()
        __dita_gen.out = self.response.out
        __dita_gen.owner = __args["owner"]
        if "type" in __args:
            __topic_type = None
            if __args["type"] in ditagen.TOPIC_MAP[__version]:
                __topic_type = ditagen.TOPIC_MAP[__version][__args["type"]]() # XXX: Should this be a class, not an instance
            # output
            __output_type = None
            if __args["output"] in ditagen.OUTPUT_MAP:
                __output_type = ditagen.OUTPUT_MAP[__args["output"]]
            else:
                raise ValueError("unsupported output type " + __args["output"])
            __topic_type = __output_type(__args["id"], __args["title"], __topic_type,
                                         __args["owner"], __args["file"])#__root
            if type(__topic_type) == ditagen.dita.SpecializationType:
                __topic_type.root = ditagen.dita.create_element(__topic_type, __args["root"], __args["id"])
            __dita_gen.topic_type = __topic_type            
            
        __domains = []
        for __d in __args["domain"]:
            if __d in ditagen.DOMAIN_MAP[__version]:
                __domains.append(ditagen.DOMAIN_MAP[__version][__d])
            else:
                raise ValueError("unsupported domain " + __d)
        # custom domains
        for __cd in __args["custom_domain"]:
            __d = CustomDomain
            __d.id = __cd["id"] + u"-d"
            __d.si_module = __cd["id"] + u"Domain.mod"
            __d.si_entity = __cd["id"] + u"Domain.end"
            __d.pi_entity = u"-//OASIS//ENTITIES DITA %s Domain//EN" % __cd["title"]
            __d.pi_module = u"-//OASIS//ELEMENTS DITA %s Domain//EN" % __cd["title"]
            __d.title = __cd["title"]
            __d.elements = [u"ph"]
            __d.parent = [ditagen.TOPIC_MAP[__version]["topic"]]
            __domains.append(__d)
        __dita_gen.domains = __domains
            
        __dita_gen.nested = __args["nested"]
        __dita_gen.title = __args["title"]
        if "stylesheet" in __args:
            __dita_gen.set_stylesheet(__args["stylesheet"])
        if "plugin_name" in __args:
            __dita_gen.plugin_name = __args["plugin_name"]
        if "plugin_version" in __args:
            __dita_gen.plugin_version = __args["plugin_version"]
        if "attrs" in __args and len(__args["attrs"]) != 0:
            __attrs = []
            for __a in __args["attrs"]:
                # TODO: add DomainAttribute instance instead of tuple
                __attrs.append((__a["name"], __a["type"], __a["values"]))
            __dita_gen.domain_attributes = __attrs
        __dita_gen.generate_subject_scheme = __args["subject_scheme"]
        
        __file_name = __dita_gen.get_file_name(__args["id"], __args["file"], "zip")
        
        self.response.headers["Content-Type"] = "application/zip"
        self.response.headers["Content-Disposition"] = "attachment; filename=" + __file_name
        __dita_gen.generate_plugin()

    def read_arguments(self):
        ret = {}
        # version
        ret["version"] = self.request.get("version")# "1.2"
        # domains
        __domains = []
        for __d in  self.request.get_all(u"domain"):
            #if __d in ditagen.DOMAIN_MAP[__version]:
            #    __domains.append(ditagen.DOMAIN_MAP[__version][__d])
            #else:
            #    raise ValueError("unsupported domain " + __d)
            __domains.append(__d)
        ret["domain"] = __domains
        # custom domains
        ret["custom_domain"] = self.parse_dict_list("dom")
        # id
        if u"id" in self.request.arguments():
            ret["id"] = self.request.get(u"id")
        else:
            raise ValueError("id missing")
        # root
        if u"root" in self.request.arguments():
            ret["root"] = self.request.get(u"root")
        # owner
        if u"owner" in self.request.arguments():
            ret["owner"] = self.request.get(u"owner")
        else:
            raise ValueError("owner missing")
        # title
        if u"title" in self.request.arguments():
            ret["title"] = self.request.get(u"title")
        else:
            raise ValueError("title missing")
        if u"plugin-name" in self.request.arguments():
            ret["plugin_name"] = self.request.get(u"plugin-name")
        else:
            ret["plugin_name"] = ret["id"]
        if u"plugin-version" in self.request.arguments():
            ret["plugin_version"] = self.request.get(u"plugin-version")
        ret["nested"] = u"nested" in self.request.arguments()
        ret["stylesheet"] = self.request.get_all(u"stylesheet")
        for s in ret["stylesheet"]:
            if s not in ("docbook", "eclipse.plugin", "fo", "rtf", "xhtml"):
                raise ValueError("unsupported stylesheet " + s)
        # file name
        ret["file"] = ret["id"]
        if u"subject-scheme" in self.request.arguments():
            ret["subject_scheme"] = self.request.get(u"subject-scheme") == "true"
        else:
            ret["subject_scheme"] = False
        # attributes
        __attrs = []
        for __a in self.parse_dict_list("att"):
            __values = []
            if "values" in __a:
                __v = __a["values"]
                if __v.strip():
                    __values = re.split("[\\s,\\|]+", __v.strip())
            __attrs.append({"name": __a["name"], "type": __a["type"], "values": __values})
        ret["attrs"] = __attrs
        if u"type" in self.request.arguments():
            ret["type"] = self.request.get(u"type")
            ret["output"] = self.request.get(u"output")
        return ret

    def parse_dict_list(self, base):
        """Parse key-value arguments into list of dicts.""" 
        ret = []
        for key in self.request.arguments():
            a = key.split(".")
            if a[0] == base and len(a) > 2:
                i = int(a[1]) - 1
                ret.extend([{} for j in range(i - len(ret) + 1)]) # guarantee index exists
                ret[i][a[2]] = self.request.get(key)
        return ret

class PluginGenerateHandler(webapp.RequestHandler):

    def post(self):
        logging.info(self.request.headers["Content-Type"])
        if self.request.headers["Content-Type"].split(";")[0] == "application/json":
            try:
                __args = json.loads(self.request.body)
                logging.info(json.dumps(__args, indent=True))
            except Exception:
                self.error(500)
                raise
            self.process(__args)
        else:
            self.get()

    def get(self):
        try:
            __args = self.read_arguments()
        except Exception:
            self.error(500)
            raise
        self.process(__args)

    def process(self, __args):
        #logging.info(json.dumps(__args, indent=True))
        try:
            __dita_gen = ditagen.pdf_generator.StylePluginGenerator()

            #validate
            if not "ot_version" in __args:
                raise ValueError("version missing")
            __dita_gen.ot_version = Version(__args["ot_version"])
            if not u"id" in __args:
                raise ValueError("id missing")
            if "plugin_name" in __args:
                __dita_gen.plugin_name = __args["plugin_name"]
            else:
                __dita_gen.plugin_name = __args["id"]
            if u"plugin_version" in self.request.arguments():
                __dita_gen.plugin_version = __args["plugin_version"]
            __dita_gen.transtype = __args["transtype"]

            __config = __args["configuration"]
            if "page-size" in __config:
                if "orientation" in __config and __config["orientation"] == u"landscape":
                    __dita_gen.page_size = __config["page_size"].reverse()
                else:
                    __dita_gen.page_size = __config["page_size"]
            __dita_gen.page_margins = __config["page_margins"]
            __dita_gen.style = __config["style"]

            __dita_gen.force_page_count = __config["force_page_count"]
            __dita_gen.chapter_layout = __config["chapter_layout"]
            __dita_gen.bookmark_style = __config["bookmark_style"]
            __dita_gen.toc_maximum_level = __config["toc_maximum_level"]
            __dita_gen.task_label = __config["task_label"]
            __dita_gen.include_related_links = __config["include_related_links"]
            if "body_column_count" in __config:
                __dita_gen.body_column_count = __config["body_column_count"]
            if "index_column_count" in __config:
                __dita_gen.index_column_count = __config["index_column_count"]
            if "column_gap" in __config:
                __dita_gen.column_gap = __config["column_gap"]
            __dita_gen.mirror_page_margins = __config["mirror_page_margins"]
            #__dita_gen.dl = __config["dl"]
            __dita_gen.title_numbering = __config["title_numbering"]
            #__dita_gen.table_numbering = __config["table_numbering"]
            #__dita_gen.figure_numbering = __config["figure_numbering"]
            #__dita_gen.link_pagenumber = __config["link_pagenumber"]
            __dita_gen.table_continued = __config["table_continued"]
            __dita_gen.formatter = __config["formatter"]
            __dita_gen.override_shell = __config["override_shell"]
            if "cover_image" in self.request.arguments() and type(self.request.POST["cover_image"]) != unicode:
                __dita_gen.cover_image = self.request.get("cover_image")
                __dita_gen.cover_image_name = self.request.POST["cover_image"].filename
            if "cover_image_metadata" in __config:
                __dita_gen.cover_image_metadata = __config["cover_image_metadata"]
            if "cover_image_topic" in __config:
                __dita_gen.cover_image_topic = __config["cover_image_topic"]
            __dita_gen.header = __config["header"]
            if "footer" in __config:
                __dita_gen.footer = __config["footer"]
            if "page_number" in __config:
                __dita_gen.page_number = __config["page_number"]
            
            __dita_gen.out = self.response.out
            self.response.headers["Content-Type"] = "application/zip"
            __file_name = __dita_gen.get_file_name(__args["id"], __args["id"], "zip")
            self.response.headers["Content-Disposition"] = "attachment; filename=" + __file_name
            __dita_gen.generate_plugin()
        except Exception:
            self.error(500)
            raise

    def read_arguments(self):
        """Read  HTTP arguments into a JSON-like structure."""
        __ret = {}
        if u"ot_version" in self.request.arguments():
            __ret["ot_version"] = self.request.get(u"ot_version")
        if u"id" in self.request.arguments():
            __ret["id"] = self.request.get(u"id")
        if u"plugin-name" in self.request.arguments():
            __ret["plugin_name"] = self.request.get(u"plugin-name")
        if u"plugin-version" in self.request.arguments() and self.request.get(u"plugin-version").strip():
            __ret["plugin_version"] = self.request.get(u"plugin-version")
        __ret["transtype"] = self.request.get(u"transtype")
        __config = {}
        if self.request.get(u"page-size"):
            __config["page_size"] = self.request.get(u"page-size").split(" ")
        __config["orientation"] = self.request.get(u"orientation")
        __config["page_margins"] = {}
        if u"page-margin-top" in self.request.arguments() and self.request.get("page-margin-top").strip():
            __config["page_margins"]["top"] = self.request.get("page-margin-top")
        if u"page-margin-outside" in self.request.arguments() and self.request.get("page-margin-outside").strip():
            __config["page_margins"]["outside"] = self.request.get("page-margin-outside")
        if u"page-margin-bottom" in self.request.arguments() and self.request.get("page-margin-bottom").strip():
            __config["page_margins"]["bottom"] = self.request.get("page-margin-bottom")
        if u"page-margin-inside" in self.request.arguments() and self.request.get("page-margin-inside").strip():
            __config["page_margins"]["inside"] = self.request.get("page-margin-inside")
        __config["style"] = {}
        for __type in set([f["type"] for f in ditagen.pdf_generator.styles]):
            group = {}
            for __property in set([f["property"] for f in ditagen.pdf_generator.styles]):
                v = self.request.get(u"" + __property + "." + __type)
                if v:
                    group[__property] = v 
            __config["style"][__type] = group
        __config["force_page_count"] = self.request.get(u"force-page-count")
        __config["chapter_layout"] = self.request.get(u"chapter-layout")
        __config["bookmark_style"] = self.request.get(u"bookmark-style")
        if u"toc-maximum-level" in self.request.arguments():
            __config["toc_maximum_level"] = int(self.request.get(u"toc-maximum-level"))
        __config["task_label"] = u"task-label" in self.request.arguments()
        __config["include_related_links"] = self.request.get(u"include-related-links")
        if u"body-column-count" in self.request.arguments():
            __config["body_column_count"] = int(self.request.get(u"body-column-count"))
        if u"index-column-count" in self.request.arguments():
            __config["index_column_count"] = int(self.request.get(u"index-column-count"))
        if u"column-gap" in self.request.arguments() and self.request.get(u"column-gap").strip():
            __config["column_gap"] = self.request.get(u"column-gap")
        __config["mirror_page_margins"] = u"mirror-page-margins" in self.request.arguments()
        #ret["dl"] = self.request.get(u"dl")
        __config["title_numbering"] = self.request.get(u"title-numbering")
        #ret["table_numbering"] = self.request.get(u"table-numbering")
        #ret["figure_numbering"] = self.request.get(u"figure-numbering")
        #ret["link_pagenumber"] = u"link-page-number" in self.request.arguments()
        __config["table_continued"] = u"table-continued" in self.request.arguments()
        __config["formatter"] = self.request.get(u"formatter")
        __config["override_shell"] = u"override_shell" in self.request.arguments()
        if "cover_image" in self.request.arguments() and type(self.request.POST["cover_image"]) != unicode:
            #ret["cover_image"] = self.request.get("cover_image")
            __config["cover_image_name"] = self.request.POST["cover_image"].filename
        if "cover_image_metadata" in self.request.arguments():
            __config["cover_image_metadata"] = self.request.get("cover_image_metadata")
        if "cover_image_topic" in self.request.arguments():
            __config["cover_image_topic"] = self.request.get("cover_image_topic")
        #ret["drop_folio"] = u"drop-folio" in self.request.arguments()
        __header_folio = []
        if not self.request.get(u"drop-folio"):
            __header_folio = ["pagenum"]
        __config["header"] = {
            "odd": self.request.get(u"header.even").split() + __header_folio,
            "even": __header_folio + self.request.get(u"header.odd").split()
            }
        if self.request.get(u"drop-folio"):
            __config["footer"] = {
                "odd": ["pagenum"],
                "even": ["pagenum"]
                }
        if "page-number" in self.request.arguments():
            __config["page_number"] = self.request.get("page-number")
        __ret["configuration"] = __config
        return __ret

    def parse_dict_list(self, base):
        """Parse key-value arguments into list of dicts.""" 
        ret = []
        for key in self.request.arguments():
            a = key.split(".")
            if a[0] == base and len(a) > 2:
                i = int(a[1]) - 1
                ret.extend([{} for j in range(i - len(ret) + 1)]) # guarantee index exists
                ret[i][a[2]] = self.request.get(key)
        return ret


def main():
    application = webapp.WSGIApplication([('/generate', GenerateHandler),
                                          ('/generate-plugin', PluginGenerateHandler),
                                          ('/.*', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
