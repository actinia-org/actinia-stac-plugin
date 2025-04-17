#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2022 mundialis GmbH & Co. KG

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
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"

stacinstances_get_docs = {
    "tags": ["STAC"],
    "description": "Get a list of STAC instances. "
    "Minimum required user role: user.",
    "parameters": [],
    "responses": {
        "200": {
            "description": "This response returns a list of STAC instances"
        }
    },
}

stacinstances_post_docs = {
    "tags": ["STAC"],
    "description": "Add a new STAC instances to the user",
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "type": "object",
            "schema": {
                "type": "object",
                "properties": {
                    "stac_instance_id": {
                        "type": "string",
                        "description": "name of the instance id to create",
                        "example": "ProjectIntance",
                    }
                },
            },
            "description": "the instance id where the collection will be stored",
            "required": True,
        }
    ],
    "responses": {
        "200": {
            "description": "This response returns a message with the instance successfully added"
        },
        "400": {
            "description": "This response returns a detail error message",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "detailed message",
                        "example": "Please check the ID given (no spaces or undercore characters)",
                    }
                },
            },
        },
    },
}
