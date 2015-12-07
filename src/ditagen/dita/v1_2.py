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
from ditagen.dtdgen import Particle as Particle
from ditagen.dtdgen import Choice as Choice
from ditagen.dtdgen import Name as Name 
from ditagen.dtdgen import Seq as Seq
from ditagen.dtdgen import Attribute as Attribute
from ditagen.dtdgen import Param as Param
from ditagen.dtdgen import ParameterEntity as ParameterEntity

# Elements
#####################################################################

OPTIONAL = Particle.Occurrences.OPTIONAL
ZERO_OR_MORE = Particle.Occurrences.ZERO_OR_MORE

class TopicElement(ditagen.dita.DitaElement):
    """Topic element."""
    name = u"topic"
    cls = u"- topic/topic "
    model = Seq([
        Choice(ParameterEntity("title")),
        Choice(ParameterEntity("titlealts"), OPTIONAL),
        Choice([ParameterEntity("shortdesc"), ParameterEntity("abstract")], Param("shortdesc")),
        Choice(ParameterEntity("prolog"), OPTIONAL),
        Choice(ParameterEntity("body"), OPTIONAL),
        Choice(ParameterEntity("related-links"), OPTIONAL),
        Param("nested")
        ])
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]
class ConceptElement(ditagen.dita.DitaElement):
    """Concept element."""
    name = u"concept"
    cls = u"- topic/topic concept/concept "
    model = Seq([
        Choice(ParameterEntity("title")),
        Choice(ParameterEntity("titlealts"), OPTIONAL),
        Choice([ParameterEntity("shortdesc"), ParameterEntity("abstract")], Param("shortdesc")),
        Choice(ParameterEntity("prolog"), OPTIONAL),
        Choice(ParameterEntity("conbody"), OPTIONAL),
        Choice(ParameterEntity("related-links"), OPTIONAL),
        Param("nested")
        ])
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]        
class TaskElement(ditagen.dita.DitaElement):
    """Task element."""
    name = u"task"
    cls = u"- topic/topic task/task "
    model = Seq([
        Choice(ParameterEntity("title")),
        Choice(ParameterEntity("titlealts"), OPTIONAL),
        Choice([ParameterEntity("shortdesc"), ParameterEntity("abstract")], Param("shortdesc")),
        Choice(ParameterEntity("prolog"), OPTIONAL),
        Choice(ParameterEntity("taskbody"), OPTIONAL),
        Choice(ParameterEntity("related-links"), OPTIONAL),
        Param("nested")
        ])
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]
class ReferenceElement(ditagen.dita.DitaElement):
    """Reference element."""
    name = u"reference"
    cls = u"- topic/topic reference/reference "
    model = Seq([
        Choice(ParameterEntity("title")),
        Choice(ParameterEntity("titlealts"), OPTIONAL),
        Choice([ParameterEntity("shortdesc"), ParameterEntity("abstract")], Param("shortdesc")),
        Choice(ParameterEntity("prolog"), OPTIONAL),
        Choice(ParameterEntity("refbody"), OPTIONAL),
        Choice(ParameterEntity("related-links"), OPTIONAL),
        Param("nested")
        ])
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]

class GlossentryElement(ditagen.dita.DitaElement):
    """Glossary entry element."""
    name = u"glossentry"
    cls = u"- topic/topic concept/concept glossentry/glossentry "
    model = Seq([
        Choice(ParameterEntity("glossterm")),
        Choice(ParameterEntity("glossdef"), OPTIONAL),
        Choice(ParameterEntity("prolog"), OPTIONAL),
        Choice(ParameterEntity("glossBody"), OPTIONAL),
        Choice(ParameterEntity("related-links"), OPTIONAL),
        Param("nested")
        ])
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]
class GlossgroupElement(ditagen.dita.DitaElement):
    """Glossary group element."""
    name = u"glossgroup"
    cls = u"- topic/topic concept/concept glossgroup/glossgroup "
    model = Seq([
        Choice(ParameterEntity("title")),
        Choice(ParameterEntity("prolog"), OPTIONAL),
        Param("nested")
        ])
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]

