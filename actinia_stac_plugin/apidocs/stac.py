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


Documentation objects for GRASS modules and actinia modules api endpoints
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "GPLv3"


import copy

from actinia_stac_plugin.model.responseModels import SimpleStatusCodeResponseModel

from actinia_stac_plugin.model.modules import Module, ModuleList


null = "null"


listModules_get_docs = {
    "tags": ["Module Viewer"],
    "description": "Get a list of modules. " "Minimum required user role: user.",
    "parameters": [
        {
            "in": "path",
            "name": "tag",
            "type": "string",
            "description": "Filter for categories",
        },
        {
            "in": "path",
            "name": "category",
            "type": "string",
            "description": "Another filter for categories",
        },
        {
            "in": "path",
            "name": "family",
            "type": "string",
            "description": "Type of GRASS GIS module",
            "enum": ["d", "db", "g", "i", "m", "ps", "r", "r3", "t", "test", "v"],
        },
        {
            "in": "path",
            "name": "record",
            "type": "string",
            "description": "If set to 'full', all information about the "
            "returned modules are given like in the single "
            "module description. Depending on active cache, "
            "this response might run into a timeout. A filter "
            "can prevent this.",
        },
    ],
    "responses": {
        "200": {
            "description": "This response returns a list of module names and "
            "the status.",
            "schema": ModuleList,
        },
        "400": {
            "description": "The error message and a detailed log why listing "
            "of modules did not succeeded",
            "schema": SimpleStatusCodeResponseModel,
        },
    },
}

describeModule_get_docs = {
    "tags": ["Module Viewer"],
    "parameters": [
        {
            "in": "path",
            "name": "module",
            "type": "string",
            "description": "The name of a module",
            "required": True,
        }
    ],
    "description": "Get the description of a module. "
    "Minimum required user role: user."
    "Can be also used to reload cache for a certain module"
    "for the full module description in listModules.",
    "responses": {
        "200": {
            "description": "This response returns a description of a module.",
            "schema": Module,
        },
        "400": {
            "description": "The error message and a detailed log why "
            "describing modules did not succeeded",
            "schema": SimpleStatusCodeResponseModel,
        },
    },
}


describeActiniaModule_get_docs = copy.deepcopy(describeModule_get_docs)
describeActiniaModule_get_docs["parameters"][0]["name"] = "actiniamodule"

describeGrassModule_get_docs = copy.deepcopy(describeModule_get_docs)
describeGrassModule_get_docs["parameters"][0]["name"] = "grassmodule"
