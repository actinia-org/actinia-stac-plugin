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


from flask import Response

from actinia_core.core.common.app import URL_PREFIX

from testsuite import ActiniaTestCase, compare_module_to_file


someActiniaModules = [
    'add_enumeration', 'default_value', 'nested_modules_test',
    'point_in_polygon', 'slope_aspect', 'vector_area', 'index_NDVI']


class ActiniaModulesTest(ActiniaTestCase):

    def test_list_modules_get(self):
        """Test HTTP GET /actinia_modules"""
        global someActiniaModules

        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + '/actinia_modules')

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')
        assert 'actinia-module' in resp.json['processes'][0]['categories']

        respModules = [i['id'] for i in resp.json['processes']]

        for i in someActiniaModules:
            assert i in respModules

    def test_filter_list_modules_get(self):
        """Test HTTP GET /actinia_modules with filter"""
        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + '/actinia_modules?tag=global')

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')
        assert len(resp.json['processes']) == 7

    def test_describe_modules_not_found(self):
        """Test HTTP GET /actinia_modules/<not-existing-module>"""
        respStatusCode = 404
        resp = self.app.get(URL_PREFIX + '/actinia_modules/not_exist',
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')


for i in someActiniaModules:
    """Test HTTP GET /actinia_modules/<module> for file based templates in loop
    for all examples in someActiniaModules above and compares response to file
    """
    # create method for every actinia-module to have a better overview in
    # test summary
    def_name = "test_describe_process_chain_template_get_" + i
    compare_module_to_file.__defaults__ = ('actinia_modules', i,)
    setattr(ActiniaModulesTest, def_name, compare_module_to_file)
