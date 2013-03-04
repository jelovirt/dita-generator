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

import logging
import sys
import ditagen.dita
import ditagen.dita.v1_1
import ditagen.dita.v1_2
import ditagen.dita.d4p
from ditagen.dtdgen import Empty as Empty
from ditagen.dtdgen import Any as Any
from ditagen.dtdgen import Mixed as Mixed
from ditagen.dtdgen import Particle as Particle
from ditagen.dtdgen import Seq as Seq
from ditagen.dtdgen import Choice as Choice
from ditagen.dtdgen import Name as Name 
from ditagen.dtdgen import Param as Param
from ditagen.dtdgen import Attribute as Attribute
from ditagen.dtdgen import ParameterEntity as ParameterEntity
import StringIO
from zipfile import ZipFile, ZipInfo
from datetime import datetime
from xml.etree import ElementTree as ET

NS_XSL = "{http://www.w3.org/1999/XSL/Transform}"
NS_FO = "{http://www.w3.org/1999/XSL/Format}"

class DtdGenerator(object):
    """DTD generator."""
    # Constants
    __WIDTH = 80    

    # Variables
    out = None

    # Methods
    def __init__(self, out=None):#sys.stdout):
        self.out = out

    def external_general_entity(self, name, system, public=None):
        """Print external general entity declaration."""
        if public == None:
            self.out.write(u"""<!ENTITY %s SYSTEM "%s">""" % (name, system))
        else:
            self.out.write(u"""<!ENTITY %s PUBLIC "%s" "%s">""" % (name, public, system))
        self.out.write("\n")

    def external_parameter_entity(self, name, system, public=None):
        """Print external parameter entity declaration."""
        if public == None:
            self.out.write(u"""<!ENTITY %% %s SYSTEM "%s">""" % (name, system))
        else:
            self.out.write(u"""<!ENTITY %% %s\n  PUBLIC "%s"\n         "%s">""" % (name, public, system))
        self.out.write("\n")

    def internal_general_entity(self, name, value, sep=u""):
        """Print internal general entity declaration."""
        __value = self.__get_entity_value(value, sep)
        __div = self.__get_start_indent(11 + len(name))
        self.out.write(u"""<!ENTITY %s%s"%s">""" % (name, __div, __value))
        self.out.write("\n")
            
    def internal_parameter_entity(self, name, value, sep=u""):
        """Print internal parameter entity declaration."""
        __value = self.__get_entity_value(value, sep)
        __div = self.__get_start_indent(11 + 2 + len(name))
        self.out.write(u"""<!ENTITY %% %s%s"%s">""" % (name, __div, __value))
        self.out.write("\n")
    
    def __get_start_indent(self, length):
        """Get whitespace before entity value."""
        if length > (24 + 1):
            return "\n" + " " * 24
        else:
            return " " * (24 + 2 - length)
    
    def __get_entity_value(self, value, sep):
        """Get entity value."""
        if type(value) == list:
            __s = sep + "\n" + " " * (24 + 1)
            return __s.join([str(v) for v in value]) + "\n" + " " * 24
        else:
            return value

    def element_declaration(self, name, model):
        """Print element declaration."""
        self.out.write("""<!ELEMENT %s (%s)>""" % (name, model))
        self.out.write("\n")

    def attribute_declaration(self, name, attrs, sep=u"\n    "):
        """Print attribute declaration."""
        if type(attrs) == list:
            __value = sep.join([str(a) for a in attrs])
            if len(attrs) > 1:
                __value = sep + __value
        else:
            __value = str(attrs)
        self.out.write("""<!ATTLIST %s %s>""" % (name, __value))
        self.out.write("\n")
    
    def parameter_entity_ref(self, name):
        """Print parameter entity reference."""
        self.out.write(u"""%%%s;""" % (name))
    
    def comment_block(self, text, before=1, after=2):
        """Print block comment."""
        __hr = u"""<!-- %s -->""" % ("".join(u"=" * self.__WIDTH))
        self.out.write(u"\n" * before)
        self.out.write(__hr)
        self.out.write(u"\n")
        self.out.write(u"""<!-- %s -->""" % (text.center(self.__WIDTH)))
        self.out.write(u"\n")
        self.out.write(__hr)
        self.out.write(u"\n" * after)
    
    def centered_comment_line(self, text, delim="=", before=1, after=2):
        """Print centered comment line."""
        self.out.write(u"\n" * before)
        self.out.write(u"""<!-- %s -->""" % (str(" " + text + " ").center(self.__WIDTH, delim)))
        self.out.write(u"\n" * after)

    def comment(self, text, before=1, after=2):
        """Print comment line."""
        self.out.write(u"\n" * before)
        self.out.write(u"<!-- ")
        __lines = text.splitlines(True)
        for __i in range(0, len(__lines)):
            #self.out.write(__l.ljust(self.__WIDTH, " "))
            if __i == len(__lines) - 1:
                __l = u"     " + __lines[__i].ljust(self.__WIDTH, u" ")
            elif __i == 0:
                __l = __lines[__i]
            else:
                __l = u"     " + __lines[__i]
            self.out.write(__l)
        self.out.write(u" -->")
        self.out.write(u"\n" * after)

