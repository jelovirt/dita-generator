#!/usr/bin/env python2.6

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
import os
import os.path
import ditagen.generator
import zipfile
import ditagen

OUTPUT_MAP = {
    u"specialization": ditagen.dita.SpecializationType,
    u"shell": ditagen.dita.ShellType
    }
DEFAULT_DOMAIN_MAP = {
    u"1.1": {
        u"concept": [u"ui-d", u"hi-d", u"pr-d", u"sw-d", u"ut-d", u"indexing-d"],
        u"reference": [u"ui-d", u"hi-d", u"pr-d", u"sw-d", u"ut-d", u"indexing-d"],
        u"task": [u"ui-d", u"hi-d", u"pr-d", u"sw-d", u"ut-d", u"indexing-d"],
        u"topic": [u"ui-d", u"hi-d", u"pr-d", u"sw-d", u"ut-d", u"indexing-d"],
        u"map": [u"mapgroup-d", u"indexing-d"],
        u"bookmap": [u"mapgroup-d", u"indexing-d", u"xnal-d"],
        },
    u"1.2": {
        u"concept": [u"hi-d", u"ut-d", u"indexing-d", u"hazard-d", u"abbrev-d", u"pr-d", u"sw-d", u"ui-d"],
        u"reference": [u"hi-d", u"ut-d", u"indexing-d", u"hazard-d", u"abbrev-d", u"pr-d", u"sw-d", u"ui-d"],
        u"task": [u"strictTaskbody-c", u"hi-d", u"ut-d", u"indexing-d", u"hazard-d", u"abbrev-d", u"pr-d", u"sw-d", u"ui-d"],
        u"generalTask": [u"hi-d", u"ut-d", u"indexing-d", u"hazard-d", u"abbrev-d", u"pr-d", u"sw-d", u"ui-d"],
        u"topic": [u"hi-d", u"ut-d", u"indexing-d", u"hazard-d", u"abbrev-d", u"pr-d", u"sw-d", u"ui-d"],
        u"machineryTask": [u"machineryTaskbody-c", u"taskreq-d", u"hazard-d", u"hi-d", u"ut-d", u"indexing-d", u"pr-d", u"sw-d", u"ui-d"],
        u"map": [u"mapgroup-d", u"indexing-d", u"delay-d", u"glossref-d"],
        u"bookmap": [u"mapgroup-d", u"indexing-d", u"delay-d", u"xnal-d"],
        u"classifyMap": [u"mapgroup-d", u"indexing-d", u"delay-d", u"classify-d"],
        u"subjectScheme": [u"mapgroup-d"],
        u"learningBase": [u"learning-d", u"learningmeta-d", u"hi-d", u"ut-d", u"indexing-d"],
        u"learningAssessment": [u"learning-d", u"learningmeta-d", u"hi-d", u"ut-d", u"indexing-d"],
        u"learningBookmap": [u"learningmap-d", u"learningmeta-d", u"mapgroup-d", u"indexing-d", u"delay-d", u"xnal-d"],
        u"learningContent": [u"learning-d", u"learningmeta-d", u"hi-d", u"ut-d", u"indexing-d"],
        u"learningMap": [u"learningmap-d", u"learningmeta-d", u"mapgroup-d", u"indexing-d", u"delay-d"],
        u"learningOverview": [u"learning-d", u"learningmeta-d", u"hi-d", u"ut-d", u"indexing-d"],
        u"learningPlan": [u"learning-d", u"learningmeta-d", u"hi-d", u"ut-d", u"indexing-d"],
        u"learningSummary": [u"learning-d", u"learningmeta-d", u"hi-d", u"ut-d", u"indexing-d"]
        }
    }
