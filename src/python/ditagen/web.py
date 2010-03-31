#!/usr/bin/env python
# -*- coding: UTF-8; indent-tabs-mode:nil; tab-width:4 -*-

# This file is part of DITA DTD Generator.
#
# Copyright 2009 Jarno Elovirta <http://www.elovirta.com/>
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

import sys
import cgitb; cgitb.enable()
import ditagen.dita
import ditagen.dtdgen
import ditagen.dita.v1_1
import ditagen.dita.v1_2
import ditagen.generator

def print_error(__msg):
    print_response_headers(None, 500, __msg)
    print __msg
    sys.exit()

def print_response_headers(__file_name, __code=200, __msg="Ok"):
    print u"Status: %d %s" % (__code, __msg) 
    print u"Content-Type: text/plain; charset=UTF-8"
    # print u"Content-disposition: attachment; file_name=%s.%s" % (__root, __f)
    #print u"Content-disposition: file_name=%s" % __file_name #__dita.getfileName(__type, __root, __f)
    print

def main(form):
    """Main method."""
    __topic_type = None
    __output_type = None
    __id = None
    __root = None
    __owner = None
    __nested = None
    #__remove = {}
    #__global_atts = None
    __format = None
    __domains = []
    #__types = []
    __version = "1.1"
    __plugin_name = None
    __stylesheet = None
    __title = None
    __file = None
    
    try:
        # read arguments
        if u"version" in form:
            __version = form.getfirst(u"version")
            if __version not in ("1.1", "1.2"):
                raise ValueError()
        else:
            print_error("version missing")
        # get domains
        for __d in form.getlist(u"domain"):
            if __d in ditagen.DOMAIN_MAP[__version]:
                __domains.append(ditagen.DOMAIN_MAP[__version][__d]())
        # get type
        __t = form.getfirst(u"type")
        if __t in ditagen.TOPIC_MAP[__version]:
            __topic_type = ditagen.TOPIC_MAP[__version][__t]()
        __o = form.getfirst(u"output")
        if __o in ditagen.OUTPUT_MAP:
            __output_type = ditagen.OUTPUT_MAP[__o]
        # get arguments
        if u"id" in form:
            __id = form.getfirst(u"id")
        else:
            print_error("id missing")
        if u"root" in form:
            __root = form.getfirst(u"root")
        if u"owner" in form:
            __owner = form.getfirst(u"owner")
        else:
            print_error("owner missing")
        if u"title" in form:
            __title = form.getfirst(u"title")
        else:
            print_error("title missing")
        #if not __title:
        #    __title = __id.capitalize()
        __nested = u"nested" in form
        #__remove = dict([(n, True) for n in form.getlist("remove")])
        #__global_atts = None#form.getfirst(u"attribute")
        if u"file" in form:
            __format = form.getfirst(u"file")
        else:
            print_error("file missing")
        __stylesheet = form.getfirst(u"stylesheet")
        __file = __id
        
        #if __id is not None:
        
        __topic_type = __output_type(__id, __title, __topic_type,
                                     __owner, __file)#__root
        if __topic_type == ditagen.dita.SpecializationType:
            __topic_type.root = ditagen.dita.create_element(__topic_type, __root, __id)
        # else would be reshelling
    except:
        #print u"HTTP/1.1 400 Invalid arguments"
        #print
        raise
        
    # run generator
    if __format== u"plugin" or not __format:
        __dita_gen = ditagen.generator.PluginGenerator()
        __dita_gen.out = sys.stdout
        __dita_gen.topic_type = __topic_type
        if not len(__domains) == 0:
            __dita_gen.domains = __domains
        __dita_gen.nested = __nested
        __dita_gen.version = __version
        #__dita_gen.set_title(__title)
        if __stylesheet:
            __dita_gen.set_stylesheet(__stylesheet)
        if __plugin_name != None:
            __dita_gen.plugin_name = __plugin_name
        if __plugin_version != None:
            __dita_gen.plugin_version = __plugin_version
        
        __file_name = __dita_gen.get_file_name(__topic_type, __file, "zip")
        print u"Status: 200 Ok"
        #print u"Content-type: application/zip"
        print u"Content-disposition: attachment; filename={0}".format(__file_name)
        print
        
        __dita_gen.generate_plugin()
    else:
        __dita_gen = ditagen.generator.DitaGenerator()
        __dita_gen.out = sys.stdout
        __dita_gen.topic_type = __topic_type
        if not len(__domains) == 0:
            __dita_gen.domains = __domains
        __dita_gen.nested = __nested
        __dita_gen.version = __version

        __file_name = __dita_gen.get_file_name(__topic_type, __file, __format)
        print_response_headers(__file_name)
        if __format == u"dtd":
            __dita_gen.generate_dtd()
        elif __format == u"mod":
            __dita_gen.generate_mod()
        elif __format == u"ent":
            __dita_gen.generate_ent()

if __name__ == "__main__":
    main()
