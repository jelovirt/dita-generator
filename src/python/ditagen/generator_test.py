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

import unittest
import ditagen.generator
import StringIO

class DtdGeneratorTestCase(unittest.TestCase):

    def setUp(self):
        self.generator = ditagen.generator.DtdGenerator()

    def tearDown(self):
        self.generator = None

    def test_generate_pi(self):
        self.assertEqual(self.generator.generate_pi(u"owner", u"description"),
                         u"-//owner//description//EN")

    def test_external_general_entity_system(self):
        __out = StringIO.StringIO()
        self.generator.set_output(__out)
        self.generator.external_general_entity(u"name", u"system")
        self.assertEqual(__out.getvalue(),
                         u"""<!ENTITY name SYSTEM "system">\n""")

    def test_external_general_entity_public(self):
        __out = StringIO.StringIO()
        self.generator.set_output(__out)
        self.generator.external_general_entity(u"name", u"system", u"public")
        self.assertEqual(__out.getvalue(),
                         u"""<!ENTITY name PUBLIC "public" "system">\n""")

    def test_internal_general_entity(self):
        __out = StringIO.StringIO()
        self.generator.set_output(__out)
        self.generator.internal_general_entity(u"name", u"value")
        self.assertEqual(__out.getvalue(),
                         u"""<!ENTITY name "value">\n""")

    def test_external_parameter_entity_system(self):
        __out = StringIO.StringIO()
        self.generator.set_output(__out)
        self.generator.external_parameter_entity(u"name", u"system")
        self.assertEqual(__out.getvalue(),
                         u"""<!ENTITY % name SYSTEM "system">\n""")

    def test_external_parameter_entity_public(self):
        __out = StringIO.StringIO()
        self.generator.set_output(__out)
        self.generator.external_parameter_entity(u"name", u"system", u"public")
        self.assertEqual(__out.getvalue(),
                         u"""<!ENTITY % name\n  PUBLIC "public"\n         "system">\n""")

    def test_internal_parameter_entity(self):
        __out = StringIO.StringIO()
        self.generator.set_output(__out)
        self.generator.internal_parameter_entity(u"name", u"value")
        self.assertEqual(__out.getvalue(),
                         u"""<!ENTITY % name "value">\n""")

    def test_element_declaration(self):
        __out = StringIO.StringIO()
        self.generator.set_output(__out)
        self.generator.element_declaration(u"name", u"model")
        self.assertEqual(__out.getvalue(),
                         u"""<!ELEMENT name (model)>\n""")

    def test_attribute_declaration(self):
        __out = StringIO.StringIO()
        self.generator.set_output(__out)
        self.generator.attribute_declaration(u"name", u"attrs")
        self.assertEqual(__out.getvalue(),
                         u"""<!ATTLIST name attrs>\n""")

    def test_parameter_entity_ref(self):
        __out = StringIO.StringIO()
        self.generator.set_output(__out)
        self.generator.parameter_entity_ref(u"name")
        self.assertEqual(__out.getvalue(),
                         u"%name;")

    def test_unique(self):
        pairs = [
            (["a", "b", "c"],
             ["a", "b", "c"]),
            (["a", "b", "a"],
             ["a", "b"]),
            (["a", "a", "a"],
             ["a"])
        ]
        for i in pairs:
            self.assertEqual(ditagen.generator.unique(i[0]), i[1])

class DitaGeneratorTestCase(unittest.TestCase):

    def setUp(self):
        self.generator = ditagen.generator.DitaGenerator()

    def tearDown(self):
        self.generator = None

    def test_set_topic_type(self):
        self.assertRaises(AssertionError , self.generator.set_topic_type, "type_topic")

if __name__ == '__main__':
    unittest.main()
