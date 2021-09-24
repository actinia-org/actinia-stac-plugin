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
__author__ = "Anika Bettge, Carmen Tawalika"
__copyright__ = "Copyright 2019, mundialis"
__maintainer__ = "Anika Bettge, Carmen Tawalika"


from flask import jsonify, make_response, request
from flask_restful_swagger_2 import swagger
from actinia_core.rest.resource_base import ResourceBase
from actinia_stac_plugin.core.stac import createStacList
from actinia_stac_plugin.core.stac import addStacValidator
from actinia_stac_plugin.core.stac import callStacCollection
from actinia_stac_plugin.core.stac import deleteStacCollection

class Stac(ResourceBase):
    """List and Add STAC options
    """
    def __init__(self):
        ResourceBase.__init__(self)

    #@swagger.doc(modules.listModules_get_docs)
    def get(self):
        """Get a list of all GRASS GIS modules.
        """
        module_list = createStacList()
        
        return make_response(module_list, 200)

    def post(self):
        """
            Add a new stac to the user catalog
        """
        
        json = request.get_json(force=True)
        new_stac = addStacValidator(json)

        return make_response(new_stac,200)

    def delete(self):
        """
            This function delete the STAC Catalog stored before on ID basis.
            Arg:
                - ID - ID/Name given to the STAC Catalog you want to delete
        """

        json = request.get_json(force=True)
        deleted_stac = deleteStacCollection(json)

        return make_response(deleted_stac,200)

class StacCollecions(ResourceBase):
    """Get the Catalog STAC
    """

    def __init__(self):
        ResourceBase.__init__(self)

    #@swagger.doc(modules.listModules_get_docs)
    def get(self, collection_id):
        """Get a list of all GRASS GIS modules.
        """

        module_list = callStacCollection(collection_id)

        return make_response(module_list, 200)


