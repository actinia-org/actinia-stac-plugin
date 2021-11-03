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

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


stacinstance_id_get_docs = {
    "tags": ["STAC"],
    "description": "Get the Instance with the ID Given "
    "Minimum required user role: user.",
    "parameters": [
        {
            "in": "path",
            "name": "stac_instance_id",
            "type": "string",
            "description": "the Instance ID of the collection to be obtained",
            "required": True,
        }
    ],
    "responses": {
        "200": {"description": "This response returns a Instance with its collections"}
    },
}

stacinstance_id_delete_docs = {
    "tags": ["STAC"],
    "description": "Delete an Instance",
    "parameters": [
        {
            "in": "path",
            "name": "stac_instance_id",
            "type": "string",
            "description": "the Instance ID to be deleted (All collections will be removed)",
            "required": True,
        }
    ],
    "responses": {
        "200": {
            "description": "This response returns a message with the "
            + "Instance and the STAC collections deleted"
        }
    },
}
