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

from jinja import Environment, PackageLoader, FileSystemLoader
from tracforge.tracenvadmin import Tracenvadmin
from time import time
from os import path as ospath
from tracenv import *

def load_template(config, templateName):
    """"Charge un template"""
    if config.template_dir == "":
        environment = Environment(loader=PackageLoader('tracforge', 'templates'))
    else:
        environment = Environment(loader=FileSystemLoader(config.template_dir))
    return environment.get_template(templateName)

def repository_diff_message(last_change_date):
    date_diff = time() - last_change_date
    nbYears = date_diff / (60 * 60 * 24 * 30 * 12)
    if nbYears == 1:
        message_diff = " plus de " + str(int(nbYears)) + " an"
    elif nbYears >= 1:
        message_diff = " plus de " + str(int(nbYears)) + " ans"
    else:
        nbMonths = date_diff / (60 * 60 * 24 * 30)
        if nbMonths > 1:
            message_diff = str(int(nbMonths)) + " mois"
        else:
            nbDays = date_diff / (60 * 60 * 24)
            if nbDays > 1:
                message_diff = str(int(nbDays)) + " jours "
            else:
                nbHours = date_diff / (60 * 60)
                if nbHours > 1:
                    message_diff = "plus de " + str(int(nbHours)) + " heures"
                else:
                    message_diff = "moins d'une heure"
    return message_diff


### VIEWS 

def view_admin(request, config):
    tmpl = load_template(config, "admin.html")
    context = {
        'users' : [{'name' : 'toto'}],
        'forge_href' : config.forge_href,
        'media_href' : config.media_href
    }
    return 200, tmpl.render(context)

def view_admin_projects(request, config, action, name):
    env_trac = Tracenvadmin()
    if action == "create":
    	env_trac.create_env(config, name)
    elif action == "delete":
    	env_trac.delete_env(config, name)
    tmpl = load_template(config, "admin.html")
    context = {
        'users' : [{'name' : 'toto'}],
        'forge_href' : config.forge_href,
        'media_href' : config.media_href
    }
    return 200, tmpl.render(context)

def view_404(request, config):
    """Page d'erreur 404"""
    tmpl = load_template(config, "404.html")
    context = {
        'forge_href' : config.forge_href,
        'media_href' : config.media_href
	}
    return 404, tmpl.render(context)

def view_index(request, config):
    """Index des projets"""
    tracProjects = TracProjects(config.trac_dir, config.trac_href)
    projects = []
    for project in tracProjects:
        date_message = repository_diff_message(project.get_last_date())
        # DEMO
        demo = False
        if ospath.exists("%s/%s" % (config.demo_dir, dir)):
            demo = True
        # TARBALL
        tarball = False
        if ospath.exists("%s/%s" % (config.archives_dir, dir)):
            tarball = True
        # a project
        proj = {'name' : project.get_name(),
                'href' : project.get_href(),
                'description' : project.get_description(),
                'activity' : {
                    'lastrev' : project.get_last_rev(),
                    'lastauthor' : project.get_last_author(),
                    'lastdate' : date_message,
                    'lastmessage' : project.get_last_message(),
                    'datediff' : time() - project.get_last_date()
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
    sort = request.getParam("sort")
    if sort == "a":
        projects.sort(lambda x,y: cmp(x['name'], y['name']))
        sort = "a"
    elif sort == "z":
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
        'debug' : ""
    }
    return 200, template.render(context)


