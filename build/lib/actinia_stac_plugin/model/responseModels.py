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


Common api methods
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from flask_restful_swagger_2 import Schema


class SimpleStatusCodeResponseModel(Schema):
    """Simple response schema to inform about status.

    """
    type = 'object'
    properties = {
        'status': {
            'type': 'number',
            'description': 'The status code of the request.'
        },
        'message': {
            'type': 'string',
            'description': 'A short message to describes the status'
        }
    }
    required = ["status", "message"]


simpleResponseExample = SimpleStatusCodeResponseModel(
    status=200, message="success")
SimpleStatusCodeResponseModel.example = simpleResponseExample
