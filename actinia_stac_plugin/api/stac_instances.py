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
from flask import make_response, request

from actinia_stac_plugin.core.stac_instances import (
    addInstance,
    createStacItemList,
    deleteStac,
)


class StacInstanceList(ResourceBase):
    def __init__(self):
        ResourceBase.__init__(self)

    def get(self):
        """Get a list of all instances."""
        instances_list = createStacItemList()

        return make_response(instances_list, 200)

    def post(self):
        """
        Add a new stac to the user collection
        """

        parameters = request.get_json(force=True)
        new_stac = addInstance(parameters)

        return make_response(new_stac, 200)

    def delete(self):
        """
            This function delete the STAC Catalog stored before on ID basis.
            Arg:
                - ID - ID/Name given to the STAC Catalog you want to delete
        """

        stac_instance_id = request.get_json(force=True)
        deleted_stac = deleteStac(stac_instance_id)

        return make_response(deleted_stac, 200)
