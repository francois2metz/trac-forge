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

class TfRequest:

    def __init__(self, uri, config_file_path):
        self.uri = uri
        self.content = ""
        self.config_file = config_file_path
        self.status = 200
        self.params = {}

    def setParam(self, param, val):
        self.params[param] = val

    def getParam(self, param):
        return self.params[param]

