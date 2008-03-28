#!/usr/bin/env python
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
#
# trac-admin initenv <projectname> <db> <repostype> <repospath> <templatepath>
#
import os
import sys
import time

sys.path.append('../')
from tracforge.config import Config

class Tracenvadmin:

	def __init__(self):
		self.db = "sqlite:db/trac.db"
		self.template = "/usr/share/trac/templates"
		self.rootpath = Config.root_dir 
		self.tracpath = Config.trac_dir
		self.svnpath = self.rootpath+"/svn/"
		self.svn = "svn"
	
	def createenv(self,projectname = None):
		if not projectname:
			raise ProjectnameUndefined 
		os.chdir(self.svnpath)
		os.system("/usr/bin/svnadmin create "+projectname)
		os.chdir(self.tracpath)	
		os.system("/usr/bin/trac-admin "+projectname+" initenv "+projectname+" "+self.db+" "+self.svn+" "+self.svnpath+projectname+" "+self.template)


if __name__ == "__main__":
	env = Tracenvadmin()
	#env.createenv("test2")

