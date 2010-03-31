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
class LearningBaseElement(ditagen.dita.DitaElement):
    """Learning Base element."""
    name = u"learningBase"
    cls = u"- topic/topic learningBase/learningBase "
    model = """(%%title;),
                (%%titlealts;)?,
                (%%shortdesc; | %%abstract;)?,
                (%%prolog;)?,
                (%%learningBasebody;),
                (%%related-links;)?
                %(nested)s"""
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        Attribute("conref", "CDATA", "#IMPLIED"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
    ]
class LearningAssessmentElement(ditagen.dita.DitaElement):
    """Learning Assessment element."""
    name = u"learningAssessment"
    cls = u"- topic/topic learningBase/learningBase learningAssessment/learningAssessment "
    model = """(%%title;),
                (%%titlealts;)?,
                (%%shortdesc; | %%abstract;)?,
                (%%prolog;)?,
                (%%learningAssessmentbody;),
                (%%related-links;)?
                %(nested)s"""
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED")
    ]

class LearningOverviewElement(ditagen.dita.DitaElement):
    """Learning Overview element."""
    name = u"learningOverview"
    cls = u"- topic/topic learningBase/learningBase learningOverview/learningOverview "
    model = """(%%title;),
                (%%titlealts;)?,
                (%%shortdesc; | %%abstract;)?,
                (%%prolog;)?,
                (%%learningOverviewbody;),
                (%%related-links;)?
                %(nested)s"""
    attrs = [
        Attribute("id", "ID" ,"#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED")
    ]

class LearningPlanElement(ditagen.dita.DitaElement):
    """Learning Plan element."""
    name = u"learningPlan"
    cls = u"- topic/topic learningBase/learningBase learningPlan/learningPlan "
    model = """(%%title;),
                (%%titlealts;)?,
                (%%shortdesc; |  %%abstract;)?,
                (%%prolog;)?,
                (%%learningPlanbody;),
                (%%related-links;)?
                %(nested)s"""
    attrs = [
        Attribute("id", "ID" ,"#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED")
    ]
    
class LearningSummaryElement(ditagen.dita.DitaElement):
    """Learning Summary element."""
    name = u"learningSummary"
    cls = u"- topic/topic learningBase/learningBase learningSummary/learningSummary "
    model = """(%%title;),
                (%%titlealts;)?,
                (%%shortdesc; | %%abstract;)?,
                (%%prolog;)?,
                (%%learningSummarybody;),
                (%%related-links;)?
                %(nested)s"""
    attrs = [
        Attribute("id", "ID" ,"#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED")
    ]