class LearningBaseElement(ditagen.dita.DitaElement):
    """Learning Base element."""
    name = u"learningBase"
    cls = u"- topic/topic learningBase/learningBase "
    model = Seq([
        Choice(ParameterEntity("title")),
        Choice(ParameterEntity("titlealts"), OPTIONAL),
        Choice([ParameterEntity("shortdesc"), ParameterEntity("abstract")], Param("shortdesc")),
        Choice(ParameterEntity("prolog"), OPTIONAL),
        Choice(ParameterEntity("learningBasebody"), OPTIONAL),
        Choice(ParameterEntity("related-links"), OPTIONAL),
        Param("nested")
        ])
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]
class LearningAssessmentElement(ditagen.dita.DitaElement):
    """Learning Assessment element."""
    name = u"learningAssessment"
    cls = u"- topic/topic learningBase/learningBase learningAssessment/learningAssessment "
    model = Seq([
        Choice(ParameterEntity("title")),
        Choice(ParameterEntity("titlealts"), OPTIONAL),
        Choice([ParameterEntity("shortdesc"), ParameterEntity("abstract")], Param("shortdesc")),
        Choice(ParameterEntity("prolog"), OPTIONAL),
        Choice(ParameterEntity("learningAssessmentbody"), OPTIONAL),
        Choice(ParameterEntity("related-links"), OPTIONAL),
        Param("nested")
        ])
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED")
    ]

class LearningOverviewElement(ditagen.dita.DitaElement):
    """Learning Overview element."""
    name = u"learningOverview"
    cls = u"- topic/topic learningBase/learningBase learningOverview/learningOverview "
    model = Seq([
        Choice(ParameterEntity("title")),
        Choice(ParameterEntity("titlealts"), OPTIONAL),
        Choice([ParameterEntity("shortdesc"), ParameterEntity("abstract")], Param("shortdesc")),
        Choice(ParameterEntity("prolog"), OPTIONAL),
        Choice(ParameterEntity("learningOverviewbody"), OPTIONAL),
        Choice(ParameterEntity("related-links"), OPTIONAL),
        Param("nested")
        ])
    attrs = [
        Attribute("id", "ID" ,"#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED")
    ]

class LearningPlanElement(ditagen.dita.DitaElement):
    """Learning Plan element."""
    name = u"learningPlan"
    cls = u"- topic/topic learningBase/learningBase learningPlan/learningPlan "
    model = Seq([
        Choice(ParameterEntity("title")),
        Choice(ParameterEntity("titlealts"), OPTIONAL),
        Choice([ParameterEntity("shortdesc"), ParameterEntity("abstract")], Param("shortdesc")),
        Choice(ParameterEntity("prolog"), OPTIONAL),
        Choice(ParameterEntity("learningPlanbody"), OPTIONAL),
        Choice(ParameterEntity("related-links"), OPTIONAL),
        Param("nested")
        ])
    attrs = [
        Attribute("id", "ID" ,"#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED")
    ]
    
class LearningSummaryElement(ditagen.dita.DitaElement):
    """Learning Summary element."""
    name = u"learningSummary"
    cls = u"- topic/topic learningBase/learningBase learningSummary/learningSummary "
    model = Seq([
        Choice(ParameterEntity("title")),
        Choice(ParameterEntity("titlealts"), OPTIONAL),
        Choice([ParameterEntity("shortdesc"), ParameterEntity("abstract")], Param("shortdesc")),
        Choice(ParameterEntity("prolog"), OPTIONAL),
        Choice(ParameterEntity("learningSummarybody"), OPTIONAL),
        Choice(ParameterEntity("related-links"), OPTIONAL),
        Param("nested")
        ])
    attrs = [
        Attribute("id", "ID" ,"#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED")
    ]

class LearningContentElement(ditagen.dita.DitaElement):
    """Learning Content element."""
    name = u"learningContent"
    cls = u"- topic/topic learningBase/learningBase learningContent/learningContent "
    model = Seq([
        Choice(ParameterEntity("title")),
        Choice(ParameterEntity("titlealts"), OPTIONAL),
        Choice([ParameterEntity("shortdesc"), ParameterEntity("abstract")], Param("shortdesc")),
        Choice(ParameterEntity("prolog"), OPTIONAL),
        Choice(ParameterEntity("learningContentbody"), OPTIONAL),
        Choice(ParameterEntity("related-links"), OPTIONAL),
        Param("nested")
        ])
    attrs = [
        Attribute("id", "ID" ,"#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED")
    ]

