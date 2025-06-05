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

This code shows the transactions valids for STAC collections id endpoints
"""
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"
__maintainer__ = "__mundialis__"


from actinia_rest_lib.resource_base import ResourceBase
from flask import make_response

from flask_restful_swagger_2 import swagger

from actinia_stac_plugin.core.stac_collection_id import (
    callStacCollection,
    deleteStacCollection,
)

from actinia_stac_plugin.apidocs import stac_collections_id_docs


class StacCollections(ResourceBase):
    """Get the Collections STAC"""

    def __init__(self):
        ResourceBase.__init__(self)

    @swagger.doc(stac_collections_id_docs.staccollection_id_get_docs)
    def get(self, stac_collection_id: str):
        """Get a list of specified Collection."""

        collection_list = callStacCollection(stac_collection_id)

        return make_response(collection_list, 200)

    @swagger.doc(stac_collections_id_docs.staccollection_id_delete_docs)
    def delete(self, stac_collection_id: str):
        """
        This function deletes the STAC collection with the given id.
        Arg:
            - ID - ID/Name given to the STAC Collection you want to delete
        """
        try:
            stac_instance_id = stac_collection_id.split(".")[1]
        except Exception:
            message = (
                "stac_collection_id does not match the pattern "
                "stac.<stac_instance_id>.rastercube.<stac_collection_id"
            )

            return make_response(message, 400)

        deleted_stac = deleteStacCollection(
            stac_instance_id, stac_collection_id
        )

        return make_response(deleted_stac, 200)