#DEFAULT_DOMAIN_MAP = {
#    "1.1": {
#        "concept": (ditagen.dita.v1_1.ConceptType, ["ui-d", "hi-d", "pr-d", "sw-d", "ut-d", "indexing-d"]),
#        "reference": (ditagen.dita.v1_1.ReferenceType, ["ui-d", "hi-d", "pr-d", "sw-d", "ut-d", "indexing-d"]),
#        "task": (ditagen.dita.v1_1.TaskType, ["ui-d", "hi-d", "pr-d", "sw-d", "ut-d", "indexing-d"]),
#        "topic": (ditagen.dita.v1_1.TopicType, ["ui-d", "hi-d", "pr-d", "sw-d", "ut-d", "indexing-d"]),
#        "map": (ditagen.dita.v1_1.MapType, ["mapgroup-d", "indexing-d"]),
#        "bookmap": (ditagen.dita.v1_1.BookMapType, ["mapgroup-d", "indexing-d", "xnal-d"]),
#        },
#    "1.2": {
#        "concept": (ditagen.dita.v1_2.ConceptType, ["hi-d", "ut-d", "indexing-d", "hazard-d", "abbrev-d", "pr-d", "sw-d", "ui-d"]),
#        "reference": (ditagen.dita.v1_2.ReferenceType, ["hi-d", "ut-d", "indexing-d", "hazard-d", "abbrev-d", "pr-d", "sw-d", "ui-d"]),
#        "task": (ditagen.dita.v1_2.TaskType, ["hi-d", "ut-d", "indexing-d", "hazard-d", "abbrev-d", "pr-d", "sw-d", "ui-d"]),
#        "generalTask": (ditagen.dita.v1_2.GeneralTaskType, ["hi-d", "ut-d", "indexing-d", "hazard-d", "abbrev-d", "pr-d", "sw-d", "ui-d"]),
#        "topic": (ditagen.dita.v1_2.TopicType, ["hi-d", "ut-d", "indexing-d", "hazard-d", "abbrev-d", "pr-d", "sw-d", "ui-d"]),
#        "machineryTask": (ditagen.dita.v1_2.MachineryTaskType, ["taskreq-d", "hazard-d", "hi-d", "ut-d", "indexing-d", "pr-d", "sw-d", "ui-d"]),
#        "map": (ditagen.dita.v1_2.MapType, ["mapgroup-d", "indexing-d", "delay-d", "glossref-d"]),
#        "bookmap": (ditagen.dita.v1_2.BookMapType, ["mapgroup-d", "indexing-d", "delay-d", "xnal-d"]),
#        "classifyMap": (ditagen.dita.v1_2.ClassificationMapType, ["mapgroup-d", "indexing-d", "delay-d", "classify-d"]),
#        "subjectScheme": (ditagen.dita.v1_2.SubjectSchemeType, ["mapgroup-d"]),
#        "learningBase": (ditagen.dita.v1_2.LearningBaseType, ["learning-d", "learningmeta-d", "hi-d", "ut-d", "indexing-d"]),
#        "learningAssessment": (ditagen.dita.v1_2.LearningAssessmentType, ["learning-d", "learningmeta-d", "hi-d", "ut-d", "indexing-d"]),
#        "learningBookmap": (ditagen.dita.v1_2.LearningBookMapType, ["learningmap-d", "learningmeta-d", "mapgroup-d", "indexing-d", "delay-d", "xnal-d"]),
#        "learningContent": (ditagen.dita.v1_2.LearningContentType, ["learning-d", "learningmeta-d", "hi-d", "ut-d", "indexing-d"]),
#        "learningMap": (ditagen.dita.v1_2.LearningMapType, ["learningmap-d", "learningmeta-d", "mapgroup-d", "indexing-d", "delay-d"]),
#        "learningOverview": (ditagen.dita.v1_2.LearningOverviewType, ["learning-d", "learningmeta-d", "hi-d", "ut-d", "indexing-d"]),
#        "learningPlan": (ditagen.dita.v1_2.LearningPlanType, ["learning-d", "learningmeta-d", "hi-d", "ut-d", "indexing-d"]),
#        "learningSummary": (ditagen.dita.v1_2.LearningSummaryType, ["learning-d", "learningmeta-d", "hi-d", "ut-d", "indexing-d"])
#        }
#    }

def main():
    if len(sys.argv) != 2:
        sys.err.write("Usage: batch.py WORK-DIR")
        sys.exit(1)
    #temp_path = os.path.join(os.path.expanduser("~"), "tmp", "ditagen", "work")
    temp_path = os.path.abspath(sys.argv[1])
    #dita_ot_path = os.environ["DITA_HOME"]

    for version in ditagen.TOPIC_MAP.keys():
        if not os.path.exists(os.path.join(temp_path, version)):
            os.makedirs(os.path.join(temp_path, version))
        for topic in ditagen.TOPIC_MAP[version].keys():
            types = list(OUTPUT_MAP.keys())
            #types.append(None)
            for type in types:
                #name = [i for i in [topic, type, version] if i is not None]
                name = [i for i in [topic, type] if i is not None]
                plugin_name = "_".join(name)
                #title = " ".join(name).capitalize()
                super = ditagen.TOPIC_MAP[version][topic]()
                title = super.title
                if type is not None:
                    title += " " + type.capitalize()

                if type is not None:
                    __type = OUTPUT_MAP[type](plugin_name, title, super, u"TEST", plugin_name)
                else:
                    __type = ditagen.TOPIC_MAP[version][topic]()

                out_path = os.path.join(temp_path, version, u"plugins", plugin_name + ".zip")
                print out_path
                out = file(out_path, "w")
                #os.remove(out + ".zip")

                __dita_gen = ditagen.generator.PluginGenerator()
                __dita_gen.out = out
                __dita_gen.topic_type = __type
                if ditagen.generator.isinstancetype(__type, ditagen.TOPIC_MAP[version][u"topic"]):
                    __dita_gen.domains = [
                        ditagen.DOMAIN_MAP[version][i]() for i in DEFAULT_DOMAIN_MAP[version][topic]#ditagen.DOMAIN_MAP[version].keys()
                        ]
                elif ditagen.generator.isinstancetype(__type, ditagen.TOPIC_MAP[version][u"map"]):
                    __dita_gen.domains = [
                        ditagen.DOMAIN_MAP[version][i]() for i in DEFAULT_DOMAIN_MAP[version][topic] #ditagen.DOMAIN_MAP[version].keys()
                        ]
                __dita_gen.nested = False
                __dita_gen.version = version
                __dita_gen.set_title(title)
                #if options.stylesheet:
                #    __dita_gen.set_stylesheet(options.stylesheet)
                __dita_gen.set_plugin_name(plugin_name)

                __dita_gen.generate_plugin()
                out.close()

                #__zip = zipfile.ZipFile(out_path, "r")
                #__zip.extractall(os.path.join(dita_ot_path, "plugins"))
                #__zip.close()

if __name__ == "__main__":
    main()
