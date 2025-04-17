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


staccollection_id_get_docs = {
    "tags": ["STAC"],
    "description": "Get the STAC collection with the id given "
    "Minimum required user role: user.",
    "parameters": [
        {
            "in": "path",
            "name": "stac_collection_id",
            "type": "string",
            "description": "the STAC collection id of the collection to be obtained",
            "required": True,
        }
    ],
    "responses": {
        "200": {"description": "This response returns a STAC collection"},
        "400": {
            "description": "This response returns a detail error message",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "detailed message",
                        "example": "Please check the collection id provide",
                    }
                },
            },
        },
    },
}

staccollection_id_delete_docs = {
    "tags": ["STAC"],
    "description": "Delete a new STAC collection to the user instance",
    "parameters": [
        {
            "in": "path",
            "name": "stac_collection_id",
            "type": "string",
            "description": "the STAC collection id of the collection to be deleted",
            "required": True,
        }
    ],
    "responses": {
        "200": {
            "description": "This response returns a message with the STAC collection successfully deleted"
        },
        "400": {
            "description": "This response returns a detail error message",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "detailed message",
                        "example": "stac_collection_id does not match the pattern "
                        + "stac.<stac_instance_id>.rastercube.<stac_collection_id",
                    }
                },
            },
        },
    },
}
