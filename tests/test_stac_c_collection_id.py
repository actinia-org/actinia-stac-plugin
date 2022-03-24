#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2021 mundialis GmbH & Co. KG

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
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "GPLv3"


from flask import Response
from testsuite import ActiniaTestCase
from actinia_api import URL_PREFIX


class StacCollectionEndpointTest(ActiniaTestCase):
    def test_m_get_collection_id(self):
        """Test if get collection id responds"""

        stac_unique_id = "stac.defaultStac.rastercube.landsat-8-l1-c1"
        resp = self.app.get(
            f"{URL_PREFIX}/stac/collections/" + stac_unique_id,
            headers=self.user_auth_header,
        )

        assert type(resp) is Response
        assert resp.status_code == 200
        assert hasattr(resp, "json")

    def test_n_get_collection_error_id(self):
        """Test if get collection id responds"""

        stac_unique_id = "element84sentinel"
        resp = self.app.get(
            f"{URL_PREFIX}/stac/collections/" + stac_unique_id,
            headers=self.user_auth_header,
        )

        assert type(resp) is Response
        assert resp.status_code == 400
        assert hasattr(resp, "json")

    def test_p_delete_collection_id(self):
        """Test if delete a collection id responds"""

        stac_unique_id = "stac.defaultStac.rastercube.landsat-8-l1-c1"
        resp = self.app.delete(
            f"{URL_PREFIX}/stac/collections/" + stac_unique_id,
            headers=self.user_auth_header,
        )

        assert type(resp) is Response
        assert resp.status_code == 200
        assert hasattr(resp, "json")

    def test_q_delete_error_collection_id(self):
        """Test if delete a collection id responds"""

        stac_unique_id = "element84sentinel"
        resp = self.app.delete(
            f"{URL_PREFIX}/stac/collections/" + stac_unique_id,
            headers=self.user_auth_header,
        )

        assert type(resp) is Response
        assert resp.status_code == 400
        assert hasattr(resp, "json")
