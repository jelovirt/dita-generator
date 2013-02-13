# -*- coding: UTF-8; indent-tabs-mode:nil; tab-width:4 -*-
# This file is part of DITA DTD Generator.
#
# Copyright 2012 Jarno Elovirta <http://www.elovirta.com/>
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

import ditagen.dita
from ditagen.dtdgen import Attribute as Attribute
from ditagen.dtdgen import ParameterEntity as ParameterEntity

import ditagen.dita.v1_2
from ditagen.dita.v1_2 import TopicType as TopicType
from ditagen.dita.v1_2 import MapType as MapType
from ditagen.dita.v1_2 import MapGroupDomain as MapGroupDomain
from ditagen.dita.v1_2 import IndexingDomain as IndexingDomain
from ditagen.dita.v1_2 import HiDomain as HiDomain

# Elements
#####################################################################

class ArticleElement(ditagen.dita.DitaElement):
    """Article element."""
    name = u"article"
    cls = u"- topic/topic article/article "
    model = """"(%%title;),
                (%%titlealts;)?,
                (%%abstract; | %%deck;)?,
                (%%prolog;)?,
                (%%body;)?,
                (%%related-links;)?,
                %(nested)s"""
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]
    
class SubsectionElement(ditagen.dita.DitaElement):
    """Subsection element."""
    name = u"subsection"
    cls = u"- topic/topic subsection/subsection "
    model = """"(%%title;),
                (%%titlealts;)?,
                (%%abstract; | %%shortdesc;)?,
                (%%prolog;)?, 
                (%%body;)?,
                (%%related-links;)?,
                %(nested)s"""
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]

class SidebarElement(ditagen.dita.DitaElement):
    """Sidebar element."""
    name = u"sidebar"
    cls = u"- topic/topic sidebar/sidebar "
    model = """"(%%title;),
                (%%titlealts;)?,
                (%%abstract; | %%shortdesc;)?,
                (%%prolog;)?, 
                (%%body;)?,
                (%%related-links;)?,
                %(nested)s"""
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]
    
class ChapterElement(ditagen.dita.DitaElement):
    """Chapter element."""
    name = u"chapter"
    cls = u"- topic/topic chapter/chapter "
    model = """"(%%title;),
                (%%titlealts;)?,
                (%%abstract; | %%shortdesc;)?,
                (%%prolog;)?, 
                (%%body;)?,
                (%%related-links;)?,
                %(nested)s"""
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]

class PartElement(ditagen.dita.DitaElement):
    """Part element."""
    name = u"part"
    cls = u"- topic/topic part/part "
    model = """"(%%title;),
                (%%titlealts;)?,
                (%%abstract; | %%shortdesc;)?,
                (%%prolog;)?, 
                (%%body;)?,
                (%%related-links;)?,
                %(nested)s"""
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]

