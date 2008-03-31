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

from mod_python import apache
from trac.env import open_environment
from dircache import listdir
from jinja import Environment, PackageLoader, FileSystemLoader
import time
from os import path
from tracforge.config import Config
from tracforge.tracenvadmin import Tracenvadmin

class TracProject:
    """"Instance d'un projet trac"""
    def __init__(self, path):
        self.path = path
	self.env = open_environment(path)
    def get_env(self):
        return self.env
    def get_repos(self):
        return self.env.get_repository()
    
class TracProjects:
    """"Tous les projets trac"""
    def __init__(self, trac_dir):
        self.trac_dir = trac_dir
        self._projects = self._get_projects()
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
    def _get_projects(self):
        projects = listdir(self.trac_dir)
        tracprojects = []
        for project in projects:
            tracprojects.append(TracProject("%s/%s" % (self.trac_dir, project)))
        return tracprojects
        
def handler(req):
    """traitement de la requete"""
    req.content_type = 'text/html; charset=utf-8'
    configFile = req.get_options()['ForgeConfig']
    config = Config(configFile)
    uri = req.uri.split("/")
    if len(uri) >= 3 and  uri[2] == "admin":
        if len(uri) >= 4 and uri[3] == "projects":
            if len(uri) >= 5 and uri[4] == "create":
                content = view_admin_projects(req, config, "create", uri[5])
            elif len(uri) >= 5 and uri[4] == "delete":
                content = view_admin_projects(req, config, "delete", uri[5])
            else:
                content = view_admin(req,config)
        else:
            content = view_admin(req, config)
    elif req.uri == config.forge_href+"/a" or req.uri == config.forge_href+"/z" or req.uri == config.forge_href+"/":
        content = view_index(req, config)
    else:
        content = view_404(req, config)
    req.write(content.encode('utf-8'))
    return apache.OK

def load_template(config, templateName):
    """"Charge un template"""
    if config.template_dir == "":
        environment = Environment(loader=PackageLoader('tracforge', 'templates'))
    else:
        environment = Environment(loader=FileSystemLoader(config.template_dir))
    return environment.get_template(templateName)
    
def view_admin(req, config):
    tmpl = load_template(config, "admin.html")
    context = {
        'users' : [{'name' : 'toto'}],
        'forge_href' : config.forge_href,
        'media_href' : config.media_href
    }
    return tmpl.render(context)

def view_admin_projects(req, config, action, project_name):
    env_trac = Tracenvadmin()
    if action == "create":
    	env_trac.create_env(config, project_name)
    elif action == "delete":
    	env_trac.delete_env(config, project_name)
    tmpl = load_template(config, "admin.html")
    context = {
        'users' : [{'name' : 'toto'}],
        'forge_href' : config.forge_href,
        'media_href' : config.media_href
    }
    return tmpl.render(context)

def view_404(req, config):
    """Page d'erreur 404"""
    req.status = 404
    tmpl = load_template(config, "404.html")
    context = {
        'forge_href' : config.forge_href,
        'media_href' : config.media_href
	}
    return tmpl.render(context)


def repository_diff_message(lastChange):
    project_date_diff = time.time() - lastChange.date
    nbYears = project_date_diff / (60 * 60 * 24 * 30 * 12)
    if nbYears > 1:
        project_message_diff = " plus de " + str(int(nbYears)) + " an"
    else:
        nbMonths = project_date_diff / (60 * 60 * 24 * 30)
        if nbMonths > 1:
            project_message_diff = str(int(nbMonths)) + " mois"
        else:
            nbDays = project_date_diff / (60 * 60 * 24)
            if nbDays > 1:
                project_message_diff = str(int(nbDays)) + " jours "
            else:
                nbHours = project_date_diff / (60 * 60)
                if nbHours > 1:
                    project_message_diff = "plus de " + str(int(nbHours)) + " heures"
                else:
                    project_message_diff = "moins d'une heure"
    return project_message_diff
                

def view_index(req, config):
    """Index des projets"""
    tracProjects = TracProjects(config.trac_dir)
    projects = []
    for project in tracProjects:
        # Prepare variable to set project
        env = project.get_env()
        repos = project.get_repos()
        dir = path.basename(project.path)
        try:
            lastChange = repos.get_changeset(repos.youngest_rev)
            project_name = env.project_name
            project_href = config.trac_href + dir
            project_description = env.project_description
            project_youngest_rev = repos.youngest_rev
            project_last_author = lastChange.author
            project_last_message = lastChange.message
            project_laste_date = lastChange.date
            project_date_diff = time.time() - lastChange.date
            project_message_diff = repository_diff_message(lastChange)
        # in the case of the repository has not yet been modified
        except:
            project_last_author = ""
            project_last_message = "This repository has not yet been modified"
            project_laste_date = time.time()
            project_name = env.project_name
            project_href = config.trac_href + dir
            project_description = env.project_description
            project_youngest_rev = "0"
            project_date_diff = time.time() - time.time()
            project_message_diff = "0 minutes"
        # DEMO
        demo = False
        if path.exists("%s/%s" % (config.demo_dir, dir)):
            demo = True
        # TARBALL
        tarball = False
        if path.exists("%s/%s" % (config.archives_dir, dir)):
            tarball = True
        # a project
        proj = {'name' : project_name,
                'href' : project_href,
                'description' : project_description,
                'activity' : {
                    'lastrev' : project_youngest_rev,
                    'lastauthor' : project_last_author,
                    'lastdate' : project_message_diff,
                    'lastmessage' : project_last_message,
                    'datediff' : project_date_diff
                },
                'demo' : {
                    'enable' : demo,
                    'href' : "%s/%s" % (config.demo_href, dir)
                },
                'tarball' : {
                    'enable' : tarball,
                    'href' : "%s/%s" % (config.archives_href, dir)
                }
               }
        projects.append(proj)
    # sort projects
    if req.uri == config.forge_href+"/a":
        projects.sort(lambda x,y: cmp(x['name'], y['name']))
        sort = "a"
    elif req.uri == config.forge_href+"/z":
        projects.sort(lambda x,y: cmp(y['name'], x['name']))
        sort = "z"
    else:
        projects.sort(lambda x, y: cmp(x['activity']['datediff'], y['activity']['datediff']))
        sort = "b"
    # apply template
    template = load_template(config, "projects.html")
    context = {
        'projects' : projects,
        'sort' : sort,
        'forge_href' : config.forge_href,
        'media_href' : config.media_href,
        'debug' : req.uri
    }
    return template.render(context)