class DitaGenerator(DtdGenerator):
    """DITA DTD generator."""

    # Constants

    __ENTITY_MAP = { "dtd": u"DTD", "ent": u"ENTITIES", "mod": u"ELEMENTS" }

    __ENTITIES = ("basic.ph", "basic.block", "basic.phandblock",
                  "basic.ph.noxref", "basic.ph.notm", "basic.block.notbl",
                  "basic.block.nonote", "basic.block.nopara",
                  "basic.block.nolq", "basic.block.notbnofg",
                  "basic.block.notbfgobj", "txt.incl", "data.elements.incl",
                  "foreign.unknown.incl", "listitem.cnt", "itemgroup.cnt",
                  "title.cnt", "xreftext.cnt", "xrefph.cnt", "shortquote.cnt",
                  "para.cnt", "note.cnt", "longquote.cnt", "tblcell.cnt",
                  "desc.cnt", "ph.cnt", "fn.cnt", "term.cnt", "defn.cnt",
                  "pre.cnt", "fig.cnt", "words.cnt", "data.cnt", "body.cnt",
                  "section.cnt", "section.notitle.cnt")
    __ENTITIES_LIST = {
        # commonElements.mod
        # ==================
        # Phrase/inline elements of various classes   
        "basic.ph": ["%ph;", "%term;", "%xref;", "%cite;", "%q;", "%boolean;",
                     "%state;", "%keyword;", "%tm;"], 
        # Elements common to most body-like contexts  
        "basic.block": ["%p;", "%lq;", "%note;", "%dl;", "%ul;", "%ol;", "%sl;",
                        "%pre;", "%lines;", "%fig;", "%image;", "%object;",
                        "%table;", "%simpletable;"], 
        # class groupings to preserve in a schema 
        "basic.phandblock": ["%basic.ph;", "%basic.block;"], 
        # Exclusions: models modified by removing excluded content      
        "basic.ph.noxref": ["%ph;", "%term;", "%q;", "%boolean;", "%state;",
                            "%keyword;", "%tm;"], 
        "basic.ph.notm": ["%ph;", "%term;", "%xref;", "%cite;", "%q;",
                          "%boolean;", "%state;", "%keyword;"], 
        "basic.block.notbl": ["%p;", "%lq;", "%note;", "%dl;", "%ul;", "%ol;",
                              "%sl;", "%pre;", "%lines;", "%fig;", "%image;",
                              "%object;"], 
        "basic.block.nonote": ["%p;", "%lq;", "%dl;", "%ul;", "%ol;", "%sl;",
                               "%pre;", "%lines;", "%fig;", "%image;",
                               "%object;", "%table;", "%simpletable;"], 
        "basic.block.nopara": ["%lq;", "%note;", "%dl;", "%ul;", "%ol;", "%sl;",
                               "%pre;", "%lines;", "%fig;", "%image;",
                               "%object;", "%table;", "%simpletable;"], 
        "basic.block.nolq": ["%p;", "%note;", "%dl;", "%ul;", "%ol;", "%sl;",
                             "%pre;", "%lines;", "%fig;", "%image;", "%object;",
                             "%table;", "%simpletable;"], 
        "basic.block.notbnofg": ["%p;", "%lq;", "%note;", "%dl;", "%ul;",
                                 "%ol;", "%sl;", "%pre;", "%lines;", "%image;",
                                 "%object;"], 
        "basic.block.notbfgobj": ["%p;", "%lq;", "%note;", "%dl;", "%ul;",
                                  "%ol;", "%sl;", "%pre;", "%lines;",
                                  "%image;"], 
        # Inclusions: defined sets that can be added into appropriate models 
        "txt.incl": ["%draft-comment;", "%required-cleanup;", "%fn;",
                     "%indextermref;", "%indexterm;"], 
        # Metadata elements intended for specialization 
        "data.elements.incl": ["%data;", "%data-about;"], 
        "foreign.unknown.incl": ["%foreign;", "%unknown;"], 
        # Predefined content model groups, based on the previous, element-only categories: 
        "listitem.cnt": ["#PCDATA", "%basic.ph;", "%basic.block;",
                         "%itemgroup;", "%txt.incl;", "%data.elements.incl;",
                         "%foreign.unknown.incl;"], 
        "itemgroup.cnt": ["#PCDATA", "%basic.ph;", "%basic.block;",
                          "%txt.incl;", "%data.elements.incl;",
                          "%foreign.unknown.incl;"], 
        "title.cnt": ["#PCDATA", "%basic.ph.noxref;", "%image;",
                      "%data.elements.incl;", "%foreign.unknown.incl;"], 
        "xreftext.cnt": ["#PCDATA", "%basic.ph.noxref;", "%image;",
                         "%data.elements.incl;", "%foreign.unknown.incl;"], 
        "xrefph.cnt": ["#PCDATA", "%basic.ph.noxref;", "%data.elements.incl;",
                       "%foreign.unknown.incl;"], 
        "shortquote.cnt": ["#PCDATA", "%basic.ph;", "%data.elements.incl;",
                           "%foreign.unknown.incl;"], 
        "para.cnt": ["#PCDATA", "%basic.ph;", "%basic.block.nopara;",
                     "%txt.incl;", "%data.elements.incl;",
                     "%foreign.unknown.incl;"], 
        "note.cnt": ["#PCDATA", "%basic.ph;", "%basic.block.nonote;",
                     "%txt.incl;", "%data.elements.incl;",
                     "%foreign.unknown.incl;"], 
        "longquote.cnt": ["#PCDATA", "%basic.ph;", "%basic.block.nolq;",
                          "%txt.incl;", "%data.elements.incl;",
                          "%foreign.unknown.incl;"], 
        "tblcell.cnt": ["#PCDATA", "%basic.ph;", "%basic.block.notbl;",
                        "%txt.incl;", "%data.elements.incl;",
                        "%foreign.unknown.incl;"], 
        "desc.cnt": ["#PCDATA", "%basic.ph;", "%basic.block.notbfgobj;",
                     "%data.elements.incl;", "%foreign.unknown.incl;"], 
        "ph.cnt": ["#PCDATA", "%basic.ph;", "%image;", "%txt.incl;",
                   "%data.elements.incl;", "%foreign.unknown.incl;"], 
        "fn.cnt": ["#PCDATA", "%basic.ph;", "%basic.block.notbl;",
                   "%data.elements.incl;", "%foreign.unknown.incl;"], 
        "term.cnt": ["#PCDATA", "%basic.ph;", "%image;", "%data.elements.incl;",
                     "%foreign.unknown.incl;"], 
        "defn.cnt": ["#PCDATA", "%basic.ph;", "%basic.block;", "%itemgroup;",
                     "%txt.incl;", "%data.elements.incl;",
                     "%foreign.unknown.incl;"], 
        "pre.cnt": ["#PCDATA", "%basic.ph;", "%txt.incl;",
                    "%data.elements.incl;", "%foreign.unknown.incl;"], 
        "fig.cnt": ["%basic.block.notbnofg;", "%simpletable;", "%xref;", "%fn;",
                    "%data.elements.incl;", "%foreign.unknown.incl;"], 
        "words.cnt": ["#PCDATA", "%keyword;", "%term;", "%data.elements.incl;",
                      "%foreign.unknown.incl;"], 
        "data.cnt": ["%words.cnt;", "%image;", "%object;", "%ph;", "%title;"],
        # topic.mod
        # =========
        "body.cnt":  ["%basic.block;", "%required-cleanup;",
                      "%data.elements.incl;", "%foreign.unknown.incl;"],
        "section.cnt":  ["#PCDATA", "%basic.ph;", "%basic.block;", "%title;",
                         "%txt.incl;", "%data.elements.incl;",
                         "%foreign.unknown.incl;"],
        "section.notitle.cnt":  ["#PCDATA", "%basic.ph;", "%basic.block;",
                                 "%txt.incl;", "%data.elements.incl;",
                                 "%foreign.unknown.incl;"]
    }

    @staticmethod
    def generate_public_identifier(ext, id, dita_version, title, owner=None, suffix=None):
        """Generate SGML public formal indentifier."""
        __ENTITY_MAP = {
            "dtd": u"DTD",
            "ent": u"ENTITIES",
            "mod": u"ELEMENTS"
            }
        desc = [__ENTITY_MAP[ext], "DITA"]
        if dita_version != None and dita_version != "":
            desc.append(dita_version.strip())
        desc.append(title)
        if suffix != None:
            desc.append(suffix)
        if owner is None:
            o = u"OASIS"
        else:
            o = owner
        return u"-//%s//%s//EN" % (o, u" ".join(desc))

    # Private methods
    
    def __init__(self):
        DtdGenerator.__init__(self)
        self._initialized = False
        self._topic_type = None
        self.domains = []
        self._root_name = None
        self._owner = None
        self.nested = None
        self.models = {}
        self.version = "1.1"
        self._dtd_base_dir = u"../../../dtd/"#u""
        self.title = None
        # internal attributes
        self.__domains = []
        self.__types = None
        self.__pi_prefix = None
        self.__constraints = None
        self.__elements = None
        self._file_name = None
        self.__all_domains = []
        # [(id, type, [value])]
        self.domain_attributes = []
        self.generate_subject_scheme = False

    def __entity(self, __id, __system, __public,
                 __owner=u"OASIS", __system_identifier=None):
        """Print external parameter entity declaration and reference."""
        __name = __id
        if __owner == None or __public == None:
            self.external_parameter_entity(__name, __system)
        else:
            self.external_parameter_entity(__name, __system, __public)
        self.parameter_entity_ref(__name)
        self.out.write("\n")
        
    def __domain_ent(self, domain):
        """Print domain entity declaration.
        
        Arguments:
        domain -- domain class
        """
        #__pi = domain.pi_entity
        #assert __pi is not None
        #if __pi == None:
        #    __pi = self.generate_public_identifier("ent", domain.id, self._pi_version, domain.title, None, u"Domain")
        self.__entity(domain.id + u"-dec", self._dtd_base_dir + domain.si_entity,
                      domain.pi_entity)
    
    def __domain_mod(self, domain):
        """Print domain module declaration."""
        #__description = domain.pi_module
        #assert __description is not None
        #if __description == None:
        #    if issubclass(domain, ditagen.dita.v1_2.Constraints):
        #        __description = self.generate_public_identifier("mod", domain.id, self._pi_version, domain.title, None, u"Constraint")
        #    else:
        #        __description = self.generate_public_identifier("mod", domain.id, self._pi_version, domain.title, None, u"Domain")
        self.__entity(domain.id + u"-def", self._dtd_base_dir + domain.si_module,
                      domain.pi_module)
    
    def __element_ent(self, topic_type):
        """Print element entity declaration."""
        __f = topic_type.file + u".ent"
        if topic_type is not self.topic_type:
            __f = self._dtd_base_dir + __f
        __pi = topic_type.pi_entity
        assert __pi is not None
        self.__entity(topic_type.id + u"-dec",# u"-d-dec"
                      __f,
                      __pi, #self.generate_public_identifier("ent", topic_type.id, self._pi_version, topic_type.title, topic_type.owner),
                      topic_type.owner)
        
    def __element_mod(self, topic_type):
        """Print element module declaration."""
        __f = topic_type.file + u".mod"
        if topic_type is not self.topic_type:
            __f = self._dtd_base_dir + __f
        if type(topic_type) in (ditagen.dita.v1_1.TopicType, ditagen.dita.v1_2.TopicType):
            __suffix = u"-type"
        else:
            __suffix = u"-typemod"
        __pi = topic_type.pi_module
        #assert __pi is not None
        if __pi is None:
            __pi = self.generate_public_identifier("mod", topic_type.id, self._pi_version, topic_type.title, topic_type.owner)
        self.__entity(topic_type.id + __suffix,
                      __f,
                      __pi,
                      topic_type.owner)
    
    def __domain_override(self, element, domains):
        """Print domain override declaration."""
        __e = [element]
        for __d in domains:
            if element in __d.elements:
                __e.append(u"""%%%s-%s;""" % (__d.id, element))
        self.internal_parameter_entity(element, __e, u" |")
    
    def __info_types(self):
        """Print info types declaration."""
        if isinstance(self.topic_type, ditagen.dita.ShellType):
            __t = self.topic_type.parent.id
        else:
            __t = self.topic_type.id
        if self.nested:
            self.internal_parameter_entity(__t + "-info-types", __t)
        else:
            self.internal_parameter_entity(__t + "-info-types", u"no-topic-nesting")
        self.out.write("\n")
    
    def __domain_included(self, domains, topic_type):
        """Print included domains."""
        __types = []
        if self.version == "1.2":
            for __t in self.__types:
                if __t.parent is not None and not isinstance(__t, ditagen.dita.ShellType) and __t.pi_entity is not None and __t not in __types:
                    __types.append(__t)
            for __t in self.__types:
                for __rt in __t.required_types:
                    if __t.pi_entity is not None and __rt not in __types:
                        __types.append(__rt)
        __included_domains = []
        for __t in __types:
            __included_domains.append(u"&%s-att;" % (__t.id))
        for __d in domains:
            if issubclass(__d, ditagen.dita.Domain) or issubclass(__d, ditagen.dita.v1_2.AttributeDomain):
                __included_domains.append(u"&%s-att;" % __d.id)
            elif issubclass(__d, ditagen.dita.v1_2.Constraints):
                if __d.att_id is not None:
                    __included_domains.append(u"&%s-constraints;" % __d.att_id)
                else:
                    __included_domains.append(u"&%s-constraints;" % __d.id)
        for d in self.domain_attributes:
            __included_domains.append("&%sAtt-d-att;" % d[0])
        self.internal_general_entity(u"included-domains", __included_domains)
        self.out.write(u"\n")
    
    def __class_declaration(self, element, cls):
        """Print class declaration."""
        __attrs = [ParameterEntity(u"global-atts"), Attribute("class", "CDATA", "\"%s\"" % (cls))]
        self.attribute_declaration(element, " ".join([str(s) for s in __attrs]))
    
    def __redefine_content_models(self, models={}):
        """Print redefined content model declarations.

        XXX: Only apply to DITA 1.1.
        """
        __entities = self.__ENTITIES_LIST.copy()
        if "separate" in models:
            __entities["listitem.cnt"] = self.__remove_from_list(__entities["listitem.cnt"], ["#PCDATA", "%basic.ph;", "%txt.incl;"])
            __entities["itemgroup.cnt"] = self.__remove_from_list(__entities["itemgroup.cnt"], ["#PCDATA", "%basic.ph;", "%txt.incl;"])
            __entities["title.cnt"] = self.__remove_from_list(__entities["title.cnt"], ["%image;"])
            __entities["xreftext.cnt"] = self.__remove_from_list(__entities["xreftext.cnt"])
            __entities["xrefph.cnt"] = self.__remove_from_list(__entities["xrefph.cnt"])
            __entities["shortquote.cnt"] = self.__remove_from_list(__entities["shortquote.cnt"])
            __entities["para.cnt"] = self.__remove_from_list(__entities["para.cnt"], ["%basic.block.nopara;"])#.extend(["%image;"])
            __entities["note.cnt"] = self.__remove_from_list(__entities["note.cnt"], ["#PCDATA", "%basic.ph;", "%txt.incl;"])
            __entities["longquote.cnt"] = self.__remove_from_list(__entities["longquote.cnt"], ["#PCDATA", "%basic.ph;", "%txt.incl;"])
            __entities["tblcell.cnt"] = self.__remove_from_list(__entities["tblcell.cnt"], ["#PCDATA", "%basic.ph;", "%txt.incl;"])
            __entities["desc.cnt"] = self.__remove_from_list(__entities["desc.cnt"], ["#PCDATA", "%basic.ph;"])
            __entities["ph.cnt"] = self.__remove_from_list(__entities["ph.cnt"])
            __entities["fn.cnt"] = self.__remove_from_list(__entities["fn.cnt"], ["#PCDATA", "%basic.ph;"])
            __entities["term.cnt"] = self.__remove_from_list(__entities["term.cnt"])
            __entities["defn.cnt"] = self.__remove_from_list(__entities["defn.cnt"], ["#PCDATA", "%basic.ph;", "%txt.incl;"])
            __entities["pre.cnt"] = self.__remove_from_list(__entities["pre.cnt"])
            __entities["fig.cnt"] = self.__remove_from_list(__entities["fig.cnt"], ["%xref;", "%fn;"])
            __entities["words.cnt"] = self.__remove_from_list(__entities["words.cnt"])
            #__entities["data.cnt"] = self.__remove_from_list(__entities["data.cnt"], ["%words.cnt;", "%image;", "%object;", "%ph;", "%title;"])
            #__entities["body.cnt"] = self.__remove_from_list(__entities["body.cnt"], ["%basic.block;"])
            __entities["section.cnt"] = self.__remove_from_list(__entities["section.cnt"], ["#PCDATA", "%basic.ph;", "%txt.incl;"])
            __entities["section.notitle.cnt"] = self.__remove_from_list(__entities["section.notitle.cnt"], ["#PCDATA", "%basic_ph;", "%txt.incl;"])
        self.__entity(u"commonDefns", u"commonElements.ent", self.generate_public_identifier(ent, None, None, u"Common Elements"))
        self.out.write("\n")
        for __i in self.__ENTITIES:
            if "foreigndata" in models:
                self.internal_parameter_entity(__i, self.__remove_from_list(__entities[__i], ["%required-cleanup;", "%data.elements.incl;", "%foreign.unknown.incl;"]), u" | ")
            else:
                self.internal_parameter_entity(__i, __entities[__i], u" | ")
        self.out.write("\n")
    
    def __remove_from_list(self, lst, rmlst=[]):
        """Remove rmlst items from lst."""
        #rmlst.extend(["%data.elements.incl;", "%foreign.unknown.incl;"])
        return [i for i in lst if i not in rmlst]

    def _get_pi(self, ext):
        """Generate Public Identifier based on file extension."""
        if self.owner is not None:
            __title = self.title #self.topic_type.title
            if ext == u"dtd" and self.__all_domains:
                __title = u"%s (%s)" % (__title,
                                        u" ".join([__d.id for __d in self.__all_domains]))
            return self.generate_public_identifier(ext, self.topic_type.file, self._pi_version, __title, self.owner)
        else:
            return None
    
    def __print_header(self, ext, pi=None, sfi=None):
        """Print boiler plate."""
        if pi:
            __pi = pi
        else:
            __pi = self._get_pi(ext)
        if sfi:
            __sfi = sfi
        else:
            __sfi = self.topic_type.file
        if __pi:
            self.comment_block(u""" Refer to this file by the following public identifier or an 
      appropriate system identifier 
PUBLIC "%s"
      Delivered as file "%s.%s" """ % (__pi, __sfi, ext), before=0)
        else:
            self.comment_block(u""" Refer to this file by an appropriate system identifier 
      Delivered as file "%s.%s" """ % (__sfi, ext), before=0)
    
    def __content_model(self, particle, indent=""):
        """Print content model into XML content specification."""
        t = type(particle)
        if t is Name:
            return str(particle.name) + str(particle.occurrence)
        elif t is Choice:
            if len(particle.particles) == 1 and type(particle.particles[0]) is ParameterEntity:
                return "(" + str(particle.particles[0]) + ")" + str(particle.occurrence)
            else:
                return "(" + (" |\n" + indent).join([self.__content_model(n, indent + " ") for n in particle.particles]) + ")" + str(particle.occurrence)
        elif t is Seq:
            if len(particle.particles) == 1 and type(particle.particles[0]) is ParameterEntity:
                return "(" + str(particle.particles[0]) + ")" + str(self.occurrence)
            else:
                return "(" + (",\n" + indent).join([self.__content_model(n, indent + " ") for n in particle.particles]) + ")" + str(particle.occurrence)
        elif t is ParameterEntity:
            return str(particle)
        else:
            raise Exception("Unsupported particle type " + str(t) + ": " + str(particle))
    
    def __resolve_params(self, particle, params):
        if type(particle) is Param:
            return params[particle.name]
        else: 
            if type(particle) is Empty:
                return Empty()
            elif type(particle) is Any:
                return Any()
            elif type(particle) is Mixed:
                return Mixed(filter(lambda x: x != None, [self.__resolve_params(n, params) for n in particle.names]))
            if isinstance(particle, Particle):
                o = particle.occurrence
                if type(o) is Param:
                    o = params[o.name]
                if type(particle) is Name:
                    return Name(self.__resolve_params(particle.name, params), o)
                else:
                    return type(particle)(filter(lambda x: x != None, [self.__resolve_params(n, params) for n in particle.particles]), o)
            else:
                return particle
    
    def _preprocess(self):
        """Preprocess arguments."""
        if self._initialized == False:
            #if self._owner is None:
            #    self._owner = self.owner
            if self.topic_type:
                if isinstance(self.topic_type, ditagen.dita.v1_2.MapType) or isinstance(self.topic_type, ditagen.dita.v1_1.MapType):
                    self.__pi_prefix = u"MAP"
                else:
                    self.__pi_prefix = u"TOPIC"
                if len(self.domains) == 0:
                    self.__domains = []
                    self.__constraints = []
                    self.__attribute_domains = []
                else:
                    #logging.info("domains: %s"  % str(self.domains))
                    self.__all_domains = filter_domains(self.topic_type, self.domains)
                    #logging.info("__all_domains: %s"  % str(self.__all_domains))
                    sort_domains(self.__all_domains)
                    self.__domains = [__d for __d in self.__all_domains if not (issubclass(__d, ditagen.dita.v1_2.Constraints) or issubclass(__d, ditagen.dita.v1_2.AttributeDomain))]
                    self.__constraints = [__d for __d in self.__all_domains if issubclass(__d, ditagen.dita.v1_2.Constraints)]
                    self.__attribute_domains = [__d for __d in self.__all_domains if issubclass(__d, ditagen.dita.v1_2.AttributeDomain)]
                sys.stderr.write(str(self.__all_domains))
                self.__elements = []
                for __d in self.__domains + self.__constraints:
                    self.__elements.extend(__d.elements)
                self.__elements = set(self.__elements)
                self.__types = get_parent_list(self.topic_type)
                if self.topic_type.file is None:
                    self._file_name = self.topic_type.file
                else:
                    self._file_name = self.plugin_name
                if self._root_name is None:
                    self._root_name = self.topic_type.root.name#id
                #if self.version == "1.2":
                #    self._dtd_base_dir = u"../../../dtd/"
            
                if self.title is None:
                    self.title = self.topic_type.id.capitalize()
            self._pi_version = " " + self.version
            # done
            self._initialized = True

    def _run_generation(self, __zip, func, filename):
        """Run a file generation."""
        __buf = None
        __dt = datetime.now()
        __zipinfo = ZipInfo(filename.encode("UTF-8"), (__dt.year, __dt.month, __dt.day, __dt.hour, __dt.minute, __dt.second))
        __zipinfo.external_attr = 0755 << 16L # give full access to included file
        try:
            __buf = StringIO.StringIO()
            self.out = __buf
            func()
            __zip.writestr(__zipinfo, __buf.getvalue().encode("UTF-8"))
        except:
            raise Exception("Failed to write " + filename, sys.exc_info()[1]), None, sys.exc_info()[2]
        finally:
            __buf.close()
    
    # Public methods

    def get_topic_type(self):
        """ Parent topic type. """
        return self._topic_type
    def set_topic_type(self, topic_type):
        """
        Set topic type.

        The topic_type argument should be either ShellType or SpecializationType,
        but for testing purposes also other subclasses of Type can be used.
        """
        assert isinstance(topic_type, ditagen.dita.Type)
        if topic_type is None:
            raise ValueError("topic type cannot be None")
        self._topic_type = topic_type
    topic_type = property(get_topic_type, set_topic_type)
    #def set_domains(self, domains):
    #    """Set domains."""
    #    self.domains = domains
    #def set_root(self, root):
    #    #deprecated
    #    self._root_name = root
    #def set_owner(self, owner):
    #    #deprecated
    #    self._owner = owner
    #def set_nested(self, nested):
    #    """Set nested topics."""
    #    self.nested = nested
    #def set_models(self, models):
    #    self._models = models
    #def set_version(self, version):
    #    """Set DITA version."""
    #    self.version = version
    #def set_title(self, title):
    #    """Set specialization title."""
    #    self.title = title

    def generate_dtd(self):
        """generate DTD file."""
        self._preprocess()
        
        self.__print_header("dtd")
        if self.version == "1.2":
            __types_ents = [__t for __t in self.__types if __t.parent is not None and
                                                           not isinstance(__t, ditagen.dita.ShellType) and
                                                           __t.pi_entity is not None]
            for __t in self.__types:
                if __t.pi_entity is not None:
                    for __rt in __t.required_types:
                        __types_ents.append(__rt)
                    #__types_ents.extend([t for t in __t.required_types])
            if __types_ents:
                self.comment_block(u"%s ENTITY DECLARATIONS" % (self.__pi_prefix))
                for __t in __types_ents:
                    self.__element_ent(__t)
                    self.out.write("\n") 
        if self.__all_domains or self.domain_attributes:
            self.comment_block(u"DOMAIN ENTITY DECLARATIONS", before=0)
            # attribute domains
            for d in self.domain_attributes:
                self.__entity(d[0] + u"Att-d-dec", d[0] + u"AttDomain.ent",
                              self.generate_public_identifier("ent", d[0], self._pi_version,
                                                              d[0].capitalize() + " Attribute",
                                                              self.owner, u"Domain"))
                self.out.write("\n")
            # domains
            __ds = []
            __ds.extend(self.__all_domains)
            for __d in __ds:
                for __rd in __d.required_domains:
                    if __rd not in __ds:
                        __ds.append(__rd)
            #logging.info("__ds: %s"  % str(__ds))
            for __d in __ds:
                #if not issubclass(__d, ditagen.dita.v1_2.Constraints):
                self.__domain_ent(__d)
                self.out.write("\n")
            self.comment_block(u"DOMAIN EXTENSIONS", before=0)
            for __e in self.__elements:
                #self.__domain_override(__e, [d for d in self.__all_domains if d not in self.__attribute_domains])
                self.__domain_override(__e, self.__domains)
            #self.out.write("\n")
        self.comment_block(u"DOMAIN ATTRIBUTE EXTENSIONS")
        for ae in (u"props", u"base"):
            __aes = [u"%%%sAtt-d-attribute;" % (a[0]) for a in self.domain_attributes if a[1] == ae]
            __aes.extend([u"%%%s-attribute;" % a.id for a in self.__attribute_domains if ae in a.attributes])
            self.internal_parameter_entity(ae + u"-attribute-extensions", __aes)
        #if isinstance(self.topic_type, ditagen.dita.v1_1.TopicType) or isinstance(self.topic_type, ditagen.dita.v1_2.TopicType):
        if isinstancetype(self.topic_type, ditagen.dita.v1_1.TopicType) or isinstancetype(self.topic_type, ditagen.dita.v1_2.TopicType):
            self.comment_block(u"TOPIC NESTING OVERRIDE")
            self.__info_types()
        self.comment_block(u"DOMAINS ATTRIBUTE OVERRIDE", before=0)
        self.__domain_included(self.__all_domains, self.topic_type)
        # not used
        #if len(models) > 0:
        #    self.comment_block(u"CONTENT MODEL REDECLARATIONS")
        #    self.__redefine_content_models(models)
        #if global_atts != None:
        #    __ga = GlobalAtts()
        #    self.internal_parameter_entity(__ga.name,
        #                                   __ga.value + " " + global_atts)
        #    self.out.write("\n")
        #if len(__all_domains) > 0:
        if self.__constraints:
            self.comment_block(u"CONTENT CONSTRAINT INTEGRATION", before=0)
            for __d in self.__constraints:
                self.__domain_mod(__d)
                self.out.write("\n")
        self.comment_block(self.__pi_prefix + u" ELEMENT INTEGRATION", before=0)
        __types_mods = self.__types
        for __t in self.__types:
            for __rt in __t.required_types:
                if __rt not in __types_mods:
                    __types_mods.append(__rt)
        for __t in __types_mods:
            if not isinstance(__t, ditagen.dita.ShellType):
                self.__element_mod(__t)
                self.out.write("\n")
