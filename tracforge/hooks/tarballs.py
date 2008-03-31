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

import pysvn
import tarfile
import bz2
from tempfile import mkdtemp
from os.path import basename, join, exists
from os import rmdir, remove, walk, mkdir

from tracforge.hooks.hook import IHook

class TarballHook(IHook):
    def getDescription(self):
        return "Fait une archive bzip2 du depot"
    def run(self, config, svnpath, rev):
        "Execute le hook"
        projectName = basename(svnpath)
        tempDir = mkdtemp()
        # Export svn
        client = pysvn.Client()
        client.export('file://'+ svnpath,
                      join(tempDir, projectName))
        # Create archive
        pathArchive = join(config.archives_dir, projectName);
        if not exists(pathArchive):
            mkdir(pathArchive)          
        nameArchive = join(pathArchive, projectName + '-r'+ rev +'.tar.bz2')
        archive = tarfile.open(nameArchive, 'w:bz2')
        archive.add(tempDir, '/')
        archive.close()
        # Delete tempDir
        for root, dirs, files in walk(tempDir, topdown=False):
            for name in files:
                remove(join(root, name))
            for name in dirs:
                rmdir(join(root, name))
        rmdir(tempDir)

if __name__ == "__main__":
    import sys
    from tracforge.config import Config
    if len(sys.argv) != 4:
        print "Usage: ./tarballs.py configpath svnpath rev"
        sys.exit();
    configpath = sys.argv[1]
    config = Config(configpath)
    svnpath = sys.argv[2]
    rev = sys.argv[3]
    hook = TarballHook()
    hook.run(config, svnpath, rev)
