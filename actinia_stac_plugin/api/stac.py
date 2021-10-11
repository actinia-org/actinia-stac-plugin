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
GRASS GIS module viewer
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "Copyright 2019-2021, mundialis"
__maintainer__ = "__mundialis__"


from flask import make_response, request
from actinia_core.rest.resource_base import ResourceBase
from actinia_stac_plugin.core.stac import createStacItemList
from actinia_stac_plugin.core.stac import addStacValidator
from actinia_stac_plugin.core.stac import callStacCollection
from actinia_stac_plugin.core.stac import deleteStac
from actinia_stac_plugin.core.stac import StacCollectionsList
from actinia_stac_plugin.core.stac import getInstance


class Stac(ResourceBase):
    """List and Add STAC options"""

    def __init__(self):
        ResourceBase.__init__(self)

    # @swagger.doc(modules.listModules_get_docs)
    def get(self):
        """Get a list of all GRASS GIS modules."""
        module_list = createStacItemList()

        return make_response(module_list, 200)

    def post(self):
        """
        Add a new stac to the user catalog
        """

        json = request.get_json(force=True)
        new_stac = addStacValidator(json)

        return make_response(new_stac, 200)

    def delete(self):
        """
        This function delete the STAC Catalog stored before on ID basis.
        Arg:
            - ID - ID/Name given to the STAC Catalog you want to delete
        """

        json = request.get_json(force=True)
        deleted_stac = deleteStac(json)

        return make_response(deleted_stac, 200)


class StacCollections(ResourceBase):
    """Get the Catalog STAC"""

    def __init__(self):
        ResourceBase.__init__(self)

    # @swagger.doc(modules.listModules_get_docs)
    def get(self, stac_collection_id):
        """Get a list of all GRASS GIS modules."""

        module_list = callStacCollection(stac_collection_id)
        return make_response(module_list, 200)


class StacCollectionList(ResourceBase):
    def __init__(self):
        ResourceBase.__init__(self)

    def get(self):
        """Get a list of all GRASS GIS modules."""
        module_list = StacCollectionsList()

        return make_response(module_list, 200)


class StacInstances(ResourceBase):
    def __init__(self):
        ResourceBase.__init__(self)

    def get(self, stac_instance_id):
        """Get a list of all GRASS GIS modules."""
        module_list = getInstance(stac_instance_id)

        return make_response(module_list, 200)


class StacInstanceList(ResourceBase):
    def __init__(self):
        ResourceBase.__init__(self)

    def get(self):
        """Get a list of all GRASS GIS modules."""
        module_list = createStacItemList()

        return make_response(module_list, 200)
