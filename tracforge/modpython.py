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

from tfhandler import *
from tfrequest import *
from mod_python import apache
 
def handler(req):
    """ Specific handler for ModPython """
    req.content_type = 'text/html; charset=utf-8'
    request = TfRequest(req.uri, req.get_options()['ForgeConfig'])
    # for every parameters in POST/GET push them with request.setParam(name,val)
    tfhandler = TfHandler(request)
    req.status, content = tfhandler.handler()
    req.write(content.encode('utf-8'))
    return apache.OK

