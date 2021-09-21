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


Test
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2018-2021, mundialis"


import pytest
import unittest
from pkg_resources import get_distribution, DistributionNotFound
from flask import Response

import actinia_stac_plugin
from testsuite import ActiniaTestCase


class AppTest(ActiniaTestCase):

    def test_app_running(self):
        """Test if app responds"""
        resp = self.app.get('/')
        assert type(resp) is Response

    # see endpoints.py why this is outcommented
    # def test_app_responding(self):
    #     respStatusCode = 200
    #     resp = self.app.get('/')
    #     assert resp.status_code == respStatusCode

    def test_app_static(self):
        """Test if index cannot be found (see above)"""
        respStatusCode = 404
        resp = self.app.get('/index.html')
        assert resp.status_code == respStatusCode


class InitTest(unittest.TestCase):

    def test_init(self):
        """Test if version can be detected"""
        # TODO: apply to __init__.py
        pkg_version = get_distribution('actinia_stac_plugin.wsgi').version
        assert actinia_stac_plugin.__version__ == pkg_version

        with pytest.raises(DistributionNotFound):
            v = get_distribution('false_distro_name').version
            assert v == 'unknown'