#        __specialization = None
#        if root is not None:
#            __specialization = SpecializationType(root, root.capitalize(),
#                                                  owner)
#        if __specialization is not None:
#            self.__element_mod(__specialization)
#            self.out.write("\n")
        if self.__all_domains or self.domain_attributes:
            self.comment_block(u"DOMAIN ELEMENT INTEGRATION", before=0)
            for __d in __ds:
                #if not issubclass(__d, ditagen.dita.v1_2.Constraints):
                if __d.pi_module is not None:
                    self.__domain_mod(__d)
                    self.out.write("\n")
        self.centered_comment_line(u"End of file", before=0, after=1)
    
    def generate_mod(self):
        """Generate mod file."""
        self._preprocess()

        #self.out.write("<!--%s %s-->"  % (self._root_name, self.topic_type.root.name))
        if self._root_name is None:
            __root = self.topic_type.root.name
        else:
            __root = self._root_name
        
        self.__print_header("mod")
        if isinstancetype(self.topic_type, ditagen.dita.v1_1.TopicType) or isinstancetype(self.topic_type, ditagen.dita.v1_2.TopicType):
            self.comment_block(u"SPECIALIZATION OF DECLARED ELEMENTS", before=0)
            self.internal_parameter_entity(__root + "-info-types", "%info-types;")
        #self.out.write("\n")
        self.comment_block(u"ELEMENT NAME ENTITIES")
        self.internal_parameter_entity(__root, __root)
        #self.out.write("\n")
        self.comment_block(u"DOMAINS ATTRIBUTE OVERRIDE")
        self.internal_parameter_entity(u"included-domains", u"")
        #self.out.write("\n")
        self.comment_block(u"ELEMENT DECLARATIONS", after=1)
        self.centered_comment_line(u"LONG NAME: " +  __root, " ")
        __model_params = { "nested": None, "shortdesc" : Particle.Occurrences.OPTIONAL }
        if self.nested:
            __model_params["nested"] = Choice(ParameterEntity(__root + "-info-types"), Particle.Occurrences.ZERO_OR_MORE)
        if "shortdesc" in self.models:
            __model_params["shortdesc"] = Particle.Occurrences.ONCE
        __model = self.__content_model(self.__resolve_params(self.topic_type.root.model, __model_params)," " * 26)
        #self.element_declaration(__root, __model)
        self.internal_parameter_entity(__root + ".content", "%s" % __model)
        __attrs_ent = [str(a) for a in self.topic_type.root.attrs]
        __attrs_list = [str(ParameterEntity(__root + ".attributes")),
                        str(ParameterEntity("arch-atts")),
                        u"domains CDATA \"&included-domains;\""]
        for __a in list(__attrs_list):
            if __a in __attrs_ent:
                __attrs_ent.remove(__a)
        self.internal_parameter_entity(__root + ".attributes", __attrs_ent)
        self.out.write("""<!ELEMENT %s %%%s.content;>""" % (__root, __root))
        self.out.write("\n")
        self.attribute_declaration(__root, __attrs_list)
        #self.attribute_declaration(__root, u"\n    ".join([str(s) for s in __attrs]))
        self.out.write("\n")
        self.comment_block(u"SPECIALIZATION ATTRIBUTE DECLARATIONS")
        #if self._root_name is None:
        self.__class_declaration(__root, self.topic_type.root.cls)
        #else:
        #    self.__class_declaration(__root, u"%s%s/%s " % (self.topic_type.root.cls, __root, __root))
        #self.out.write("\n")
        self.centered_comment_line(u"End of file", after=1)
    
    def generate_ent(self):
        """generate DTD entity file."""
        #if self.version == "1.2":
        self._preprocess()
        
        self.__print_header("ent")
        self.comment_block(u"%s ENTITIES" % (self.title.upper())) #(self.topic_type.title.upper()))
        __parents = [i.id for i in get_parent_list(self.topic_type)]
        self.internal_general_entity(self.topic_type.id + u"-att",
                                     u"(%s)" % (" ".join(__parents)))
        self.out.write("\n")
        self.centered_comment_line(u"End of file", after=1)
    
    def generate_att_ent(self, d):
        """generate attribute domain entity file."""
        #if self.version == "1.2":
        self._preprocess()
        
        self.__print_header("ent",
                            self.generate_public_identifier("ent", d[0], self._pi_version,
                                                            d[0].capitalize() + " Attribute",
                                                            self.owner, u"Domain"),
                            d[0] + u"AttDomain")
        self.comment_block(u"ATTRIBUTE EXTENSION ENTITY DECLARATIONS")
        if self.generate_subject_scheme:
            __value = u"%s CDATA #IMPLIED" % d[0]
        elif d[2]:
            __value = u"%s (%s) #IMPLIED" % (d[0], "|".join(d[2]))
        else:
            __value = u"%s NMTOKENS #IMPLIED" % d[0] #CDATA
        self.internal_parameter_entity(d[0]+ u"Att-d-attribute", __value)
        self.comment_block(u"DOMAIN ENTITY DECLARATION")
        self.internal_general_entity(d[0] + u"Att-d-att",
                                     u"a(%s %s)" % (d[1], d[0]))
        self.centered_comment_line(u"End of file", after=1)
    
    #def get_file_name(self, topic_type, root, ext):
    def get_file_name(self, id, root, ext):
        """Get file name."""
        #if root is None:
        #    return "{0}.{1}".format(topic_type.id, ext)
        #else:
        #    return "{0}.{1}".format(root, ext)
        return u"%s.%s" % (id, ext)
    
    #def generate_zip(self, out, topic_type, domains, root, owner, nested):
    #def generate_zip(self, __output):
    #    """Generate ZIP file with specified DTD."""
    #    self._preprocess()
    #
    #    __output = self.out
    #
    #    __temp = StringIO.StringIO()
    #    try:
    #        __zip = ZipFile(__temp, "w")
    #        __zip.debug = 3
    #        try:
    #            #_file_name = str(self.topic_type.file)
    #            # DTD
    #            self._run_generation(__zip,
    #                                self.generate_dtd,
    #                                self._file_name + ".dtd")
    #            if isinstance(self.topic_type, ditagen.dita.SpecializationType):
    #                # MOD
    #                self._run_generation(__zip,
    #                                    self.generate_mod,
    #                                    self._file_name + ".mod")
    #                if self.version == "1.2":
    #                    # ENT
    #                    self._run_generation(__zip,
    #                                        self.generate_ent,
    #                                        self._file_name + ".ent")
    #                    # ATTR ENT
    #                    if self.domain_attributes:
    #                        self._run_generation(__zip,
    #                                            self.generate_att_ent,
    #                                            self._file_name + "AttDomain.ent")
    #                    
    #        except:
    #            print "Failed to write zip:", sys.exc_info()[0]
    #            raise
    #        finally:
    #            if __zip != None:
    #                __zip.close()
    #        __output.write(__temp.getvalue())
    #    except:
    #        print "Failed to write ZIP file to output:", sys.exc_info()[0]
    #        raise
    #    finally:
    #        __temp.close()


