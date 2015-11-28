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

class Entity(object):
    """Base for entities."""
    name = None
    value = None
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
class ParameterEntity(Entity):
    """Base for parameter entities."""
    def __init__(self, name, value=None):
        Entity.__init__(self, name, value)
    def __str__(self):
        return "%%%s;" % self.name
class GeneralEntity(Entity):
    """Base for general entities."""
    def __init__(self, name, value=None):
        Entity.__init__(self, name, value)
    def __str__(self):
        return "&%s;" % self.name
class GlobalAtts(ParameterEntity):
    #_value = u"""xtrc CDATA #IMPLIED
    #             xtrf CDATA #IMPLIED"""
    def __init__(self):
        ParameterEntity.__init__(self, u"global-atts", u"")

class Attribute(object):
    name = None
    attr_type = None
    default = None
    def __init__(self, name, attr_type, default):
        self.name = name
        self.attr_type = attr_type
        self.default = default
    def get_name(self):
        return self.name
    def get_type(self):
        return self.attr_type
    def get_default(self):
        return self.default
    def __str__(self):
        return "%s %s %s" % (self.name, self.attr_type, self.default)

class Element(object):
    """Base for elements."""
    name = None
    model = None
    attrs = None
    def __init__(self):
        pass
    def get_name(self):
        """Get element name."""
        return self.name
    def get_model(self):
        """Get element content model."""
        return self.model
    def get_attributes(self):
        """Get element attributes."""
        return self.attrs

def enum(**enums):
    return type('Enum', (), enums)

class Empty(object):
    def __str__(self):
        return "EMPTY"
class Any(object):
    def __str__(self):
        return "ANY"
class Mixed(object):
    names = None
    def __init__(self, names=[]):
        Particle.__init__(self)
        self.names = names
    def __str__(self):
        return "(" + " | ".join([str(n) for n in self.names]) + ")*"
class Particle(object):
    Occurrences = enum(ONCE = "", OPTIONAL = "?", ZERO_OR_MORE = "*", ONCE_OR_MORE = "+")
    occurrence = None
    def __init__(self, occurrence=Occurrences.ONCE):
        self.occurrence = occurrence
class Name(Particle):
    name = None
    def __init__(self, name, occurrence=Particle.Occurrences.ONCE):
        Particle.__init__(self, occurrence)
        self.name = name
    def __str__(self):
        return str(self.name) + str(self.occurrence)
class Choice(Particle):
    particles = []
    def __init__(self, particles, occurrence=Particle.Occurrences.ONCE):
        Particle.__init__(self, occurrence)
        if type(particles) is list:
            self.particles = particles
        else:
            self.particles = [particles]
    def __str__(self):
        return "(" + " | ".join([str(n) for n in self.particles]) + ")" + str(self.occurrence)
class Seq(Particle):
    particles = []
    def __init__(self, particles, occurrence=Particle.Occurrences.ONCE):
        Particle.__init__(self, occurrence)
        if type(particles) is list:
            self.particles = particles
        else:
            self.particles = [particles]
    def __str__(self):
        return "(" + ", ".join([str(n) for n in self.particles]) + ")" + str(self.occurrence)

class Param(object):
    name = None
    def __init__(self, name):
        self.name = name

