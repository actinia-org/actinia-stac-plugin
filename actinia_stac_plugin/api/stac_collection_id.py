#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018-2021 mundialis GmbH & Co. KG
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
STAC plugin
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "Copyright 2019-2021, mundialis"
__maintainer__ = "__mundialis__"


from actinia_core.rest.resource_base import ResourceBase
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
        stac_instance_id = stac_collection_id.split(".")[1]

        deleted_stac = deleteStacCollection(stac_instance_id, stac_collection_id)

        return make_response(deleted_stac, 200)
