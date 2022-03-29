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
<<<<<<< HEAD

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

=======

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

>>>>>>> 2d3a4d1f6903dae447e07a1ad45af8ee5971f030
This code shows the functional elements in common for STAC endpoints
"""
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"
__maintainer__ = "__mundialis__"

import requests
from werkzeug.exceptions import BadRequest
from actinia_core.core.common.config import Configuration
from actinia_core.core.common.app import URL_PREFIX
from stac_validator import stac_validator

from actinia_stac_plugin.core.stac_redis_interface import redis_actinia_interface


def connectRedis():
    """This method initializes the connection with redis."""
    conf = Configuration()
    try:
        conf.read()
    except Exception:
        print("Error")

    server = conf.REDIS_SERVER_URL
    port = conf.REDIS_SERVER_PORT
    if conf.REDIS_SERVER_PW:
        redis_password = conf.REDIS_SERVER_PW
    else:
        redis_password = None

    redis_actinia_interface.connect(host=server, port=port, password=redis_password)

    return redis_actinia_interface


def defaultInstance():

    connectRedis()
    exist = redis_actinia_interface.exists("defaultStac")

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
        return redis_actinia_interface.read("defaultStac")
    else:
        redis_actinia_interface.create("defaultStac", defaultStac)
        return redis_actinia_interface.read("defaultStac")


def readStacCollection(stac_instance_id: str, stac_collection_id: str):
    connectRedis()
    try:
        if redis_actinia_interface.exists(stac_collection_id):
            stac = redis_actinia_interface.read(stac_collection_id)
        else:
            stac_dict = redis_actinia_interface.read(stac_instance_id)
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
    stac.run()
    valid = stac.message[0]["valid_stac"]
    type = stac.message[0]["asset_type"]
    if valid and type == "COLLECTION":
        return True
    else:
        return False


def resolveCollectionURL(url):
    collection_url = url

    stac = stac_validator.StacValidate(url)
    stac.run()
    type = stac.message[0]["asset_type"]
    if type == "COLLECTION":
        collection_url = url

    return collection_url
