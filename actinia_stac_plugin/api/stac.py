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

__license__ = "GPLv3"
__author__ = "Anika Bettge, Carmen Tawalika"
__copyright__ = "Copyright 2019, mundialis"
__maintainer__ = "Anika Bettge, Carmen Tawalika"


from flask import jsonify, make_response, request
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
        """Get a list of Instances and Genera Information."""
        stac_info = createStacItemList()

        return make_response(stac_info, 200)

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
        stac_deleted = deleteStac(json)

        return make_response(stac_deleted, 200)


class StacCollections(ResourceBase):
    """
    Get the STAC Collections
    """

    def __init__(self):
        ResourceBase.__init__(self)

    def get(self, stac_collection_id):
        """Get a Collection stored based in stac_collection_id"""

        stac_collection = callStacCollection(stac_collection_id)
        return make_response(stac_collection, 200)


class StacCollectionList(ResourceBase):
    """
    Get the STAC Collections list
    """

    def __init__(self):
        ResourceBase.__init__(self)

    def get(self):
        """
        Get a list of all stac collections stored:
            - OpenEo specifications
            - All retrivals from each collections stored
        """
        stac_collections_list = StacCollectionsList()

        return make_response(stac_collections_list, 200)


class StacInstances(ResourceBase):
    """
    Get the Intance
    """
    def __init__(self):
        ResourceBase.__init__(self)

    def get(self, stac_instance_id):
        """
        Get a Instance based on stac_instance_id
            - Based on stac_instance_id
            - Retrieve List of collection with:
                - href: relative reference URL for ACTINIA
                - root: URL linked to the STAC Collection
        """

        stac_instance = getInstance(stac_instance_id)

        return make_response(stac_instance, 200)


class StacInstanceList(ResourceBase):
    """
    Get the Instances list
    """
    def __init__(self):
        ResourceBase.__init__(self)

    def get(self):
        """
        Get a Instance List
            - Retrieve List of Instances for the user with:
                - stac_instances_id: relative reference URL for ACTINIA
                - path: convention name to reach any collecion in the instance
        """
        module_list = createStacItemList()

        return make_response(module_list, 200)
