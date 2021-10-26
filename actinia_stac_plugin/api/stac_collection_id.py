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

from actinia_stac_plugin.core.stac_collection_id import callStacCollection


class StacCollections(ResourceBase):
    """Get the Collections STAC"""

    def __init__(self):
        ResourceBase.__init__(self)

    # @swagger.doc(modules.listModules_get_docs)
    def get(self, stac_collection_id):
        """Get a list of specified Collection."""

        collection_list = callStacCollection(stac_collection_id)
        return make_response(collection_list, 200)
