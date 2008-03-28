#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of TracForge Project
#
# Copyright (C) 2008 TracForge Project
#
# See AUTHORS for more informations
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "TracForge",
    version = "0.1",

    author = "TracForge Team",
    author_email = "francois@2metz.fr",
    description = "Forge for trac",
    long_description = "",
    license = "GNU AGPL 3",
    url = "http://etna.2bass.fr/p/trac-forge",

    zip_safe = False,

    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data = {
        '' : ['templates/*']
        },


    test_suite = "tracforge.tests.suite.suite",

    install_requires = [
#        'setuptools>=0.6c',
#        'Trac>=0.10'
        ],

    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
    
)
