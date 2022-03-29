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


Test code for STAC module api endpoints
"""
__author__ = "Jorge Herrera"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"

import json

from flask import Response
from testsuite import ActiniaTestCase
from actinia_core.core.common.app import URL_PREFIX


class StacCollectionsEndpointTest(ActiniaTestCase):
    def test_i_get_collections(self):
        """Test if get collections responds"""
        resp = self.app.get(
            f"{URL_PREFIX}/stac/collections", headers=self.user_auth_header
        )

        assert type(resp) is Response

    def test_k_post_collections(self):
        """Test if add a new collection responds"""

        respStatusCode = 200

        collection_add_body = {
            "stac_instance_id": "defaultStac",
            "stac_url": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a",
        }

        resp = self.app.post(
            f"{URL_PREFIX}/stac/collections",
            headers=self.user_auth_header,
            data=json.dumps(collection_add_body),
            content_type="application/json",
        )

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")

    def test_l_post_error_collections(self):
        """Test if add a new collection responds"""

        respStatusCode = 400

        collection_add_body = {
            "stac_instance_id": "STACtestNoInInstance",
            "stac_url": "https://earth-search.aws.element84.com/v0",
        }

        resp = self.app.post(
            f"{URL_PREFIX}/stac/collections",
            headers=self.user_auth_header,
            data=json.dumps(collection_add_body),
            content_type="application/json",
        )

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
