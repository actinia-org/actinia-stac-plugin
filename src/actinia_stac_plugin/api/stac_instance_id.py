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

This code shows the transactions valids for STAC instance id endpoint
"""
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"
__maintainer__ = "__mundialis__"


from actinia_rest_lib.resource_base import ResourceBase
from flask import make_response

from flask_restful_swagger_2 import swagger

from actinia_stac_plugin.core.stac_instance_id import (
    getInstance,
    deleteStacInstance,
)

from actinia_stac_plugin.apidocs import stac_instances_id_docs


class StacInstances(ResourceBase):
    def __init__(self):
        ResourceBase.__init__(self)

    @swagger.doc(stac_instances_id_docs.stacinstance_id_get_docs)
    def get(self, stac_instance_id: str):
        """Get a list of collection that are inside a instance and its notation."""
        instance = getInstance(stac_instance_id)

        return make_response(instance, 200)

    @swagger.doc(stac_instances_id_docs.stacinstance_id_delete_docs)
    def delete(self, stac_instance_id: str):
        """
        This function delete the STAC Collection stored before on ID basis.
        Arg:
            - ID - ID/Name given to the STAC Collection you want to delete
        """

        deleted_stac = deleteStacInstance(stac_instance_id)

        message = {
            "message": "The instance --"
            + deleted_stac
            + "-- was deleted with all the collections stored inside"
        }

        return make_response(message, 200)
