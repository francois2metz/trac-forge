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

from tracforge.config import Config

class Tracenvadmin:

    def __init__(self):
        self.db = "sqlite:db/trac.db"
        self.template = "/usr/share/trac/templates"
        self.svn = "svn"
    
    def create_env(self, config, projectname = None):
        os.chdir(config.svn_dir)
        os.system("/usr/bin/svnadmin create "+projectname)
        os.chdir(config.trac_dir)    
        os.system("/usr/bin/trac-admin "+projectname+" initenv "+projectname+" "+self.db+" "+self.svn+" "+config.svn_dir+"/"+projectname+" "+self.template)

    def delete_env(self, config, projectname = None):
        os.system("/bin/rm -Rf "+config.svn_dir+"/"+projectname)
        os.system("/bin/rm -Rf "+config.trac_dir+"/"+projectname)

if __name__ == "__main__":
    env = Tracenvadmin()
    #env.createenv("test2")

