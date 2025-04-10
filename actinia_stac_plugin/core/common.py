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

This code shows the functional elements in common for STAC endpoints
"""
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"
__maintainer__ = "__mundialis__"

import requests
from werkzeug.exceptions import BadRequest
from actinia_core.core.common.config import Configuration
from actinia_api import URL_PREFIX
from stac_validator import stac_validator

from actinia_stac_plugin.core.stac_kvdb_interface import (
    kvdb_actinia_interface,
)


def connectKvdb():
    """This method initializes the connection with a kvdb."""
    conf = Configuration()
    try:
        conf.read()
    except Exception:
        print("Error reading configuration")

    server = conf.KVDB_SERVER_URL
    port = conf.KVDB_SERVER_PORT
    if conf.KVDB_SERVER_PW:
        kvdb_password = conf.KVDB_SERVER_PW
    else:
        kvdb_password = None

    kvdb_actinia_interface.connect(
        host=server, port=port, password=kvdb_password
    )

    return kvdb_actinia_interface


def defaultInstance():
    connectKvdb()
    exist = kvdb_actinia_interface.exists("defaultStac")

    defaultStac = {
        "stac.defaultStac.rastercube.landsat-8-l1-c1": {
            "root": "https://earth-search.aws.element84.com/v0/collections/landsat-8-l1-c1",
            "href": f"{URL_PREFIX}/stac/collections/stac.defaultStac.rastercube.landsat-8-l1-c1",
        },
        "stac.defaultStac.rastercube.sentinel-s2-l2a": {
            "root": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a",
            "href": f"{URL_PREFIX}/stac/collections/stac.defaultStac.rastercube.sentinel-s2-l2a",
        },
    }

    if exist:
        return kvdb_actinia_interface.read("defaultStac")
    else:
        kvdb_actinia_interface.create("defaultStac", defaultStac)
        return kvdb_actinia_interface.read("defaultStac")


def readStacCollection(stac_instance_id: str, stac_collection_id: str):
    connectKvdb()
    try:
        if kvdb_actinia_interface.exists(stac_collection_id):
            stac = kvdb_actinia_interface.read(stac_collection_id)
        else:
            stac_dict = kvdb_actinia_interface.read(stac_instance_id)
            stac_root_url = stac_dict[stac_collection_id]["root"]
            response = requests.get(stac_root_url)
            stac = response.content
    except Exception:
        raise BadRequest(
            "Something went wrong, please check the collection and catalog to retrieved"
        )

    return stac


def collectionValidation(url: str) -> bool:
    """
    Verify that the URL provided belong to a STAC endpoint
    """
    stac = stac_validator.StacValidate(url)
    if stac.run() is False:
        print("This <%s> is not a valid STAC collection" % stac)
        return False
    if "valid_stac" not in stac.message[0].keys():
        print("This <%s> is not a valid STAC collection" % stac)
        return False
    if stac.message[0]["valid_stac"] is False:
        print("This <%s> is not a valid STAC collection" % stac)
        return False
    if "asset_type" not in stac.message[0].keys():
        print("This <%s> is not a valid STAC collection" % stac)
        return False
    if stac.message[0]["asset_type"] != "COLLECTION":
        print("This <%s> is not a valid STAC collection" % stac)
        return False

    return True


def resolveCollectionURL(url):
    stac = stac_validator.StacValidate(url)
    if stac.run() is False:
        print("This <%s> is not a valid STAC collection" % stac)
        return None
    if "valid_stac" not in stac.message[0].keys():
        print("This <%s> is not a valid STAC collection" % stac)
        return None
    if stac.message[0]["valid_stac"] is False:
        print("This <%s> is not a valid STAC collection" % stac)
        return None
    if "asset_type" not in stac.message[0].keys():
        print("This <%s> is not a valid STAC collection" % stac)
        return None
    if stac.message[0]["asset_type"] != "COLLECTION":
        print("This <%s> is not a valid STAC collection" % stac)
        return None

    return url
