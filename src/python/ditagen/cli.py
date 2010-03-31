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

"""Command line interface to DITA DTD Generator."""

#from ditagen.generator import DitaGenerator
import sys
import ditagen.dita
import ditagen.dtdgen
from ditagen.dita.v1_2 import *
from ditagen.dita.v1_1 import *
import ditagen.generator
from optparse import OptionParser, OptionGroup
#import urllib

#class UrnDitaGenerator(ditagen.generator.PluginGenerator):
#
#    @staticmethod
#    def generate_public_identifier(ext, id, dita_version, title, owner=None, suffix=None):
#        """Generate URN public formal indentifier."""
#        if owner != None and owner != u"OASIS":
#            __ENTITY_MAP = {
#                "dtd": u"doctypes",
#                "ent": u"entities",
#                "mod": u"modules"
#                }
#            desc = ["urn"]
#            if owner is None:
#                desc.extend([u"oasis", u"names", u"tc", u"dita"])
#            else:
#                desc.append(urllib.quote(owner))
#            desc.append(urllib.quote(id))
#            desc.append(__ENTITY_MAP[ext])
#            if suffix != None:
#                desc.append(urllib.quote(suffix))
#            if dita_version != None and dita_version != "":
#                desc.append(dita_version.strip())
#            return u":".join(desc).lower()
#        else:
#            return ditagen.generator.DitaGenerator.generate_public_identifier(ext, id, dita_version, title, owner, suffix)

