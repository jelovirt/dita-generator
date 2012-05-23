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

import ditagen.dita
from ditagen.dtdgen import Attribute as Attribute
from ditagen.dtdgen import ParameterEntity as ParameterEntity

# Elements
#####################################################################

class TopicElement(ditagen.dita.DitaElement):
    """Topic element."""
    name = u"topic"
    cls = u"- topic/topic "
    model = """(%%title;), (%%titlealts;)?,
        (%%shortdesc; | %%abstract;)%(shortdesc)s,
        (%%prolog;)?, (%%body;)?, (%%related-links;)?%(nested)s"""
    #(%%s-info-types;)*
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]
class ConceptElement(ditagen.dita.DitaElement):
    """Concept element."""
    name = u"concept"
    cls = u"- topic/topic concept/concept "
    model = """(%%title;), (%%titlealts;)?,
        (%%shortdesc; | %%abstract;)%(shortdesc)s,
        (%%prolog;)?, (%%conbody;)?, (%%related-links;)?%(nested)s"""
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]        
class TaskElement(ditagen.dita.DitaElement):
    """Task element."""
    name = u"task"
    cls = u"- topic/topic task/task "
    model = """(%%title;), (%%titlealts;)?,
        (%%shortdesc; | %%abstract;)%(shortdesc)s,
        (%%prolog;)?, (%%taskbody;)?,
        (%%related-links;)?%(nested)s"""
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]
class ReferenceElement(ditagen.dita.DitaElement):
    """Reference element."""
    name = u"reference"
    cls = u"- topic/topic reference/reference "
    model = """(%%title;), (%%titlealts;)?,
        (%%shortdesc; | %%abstract;)%(shortdesc)s,
        (%%prolog;)?, (%%refbody;)?, (%%related-links;)?%(nested)s"""
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]
class MapElement(ditagen.dita.DitaElement):
    """Map element."""
    name = u"map"
    cls = u"- map/map "
    model = """((%%title;)?,
       (%%topicmeta;)?,
       (%%anchor; |
        %%data.elements.incl; |
        %%navref; |
        %%reltable; |
        %%topicref;)*)"""
    attrs = [
        Attribute("title", "CDATA", "#IMPLIED"),
        Attribute("id", "ID", "#IMPLIED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        Attribute("anchorref", "CDATA", "#IMPLIED"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
        ParameterEntity("localization-atts"),
        ParameterEntity("topicref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("arch-atts"),
    ]
class BookMapElement(ditagen.dita.DitaElement):
    """BookMap element."""
    name = u"bookmap"
    cls = u"- map/map bookmap/bookmap "
    model = """(((%%title;) |
        (%%booktitle;))?,
        (%%bookmeta;)?,
        (%%frontmatter;)?,
        (%%chapter;)*,
        (%%part;)*,
        (%%appendix;)*,
        (%%backmatter;)?,
        (%%reltable;)*)"""
    attrs = [
        Attribute("id", "ID", "#IMPLIED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        Attribute("anchorref", "CDATA", "#IMPLIED"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
        ParameterEntity("localization-atts"),
        ParameterEntity("topicref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("arch-atts"),
    ]

# Topic types
#####################################################################

class TopicType(ditagen.dita.Type):
    """Topic topic type."""
    id = u"topic"
    file = u"topic"
    title = u"Topic"
    parent = None
    root = TopicElement()
class ConceptType(TopicType):
    """Concept topic type."""
    id = u"concept"
    file = u"concept"
    title = u"Concept"
    parent = TopicType()
    root = ConceptElement()
class TaskType(TopicType):
    """Task topic type."""
    id = u"task"
    file = u"task"
    title = u"Task"
    parent = TopicType()
    root = TaskElement()
class ReferenceType(TopicType):
    """Reference topic type."""
    id = u"reference"
    file = u"reference"
    title = u"Reference"
    parent = TopicType()
    root = ReferenceElement()
class MapType(ditagen.dita.Type):
    """Map topic type."""
    id = u"map"
    file = u"map" # the .dtd file is at technicalContent
    title = u"Map"
    parent = None
    root = MapElement()
class BookMapType(MapType):
    """BookMap topic type."""
    id = u"bookmap"
    file = u"bookmap"
    title = u"BookMap"
    parent = MapType()
    root = BookMapElement()


# Domains
#####################################################################
    
class UiDomain(ditagen.dita.Domain):
    """User interface domain."""
    id = u"ui-d"
    si_module = u"uiDomain.mod"
    si_entity = u"uiDomain.ent"
    title = u"User Interface"
    elements = [u"pre", u"keyword", u"ph"]
    parent = [TopicType]
class HiDomain(ditagen.dita.Domain):
    """Hilight domain."""
    id = u"hi-d"
    si_module = u"highlightDomain.mod"
    si_entity = u"highlightDomain.ent"
    title = u"Highlight"
    elements = [u"ph"]
    parent = [TopicType]
class PrDomain(ditagen.dita.Domain):
    """Programmign domain."""
    id = u"pr-d"
    si_module = u"programmingDomain.mod"
    si_entity = u"programmingDomain.ent"
    title = u"Programming"
    elements = [u"pre", u"keyword", u"ph", u"fig", u"dl"]
    parent = [TopicType]
class SwDomain(ditagen.dita.Domain):
    """Software development domain."""
    id = u"sw-d"
    si_module = u"softwareDomain.mod"
    si_entity = u"softwareDomain.ent"
    title = u"Software"
    elements = [u"pre", u"keyword", u"ph"]
    parent = [TopicType]
class UtDomain(ditagen.dita.Domain):
    """Utilities domain."""
    id = u"ut-d"
    si_module = u"utilitiesDomain.mod"
    si_entity = u"utilitiesDomain.ent"
    title = u"Utilities"
    elements = [u"fig"]
    parent = [TopicType]
class IndexingDomain(ditagen.dita.Domain):
    """Indexing domain."""
    id = u"indexing-d"
    si_module = u"indexingDomain.mod"
    si_entity = u"indexingDomain.ent"
    title = u"Indexing"
    elements = [u"index-base"]
    parent = [TopicType, MapType]
class MapGroupDomain(ditagen.dita.Domain):
    """Map group domain."""
    id = u"mapgroup-d"
    si_module = u"mapGroup.mod"
    si_entity = u"mapGroup.ent"
    title = u"Map Group"
    elements = [u"topicref"]
    parent = [MapType]
class XNALDomain(ditagen.dita.Domain):
    """XNAL domain."""
    id = u"xnal-d"
    si_module = u"xnalDomain.mod"
    si_entity = u"xnalDomain.ent"
    title = u"XNAL"
    elements = [u"author"]
    parent = [MapType]

# Defaults

TopicType.default_domains = [UiDomain, HiDomain, PrDomain, SwDomain, UtDomain, IndexingDomain]
ConceptType.default_domains = [UiDomain, HiDomain, PrDomain, SwDomain, UtDomain, IndexingDomain]
TaskType.default_domains = [UiDomain, HiDomain, PrDomain, SwDomain, UtDomain, IndexingDomain]
ReferenceType.default_domains = [UiDomain, HiDomain, PrDomain, SwDomain, UtDomain, IndexingDomain]
MapType.default_domains = [MapGroupDomain, IndexingDomain]
BookMapType.default_domains = [MapGroupDomain, IndexingDomain, XNALDomain]
