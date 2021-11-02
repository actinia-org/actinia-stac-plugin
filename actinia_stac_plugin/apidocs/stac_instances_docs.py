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
Documentation objects for GRASS modules and actinia modules api endpoints
"""

__author__ = "Jorge Herrera"
__copyright__ = "2019-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"

from actinia_stac_plugin.apidocs.schemas import AddInstaceModel

null = "null"


stacinstances_get_docs = {
    "tags": ["STAC"],
    "description": "Get a list of STAC Instances. " "Minimum required user role: user.",
    "parameters": [],
    "responses": {
        "200": {"description": "This response returns a list of STAC Instances"}
    },
}

stacinstances_post_docs = {
    "tags": ["STAC"],
    "description": "Add a new STAC instances to the user",
    "parameters": [
        {
            "in": "body",
            "name": "Adding Instance",
            "type": "object",
            "schema": AddInstaceModel,
            "description": "the Instance ID where the Collection will be storaged",
            "required": True,
        }
    ],
    "responses": {
        "200": {
            "description": "This response returns a message with the Instance successfully added"
        }
    },
}