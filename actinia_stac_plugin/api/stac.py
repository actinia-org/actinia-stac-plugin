#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2022 mundialis GmbH & Co. KG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

This code shows the transactions valids for STAC endpoint
"""
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"
__maintainer__ = "__mundialis__"


from actinia_core.rest.base.resource_base import ResourceBase
from flask import make_response

from flask_restful_swagger_2 import swagger

from actinia_stac_plugin.core.stac import createStacItemList

from actinia_stac_plugin.apidocs import stac


class Stac(ResourceBase):
    """List and Add STAC options"""

    def __init__(self):
        ResourceBase.__init__(self)

    @swagger.doc(stac.stac_get_docs)
    def get(self):
        """Get a list of instances and its notation."""
        instances_list = createStacItemList()

        return make_response(instances_list, 200)
