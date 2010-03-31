#!/usr/bin/env python
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

from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(name='DITA Generator',
      version='@version@',
      description='DITA Generator library',
      author='Jarno Elovirta',
      author_email='jarno@elovirta.com',
      url='http://code.google.com/p/dita-generator/',
      packages=['ditagen', 'ditagen.dita'],
      #data_files = [('ditagen-data', ['../resources/lgpl.txt'])]
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Text Processing :: Markup :: XML',
          'Topic :: Software Development :: Code Generators',
          ],
      
     )