class CoverElement(ditagen.dita.DitaElement):
    """Cover element."""
    name = u"cover"
    cls = u"- topic/topic cover/cover "
    model = """"(%%title;),
                (%%titlealts;)?,
                (%%abstract; | %%shortdesc;)?,
                (%%prolog;)?, 
                (%%body;)?,
                (%%related-links;)?,
                %(nested)s"""
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]
class PubmapElement(ditagen.dita.DitaElement):
    """Pubmap element."""
    name = u"pubmap"
    cls = u"- map/map pubmap/pubmap "
    model = """(%%pubtitle;)?, 
               (%%pubmeta;)?,
               (%%keydefs;)?,
               (%%topicref;)*,
               ((%%mapref;) |
                ((%%publication;) |
                 (%%publication-mapref;))|
                ((%%covers;)?,
                 (%%colophon;)?, 
                 ((%%frontmatter;) |
                  (%%department;) |
                  (%%page;))*,
                 ((%%pubbody;) |
                  (%%part;) |
                  (%%chapter;) |
                  (%%sidebar;) |
                  (%%subsection;))?, 
                 ((%%appendixes;) |
                  (%%appendix;) |
                  (%%backmatter;) |
                  (%%page;) |
                  (%%department;) |
                  (%%colophon;))*)),
               (%%data.elements.incl; |
                %%reltable;)*"""
    attrs = [
        Attribute("title", "CDATA", "#IMPLIED"),
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        Attribute("anchorref", "CDATA", "#IMPLIED"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
        ParameterEntity("localization-atts"),
        ParameterEntity("topicref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("arch-atts"),
    ]    

# Topic types
#####################################################################

class ArticleType(TopicType):
    """Article topic type."""
    id = u"article"
    file = u"article"
    pi_entity = None
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:article"
    title = u"Article"
    owner = u"DITA 4 Publishers"
    parent = TopicType()
    root = ArticleElement()

class SubsectionType(TopicType):
    """Subsection topic type."""
    id = u"subsection"
    file = u"subsection"
    pi_entity = None
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:subsection"
    title = u"Subsection"
    owner = u"DITA 4 Publishers"
    parent = TopicType()
    root = SubsectionElement()

class SidebarType(TopicType):
    """Sidebar topic type."""
    id = u"sidebar"
    file = u"sidebar"
    pi_entity = None
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:sidebar"
    title = u"Sidebar"
    owner = u"DITA 4 Publishers"
    parent = TopicType()
    root = SidebarElement()

class ChapterType(TopicType):
    """Chapter topic type."""
    id = u"chapter"
    file = u"chapter"
    pi_entity = None
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:chapter"
    title = u"Chapter"
    owner = u"DITA 4 Publishers"
    parent = TopicType()
    root = ChapterElement()

class PartType(TopicType):
    """Part topic type."""
    id = u"part"
    file = u"part"
    pi_entity = None
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:part"
    title = u"Part"
    owner = u"DITA 4 Publishers"
    parent = TopicType()
    root = PartElement()

class CoverType(TopicType):
    """Cover topic type."""
    id = u"d4pCover"
    file = u"d4pCover"
    pi_entity = None
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:d4pCover"
    title = u"Cover"
    owner = u"DITA 4 Publishers"
    parent = TopicType()
    root = CoverElement()

class PubmapType(MapType):
    """Pub map type."""
    id = u"pubmap"
    file = u"pubmap"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:entities:dtd:pubmap"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:dtd:pubmap"
    title = u"pubmap"
    owner = u"DITA 4 Publishers"
    parent = MapType()
    root = PubmapElement()

ArticleType.required_types = [SubsectionType, SidebarType]
SubsectionType.required_types = [SidebarType]
SidebarType.required_types = [SubsectionType]
ChapterType.required_types = [SubsectionType, SidebarType]

#class ArticleType(ditagen.dita.ShellType):
#    """Article Task topic type."""
#    def __init__(self):
#        super(ArticleType, self).__init__(u"article", u"Article", TopicType(), file=u"article")
#        self.pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:article"
#        self.owner = u"DITA 4 Publishers"

# Domains
#####################################################################

class FormattingDomain(ditagen.dita.Domain):
    """DITA For Publishers Formatting Domain."""
    # TODO: Requires hi-d
    id = u"d4p_formatting-d"
    si_module = u"d4p_formattingDomain.mod"
    si_entity = u"d4p_formattingDomain.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_formattingDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_formattingDomain:entities"
    title = u"Formatting"
    elements = [u"ph", u"p", u"foreign"]
    parent = [TopicType]
    required_domains = [HiDomain]

class EnumerationTopicDomain(ditagen.dita.Domain):
    """DITA For Publishers Enumeration Domain."""
    id = u"d4p_enumerationTopic-d"
    si_module = u"d4p_enumerationTopic.mod"
    si_entity = u"d4p_enumerationTopic.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:dita:modules:d4p_enumerationTopicDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:entities:dtd:dita:d4p_enumerationTopicDomain:entities"
    title = u"Enumeration"
    elements = [u"data"]
    parent = [TopicType]

class EnumerationMapDomain(ditagen.dita.Domain):
    """DITA For Publishers Enumeration Domain."""
    id = u"d4p_enumerationMap-d"
    si_module = u"d4p_enumerationMap.mod"
    si_entity = u"d4p_enumerationMap.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:dita:modules:d4p_enumerationMap"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:entities:dtd:dita:d4p_enumerationMap:entities"
    title = u"Enumeration"
    elements = [u"topicref"]
    parent = [MapType]


class SimpleEnumerationDomain(ditagen.dita.Domain):
    """DITA For Publishers Simple Enumeration Domain."""
    id = u"d4p_simpleEnumeration-d"
    si_module = u"d4p_simpleEnumeration.mod"
    si_entity = u"d4p_simpleEnumeration.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:dita:modules:d4p_simpleEnumerationDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:entities:dtd:dita:d4p_simpleEnumerationDomain:entities"
    title = u"Simple Enumeration"
    elements = [u"data"]
    parent = [TopicType]

class MathDomain(ditagen.dita.Domain):
    """DITA For Publishers Math Domain."""
    id = u"d4p_math-d"
    si_module = u"d4p_mathDomain.mod"
    si_entity = u"d4p_mathDomain.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_mathDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_mathDomain:entities"
    title = u"Math"
    elements = [u"ph", u"p", u"fig", u"foreign"]
    parent = [TopicType]
    
class MediaDomain(ditagen.dita.Domain):
    """DITA For Publishers Media Domain."""
    id = u"d4p_media-d"
    si_module = u"d4p_mediaDomain.mod"
    si_entity = u"d4p_mediaDomain.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_mediaDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_mediaDomain:entities"
    title = u"Media"
    elements = [u"object"]
    parent = [TopicType]

class ClassificationDomain(ditagen.dita.Domain):
    """DITA For Publishers Classification Domain."""
    id = u"d4p_classification-d"
    si_module = u"d4p_classification.mod"
    si_entity = u"d4p_classification.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_classificationDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_classificationDomain:entities"
    title = u"Classification"
    elements = [u"data"]
    parent = [TopicType]

class PubcontentDomain(ditagen.dita.Domain):
    """DITA For Publishers Pubcontent Domain."""
    id = u"d4p_pubcontent-d"
    si_module = u"d4p_pubcontent.mod"
    si_entity = u"d4p_pubcontent.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_pubcontentDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_pubcontentDomain:entities"
    title = u"Pubcontent"
    elements = [u"p", u"bodydiv", u"sectiondiv"]
    parent = [TopicType]

class RubyDomain(ditagen.dita.Domain):
    """DITA For Publishers Ruby Domain."""
    id = u"d4p_ruby-d"
    si_module = u"d4p_ruby.mod"
    si_entity = u"d4p_ruby.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_rubyDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_rubyDomain:entities"
    title = u"Ruby"
    elements = [u"ph"]
    parent = [TopicType]

class VariablesDomain(ditagen.dita.Domain):
    """DITA For Publishers Variables Domain."""
    id = u"d4p_variables-d"
    si_module = u"d4p_variables.mod"
    si_entity = u"d4p_variables.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_variablesDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_variablesDomain:entities"
    title = u"Variables"
    elements = [u"data", u"text", u"keyword"]
    parent = [TopicType]

class VerseDomain(ditagen.dita.Domain):
    """DITA For Publishers Verse Domain."""
    id = u"d4p_verse-d"
    si_module = u"d4p_verse.mod"
    si_entity = u"d4p_verse.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_verseDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_verseDomain:entities"
    title = u"Verse"
    elements = [u"lines"]
    parent = [TopicType]

class XmlDomain(ditagen.dita.Domain):
    """DITA For Publishers XML Domain."""
    id = u"xml-d"
    si_module = u"xml.mod"
    si_entity = u"xml.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:xml:declarations"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:xml:entities"
    title = u"XML"
    elements = [u"keyword"]
    parent = [TopicType]

class PubmapDomain(ditagen.dita.Domain):
    """DITA For Publishers Pubmap Domain."""
    id = u"pubmap-d"
    si_module = u"pubmap.mod"
    si_entity = u"pubmap.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:dtd:pubmapDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:entities:dtd:pubmapDomain"
    title = u"Pubmap"
    attributes = [u"topicref", u"title"]
    parent = [MapType]

class PubmapMaprefDomain(ditagen.dita.Domain):
    """DITA For Publishers Pubmap Mapref Domain."""
    id = u"pubmapMapref-d"
    si_module = u"pubmapMapref.mod"
    si_entity = u"pubmapMapref.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:dtd:pubmapMaprefDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:entities:dtd:pubmapMaprefDomain"
    title = u"PubmapMapref"
    attributes = [u"topicref", u"appendix", u"appendixes", u"article", u"backmatter", u"chapter", u"covers", u"department", u"glossary", u"keydef-group", u"part", u"pubbody", u"publication", u"subsection", u"sidebar", u"wrap-cover"]
    parent = [MapType]

class PubmetadataDomain(ditagen.dita.Domain):
    """DITA For Publishers Pubmetadata Domain."""
    id = u"pubmetadata-d"
    si_module = u"pubmetadata.mod"
    si_entity = u"pubmetadata.ent"
    pi_module = u"urn:pubid:dita4publishers.sourceforge.net:modules:dtd:pubmetadataDomain"
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:entities:dtd:pubmetadataDomain"
    title = u"Pubmetadata"
    attributes = [u"topicmeta"]
    parent = [MapType]

class RenditionTargetAttDomain(ditagen.dita.v1_2.AttributeDomain):
    """DITA For Publishers Rendition Target Attribute Domain."""
    id = u"d4p_renditionTargetAtt-d"
    si_module = None
    si_entity = u"d4p_renditionTarget.ent"
    pi_module = None
    pi_entity = u"urn:pubid:dita4publishers.sourceforge.net:doctypes:dita:modules:d4p_renditionTargetAttDomain:entities"
    title = u"Rendition Target Attribute"
    attributes = [u"props"]
    parent = [TopicType]

# Defaults
__commonDomains = [FormattingDomain, EnumerationTopicDomain, SimpleEnumerationDomain, MathDomain, MediaDomain, ClassificationDomain, PubcontentDomain, RubyDomain, VariablesDomain, VerseDomain, XmlDomain, RenditionTargetAttDomain]
ArticleType.default_domains = __commonDomains
ChapterType.default_domains = __commonDomains
CoverType.default_domains = __commonDomains
PartType.default_domains = __commonDomains
SidebarType.default_domains = __commonDomains
SubsectionType.default_domains = __commonDomains
PubmapType.default_domains = [MapGroupDomain, PubmapDomain, PubmapMaprefDomain, PubmetadataDomain, EnumerationMapDomain, SimpleEnumerationDomain, VariablesDomain, IndexingDomain]





