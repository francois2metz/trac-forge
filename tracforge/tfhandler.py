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

from tracforge.config import Config
from tracforge.projects import *

class TfHandler:
    """ Gerneric handler to interface between specific handlers and tracforge """ 

    def __init__(self, request):
        self.request = request
        self.config = Config(self.request.config_file)
        forge_href_len= len(self.config.forge_href)
        # TODO: test if uri is smaller than forge_href_len
        relative_uri = self.request.uri[forge_href_len+1:]
        self.request.setParam("relativuri",relative_uri)
        self.uri = relative_uri.split("/")

    def handler(self):
        """
        main function of the generic handler, it is as well the role
        of the controller.
        """
        
        if len(self.uri) >= 1 :
            mainPage = self.uri[0]
        else :
            mainPage = ""

        # Admin part
        if len(self.uri) >= 1 and  mainPage == "admin":
            self.admin_handler(self.uri)
        # Project display
        elif mainPage == "a" or mainPage == "z" or mainPage == "":
            self.request.setParam("sort", mainPage)
            self.status, self.content = view_index(self.request, self.config)
        # File not found
        else:
            self.status, self.content = view_404(self.request, self.config)
        return self.status, self.content

    def admin_handler(self, uri) :
        """
        Admin handler part.
        This is actually only for testing the admin function.
        """
        if len(self.uri) >= 4 and self.uri[1] == "projects":
            action = uri[2]
            projectname = uri[3]
            if action == "create" or action == "delete" :
                self.status, self.content = view_admin_projects(self.request, self.config, action, projectname)
            else:
                self.status, self.content = view_admin(self.request, self.config)
        else:
            self.status, self.content = view_admin(self.request, self.config)
        
        
