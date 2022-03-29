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


from flask import Response
from testsuite import ActiniaTestCase
from actinia_core.core.common.app import URL_PREFIX


class StacInstanceEndpointTest(ActiniaTestCase):
    def test_e_get_instance_id(self):
        """Test if get an instance responds"""

        stac_instance_id = "defaultStac"
        resp = self.app.get(
            f"{URL_PREFIX}/stac/instances/" + stac_instance_id,
            headers=self.user_auth_header,
        )
        assert type(resp) is Response
        assert resp.status_code == 200
        assert hasattr(resp, "json")

    def test_f_get_error_instance_id(self):
        """Test if get an instance responds"""

        stac_instance_id = "STAC-NoExist-"
        resp = self.app.get(
            f"{URL_PREFIX}/stac/instances/" + stac_instance_id,
            headers=self.user_auth_header,
        )
        assert type(resp) is Response
        assert resp.status_code == 400
        assert hasattr(resp, "json")

    def test_g_delete_instance_id(self):
        """Test if delete an instance responds"""

        stac_instance_id = "STACtestinstance"
        resp = self.app.delete(
            f"{URL_PREFIX}/stac/instances/" + stac_instance_id,
            headers=self.user_auth_header,
        )

        assert type(resp) is Response
        assert resp.status_code == 200
        assert hasattr(resp, "json")

    def test_h_delete_error_instance_id(self):
        """Test if delete an instance responds"""

        stac_instance_id = "STAC-NoExist-"
        resp = self.app.delete(
            f"{URL_PREFIX}/stac/instances/" + stac_instance_id,
            headers=self.user_auth_header,
        )

        assert type(resp) is Response
        assert resp.status_code == 400
        assert hasattr(resp, "json")
