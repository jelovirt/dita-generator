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

import ditagen.dtdgen

class DitaElement(ditagen.dtdgen.Element):
    """Base for DITA elements."""
    cls = None

class Type(object):
    """DITA topic type base."""
    id = None
    file = None
    pi_entity = None
    pi_module = None
    title = None #TODO: Remove in favour of outside title
    parent = None
    root = None
    owner = u"OASIS"
    default_domains = []
    required_domains = []
    required_types = []

class SpecializationType(Type):
    """Specialization topic type."""
    def __init__(self, id, title, parent, owner=None, file=None):
        ditagen.dita.Type.__init__(self)
        self.id = id
        self.title = title
        self.parent = parent
        self.owner = owner
        if file is not None:
            self.file = file
        else:
            self.file = id
        self.__root = None
    def __get_root(self):
        if self.__root is not None:
            return self.__root
        else:
            return self.parent.root
    def __set_root(self, __r):
        self.__root = __r
    root = property(__get_root, __set_root)        

class ShellType(Type):
    """Shell topic type."""
    def __init__(self, id, title, parent, owner=None, file=None):
        ditagen.dita.Type.__init__(self)
        self.id = id
        self.title = title
        self.parent = parent
        self.owner = owner
        if file is not None:
            self.file = file
        else:
            self.file = id
        self.root = parent.root

class DomainBase(object):
    """Base class for domains and constraints."""
    id = None
    title = None
    _file = None
    file_suffix = None
    #elements = None
    parent = []
    # Required domains which are not integrated themselves
    required_domains = []
    _att_id = None
    pi_module = None
    pi_entity = None
    def get_file(self):
        """Get domain file name."""
        return self._file + self.file_suffix
    def set_file(self, file):
        self._file = file
    file = property(get_file, set_file)
    def get_att_id(self):
        """Get domain attribute entity ID."""
        if self._att_id is not None:
            return self._att_id
        else:
            return self.id
    def set_att_id(self, att_id):
        """Set domain attribute entity ID."""
        self._att_id = att_id
    att_id = property(get_att_id, set_att_id)

class Domain(DomainBase):
    """Base class for domains."""
    file_suffix = u""
    fpi_suffix = u" Domain"
    elements = []
    def get_file_name(self, extension):
        return self._file + self._file_suffix + "." + extension

def create_element(__type, __root, __id):
    """Create new DITA element from an existing type's root element."""
    __r = type(__type.root)()
    __r.name = __root
    __r.cls = u"%s%s/%s " % (__r.cls, __id, __root)
    return __r