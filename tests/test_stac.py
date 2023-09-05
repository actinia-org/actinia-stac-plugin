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

from testsuite import ActiniaTestCase
from actinia_api import URL_PREFIX


class StacEndpointTest(ActiniaTestCase):
    def test_a_app_instances(self):
        """Test if app responds"""
        resp = self.app.get(
            f"{URL_PREFIX}/stac", headers=self.user_auth_header
        )

        assert resp.status_code == 200
        assert hasattr(resp, "json")