class SubjectSchemeElement(ditagen.dita.DitaElement):
    """Subject scheme element."""
    name = u"subjectScheme"
    cls = u"- map/map subjectScheme/subjectScheme "
    model = Seq([
        Choice(ParameterEntity("title"), OPTIONAL),
        Choice(ParameterEntity("topicmeta"), OPTIONAL),
        Choice([
            ParameterEntity("anchor"),
            ParameterEntity("data.elements.incl"),
            ParameterEntity("enumerationdef"),
            ParameterEntity("hasInstance"),
            ParameterEntity("hasKind"),
            ParameterEntity("hasNarrower"),
            ParameterEntity("hasPart"),
            ParameterEntity("hasRelated"),
            ParameterEntity("navref"),
            ParameterEntity("relatedSubjects"),
            ParameterEntity("reltable"),
            ParameterEntity("schemeref"),
            ParameterEntity("subjectdef"),
            ParameterEntity("subjectHead"),
            ParameterEntity("subjectRelTable"),
            ParameterEntity("topicref")
            ], ZERO_OR_MORE)
        ])
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        Attribute("anchorref", "CDATA", "#IMPLIED"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
        ParameterEntity("localization-atts"),
        ParameterEntity("topicref-atts"),
        ParameterEntity("select-atts")
    ]

