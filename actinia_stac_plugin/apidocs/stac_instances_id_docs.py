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


Documentation for STAC module api endpoints
"""

__author__ = "Jorge Herrera"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "GPLv3"


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