def main():
    """Main method."""
    __topic_type = None
    __parent_topic_type = None
    __remove = {}
    __global_atts = None
    __domains = []
    
    # new arguments
    __parser = OptionParser(usage="usage: %prog [options] type topic id title [root]",
                            description="DITA Generator.")
    __parser.add_option("-d", "--domain", action="append", dest="domains",
                        help="Add domain DOMAIN. Multiple occurrances allowed.", metavar="DOMAIN")
    __parser.add_option("-v", "--version", dest="version", choices=("1.1", "1.2"),
                        help="DITA version. Defaults to 1.1.", metavar="VERSION")
    __parser.set_defaults(version="1.1")
    __parser.add_option("-o", "--owner", dest="owner",
                        help="Owner in FPI.", metavar="OWNER")
    __parser.add_option("-u", "--system-identifier", dest="system_identifier",
                        help="System identifier base URI.", metavar="SYSTEM_IDENTIFIER")
    __parser.add_option("-s", "--stylesheet", action="append",  dest="stylesheet", choices=("docbook", "eclipse.plugin", "fo", "rtf", "xhtml"),
                        help="Stylesheet skeleton. Multiple occurrances allowed.", metavar="STYLE")
    __parser.add_option("--plugin-name", dest="plugin_name",
                        help="Plugin name. Defaults to plugin ID.", metavar="PLUGIN_NAME")
    __parser.add_option("--plugin-version", dest="plugin_version",
                        help="Plugin version", metavar="PLUGIN_VERSION")
    __parser.add_option("-n", "--nested", dest="nested", action="store_true",
                        help="Support nested topics.")
    __parser.set_defaults(nested=False)
    __group = OptionGroup(__parser, "Advanced Options")
    __group.add_option("--format", dest="format", choices=("dtd", "mod", "ent", "plugin"),
                       help="Output format, one of dtd, mod, ent, zip, plugin. Defaults to plugin.", metavar="FORMAT")
    __parser.set_defaults(format="plugin")
    __parser.add_option_group(__group)
    (options, args) = __parser.parse_args()
    # read arguments
    if len(args) >= 1:
        if args[0] in ditagen.OUTPUT_MAP:
            __topic_type_class = ditagen.OUTPUT_MAP[args[0]]
        else:
            __parser.error("output type %s not found, supported types: %s."
                           % (args[0], ", ".join(ditagen.OUTPUT_MAP.keys())))
    else:
        __parser.error("output type not set")
        
    if len(args) >= 2:
        if args[1] in ditagen.TOPIC_MAP[options.version]:
            __parent_topic_type = ditagen.TOPIC_MAP[options.version][args[1]]()
        else:
            __parser.error("topic type %s not found, supported topics: %s."
                           % (args[1], ", ".join(TOPIC_MAP[options.version].keys())))
    else:
        __parser.error("topic not set")
        
    if len(args) >= 3:
        options.id = args[2]
    else:
        __parser.error("id not set")
        
    if len(args) >= 4:
        options.title = args[3]
    else:
        __parser.error("title not set")
        
    if len(args) >= 5:
        options.root = args[4]
    elif (args[0] == "specialization"):
        __parser.error("root not set")

    if options.domains != None:
        for __d in options.domains:
            if __d in ditagen.DOMAIN_MAP[options.version]:
                __domains.append(ditagen.DOMAIN_MAP[options.version][__d]())
            else:
                __parser.error("domain %s not found, supported domains: %s.".format(__d, ", ".join(ditagen.DOMAIN_MAP[options.version].keys())))
    
    #if  hasattr(options, "root") and options.root is not None:
    __topic_type = __topic_type_class(options.id, options.title, __parent_topic_type,
                           options.owner, file=options.id) #options.root
    if type(__topic_type) == ditagen.dita.SpecializationType:
        __topic_type.root = ditagen.dita.create_element(__topic_type, options.root, options.id)
    #elif options.format in ("mod", "ent", "zip"):
    #    __parser.error("cannot generate %s for base topic type.".format(options.format))

    # run generator
    if options.format == u"plugin":
        #__dita_gen = UrnDitaGenerator()
        __dita_gen = ditagen.generator.PluginGenerator()
        __dita_gen.out = sys.stdout
        __dita_gen.topic_type = __topic_type
        __dita_gen.domains = __domains
        __dita_gen.nested = options.nested
        __dita_gen.version = options.version
        #if hasattr(options, "title") and  options.title:
        #    __dita_gen.set_title(options.title)
        if options.stylesheet:
            __dita_gen.set_stylesheet(options.stylesheet)
        if options.plugin_name:
            __dita_gen.plugin_name = options.plugin_name
        if options.plugin_version:
            __dita_gen.plugin_version = options.plugin_version

        #__dita_gen.generate_public_identifier = generate_urn_identifier
        __dita_gen.generate_plugin()
    else:
        __dita_gen = ditagen.generator.DitaGenerator()
        __dita_gen.out = sys.stdout
        __dita_gen.topic_type = __topic_type
        __dita_gen.domains = __domains
        __dita_gen.nested = options.nested
        __dita_gen.version = options.version
        #if hasattr(options, "title") and  options.title:
        #    __dita_gen.set_title(options.title)
        
        if options.format == u"dtd":
            #__file_name = __dita_gen.get_file_name(__topic_type, __root, __format)
            __dita_gen.generate_dtd()
        elif options.format == u"mod":
            #__file_name = __dita_gen.get_file_name(__topic_type, __root, __format)
            __dita_gen.generate_mod()
        elif options.format == u"ent":
            #__file_name = __dita_gen.get_file_name(__topic_type, __root, __format)
            __dita_gen.generate_ent()
        #elif options.format == u"zip":
        #    #__file_name = __dita_gen.get_file_name(__topic_type, __root, "zip")
        #    __dita_gen.generate_zip(sys.stdout)
        #elif __format == u"tgz":
        #    __file_name = __dita_gen.get_file_name(__topic_type, __root, "tar.gz")
        #    __dita_gen.generate_zip(sys.stdout, __topic_type, __domains, __root, __owner, __nested, __remove, __global_atts)
        #elif __format == u"xzip":
        #    __file_name = __dita_gen.get_file_name(__topic_type, __root, "zip")
        #    zip_dita_gen = ditagen.generator.ZipGenerator(sys.stdout)
        #    zip_dita_gen.generate_zip(sys.stdout, __topic_type, __domains, __root, __owner, __nested)

if __name__ == "__main__":
    main()
