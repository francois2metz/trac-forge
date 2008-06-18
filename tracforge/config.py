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

from ConfigParser import ConfigParser

class Config:
    """Contient la configuration"""
    def __init__(self, pathConfigFile):
        configFile = ConfigParser()
        configFile.readfp(open(pathConfigFile))

        self.forge_href    = configFile.get('forge', 'href')
        self.template_dir  = configFile.get('templates', 'dir')
        self.media_href    = configFile.get('media', 'href')
        self.demo_href     = configFile.get('demo', 'href')
        self.demo_dir      = configFile.get('demo', 'dir')
        self.archives_href = configFile.get('archives', 'href')
        self.archives_dir  = configFile.get('archives', 'dir')
        self.trac_dir      = configFile.get('trac', 'dir')
        self.trac_href     = configFile.get('trac', 'href')
        self.svn_dir       = configFile.get('svn','dir')
        self.svn_href      = configFile.get('svn','href')

