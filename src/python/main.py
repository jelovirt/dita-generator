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


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
import os.path
import ditagen
import sys
import ditagen.dita
import ditagen.dtdgen
import ditagen.dita.v1_1
import ditagen.dita.v1_2
import ditagen.generator
import re


class MainHandler(webapp.RequestHandler):
    
    def get(self):
        path_args = [a.strip() for a in self.request.path.split("/")[1:]]
        template_values = {
            #"advanced": self.request.get("debug") == "true",
            "advanced": False,
            "title": "DITA DTD Generator"
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
                #template_file = "form.html"
                if a in ("shell", "specialization", "attribute"):
                    template_values["output"] = a
                    if a == "attribute":
                        template_values["title"] = "DITA %s Specialization Generator" % path_args[__idx].capitalize()
                    else:
                        template_values["title"] = "DITA %s Generator" % path_args[__idx].capitalize()
                    template_file = a + ".html"
                else:
                    self.response.set_status(404)
                    self.response.out.write("Unrecognized output type " + a)
                    return
            elif __idx == 1:
                if a in ("1.1", "1.2"):
                    template_values["version"] = a
                else:
                    self.response.set_status(404)
                    self.response.out.write("Unrecognized DITA version " + a)
                    return
            __idx += 1
        
        path = os.path.join(os.path.dirname(__file__), template_file)
        self.response.out.write(template.render(path, template_values))


class GenerateHandler(webapp.RequestHandler):

    def post(self):
        self.get()

    def get(self):
        __topic_type = None
        __output_type = None
        __id = None
        __root = None
        __owner = None
        __nested = None
        __format = None
        __domains = []
        __version = None
        __plugin_name = None
        __plugin_version = None
        __stylesheet = None
        __title = None
        __file = None
        __attrs = []
        try:
            # version
            if u"version" in self.request.arguments():
                __version = self.request.get(u"version")
                if __version not in ("1.1", "1.2"):
                    raise ValueError("unsupported version " + __version)
            else:
                raise ValueError("version missing")
            # domains
            for __d in  self.request.get_all(u"domain"):
                if __d in ditagen.DOMAIN_MAP[__version]:
                    __domains.append(ditagen.DOMAIN_MAP[__version][__d]())
                else:
                    raise ValueError("unsupported domain " + __d)
            # id
            if u"id" in self.request.arguments():
                __id = self.request.get(u"id")
            else:
                raise ValueError("id missing")
            # root
            if u"root" in self.request.arguments():
                __root = self.request.get(u"root")
            # owner
            if u"owner" in self.request.arguments():
                __owner = self.request.get(u"owner")
            else:
                raise ValueError("owner missing")
            # title
            if u"title" in self.request.arguments():
                __title = self.request.get(u"title")
            else:
                raise ValueError("title missing")
            if u"plugin-name" in self.request.arguments():
                __plugin_name = self.request.get(u"plugin-name")
            else:
                __plugin_name = __id
            if u"plugin-version" in self.request.arguments():
                __plugin_version = self.request.get(u"plugin-version")
            #if not __title:
            #    __title = __id.capitalize()
            __nested = u"nested" in self.request.arguments()
            #__remove = dict([(n, True) for n in form.getlist("remove")])
            #__global_atts = None#self.request.get(u"attribute")
            # output type
            if u"file" in self.request.arguments():
                __format = self.request.get(u"file")
            else:
                raise ValueError("file missing")
            # stylesheet
            __stylesheet = self.request.get_all(u"stylesheet")
            for s in __stylesheet:
                if s not in ("docbook", "eclipse.plugin", "fo", "rtf", "xhtml"):
                    raise ValueError("unsupported stylesheet " + s)
            # file name
            __file = __id
            # attributes
            for i in [t[1] for t in [a.split(".") for a in self.request.arguments()] if t[0] == "att" and t[2] == "name"]:
                __v = self.request.get(u"att." + i +".values").strip()
                if __v:
                    __values = re.split("[\\s,\\|]+", __v)
                else:
                    __values = []
                __attrs.append((self.request.get(u"att." + i +".name"),
                                self.request.get(u"att." + i +".type"),
                                __values))
            if u"type" in self.request.arguments():
                # topic type
                __t = self.request.get(u"type")
                if __t in ditagen.TOPIC_MAP[__version]:
                    __topic_type = ditagen.TOPIC_MAP[__version][__t]()
                # output
                __o = self.request.get(u"output")
                if __o in ditagen.OUTPUT_MAP:
                    __output_type = ditagen.OUTPUT_MAP[__o]
                else:
                    raise ValueError("unsupported output type " + __o)
                __topic_type = __output_type(__id, __title, __topic_type,
                                             __owner, __file)#__root
                if __topic_type == ditagen.dita.SpecializationType:
                    __topic_type.root = ditagen.dita.create_element(__topic_type, __root, __id)
        except Exception:
            self.error(500)
            raise
            
        # run generator
        if __format== u"plugin" or not __format:
            __dita_gen = ditagen.generator.PluginGenerator()
            __dita_gen.out = self.response.out
            __dita_gen.owner = __owner

            if __topic_type is not None:
                __dita_gen.topic_type = __topic_type
            if not len(__domains) == 0:
                __dita_gen.domains = __domains
            __dita_gen.nested = __nested
            __dita_gen.version = __version
            __dita_gen.title = __title
            if __stylesheet:
                __dita_gen.set_stylesheet(__stylesheet)
            if __plugin_name != None:
                __dita_gen.plugin_name = __plugin_name
            if __plugin_version != None:
                __dita_gen.plugin_version = __plugin_version
            if __attrs:
                __dita_gen.domain_attributes = __attrs
            __file_name = __dita_gen.get_file_name(__id, __file, "zip")
            
            self.response.headers.add_header("Content-type", "application/zip")
            self.response.headers.add_header("Content-disposition", "attachment; filename=" + __file_name)
            __dita_gen.generate_plugin()
        else:
            __dita_gen = ditagen.generator.DitaGenerator()
            __dita_gen.out = self.response.out
            __dita_gen.topic_type = __topic_type
            if not len(__domains) == 0:
                __dita_gen.domains = __domains
            __dita_gen.nested = __nested
            __dita_gen.version = __version
            if __attrs:
                __dita_gen.domain_attributes = __attrs
            __file_name = __dita_gen.get_file_name(__topic_type, __file, __format)
            
            self.response.headers.add_header("Content-Type", "text/plain; charset=UTF-8")
            if __format == u"dtd":
                __dita_gen.generate_dtd()
            elif __format == u"mod":
                __dita_gen.generate_mod()
            elif __format == u"ent":
                __dita_gen.generate_ent()


def main():
    application = webapp.WSGIApplication([('/generate', GenerateHandler),
                                          ('/.*', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
