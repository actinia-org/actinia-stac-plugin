#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2021 mundialis GmbH & Co. KG

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


GRASS GIS module viewer
"""

__license__ = "GPLv3"
__author__ = "Anika Bettge, Carmen Tawalika"
__copyright__ = "Copyright 2019, mundialis"
__maintainer__ = "Anika Bettge, Carmen Tawalika"


from actinia_core.rest.resource_base import ResourceBase
from flask import make_response, request

from actinia_stac_plugin.core.stac import (
    StacCollectionsList,
    addStacValidator,
    callStacCollection,
    createStacItemList,
    deleteStac,
    getInstance,
)


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