class PluginGenerator(DitaGenerator):
    """Generator for a DITA-OT plugin."""
    
    def __init__(self):
        DitaGenerator.__init__(self)
        self.plugin_name = None
        self.plugin_version = None
        self._stylesheet_stump = []

    def _preprocess(self):
        """Preprocess arguments."""
        if self._initialized == False:
            DitaGenerator._preprocess(self)
            #if self.plugin_name is None:
            #    self.plugin_name = self.topic_type.id
            # done
            self._initialized = True
            
    def set_stylesheet(self, stylesheet_base):
        """Set stylesheet to generate stub for."""
        # TODO: Remove once clients have been changed
        if type(stylesheet_base) != list:
            raise ValueError("Argument must be a list of strings")
        for s in stylesheet_base:
            if s not in ("docbook", "eclipse.plugin", "fo", "rtf", "xhtml"):
                raise ValueError("unsupported stylesheet " + s)
        self._stylesheet_stump = stylesheet_base
    
    def __generate_integrator(self):
        """Generate plugin integrator Ant file."""
        __root = ET.Element("project", {
            "name": self.plugin_name,
            "default": "all",
            "basedir": "../.."
            })
        ET.SubElement(__root, "import", {
            "file": "${basedir}/integrator.xml"
            })
        ET.SubElement(__root, "target", {
            "name": "all",
            "depends": "integrate"
            })
        indent(__root)
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def __generate_plugin_file(self):
        """Generate plugin configuration file."""
        __root = ET.Element("plugin", {
            "id": "org.dita.specialization." + self.plugin_name
            })
        if self.plugin_version != None:
            ET.SubElement(__root, "feature", {
                    "extension": 'package.version',
                    "value": self.plugin_version
                    })
        if self.owner is not None or self.topic_type.system_identifier is not None:
            ET.SubElement(__root, "feature", {
                "extension": 'dita.specialization.catalog.relative',
                "value": 'catalog-dita.xml',
                "type": 'file'
                })
        for ss in self._stylesheet_stump:
            ET.SubElement(__root, "feature", {
                "extension": 'dita.xsl.' + ss,
                "value": 'xslt/%s2%s.xsl' % (self._root_name, ss),
                "type": 'file'
                })
        indent(__root)
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")
    
    def __generate_catalog(self):
        """Generate catalog file."""
        #_file_name = str(self.topic_type.file)
        __c = []
        if self.topic_type:
            __c.append((self._get_pi("dtd"), "%s.dtd" % self._file_name))
            if isinstance(self.topic_type, ditagen.dita.SpecializationType):
                __c.append((self._get_pi("mod"), "%s.mod" % self._file_name))
                if self.version == "1.2":
                    __c.append((self._get_pi("ent"), "%s.ent" % self._file_name))
        for d in self.domain_attributes:
            __c.append((self.generate_public_identifier("ent", d[0], self._pi_version,
                                                              d[0].capitalize() + " Attribute",
                                                              self.owner, u"Domain"),
                        "%sAttDomain.ent" % d[0]))
        
        __root = ET.Element("catalog", prefer="public")
        #__group = ET.SubElement(__root, "group", {
        #    "xml:base": "plugins/%s/dtd/" % self.plugin_name
        #    })
        for (pi, sfi) in __c:
            ET.SubElement(__root, "public", {
                "publicId": pi,
                "uri": "dtd/%s" % sfi
                })
        indent(__root)
        set_prefixes(__root, {"": "urn:oasis:names:tc:entity:xmlns:xml:catalog"})
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")
    
    def __generate_subject_scheme(self):
        """Generate subject scheme."""
        __root = ET.Element("subjectScheme")
        for a in self.domain_attributes:
            __def = ET.SubElement(__root, "subjectdef", {"keys": a[0] + ".values"})
            for v in a[2]:
                ET.SubElement(__def, "subjectdef", {"keys": v})
            __enum = ET.SubElement(__root, "enumerationdef")
            ET.SubElement(__enum, "attributedef", {"name": a[0]})
            ET.SubElement(__enum, "subjectdef", {"keyref": a[0] + ".values"})
            #ET.SubElement(__enum, "defaultSubject", {"keyref": a[0] + ".values"})
        indent(__root)
        __d = ET.ElementTree(__root)
        self.out.write("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE subjectScheme PUBLIC "-//OASIS//DTD DITA Subject Scheme Map//EN" "subjectScheme.dtd">
""")
        __d.write(self.out, "UTF-8", False)
    
    def __generate_stylesheet(self):
        """Generate stylesheet file."""
        __root = ET.Element(NS_XSL + "stylesheet", {
            "version": "1.0"
            })
        #__import = "../../../xsl/dita2{0}.xsl".format(self._stylesheet_stump)
        #ET.SubElement(__root, NS_XSL + "import", { "href": __import })
        indent(__root)
        set_prefixes(__root, {"xsl": "http://www.w3.org/1999/XSL/Transform", "fo": "http://www.w3.org/1999/XSL/Format"})
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")
        
    def generate_plugin(self):
        """Generate ZIP file with specified DTD."""
        self._preprocess()
        
        __output = self.out
                
        __temp = StringIO.StringIO()
        try:
            __zip = ZipFile(__temp, "w")
            __zip.debug = 3
            try:
                #_file_name = str(self.topic_type.file)
                if self.topic_type:
                    # DTD
                    self._run_generation(__zip,
                                        self.generate_dtd,
                                        "%s/dtd/%s.dtd" % (self.plugin_name, self._file_name))
                    if isinstance(self.topic_type, ditagen.dita.SpecializationType):
                        # MOD
                        self._run_generation(__zip,
                                            self.generate_mod,
                                            "%s/dtd/%s.mod" % (self.plugin_name, self._file_name))
                        # ENT
                        if self.version == "1.2":
                            self._run_generation(__zip,
                                                self.generate_ent,
                                                "%s/dtd/%s.ent" % (self.plugin_name, self._file_name))
                # ATTR ENT
                for a in self.domain_attributes:
                    self._run_generation(__zip,
                                        lambda: self.generate_att_ent(a),
                                        "%s/dtd/%sAttDomain.ent" % (self.plugin_name, a[0]))
                # integrator
                self._run_generation(__zip,
                                    self.__generate_integrator,
                                    "%s/integrator.xml" % (self.plugin_name))
                # plugin
                self._run_generation(__zip,
                                    self.__generate_plugin_file,
                                    "%s/plugin.xml" % (self.plugin_name))
                # catalog
                if self.owner is not None:
                    self._run_generation(__zip,
                                        self.__generate_catalog,
                                        "%s/catalog-dita.xml" % (self.plugin_name))
                # subject scheme
                if self.generate_subject_scheme and self.version >= 1.2:
                    if self.domain_attributes:
                        self._run_generation(__zip,
                                            self.__generate_subject_scheme,
                                            "%s/subject_scheme.ditamap" % (self.plugin_name))
                # stylesheet
                for ss in self._stylesheet_stump:
                    self._run_generation(__zip,
                                        self.__generate_stylesheet,
                                        "%s/xslt/%s2%s.xsl" % (self.plugin_name, self._root_name, ss))
            except:
                raise Exception("Failed to write plugin", sys.exc_info()[1]), None, sys.exc_info()[2]
            finally:
                if __zip != None:
                    __zip.close()
            __output.write(__temp.getvalue())
        except:
            logging.error("Failed to write ZIP file to output:", sys.exc_info()[0])
            raise
        finally:
            __temp.close()

class Version(object):
    """DITA-OT version number object."""

    def __init__(self, version):
        self.version = version
        self.tokens = [int(i) for i in version.split(".")]

    def __str__(self):
        return self.version

    def __cmp__(self, other):
        if self.version == other.version:
            return 0
        else:
            n = min([len(self.tokens), len(other.tokens)])
            for i in range(n):
                #c = self.tokens[i].__cmp__(other.tokens[i])
                if self.tokens[i] > other.tokens[i]:
                    return 1
                elif self.tokens[i] < other.tokens[i]:
                    return -1
            if len(self.tokens) > n:
                return 1
            else:
                return -1

def sort_domains(domains):
    """Sort domains in order of required domains.

    FIXME: Currently only sorts domains with no requirements first
    """
    domains.sort(domain_comparator)

class SparseDict(dict):
    def __missing__(self, key):
        return 3

from collections import defaultdict
__domain_order = defaultdict(lambda: 3)
__domain_order.update({ u"hi-d": 0, u"ui-d": 1, u"indexing-d": 2 })

def domain_comparator(x, y):
    """ Sort constraints after domains, then by required domains amount. """
    if issubclass(x, ditagen.dita.v1_2.Constraints) and not issubclass(y, ditagen.dita.v1_2.Constraints):
        return 1
    elif issubclass(y, ditagen.dita.v1_2.Constraints) and not issubclass(x, ditagen.dita.v1_2.Constraints):
        return -1
    elif x.id in __domain_order or y.id in __domain_order:
        return __domain_order[x.id] - __domain_order[y.id]
    else:
        return len(x.required_domains) - len(y.required_domains)

def filter_domains(topic_type, domains):
    """Filter the domains list for aliases, non-applicable domains, and add reqired domains."""
    #__domains = [d for d in domains if issubclass(topic_type, d.parent)]
    __result_domains = []
    #__alias = topic_type.get_alias()
    for __d in domains:
        for __p in __d.parent:
            if isinstancetype(topic_type, __p):# or isinstance(topic_type.parent, __p):# or isinstance(__alias, __p):
                #print "add " + str(__d)
                __result_domains.append(__d)
                break
    __t = topic_type
    while __t is not None:
        for __d in __t.required_domains:
            __result_domains.append(__d)
        __t = __t.parent
    __result_domains.sort()
    return unique(__result_domains, lambda x: x) #unique_classes(__result_domains)

def unique_classes(seq):
    """Remove duplicates by class."""
    return unique(seq, lambda x: x.__class__.__name__)

def unique(seq, idfun=None):
    """Remove duplicates preserving order."""
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result

def get_parent_list(topic_type):
    """Get list of topic type's super types, including topic type itself."""
    __result_types = []
    #if topic_type.get_alias() is None:
    #if not isinstancetype(topic_type, ditagen.dita.ShellType):
    __result_types.append(topic_type)
    __t = topic_type
    #else:
    #    __result_types.append(topic_type.get_alias())
    #    __t = topic_type.get_alias()
    while __t.parent != None:
        __result_types.insert(0, __t.parent)
        __t = __t.parent
    return __result_types
    
def isinstancetype(__type, type_class):
    """Recursive isinstance for types."""
    __t = __type
    while __t is not None:
        if isinstance(__t, type_class):
            return True
        __t = __t.parent
    return False

#def kimber_urn_pi(ext, dita_version, title, owner=None, suffix=None):
#    """Generate Kimber URN public indentifier."""
#    __ENTITY_MAP = {
#        "dtd": u"doctypes",
#        "ent": u"entities",
#        "mod": u"modules"
#        }
#    return owner + ":" + description + ":" + version

#u"ELEMENTS DITA" + self._pi_version + " " + title + u" Constraints"
#u"ELEMENTS DITA" + self._pi_version + " " + title + u" Domain"
#u"ENTITIES DITA" + self._pi_version + " " + title + u" Domain"
#u"ENTITIES DITA" + self._pi_version + " " + title,
#u"ELEMENTS DITA" + self._pi_version + " " + title,
#dec
#mod -> "ELEMENTS"
#ent -> "ENTITIES"
#dtd

def indent(elem, level=0, max=100):
    """XML pretty-printer."""
    i = "\n" + level*"  "
    if len(elem):
        if level < max:
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        if level < max:
            for elem in elem:
                indent(elem, level+1, max)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            
def set_prefixes(elem, prefix_map):
    # check if this is a tree wrapper
    if not ET.iselement(elem):
        elem = elem.getroot()
    # build uri map and add to root element
    uri_map = {}
    for prefix, uri in prefix_map.items():
        uri_map[uri] = prefix
        if prefix == "":
            elem.set("xmlns", uri)
        else:
            elem.set("xmlns:" + prefix, uri)
    # fixup all elements in the tree
    memo = {}
    for elem in elem.getiterator():
        fixup_element_prefixes(elem, uri_map, memo)

def fixup_element_prefixes(elem, uri_map, memo):
    def fixup(name):
        try:
            return memo[name]
        except KeyError:
            if hasattr(name, "__getitem__"):
                if name[0] != "{":
                    return
                uri, tag = name[1:].split("}")
                if uri in uri_map:
                    new_name = uri_map[uri] + ":" + tag
                    memo[name] = new_name
                    return new_name
    # fix element name
    name = fixup(elem.tag)
    if name:
        elem.tag = name
    # fix attribute names
    for key, value in elem.items():
        name = fixup(key)
        if name:
            elem.set(name, value)
            del elem.attrib[key]
