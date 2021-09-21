#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2019-present mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Model classes for grassmodule and process chain template object
"""

__author__ = "Anika Bettge, Carmen Tawalika"
__copyright__ = "2019-present mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


import os
import json

from flask_restful_swagger_2 import Schema


script_dir = os.path.dirname(os.path.abspath(__file__))
rel_path = "../apidocs/examples/gm_describemodule_get_example_v_random.json"
abs_file_path = os.path.join(script_dir, rel_path)
with open(abs_file_path) as jsonfile:
    describemodule_get_docs_example = json.load(jsonfile)


class ModuleParameterSchema(Schema):
    """Schema property for Parameter
    TODO: add  {"type": "array", "items": {"type": "string"}}
    """

    type = 'object'
    properties = {
        'type': {
            'type': 'string',
            'description': ''
        },
        'subtype': {
            'type': 'string',
            'description': ''
        },
        'enum': {
            'type': 'array',
            'items': {
                'type': 'string'
            },
            'description': ''
        }
    }
    description = 'A schema object according to the specification of JSON '
    ' Schema draft-07. Additional values for format are defined '
    ' centrally in the API documentation, e.g. bbox or crs. '
    ' Callback parameters are defined with the custom schema '
    ' keyword parameters.'


class ModuleParameter(Schema):
    """Parameters from Module
    """

    type = 'object'
    properties = {
        'name': {
            'type': 'string',
            'description': 'A unique name for the parameter. '
        },
        'description': {
            'type': 'string',
            'description': 'Detailed description to fully explain the entity.'
        },
        'optional': {
            'type': 'boolean',
            'description': 'Determines whether this parameter is mandatory. '
                           ' Default: true'
        },
        'default': {
            'type': 'string',
            'description': 'The default value for this parameter.'
        },
        'schema': ModuleParameterSchema
        # 'comment': {
        #     'type': 'string',
        #     'description': 'Comment for parameter.'
        # }
    }
    description = 'A list of parameters that are applicable for this process.'
    required = ["description", "schema", "name"]


class ModuleReturns(ModuleParameter):
    properties = ModuleParameter.properties
    required = ModuleParameter.required
    type = ModuleParameter.type
    description = "The data that is returned from this process."


class ModuleImportDescription(ModuleParameter):
    properties = ModuleParameter.properties
    required = ModuleParameter.required
    type = ModuleParameter.type
    description = "Import parameters to import data for this process."


class ModuleExportDescription(ModuleParameter):
    properties = ModuleParameter.properties
    required = ModuleParameter.required
    type = ModuleParameter.type
    description = "Export parameters to export returned data from this process"


class Module(Schema):
    """Response schema for module
    """
    type = 'object'
    properties = {
        'id': {
            'type': 'string',
            'description': 'Unique identifier of the process. '
        },
        'summary': {
            'type': 'string',
            'description': 'A short summary of what the process does.'
        },
        'description': {
            'type': 'string',
            'description': 'Detailed description to fully explain the entity.'
        },
        'categories': {
            'type': 'array',
            'items': {'type': 'string'},
            'description': 'A list of categories. GRASS GIS addons have the '
                           'category "grass-module" and the actinia core '
                           'modules are identified with "actinia-module"'
        },
        'parameters': ModuleParameter,
        'returns': ModuleReturns,
        'import_descr': ModuleImportDescription,
        'export': ModuleExportDescription

    }
    example = describemodule_get_docs_example
    required = ["id", "description"]
    # required = ["id", "description", "parameters", "returns"]


class ModuleList(Schema):
    """Response schema for module lists
    The answer bases on openeo v0.4: https://open-eo.github.io/openeo-api/v
    /0.4.0/apireference/#tag/Process-Discovery/paths/~1processes/get
    Differences:
    * module name is set to id
    * keywords to categories
    * description is set to required description and not to optional summary
    """
    type = 'object'
    properties = {
        'status': {
            'type': 'string',
            'description': 'The status of the resource, values: accepted, '
                           'running, finished, terminated, error'
        },
        'processes': {
            'type': 'array',
            'items': Module,
            'description': 'The list of modules in GRASS GIS'
        }
    }
    example = {"processes": [{
        "id": "v.random",
        "description": "Generates random 2D/3D vector points.",
        "categories": ["vector", "sampling", "statistics", "random",
                       "point pattern", "stratified random sampling",
                       "level1"]}
    ], "status": "success"}
    required = ["status", "processes"]
