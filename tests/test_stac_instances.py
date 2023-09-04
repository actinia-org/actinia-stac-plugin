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

from testsuite import ActiniaTestCase
from actinia_api import URL_PREFIX


class StacInstancesEndpointTest(ActiniaTestCase):
    def test_b_get_instances(self):
        """Test if get instances responds"""
        resp = self.app.get(
            f"{URL_PREFIX}/stac/instances", headers=self.user_auth_header
        )

        assert resp.status_code == 200
        assert hasattr(resp, "json")

    def test_c_post_error_instances(self):
        """Test if add a new instance responds"""

        respStatusCode = 400

        instance_add_body = {"stac_instance": ""}

        resp = self.app.post(
            f"{URL_PREFIX}/stac/instances",
            headers=self.user_auth_header,
            data=json.dumps(instance_add_body),
            content_type="application/json",
        )

        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")

    def test_d_post_instances(self):
        """Test if add a new instance responds"""

        respStatusCode = 200

        instance_add_body = {"stac_instance_id": "STACtestinstance"}

        resp = self.app.post(
            f"{URL_PREFIX}/stac/instances",
            headers=self.user_auth_header,
            data=json.dumps(instance_add_body),
            content_type="application/json",
        )

        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")

    def test_e_get_instance_id(self):
        """Test if get an instance responds"""

        stac_instance_id = "STACtestinstance"
        resp = self.app.get(
            f"{URL_PREFIX}/stac/instances/" + stac_instance_id,
            headers=self.user_auth_header,
        )
        assert resp.status_code == 200
        assert hasattr(resp, "json")

    def test_f_get_error_instance_id(self):
        """Test if get an instance responds"""

        stac_instance_id = "STAC-NoExist-"
        resp = self.app.get(
            f"{URL_PREFIX}/stac/instances/" + stac_instance_id,
            headers=self.user_auth_header,
        )
        assert resp.status_code == 400
        assert hasattr(resp, "json")

    def test_g_delete_instance_id(self):
        """Test if delete an instance responds"""

        stac_instance_id = "STACtestinstance"
        resp = self.app.delete(
            f"{URL_PREFIX}/stac/instances/" + stac_instance_id,
            headers=self.user_auth_header,
        )

        assert resp.status_code == 200
        assert hasattr(resp, "json")

    def test_h_delete_error_instance_id(self):
        """Test if delete an instance responds"""

        stac_instance_id = "STAC-NoExist-"
        resp = self.app.delete(
            f"{URL_PREFIX}/stac/instances/" + stac_instance_id,
            headers=self.user_auth_header,
        )

        assert resp.status_code == 400
        assert hasattr(resp, "json")
