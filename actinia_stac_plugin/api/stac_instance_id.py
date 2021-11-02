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

from actinia_stac_plugin.core.stac_instance_id import getInstance, deleteStacInstance

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
            This function delete the STAC Catalog stored before on ID basis.
            Arg:
                - ID - ID/Name given to the STAC Catalog you want to delete
        """

        deleted_stac = deleteStacInstance(stac_instance_id)

        return make_response(deleted_stac, 200)
