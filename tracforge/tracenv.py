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

from trac.env import open_environment
from dircache import listdir
from os import path as ospath
from time import time

class TracProject:
    """"Project description"""
    def __init__(self, path, href):
        # env information
        self.path               = path
        self.env                = open_environment(path)
        self.name               = self.env.project_name
        self.href               = href
        self.description        = self.env.project_description
        # last commit information
        self.last_author        = ""
        self.last_message       = "This repository has not yet been modified"
        # hack to get an time object with value = 0
        self.last_date          = 0
        self.last_rev           = "0"
        self._set_info()

    def _set_info(self):
        # in crashes if no commit have been done.
        try :
            # last commit information
            repo                = get_repos()
            last_action         = repo.get_changeset(repos.youngest_rev)
            self.last_rev       = repo.youngest_rev
            self.last_author    = last_action.author
            self.last_message   = last_action.message
            self.last_date      = last_action.date
        except :
            pass

    def get_repos(self):
        return self.env.get_repository()

    def get_path(self):
        return self.path

    def get_env(self):
        return self.env

    def get_name(self):
        return self.name

    def get_href(self):
        return self.href

    def get_description(self):
        return self.description

    def get_last_author(self):
        return self.last_author

    def get_last_message(self):
        return self.last_message

    def get_last_date(self):
        return self.last_date

    def get_last_rev(self):
        return self.last_rev


class TracProjects:
    """"All the projects"""
    def __init__(self, trac_dir, trac_href):
        self.trac_dir = trac_dir
        self._projects = self._get_projects(trac_href)
        self.index = 0

    def next(self):
        nb = len(self._projects)
        if self.index < nb:
            project = self._projects[self.index]
            self.index = self.index + 1
            return project
        else:
            raise StopIteration

    def __iter__(self):
        self.index = 0
        return self

    def _get_projects(self, trac_href):
        projects = listdir(self.trac_dir)
        tracprojects = []
        for project in projects:
            path = "%s/%s" % (self.trac_dir, project)
            href = trac_href + ospath.basename(path)
            tracprojects.append(TracProject(path, href))
        return tracprojects

