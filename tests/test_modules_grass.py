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


# import unittest

from flask import Response

from actinia_core.core.common.app import URL_PREFIX

from testsuite import ActiniaTestCase, compare_module_to_file


someGrassModules = ['r.slope.aspect', 'importer', 'exporter']


class GmodulesTest(ActiniaTestCase):

    # @unittest.skip("demonstrating skipping")
    def test_list_modules_get(self):
        """Test HTTP GET /grass_modules"""
        global someGrassModules

        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + '/grass_modules',
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

        assert len(resp.json['processes']) > 500
        assert 'categories' in resp.json['processes'][0]
        assert 'description' in resp.json['processes'][0]
        assert 'id' in resp.json['processes'][0]

        respModules = [i['id'] for i in resp.json['processes']]

        for i in someGrassModules:
            assert i in respModules

    def test_filter_list_modules_get(self):
        """Test HTTP GET /grass_modules with filter"""
        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + '/grass_modules?category=slope',
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons
        assert len(resp.json['processes']) == 2

    def test_filter_list_modules_get_2(self):
        """Test HTTP GET /grass_modules with filter"""
        respStatusCode = 200
        url_path = '/grass_modules?record=full&family=ps'
        resp = self.app.get(URL_PREFIX + url_path,
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons
        assert len(resp.json['processes']) == 1
        assert resp.json['processes'][0]['categories'] != 0
        assert resp.json['processes'][0]['parameters'] != 0

    def test_filter_list_modules_get_3(self):
        """Test HTTP GET /grass_modules with filter"""
        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + '/grass_modules?family=test',
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons
        assert len(resp.json['processes']) == 2
        assert resp.json['processes'][0]['categories'] != 0
        assert hasattr(resp.json['processes'][0], 'parameters') is False


for i in someGrassModules:
    """Test HTTP GET /grass_modules/<module> for GRASS GIS modules in loop
    for all examples in someGrassModules above and compares response to file
    """
    # create method for every grass-module to have a better overview in
    # test summary
    def_name = "test_describe_module_get_" + i
    compare_module_to_file.__defaults__ = ('grass_modules', i,)
    setattr(GmodulesTest, def_name, compare_module_to_file)