class LearningContentElement(ditagen.dita.DitaElement):
    """Learning Content element."""
    name = u"learningContent"
    cls = u"- topic/topic learningBase/learningBase learningContent/learningContent "
    model = """(%%title;),
                (%%titlealts;)?,
                (%%shortdesc; |  %%abstract;)?,
                (%%prolog;)?,
                (%%learningContentbody;),
                (%%related-links;)?
                %(nested)s"""
    attrs = [
        Attribute("id", "ID" ,"#REQUIRED"),
        ParameterEntity("conref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("localization-atts"),
        ParameterEntity("arch-atts"),
        Attribute("outputclass", "CDATA", "#IMPLIED")
    ]

class SubjectSchemeElement(ditagen.dita.DitaElement):
    """Subject scheme element."""
    name = u"subjectScheme"
    cls = u"- map/map subjectScheme/subjectScheme "
    model = """(%%title;)?,
                (%%topicmeta;)?,
                ((%%anchor; |
                  %%data.elements.incl; |
                  %%enumerationdef; |
                  %%hasInstance; |
                  %%hasKind; |
                  %%hasNarrower; |
                  %%hasPart; |
                  %%hasRelated; |
                  %%navref; |
                  %%relatedSubjects; |
                  %%reltable; |
                  %%schemeref; |
                  %%subjectdef; |
                  %%subjectHead; |
                  %%subjectRelTable; |
                  %%topicref;)*)"""
    attrs = [
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
        Attribute("anchorref", "CDATA", "#IMPLIED"),
        Attribute("outputclass", "CDATA", "#IMPLIED"),
        ParameterEntity("localization-atts"),
        ParameterEntity("topicref-atts"),
        ParameterEntity("select-atts"),
        ParameterEntity("arch-atts"),
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
        Attribute("id", "ID", "#REQUIRED"),
        ParameterEntity("conref-atts"),
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

class TopicType(ditagen.dita.Type):
    """Topic topic type."""
    id = u"topic"
    file = u"base/dtd/topic" # the .dtd file is at technicalContent
    title = u"Topic"
    parent = None
    root = TopicElement()
class ConceptType(TopicType):
    """Concept topic type."""
    id = u"concept"
    file = u"technicalContent/dtd/concept"
    title = u"Concept"
    parent = TopicType()
    root = ConceptElement()
class TaskType(TopicType):
    """Task topic type."""
    id = u"task"
    file = u"technicalContent/dtd/task"
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
    title = u"Reference"
    parent = TopicType()
    root = ReferenceElement()
class MapType(ditagen.dita.Type):
    """Map topic type."""
    id = u"map"
    file = u"base/dtd/map" # the .dtd file is at technicalContent
    title = u"Map"
    parent = None
    root = MapElement()

class BookMapType(MapType):
    """BookMap topic type."""
    id = u"bookmap"
    file = u"bookmap/dtd/bookmap"
    title = u"BookMap"
    parent = MapType()
    root = BookMapElement()

class MachineryTaskType(ditagen.dita.ShellType):
    """Machinery Task topic type."""
    def __init__(self):
        super(MachineryTaskType, self).__init__(u"machineryTask", u"Machinery Task", TaskType(), file=u"machineryIndustry/dtd/machineryTask")
        #self.parent.required_domains = [MachineryTaskbodyConstraints]

class LearningBaseType(TopicType):
    """Learning Base topic type."""
    id = u"learningBase"
    file = u"learning/dtd/learningBase"
    title = u"Learning Base"
    parent = TopicType()
    root = LearningBaseElement()
class LearningAssessmentType(LearningBaseType):
    """Learning Assessment topic type."""
    id = u"learningAssessment"
    file = u"learning/dtd/learningAssessment"
    title = u"Learning Assessment"
    parent = LearningBaseType()
    root = LearningAssessmentElement()
class LearningOverviewType(LearningBaseType):
    """Learning Overview topic type."""
    id = u"learningOverview"
    file = u"learning/dtd/learningOverview"
    title = u"Learning Overview"
    parent = LearningBaseType()
    root = LearningOverviewElement()
class LearningPlanType(LearningBaseType):
    """Learning Plan topic type."""
    id = u"learningPlan"
    file = u"learning/dtd/learningPlan"
    title = u"Learning Plan"
    parent = LearningBaseType()
    root = LearningPlanElement()
class LearningSummaryType(LearningBaseType):
    """Learning Summary topic type."""
    id = u"learningSummary"
    file = u"learning/dtd/learningSummary"
    title = u"Learning Summary"
    parent = LearningBaseType()
    root = LearningSummaryElement()
class LearningContentType(LearningBaseType):
    """Learning Content topic type."""
    id = u"learningContent"
    file = u"learning/dtd/learningContent"
    title = u"Learning Content"
    parent = LearningBaseType()
    root = LearningContentElement()
    def __init__(self):
        super(LearningContentType, self).__init__()
        self.required_types = [TaskType(), ConceptType(), ReferenceType(), LearningSummaryType(), LearningAssessmentType()]
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
    file_suffix = u""
    fpi_suffix = u" Constraint"
    elements = []
    def get_file_name(self, extension):
        return self.file + self.file_suffix + "." + extension

# Domains

class UiDomain(ditagen.dita.Domain):
    """User interface domain."""
    id = u"ui-d"
    _file = u"technicalContent/dtd/uiDomain"
    title = u"User Interface"
    elements = [u"pre", u"keyword", u"ph"]
    parent = [TopicType]
class HiDomain(ditagen.dita.Domain):
    """Hilight domain."""
    id = u"hi-d"
    _file = u"base/dtd/highlightDomain"
    title = u"Highlight"
    elements = [u"ph"]
    parent = [TopicType]
class PrDomain(ditagen.dita.Domain):
    """Programmign domain."""
    id = u"pr-d"
    _file = u"technicalContent/dtd/programmingDomain"
    title = u"Programming"
    elements = [u"pre", u"keyword", u"ph", u"fig", u"dl"]
    parent = [TopicType]
class SwDomain(ditagen.dita.Domain):
    """Software development domain."""
    id = u"sw-d"
    _file = u"technicalContent/dtd/softwareDomain"
    title = u"Software"
    elements = [u"pre", u"keyword", u"ph"]
    parent = [TopicType]
class UtDomain(ditagen.dita.Domain):
    """Utilities domain."""
    id = u"ut-d"
    _file = u"base/dtd/utilitiesDomain"
    title = u"Utilities"
    elements = [u"fig"]
    parent = [TopicType]
class IndexingDomain(ditagen.dita.Domain):
    """Indexing domain."""
    id = u"indexing-d"
    _file = u"base/dtd/indexingDomain"
    title = u"Indexing"
    elements = [u"index-base"]
    parent = [TopicType, MapType]
class LearningDomain(ditagen.dita.Domain):
    """Learning domain."""
    id = u"learning-d"
    _file = u"learning/dtd/learningDomain"
    title = u"Learning"
    elements = [u"note", u"fig"]
    # XXX: This builds on 
    parent = [TopicType]
    required_domains = [UtDomain]
class LearningMetaDomain(ditagen.dita.Domain):
    """Learning metadata domain."""
    id = u"learningmeta-d"
    _file = u"learning/dtd/learningMetadataDomain"
    title = u"Learning Metadata"
    elements = [u"metadata"]
    parent = [TopicType]
class LearningMapDomain(ditagen.dita.Domain):
    """Learning map domain."""
    id = u"learningmap-d"
    _file = u"learning/dtd/learningMapDomain"
    title = u"Learning Map"
    elements = [u"topicref"]
    parent = [MapType]
class TaskRequirementsDomain(ditagen.dita.Domain):
    """Task requirements domain."""
    id = u"taskreq-d"
    _file = u"technicalContent/dtd/taskreqDomain"
    title = u"Machine Industry Task"
    elements = [u"prereq", u"postreq"]
    parent = [TaskType]
class HazardStatementDomain(ditagen.dita.Domain):
    """Hazard statement domain."""
    id = u"hazard-d"
    _file = u"base/dtd/hazardstatementDomain"
    title = u"Hazard Statement"
    elements = [u"note"]
    parent = [TopicType]
class MapGroupDomain(ditagen.dita.Domain):
    """Map group domain."""
    id = u"mapgroup-d"
    _file = u"base/dtd/mapGroup" # This is an exception to DITA's naming scheme
    title = u"Map Group"
    elements = [u"topicref"]
    parent = [MapType]
class AbbreviatedFormDomain(ditagen.dita.Domain):
    """Abbreviated form domain."""
    id = u"abbrev-d"
    _file = u"technicalContent/dtd/abbreviateDomain"
    title = u"Abbreviated Form"
    elements = [u"term"]
    parent = [TopicType]
class XNALDomain(ditagen.dita.Domain):
    """XNAL domain."""
    id = u"xnal-d"
    _file = u"xnal/dtd/xnalDomain"
    title = u"XNAL"
    elements = [u"author"]
    parent = [MapType]
class UserDelayedResolutionDomain(ditagen.dita.Domain):
    """User delayed resolution domain."""
    id = u"delay-d"
    _file = u"base/dtd/delayResolutionDomain"
    title = u"Delayed Resolution"
    elements = [u"keywords"]
    parent = [TopicType, MapType]
class ClassifyDomain(ditagen.dita.Domain):
    """Classify domain."""
    id = u"classify-d"
    _file = u"subjectScheme/dtd/classifyDomain"
    title = u"Map Subject Classification"
    elements = [u"topicref", u"reltable"]
    parent = [TopicType, MapType]
class GlossaryReferenceDomain(ditagen.dita.Domain):
    """Glossary reference domain."""
    id = u"glossref-d"
    _file = u"technicalContent/dtd/glossrefDomain"
    title = u"Glossary Reference"
    elements = [u"topicref"]
    parent = [MapType]

# Constraints

class StrictTaskbodyConstraints(Constraints):
    """Strict taskbody constraints."""
    id = u"strictTaskbody-c"
    _file = u"technicalContent/dtd/strictTaskbodyConstraint"
    title = u"Strict Taskbody"
    parent = [TaskType]
    _att_id = u"taskbody"
class MachineryTaskbodyConstraints(Constraints):
    """Machinery taskbody constraints."""
    id = u"machineryTaskbody-c"
    _file = u"machineryIndustry/dtd/machineryTaskbodyConstraint"
    title = u"Machinery Taskbody"
    parent = [TaskType]
    _att_id = u"taskbody"

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
