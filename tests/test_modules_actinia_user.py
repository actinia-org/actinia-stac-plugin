#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2021 mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Test Module Lists and Self-Description
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"

import json
from flask import Response

from actinia_core.core.common.app import URL_PREFIX

from testsuite import ActiniaTestCase, import_user_template, \
     delete_user_template

someActiniaModules = [
    'add_enumeration', 'default_value', 'nested_modules_test',
    'point_in_polygon', 'slope_aspect', 'vector_area', 'index_NDVI']


class ActiniaModulesTest(ActiniaTestCase):

    def test_read_user_module_get(self):
        """Test HTTP GET /actinia_modules/<module> for redis based templates"""
        import_user_template(self, 'user_point_in_polygon')

        respStatusCode = 200
        json_path = 'tests/resources/actinia_modules/point_in_polygon.json'
        url_path = '/actinia_modules/user_point_in_polygon'

        with open(json_path) as file:
            expectedResp = json.load(file)
        expectedResp['id'] = 'user_point_in_polygon'
        curr = expectedResp['categories']
        new = [s.replace('global-template', 'user-template') for s in curr]
        expectedResp['categories'] = new

        resp = self.app.get(URL_PREFIX + url_path,
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')
        assert resp.json == expectedResp

        delete_user_template(self, 'user_point_in_polygon')
