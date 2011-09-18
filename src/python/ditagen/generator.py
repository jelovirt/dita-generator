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
import ditagen.dita
import ditagen.dita.v1_1
import ditagen.dita.v1_2
from ditagen.dtdgen import Attribute as Attribute
from ditagen.dtdgen import ParameterEntity as ParameterEntity
import StringIO
from zipfile import ZipFile, ZipInfo
from xml.etree import ElementTree as ET

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
    
    def __get_start_indent(self, len):
        """Get whitespace before entity value."""
        if len > (24 + 1):
            return "\n" + " " * 24
        else:
            return " " * (24 + 2 - len)
    
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
        self.__pfi_prefix = None
        self.__constraints = None
        self.__elements = None
        self._file_name = None
        self.__all_domains = []
        self.domain_attributes = []

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
        """Print domain entity declaration."""
        self.__entity(domain.id + u"-dec", self._dtd_base_dir + domain.file + u".ent",
                      self.generate_public_identifier("ent", domain.id, self._pfi_version, domain.title, None, u"Domain"))
    
    def __domain_mod(self, domain):
        """Print domain module declaration."""
        if isinstance(domain, ditagen.dita.v1_2.Constraints):
            __description = self.generate_public_identifier("mod", domain.id, self._pfi_version, domain.title, None, u"Constraint")
        else:
            __description = self.generate_public_identifier("mod", domain.id, self._pfi_version, domain.title, None, u"Domain")
        self.__entity(domain.id + u"-def", self._dtd_base_dir + domain.file + u".mod",
                      __description)
    
    def __element_ent(self, topic_type):
        """Print element entity declaration."""
        __f = topic_type.file + u".ent"
        if topic_type is not self.topic_type:
            __f = self._dtd_base_dir + __f
        self.__entity(topic_type.id + u"-dec",# u"-d-dec"
                      __f,
                      self.generate_public_identifier("ent", topic_type.id, self._pfi_version, topic_type.title, topic_type.owner),
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
        self.__entity(topic_type.id + __suffix,
                      __f,
                      self.generate_public_identifier("mod", topic_type.id, self._pfi_version, topic_type.title, topic_type.owner),
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
        __included_domains = []
        if self.version == "1.2":
            for __t in self.__types:
                if __t.parent is not None and not isinstance(__t, ditagen.dita.ShellType):
                    __included_domains.append(u"&%s-att;" % (__t.id))
            for __t in self.__types:
                for __rt in __t.required_types:
                    __included_domains.append(u"&%s-att;" % (__rt.id))
        for __d in domains:
            if isinstance(__d, ditagen.dita.Domain):
                __s = u"&%s-att;"
            elif isinstance(__d, ditagen.dita.v1_2.Constraints):
                __s = u"&%s-constraints;"
            __included_domains.append(__s % (__d.get_att_id()))
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

    def _get_pfi(self, ext):
        """Generate Formal Public Identifier based on file extension."""
        if self.owner is not None:
            __title = self.title #self.topic_type.title
            if ext == u"dtd" and self.__all_domains:
                __title = u"%s (%s)" % (__title,
                                               u" ".join([__d.id for __d in self.__all_domains]))
            return self.generate_public_identifier(ext, self.topic_type.file, self._pfi_version, __title, self.owner)
        else:
            return None
    
    def __print_header(self, ext, pfi=None, sfi=None):
        """Print boiler plate."""
        if pfi:
            __pfi = pfi
        else:
            __pfi = self._get_pfi(ext)
        if sfi:
            __sfi = sfi
        else:
            __sfi = self.topic_type.file
        if __pfi:
            self.comment_block(u""" Refer to this file by the following public identifier or an 
      appropriate system identifier 
PUBLIC "%s"
      Delivered as file "%s.%s" """ % (__pfi, __sfi, ext), before=0)
        else:
            self.comment_block(u""" Refer to this file by an appropriate system identifier 
      Delivered as file "%s.%s" """ % (__sfi, ext), before=0)
    
    def _preprocess(self):
        """Preprocess arguments."""
        if self._initialized == False:
            #if self._owner is None:
            #    self._owner = self.owner
            if self.topic_type:
                if isinstance(self.topic_type, ditagen.dita.v1_2.MapType) or isinstance(self.topic_type, ditagen.dita.v1_1.MapType):
                    self.__pfi_prefix = u"MAP"
                else:
                    self.__pfi_prefix = u"TOPIC"
                if len(self.domains) == 0:
                    self.__domains = []
                    self.__constraints = []
                else:
                    self.__all_domains = filter_domains(self.topic_type, self.domains)
                    sort_domains(self.__all_domains)
                    self.__domains = [__d for __d in self.__all_domains if not isinstance(__d, ditagen.dita.v1_2.Constraints)]
                    self.__constraints = [__d for __d in self.__all_domains if isinstance(__d, ditagen.dita.v1_2.Constraints)]
                self.__elements = []
                for __d in self.__all_domains:
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
            self._pfi_version = " " + self.version
            # done
            self._initialized = True

    def _run_generation(self, __zip, func, filename):
        """Run a file generation."""
        __buf = None
        __zipinfo = ZipInfo(filename.encode("UTF-8"))
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
            __types_ents = [__t for __t in self.__types if __t.parent is not None]
            for __t in self.__types:
                __types_ents.extend(__t.required_types)
            if __types_ents:
                self.comment_block(u"%s ENTITY DECLARATIONS" % (self.__pfi_prefix))
                for __t in __types_ents:
                    if not isinstance(__t, ditagen.dita.ShellType):
                        self.__element_ent(__t)
                        self.out.write("\n")
        if self.__all_domains or self.domain_attributes:
            self.comment_block(u"DOMAIN ENTITY DECLARATIONS", before=0)
            for d in self.domain_attributes:
                self.__entity(d[0] + u"Att-d-dec", d[0] + u"AttDomain.ent",
                              self.generate_public_identifier("ent", d[0], self._pfi_version,
                                                              d[0].capitalize() + " Attribute",
                                                              self.owner, u"Domain"))
                self.out.write("\n")
            for __d in self.__domains:
                #if not isinstance(__d, ditagen.dita.v1_2.Constraints):
                self.__domain_ent(__d)
                self.out.write("\n")
            self.comment_block(u"DOMAIN EXTENSIONS", before=0)
            for __e in self.__elements:
                self.__domain_override(__e, self.__all_domains)
            #self.out.write("\n")
        self.comment_block(u"DOMAIN ATTRIBUTE EXTENSIONS")
        for ae in (u"props", u"base"):
            __aes = [u"%%%sAtt-d-attribute;" % (a[0]) for a in self.domain_attributes if a[1] == ae]
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
        self.comment_block(self.__pfi_prefix + u" ELEMENT INTEGRATION", before=0)
        __types_mods = self.__types
        for __t in self.__types:
            __types_mods.extend(__t.required_types)
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
        if self.__domains:
            self.comment_block(u"DOMAIN ELEMENT INTEGRATION", before=0)
            for __d in self.__domains:
                #if not isinstance(__d, ditagen.dita.v1_2.Constraints):
                self.__domain_mod(__d)
                self.out.write("\n")
        self.centered_comment_line(u"End of file", before=0, after=1)
    
    def generate_mod(self):
        """Generate mod file."""
        self._preprocess()

        self.out.write("<!--%s %s-->"  % (self._root_name, self.topic_type.root.name))
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
        __model_params = { "nested": u"", "shortdesc" : u"?" }
        if self.nested:
            __model_params["nested"] = u", (%%%s-info-types;)*" % (__root)
        if "shortdesc" in self.models:
            __model_params["shortdesc"] = u""
        __model = self.topic_type.root.model % (__model_params)
        #self.element_declaration(__root, __model)
        self.internal_parameter_entity(__root + ".content", "(%s)" % __model)
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
                            self.generate_public_identifier("ent", d[0], self._pfi_version,
                                                            d[0].capitalize() + " Attribute",
                                                            self.owner, u"Domain"),
                            d[0] + u"AttDomain")
        self.comment_block(u"ATTRIBUTE EXTENSION ENTITY DECLARATIONS")
        if d[2]:
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
            __c.append((self._get_pfi("dtd"), "%s.dtd" % self._file_name))
            if isinstance(self.topic_type, ditagen.dita.SpecializationType):
                __c.append((self._get_pfi("mod"), "%s.mod" % self._file_name))
                if self.version == "1.2":
                    __c.append((self._get_pfi("ent"), "%s.ent" % self._file_name))
        for d in self.domain_attributes:
            __c.append((self.generate_public_identifier("ent", d[0], self._pfi_version,
                                                              d[0].capitalize() + " Attribute",
                                                              self.owner, u"Domain"),
                        "%sAttDomain.ent" % d[0]))
        
        __root = ET.Element("catalog", {
            "xmlns": "urn:oasis:names:tc:entity:xmlns:xml:catalog",
            "prefer": "public"
            })
        #__group = ET.SubElement(__root, "group", {
        #    "xml:base": "plugins/%s/dtd/" % self.plugin_name
        #    })
        for (pfi, sfi) in __c:
            ET.SubElement(__root, "public", {
                "publicId": pfi,
                "uri": "dtd/%s" % sfi
                })
        indent(__root)
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")
    
    def __generate_stylesheet(self):
        """Generate stylesheet file."""
        __root = ET.Element("xsl:stylesheet", {
            "xmlns:xsl": "http://www.w3.org/1999/XSL/Transform",
            "version": "1.0"
            })
        #__import = "../../../xsl/dita2{0}.xsl".format(self._stylesheet_stump)
        #ET.SubElement(__root, "xsl:import", { "href": __import })
        indent(__root)
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
            print "Failed to write ZIP file to output:", sys.exc_info()[0]
            raise
        finally:
            __temp.close()

class StylePluginGenerator(DitaGenerator):
    """Generator for a DITA-OT style plug-in."""

    def __init__(self):
        DitaGenerator.__init__(self)
        self.ot_version = None
        self.transtype = None
        self.plugin_name = None
        self.plugin_version = None
        self.page_size = None
        self.page_margins = None
        self.font_family = None
        self.color = None
        self.link_font_weight = None
        self.link_font_style = None
        self.link_color = None
        self.link_text_decoration = None
        self.force_page_count = None
        self.chapter_layout = None
        self.body_column_count = None
        self.bookmark_style = None
        self.toc_maximum_level = None
        self.task_label = None
        self.include_related_links = None
        self.side_col_width = None
        self._stylesheet_stump = []

    def _preprocess(self):
        """Preprocess arguments."""
        if self._initialized == False:
            DitaGenerator._preprocess(self)
            self._initialized = True

    def __generate_integrator(self):
        """Generate plugin integrator Ant file."""
        __root = ET.Element("project", {
            "name": self.plugin_name,
            })
        __init = ET.SubElement(__root, "target", {
            "name": ("dita2%s.init" % self.transtype)
            })
        ET.SubElement(__init, "property", {
            "name": "customization.dir",
            "location": ("${dita.plugin.%s.dir}/cfg" % self.plugin_name)
            })
        if self.chapter_layout:
            ET.SubElement(__init, "property", {
                "name": "args.chapter.layout",
                "value": self.chapter_layout
                })
        if self.bookmark_style:
            ET.SubElement(__init, "property", {
                "name": "args.bookmark.style",
                "value": self.bookmark_style
                })
        if self.task_label:
            ET.SubElement(__init, "property", {
                "name": "args.gen.task.lbl",
                "value": self.task_label
                })
        if self.include_related_links:
            ET.SubElement(__init, "property", {
                "name": "args.fo.include.rellinks",
                "value": self.include_related_links
                })
        ET.SubElement(__root, "target", {
            "name": "dita2%s" % self.transtype,
            "depends": ("dita2%s.init, dita2pdf2" % self.transtype),
            })
        indent(__root)
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def __generate_plugin_file(self):
        """Generate plugin configuration file."""
        __root = ET.Element("plugin", id=self.plugin_name)
        if self.plugin_version:
            ET.SubElement(__root, "feature", extension="package.version", value=self.plugin_version)
        ET.SubElement(__root, "require", plugin="org.dita.pdf2")
        ET.SubElement(__root, "feature", extension="dita.conductor.transtype.check", value=self.transtype)
        ET.SubElement(__root, "feature", extension="dita.conductor.target.relative", file="integrator.xml")
        indent(__root)
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def __generate_catalog(self):
        """Generate plugin configuration file."""
        __root = ET.Element("catalog", xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog", prefer="system")
        ET.SubElement(__root, "uri", name="cfg:fo/attrs/custom.xsl", uri="fo/attrs/custom.xsl")
        #ET.SubElement(__root, "uri", name="cfg:fo/xsl/custom.xsl", uri="fo/xsl/custom.xsl")
        indent(__root)
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def __generate_custom(self):
        """Generate plugin custom XSLT file."""
        __root = ET.Element("xsl:stylesheet", {
            "xmlns:xsl": "http://www.w3.org/1999/XSL/Transform",
            "xmlns:fo": "http://www.w3.org/1999/XSL/Format",
            "version": "2.0"})
        indent(__root)
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def __generate_custom_attr(self):
        """Generate plugin custom XSLT file."""
        __root = ET.Element("xsl:stylesheet", {
            "xmlns:xsl": "http://www.w3.org/1999/XSL/Transform",
            "xmlns:fo": "http://www.w3.org/1999/XSL/Format",
            "version": "2.0"})
        
        __root_attr = ET.SubElement(__root, u"xsl:attribute-set", name="__fo__root")
        # font family
        if self.font_family:
            ET.SubElement(__root_attr, u"xsl:attribute", name=u"font-family").text = self.font_family
        # font color
        if self.color:
            ET.SubElement(__root_attr, u"xsl:attribute", name=u"color").text = self.color
        # link
        link_attr_sets = []
        if self.ot_version >= Version("1.5.4"):
            link_attr_sets.extend(["common.link"])
        else:
            link_attr_sets.extend(["link__content", "xref"])
        for n in link_attr_sets:
            __link_attr = ET.SubElement(__root, u"xsl:attribute-set", name=n)
            if self.link_color:
                ET.SubElement(__link_attr, u"xsl:attribute", name=u"color").text = self.link_color
            if self.link_font_weight:
                ET.SubElement(__link_attr, u"xsl:attribute", name=u"font-weight").text = self.link_font_weight
            if self.link_font_style:
                ET.SubElement(__link_attr, u"xsl:attribute", name=u"font-style").text = self.link_font_style
            if self.link_text_decoration:
                ET.SubElement(__link_attr, u"xsl:attribute", name=u"text-decoration").text = self.link_text_decoration

        # page column count
        if self.body_column_count and self.ot_version >= Version("1.5.4"):
            for a in ["region-body.odd", "region-body.even"]:
                __region_body_attr = ET.SubElement(__root, u"xsl:attribute-set", name=a)
                ET.SubElement(__region_body_attr, u"xsl:attribute", name=u"column-count").text = self.body_column_count
            for a in ["region-body__frontmatter.odd", "region-body__frontmatter.even"]:
                __region_body_attr = ET.SubElement(__root, u"xsl:attribute-set", name=a)
                ET.SubElement(__region_body_attr, u"xsl:attribute", name=u"column-count").text = "1"

        # force page count
        if self.force_page_count:
            __page_count_attr = ET.SubElement(__root, u"xsl:attribute-set", name="__force__page__count")
            ET.SubElement(__page_count_attr, u"xsl:attribute", name=u"force-page-count").text = self.force_page_count
        # page size
        if self.page_size:
            ET.SubElement(__root, u"xsl:variable", name=u"page-width").text = self.page_size[0]
            ET.SubElement(__root, u"xsl:variable", name=u"page-height").text = self.page_size[1]
        # page margins
        for k, v in self.page_margins.iteritems():
            if v:
                ET.SubElement(__root, u"xsl:variable", name=k).text = v
        # font size
        if self.default_font_size:
            ET.SubElement(__root, u"xsl:variable", name=u"default-font-size").text = self.default_font_size
        # body indent
        if self.side_col_width:
            ET.SubElement(__root, u"xsl:variable", name=u"side-col-width").text = self.side_col_width
        # toc
        if self.toc_maximum_level:
            ET.SubElement(__root, u"xsl:variable", name=u"tocMaximumLevel").text = self.toc_maximum_level
        
        indent(__root)
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def generate_plugin(self):
        """Generate ZIP file with specified stylesheets."""
        self._preprocess()

        __output = self.out

        __temp = StringIO.StringIO()
        __failed = False
        try:
            __zip = ZipFile(__temp, "w")
            __zip.debug = 3
            try:
                # integrator
                self._run_generation(__zip, self.__generate_integrator,
                                    "%s/integrator.xml" % (self.plugin_name))
                # plugin
                self._run_generation(__zip, self.__generate_plugin_file,
                                    "%s/plugin.xml" % (self.plugin_name))
                # catalog
                self._run_generation(__zip, self.__generate_catalog,
                                    "%s/cfg/catalog.xml" % (self.plugin_name))
                # custom XSLT
#                self._run_generation(__zip, self.__generate_custom,
#                                    "%s/cfg/fo/xsl/custom.xsl" % (self.plugin_name))
                # custom XSLT attribute sets
                self._run_generation(__zip, self.__generate_custom_attr,
                                    "%s/cfg/fo/attrs/custom.xsl" % (self.plugin_name))
            except:
                __failed = True
                raise Exception("Failed to write plugin", sys.exc_info()[1]), None, sys.exc_info()[2]
            finally:
                if __zip != None:
                    __zip.close()
            if not __failed:
                __output.write(__temp.getvalue())
        except:
            __failed = True
            raise Exception("Failed to write ZIP file to output", sys.exc_info()[1]), None, sys.exc_info()[2]
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
                c = self.tokens[i].__cmp__(other.tokens[i])
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
    if isinstance(x, ditagen.dita.v1_2.Constraints) and not isinstance(y, ditagen.dita.v1_2.Constraints):
        return 1
    elif isinstance(y, ditagen.dita.v1_2.Constraints) and not isinstance(x, ditagen.dita.v1_2.Constraints):
        return -1
    elif x.id in __domain_order or y.id in __domain_order:
        return __domain_order[x.id] - __domain_order[y.id]
    else:
        return len(x.required_domains) - len(y.required_domains)

def filter_domains(topic_type, domains):
    """Filter the domains list for aliases, non-applicable domains, and add reqired domains."""
    #__domains = [d for d in domains if isinstance(topic_type, d.parent)]
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
            __result_domains.append(__d())
        __t = __t.parent
    __result_domains.sort()
    return unique_classes(__result_domains)

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
    """
    Get list of topic type's super types, including topic type itself.
    
    If the topic type is an alias type, add alias into the list instead.
    """
    __result_types = []
    #if topic_type.get_alias() is None:
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

#u"ELEMENTS DITA" + self._pfi_version + " " + title + u" Constraints"
#u"ELEMENTS DITA" + self._pfi_version + " " + title + u" Domain"
#u"ENTITIES DITA" + self._pfi_version + " " + title + u" Domain"
#u"ENTITIES DITA" + self._pfi_version + " " + title,
#u"ELEMENTS DITA" + self._pfi_version + " " + title,
#dec
#mod -> "ELEMENTS"
#ent -> "ENTITIES"
#dtd

def indent(elem, level=0):
    """XML pretty-printer."""
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
