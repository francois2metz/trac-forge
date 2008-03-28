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

import unittest
from tracforge.config import Config
from tracforge.tests import dirname

here = dirname()

class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.pathFile = here+"/forge.ini"
        self.config = Config(self.pathFile)
    def test_ReadForgeHref(self):
        """Il lit le fichier et remplit la propriete forge_href"""
        self.assertEquals('/forge', self.config.forge_href)
    def test_ReadTemplatesDir(self):
        """Il lit l'emplacement des templates"""
        self.assertEquals('/home/ter', self.config.template_dir)
    def test_ReadTrac(self):
        """Il lit les infos du trac"""
        self.assertEquals('/var/trac', self.config.trac_dir)
        self.assertEquals('/trac', self.config.trac_href)
    def test_ReadMediaHref(self):
        """Il lit l'uri de media"""
        self.assertEquals('/media', self.config.media_href)
    def test_ReadDemo(self):
        """Il lit les informations de la demo"""
        self.assertEquals('/demohref', self.config.demo_href)
        self.assertEquals('/demodir', self.config.demo_dir)
    def test_ReadArchives(self):
        """Il lit les informations de l'archives """
        self.assertEquals('/archivehref', self.config.archives_href)
        self.assertEquals('/archivedir', self.config.archives_dir)

def suite():
    return unittest.makeSuite(ConfigTestCase, 'test')
        
if __name__ == '__main__':
    unittest.main()

