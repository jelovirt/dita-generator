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

import inspect
import ditagen.dita
import ditagen.dita.v1_1
import ditagen.dita.v1_2

OUTPUT_MAP = {
    "specialization": ditagen.dita.SpecializationType,
    "shell": ditagen.dita.ShellType
    }
#DOMAIN_MAP = {
#    "1.1": {
#        "ui-d": ditagen.dita.v1_1.UiDomain,
#        "hi-d": ditagen.dita.v1_1.HiDomain,
#        "pr-d": ditagen.dita.v1_1.PrDomain,
#        "sw-d": ditagen.dita.v1_1.SwDomain,
#        "ut-d": ditagen.dita.v1_1.UtDomain,
#        "indexing-d": ditagen.dita.v1_1.IndexingDomain,
#        "mapgroup-d": ditagen.dita.v1_1.MapGroupDomain,
#        #"abbreviated-d": ditagen.dita.v1_1.AbbreviatedFormDomain,
#        "xnal-d": ditagen.dita.v1_1.XNALDomain,
#        },
#    "1.2": {
#        "ui-d": ditagen.dita.v1_2.UiDomain,
#        "hi-d": ditagen.dita.v1_2.HiDomain,
#        "pr-d": ditagen.dita.v1_2.PrDomain,
#        "sw-d": ditagen.dita.v1_2.SwDomain,
#        "ut-d": ditagen.dita.v1_2.UtDomain,
#        "indexing-d": ditagen.dita.v1_2.IndexingDomain,
#        "learning-d": ditagen.dita.v1_2.LearningDomain,
#        "learningmeta-d": ditagen.dita.v1_2.LearningMetaDomain,
#        "learningmap-d": ditagen.dita.v1_2.LearningMapDomain,
#        "taskreq-d": ditagen.dita.v1_2.TaskRequirementsDomain,
#        "hazardstatement-d": ditagen.dita.v1_2.HazardStatementDomain,
#        "mapgroup-d": ditagen.dita.v1_2.MapGroupDomain,
#        "glossref-d": ditagen.dita.v1_2.GlossaryReferenceDomain,
#        "abbreviated-d": ditagen.dita.v1_2.AbbreviatedFormDomain,
#        "xnal-d": ditagen.dita.v1_2.XNALDomain,
#        "delay-d": ditagen.dita.v1_2.UserDelayedResolutionDomain,
#        "classify-d": ditagen.dita.v1_2.ClassifyDomain,
#        "taskbody-c": ditagen.dita.v1_2.MachineryTaskbodyConstraints,
#        "strictTaskbody-c": ditagen.dita.v1_2.StrictTaskbodyConstraints
#        }
#    }
#TOPIC_MAP = {
#    "1.1": {
#        "concept": ditagen.dita.v1_1.ConceptType,
#        "reference": ditagen.dita.v1_1.ReferenceType,
#        "task": ditagen.dita.v1_1.TaskType,
#        "topic": ditagen.dita.v1_1.TopicType,
#        "map": ditagen.dita.v1_1.MapType,
#        "bookmap": ditagen.dita.v1_1.BookMapType,
#        },
#    "1.2": {
#        "concept": ditagen.dita.v1_2.ConceptType,
#        "reference": ditagen.dita.v1_2.ReferenceType,
#        "task": ditagen.dita.v1_2.TaskType,
#        "generalTask": ditagen.dita.v1_2.GeneralTaskType,
#        "topic": ditagen.dita.v1_2.TopicType,
#        "machineryTask": ditagen.dita.v1_2.MachineryTaskType,
#        "map": ditagen.dita.v1_2.MapType,
#        "bookmap": ditagen.dita.v1_2.BookMapType,
#        "classifyMap": ditagen.dita.v1_2.ClassificationMapType,
#        "subjectScheme": ditagen.dita.v1_2.SubjectSchemeType,
#        "learningAssessment": ditagen.dita.v1_2.LearningAssessmentType,
#        "learningBookmap": ditagen.dita.v1_2.LearningBookMapType,
#        "learningContent": ditagen.dita.v1_2.LearningContentType,
#        "learningMap": ditagen.dita.v1_2.LearningMapType,
#        "learningOverview": ditagen.dita.v1_2.LearningOverviewType,
#        "learningPlan": ditagen.dita.v1_2.LearningPlanType,
#        "learningSummary": ditagen.dita.v1_2.LearningSummaryType
#        }
#    }

def find_subclasses(module, clazz):
    return [cls for name, cls in inspect.getmembers(module)
            if cls not in clazz and inspect.isclass(cls) and
                [i for i in clazz if issubclass(cls, i)]]
def get_map(module, clazz):
    return dict([(cls().id, cls) for cls in find_subclasses(module, clazz)])

DOMAIN_MAP = {
    "1.1": get_map(ditagen.dita.v1_1, [ditagen.dita.Domain]),
    "1.2": get_map(ditagen.dita.v1_2, [ditagen.dita.Domain, ditagen.dita.v1_2.Constraints]),
}
TOPIC_MAP = {
    "1.1": get_map(ditagen.dita.v1_1, [ditagen.dita.Type]),
    "1.2": get_map(ditagen.dita.v1_2, [ditagen.dita.Type]),
}