class MapElement(ditagen.dita.DitaElement):
    """Map element."""
    name = u"map"
    cls = u"- map/map "
    model = Seq([
        Choice(ParameterEntity("title"), OPTIONAL),
        Choice(ParameterEntity("topicmeta"), OPTIONAL),
        Choice([
            ParameterEntity("anchor"),
            ParameterEntity("data.elements.incl"),
            ParameterEntity("navref"),
            ParameterEntity("reltable"),
            ParameterEntity("topicref")
            ], ZERO_OR_MORE)
        ])
    attrs = [
        Attribute("title", "CDATA", "#IMPLIED"),
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        Attribute("anchorref", "CDATA", "#IMPLIED"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
        ParameterEntity("localization-atts"),
        ParameterEntity("topicref-atts"),
        ParameterEntity("select-atts")
    ]
class BookMapElement(ditagen.dita.DitaElement):
    """BookMap element."""
    name = u"bookmap"
    cls = u"- map/map bookmap/bookmap "
    model = Seq([
        Choice([Choice(ParameterEntity("title")), Choice(ParameterEntity("booktitle"))], OPTIONAL),
        Choice(ParameterEntity("bookmeta"), OPTIONAL),
        Choice(ParameterEntity("frontmatter"), OPTIONAL),
        Choice(ParameterEntity("chapter"), ZERO_OR_MORE),
        Choice(ParameterEntity("part"), ZERO_OR_MORE),
        Choice([Choice(ParameterEntity("appendices"), OPTIONAL), Choice(ParameterEntity("appendix"), ZERO_OR_MORE)]),
        Choice(ParameterEntity("backmatter"), OPTIONAL),
        Choice(ParameterEntity("reltable"), ZERO_OR_MORE)
        ])
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        Attribute("anchorref", "CDATA", "#IMPLIED"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
        ParameterEntity("localization-atts"),
        ParameterEntity("topicref-atts"),
        ParameterEntity("select-atts")
    ]

# Topic types
#####################################################################

class TopicType(ditagen.dita.Type):
    """Topic topic type."""
    id = u"topic"
    file = u"base/dtd/topic" # the .dtd file is at technicalContent
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Topic//EN"
    title = u"Topic"
    parent = None
    root = TopicElement()
class ConceptType(TopicType):
    """Concept topic type."""
    id = u"concept"
    file = u"technicalContent/dtd/concept"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Concept//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Concept//EN"
    title = u"Concept"
    parent = TopicType()
    root = ConceptElement()
class TaskType(TopicType):
    """Task topic type."""
    id = u"task"
    file = u"technicalContent/dtd/task"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Task//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Task//EN"
    title = u"Task"
    parent = TopicType()
    root = TaskElement()
    def __init__(self):
        super(TaskType, self).__init__()
        #self.required_domains = [StrictTaskbodyConstraints]
class GeneralTaskType(ditagen.dita.ShellType):
    """General Task topic type."""
    def __init__(self):
        super(GeneralTaskType, self).__init__(u"generalTask", u"General Task", TaskType())
        #self.parent.required_domains = []
class ReferenceType(TopicType):
    """Reference topic type."""
    id = u"reference"
    file = u"technicalContent/dtd/reference"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Reference//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Reference//EN"
    title = u"Reference"
    parent = TopicType()
    root = ReferenceElement()
class MapType(ditagen.dita.Type):
    """Map topic type."""
    id = u"map"
    file = u"base/dtd/map" # the .dtd file is at technicalContent
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Map//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Map//EN"
    title = u"Map"
    parent = None
    root = MapElement()

class BookMapType(MapType):
    """BookMap topic type."""
    id = u"bookmap"
    file = u"bookmap/dtd/bookmap"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 BookMap//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 BookMap//EN"
    title = u"BookMap"
    parent = MapType()
    root = BookMapElement()

class GlossentryType(ConceptType):
    """Glossary entry topic type."""
    id = u"glossentry"
    file = u"technicalContent/dtd/glossentry"
    pi_entity = u"-//OASIS//ENTITIES DITA Glossary Entry//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA Glossary Entry//EN"
    title = u"Glossary Entry"
    parent = ConceptType()
    root = GlossentryElement()
class GlossgroupType(ConceptType):
    """Glossary group topic type."""
    id = u"glossgroup"
    file = u"technicalContent/dtd/glossgroup"
    pi_entity = u"-//OASIS//ENTITIES DITA Glossary Group//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA Glossary Group//EN"
    title = u"Glossary Group"
    parent = ConceptType()
    root = GlossgroupElement()

class MachineryTaskType(ditagen.dita.ShellType):
    """Machinery Task topic type."""
    def __init__(self):
        super(MachineryTaskType, self).__init__(u"machineryTask", u"Machinery Task", TaskType(), file=u"machineryIndustry/dtd/machineryTask")
        #self.parent.required_domains = [MachineryTaskbodyConstraints]

class LearningBaseType(TopicType):
    """Learning Base topic type."""
    id = u"learningBase"
    file = u"learning/dtd/learningBase"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Learning Base//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Learning Base//EN"
    title = u"Learning Base"
    parent = TopicType()
    root = LearningBaseElement()
class LearningAssessmentType(LearningBaseType):
    """Learning Assessment topic type."""
    id = u"learningAssessment"
    file = u"learning/dtd/learningAssessment"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Learning Assessment//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Learning Assessment//EN"
    title = u"Learning Assessment"
    parent = LearningBaseType()
    root = LearningAssessmentElement()
class LearningOverviewType(LearningBaseType):
    """Learning Overview topic type."""
    id = u"learningOverview"
    file = u"learning/dtd/learningOverview"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Learning Overview//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Learning Overview//EN"
    title = u"Learning Overview"
    parent = LearningBaseType()
    root = LearningOverviewElement()
class LearningPlanType(LearningBaseType):
    """Learning Plan topic type."""
    id = u"learningPlan"
    file = u"learning/dtd/learningPlan"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Learning Plan//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Learning Plan//EN"
    title = u"Learning Plan"
    parent = LearningBaseType()
    root = LearningPlanElement()
class LearningSummaryType(LearningBaseType):
    """Learning Summary topic type."""
    id = u"learningSummary"
    file = u"learning/dtd/learningSummary"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Learning Summary//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Learning Summary//EN"
    title = u"Learning Summary"
    parent = LearningBaseType()
    root = LearningSummaryElement()
class LearningContentType(LearningBaseType):
    """Learning Content topic type."""
    id = u"learningContent"
    file = u"learning/dtd/learningContent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Learning Content//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Learning Content//EN"
    title = u"Learning Content"
    parent = LearningBaseType()
    root = LearningContentElement()
    def __init__(self):
        super(LearningContentType, self).__init__()
        self.required_types = [TaskType, ConceptType, ReferenceType, LearningSummaryType, LearningAssessmentType]
class LearningMapType(ditagen.dita.ShellType):
    """Learning Map topic type."""
    def __init__(self):
        super(LearningMapType, self).__init__(u"learningMap", u"Learning Map", MapType(), file=u"learning/dtd/learningMap")
        #self.parent.required_domains = []
class LearningBookMapType(ditagen.dita.ShellType):
    """Learning BookMap topic type."""
    def __init__(self):
        super(LearningBookMapType, self).__init__(u"learningBookmap", u"Learning BookMap", BookMapType(), file=u"learning/dtd/learningBookmap")
        #self.parent.required_domains = []

class ClassificationMapType(ditagen.dita.ShellType):
    """Classification Map topic type."""
    def __init__(self):
        super(ClassificationMapType, self).__init__(u"classifyMap", u"Classification Map", MapType(), file=u"subjectScheme/dtd/classifyMap")
        #self.parent.required_domains = []
class SubjectSchemeType(MapType):
    """Subject Scheme Map topic type."""
    id = u"subjectScheme"
    file = u"subjectScheme/dtd/subjectScheme"
    title = u"Subject Scheme Map"
    parent = MapType()
    root = SubjectSchemeElement()


# Domains
#####################################################################

class Constraints(ditagen.dita.DomainBase):
    """Base class for constraints."""
#    file_suffix = u""
    pi_suffix = u" Constraint"
    elements = []
    att_id = None
    def get_file_name(self, extension):
        return self.file + self.file_suffix + "." + extension

class AttributeDomain(ditagen.dita.DomainBase):
    """Base class for attribute domains."""
#    file_suffix = u"Att"
    pi_suffix = u" Attribute Domain"
    #elements = []
    attributes = []
    def get_file_name(self, extension):
        return self.file + self.file_suffix + "." + extension

# Domains

class UiDomain(ditagen.dita.Domain):
    """User interface domain."""
    id = u"ui-d"
    si_module = u"technicalContent/dtd/uiDomain.mod"
    si_entity = u"technicalContent/dtd/uiDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 User Interface Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 User Interface Domain//EN"
    title = u"User Interface"
    elements = [u"pre", u"keyword", u"ph"]
    parent = [TopicType]
class HiDomain(ditagen.dita.Domain):
    """Hilight domain."""
    id = u"hi-d"
    si_module = u"base/dtd/highlightDomain.mod"
    si_entity = u"base/dtd/highlightDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Highlight Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Highlight Domain//EN"
    title = u"Highlight"
    elements = [u"ph"]
    parent = [TopicType]
class PrDomain(ditagen.dita.Domain):
    """Programmign domain."""
    id = u"pr-d"
    si_module = u"technicalContent/dtd/programmingDomain.mod"
    si_entity = u"technicalContent/dtd/programmingDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Programming Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Programming Domain//EN"
    title = u"Programming"
    elements = [u"pre", u"keyword", u"ph", u"fig", u"dl"]
    parent = [TopicType]
class SwDomain(ditagen.dita.Domain):
    """Software development domain."""
    id = u"sw-d"
    si_module = u"technicalContent/dtd/softwareDomain.mod"
    si_entity = u"technicalContent/dtd/softwareDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Software Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Software Domain//EN"
    title = u"Software"
    elements = [u"pre", u"keyword", u"ph"]
    parent = [TopicType]
class UtDomain(ditagen.dita.Domain):
    """Utilities domain."""
    id = u"ut-d"
    si_module = u"base/dtd/utilitiesDomain.mod"
    si_entity = u"base/dtd/utilitiesDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Utilities Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Utilities Domain//EN"
    title = u"Utilities"
    elements = [u"fig"]
    parent = [TopicType]
class IndexingDomain(ditagen.dita.Domain):
    """Indexing domain."""
    id = u"indexing-d"
    si_module = u"base/dtd/indexingDomain.mod"
    si_entity = u"base/dtd/indexingDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Indexing Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Indexing Domain//EN"
    title = u"Indexing"
    elements = [u"index-base"]
    parent = [TopicType, MapType]
class LearningDomain(ditagen.dita.Domain):
    """Learning domain."""
    id = u"learning-d"
    si_module = u"learning/dtd/learningDomain.mod"
    si_entity = u"learning/dtd/learningDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Learning Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Learning Domain//EN"
    title = u"Learning"
    elements = [u"note", u"fig"]
    # XXX: This builds on 
    parent = [TopicType]
    required_domains = [UtDomain]
class LearningMetaDomain(ditagen.dita.Domain):
    """Learning metadata domain."""
    id = u"learningmeta-d"
    si_module = u"learning/dtd/learningMetadataDomain.mod"
    si_entity = u"learning/dtd/learningMetadataDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Learning Metadata Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Learning Metadata Domain//EN"
    title = u"Learning Metadata"
    elements = [u"metadata"]
    parent = [TopicType]
class LearningMapDomain(ditagen.dita.Domain):
    """Learning map domain."""
    id = u"learningmap-d"
    si_module = u"learning/dtd/learningMapDomain.mod"
    si_entity = u"learning/dtd/learningMapDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Learning Map Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Learning Map Domain//EN"
    title = u"Learning Map"
    elements = [u"topicref"]
    parent = [MapType]
class TaskRequirementsDomain(ditagen.dita.Domain):
    """Task requirements domain."""
    id = u"taskreq-d"
    si_module = u"technicalContent/dtd/taskreqDomain.mod"
    si_entity = u"technicalContent/dtd/taskreqDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Task Requirements Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Task Requirements Domain//EN"
    title = u"Machine Industry Task"
    elements = [u"prereq", u"postreq"]
    parent = [TaskType]
class HazardStatementDomain(ditagen.dita.Domain):
    """Hazard statement domain."""
    id = u"hazard-d"
    si_module = u"base/dtd/hazardstatementDomain.mod"
    si_entity = u"base/dtd/hazardstatementDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Hazard Statement Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Hazard Statement Domain//EN"
    title = u"Hazard Statement"
    elements = [u"note"]
    parent = [TopicType]
class MapGroupDomain(ditagen.dita.Domain):
    """Map group domain."""
    id = u"mapgroup-d"
    si_module = u"base/dtd/mapGroup.mod"
    si_entity = u"base/dtd/mapGroup.ent" # This is an exception to DITA's naming scheme
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Map Group Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Map Group Domain//EN"
    title = u"Map Group"
    elements = [u"topicref"]
    parent = [MapType]
class AbbreviatedFormDomain(ditagen.dita.Domain):
    """Abbreviated form domain."""
    id = u"abbrev-d"
    si_module = u"technicalContent/dtd/abbreviateDomain.mod"
    si_entity = u"technicalContent/dtd/abbreviateDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Abbreviated Form Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Abbreviated Form Domain//EN"
    title = u"Abbreviated Form"
    elements = [u"term"]
    parent = [TopicType]
class XNALDomain(ditagen.dita.Domain):
    """XNAL domain."""
    id = u"xnal-d"
    si_module = u"xnal/dtd/xnalDomain.mod"
    si_entity = u"xnal/dtd/xnalDomain.ent"
    title = u"XNAL"
    elements = [u"author"]
    parent = [MapType]
class UserDelayedResolutionDomain(ditagen.dita.Domain):
    """User delayed resolution domain."""
    id = u"delay-d"
    si_module = u"base/dtd/delayResolutionDomain.mod"
    si_entity = u"base/dtd/delayResolutionDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Delayed Resolution Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Delayed Resolution Domain//EN"
    title = u"Delayed Resolution"
    elements = [u"keywords"]
    parent = [TopicType, MapType]
class ClassifyDomain(ditagen.dita.Domain):
    """Classify domain."""
    id = u"classify-d"
    si_module = u"subjectScheme/dtd/classifyDomain.mod"
    si_entity = u"subjectScheme/dtd/classifyDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Classification Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Classification Domain//EN"
    title = u"Map Subject Classification"
    elements = [u"topicref", u"reltable"]
    parent = [TopicType, MapType]
class GlossaryReferenceDomain(ditagen.dita.Domain):
    """Glossary reference domain."""
    id = u"glossref-d"
    si_module = u"technicalContent/dtd/glossrefDomain.mod"
    si_entity = u"technicalContent/dtd/glossrefDomain.ent"
    pi_entity = u"-//OASIS//ENTITIES DITA 1.2 Glossary Reference Domain//EN"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Glossary Reference Domain//EN"
    title = u"Glossary Reference"
    elements = [u"topicref"]
    parent = [MapType]

# Constraints

class StrictTaskbodyConstraints(Constraints):
    """Strict taskbody constraints."""
    id = u"strictTaskbody-c"
    si_module = u"technicalContent/dtd/strictTaskbodyConstraint.mod"
    si_entity = u"technicalContent/dtd/strictTaskbodyConstraint.ent"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Strict Taskbody Constraint//EN"
    title = u"Strict Taskbody"
    parent = [TaskType]
    att_id = u"taskbody"
class MachineryTaskbodyConstraints(Constraints):
    """Machinery taskbody constraints."""
    id = u"machineryTaskbody-c"
    si_module = u"machineryIndustry/dtd/machineryTaskbodyConstraint.mod"
    si_entity = u"machineryIndustry/dtd/machineryTaskbodyConstraint.ent"
    pi_module = u"-//OASIS//ELEMENTS DITA 1.2 Machinery Taskbody Constraint//EN"
    title = u"Machinery Taskbody"
    parent = [TaskType]
    att_id = u"taskbody"

# Defaults

TopicType.default_domains = [HiDomain, UtDomain, IndexingDomain, HazardStatementDomain, AbbreviatedFormDomain, PrDomain, SwDomain, UiDomain]
ConceptType.default_domains = [HiDomain, UtDomain, IndexingDomain, HazardStatementDomain, AbbreviatedFormDomain, PrDomain, SwDomain, UiDomain]
TaskType.default_domains = [HiDomain, UtDomain, IndexingDomain, HazardStatementDomain, AbbreviatedFormDomain, PrDomain, SwDomain, UiDomain, StrictTaskbodyConstraints]
GeneralTaskType.default_domains = [HiDomain, UtDomain, IndexingDomain, HazardStatementDomain, AbbreviatedFormDomain, PrDomain, SwDomain, UiDomain]
ReferenceType.default_domains = [HiDomain, UtDomain, IndexingDomain, HazardStatementDomain, AbbreviatedFormDomain, PrDomain, SwDomain, UiDomain]
MachineryTaskType.default_domains = [TaskRequirementsDomain, HazardStatementDomain, HiDomain, UtDomain, IndexingDomain, PrDomain, SwDomain, UiDomain, MachineryTaskbodyConstraints]
MapType.default_domains = [MapGroupDomain, IndexingDomain, UserDelayedResolutionDomain, GlossaryReferenceDomain]
BookMapType.default_domains = [MapGroupDomain, IndexingDomain, UserDelayedResolutionDomain, XNALDomain]
ClassificationMapType.default_domains = [MapGroupDomain, IndexingDomain, UserDelayedResolutionDomain, ClassifyDomain]
SubjectSchemeType.default_domains = [MapGroupDomain]
LearningAssessmentType.default_domains = [LearningDomain, LearningMetaDomain, HiDomain, UtDomain, IndexingDomain]
LearningBookMapType.default_domains = [LearningMapDomain, LearningMetaDomain, MapGroupDomain, IndexingDomain, UserDelayedResolutionDomain, XNALDomain]
LearningContentType.default_domains = [LearningDomain, LearningMetaDomain, HiDomain, UtDomain, IndexingDomain]
LearningMapType.default_domains = [LearningMapDomain, LearningMetaDomain, MapGroupDomain, IndexingDomain, UserDelayedResolutionDomain]
LearningOverviewType.default_domains = [LearningDomain, LearningMetaDomain, HiDomain, UtDomain, IndexingDomain]
LearningPlanType.default_domains = [LearningDomain, LearningMetaDomain, HiDomain, UtDomain, IndexingDomain]
LearningSummaryType.default_domains = [LearningDomain, LearningMetaDomain, HiDomain, UtDomain, IndexingDomain]
GlossentryType.default_domains = [HiDomain, UtDomain, IndexingDomain, HazardStatementDomain, AbbreviatedFormDomain, PrDomain, SwDomain, UiDomain]
GlossgroupType.default_domains = [HiDomain, UtDomain, IndexingDomain, HazardStatementDomain, AbbreviatedFormDomain, PrDomain, SwDomain, UiDomain]
