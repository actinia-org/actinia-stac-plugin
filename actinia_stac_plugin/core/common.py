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
STAC module
* List all API availables
* Describe available actions on STAC formats in Actinia
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "Copyright 2019-2021, mundialis"
__maintainer__ = "__mundialis__"

import requests
from actinia_core.core.common.config import Configuration
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
        "stac.defaultStac.rastercube.landsat-8": {
            "root": "https://landsat-stac.s3.amazonaws.com/landsat-8-l1/catalog.json",
            "href": "/api/v1/stac/collections/stac.defaultStac.rastercube.landsat-8",
        },
        "stac.defaultStac.rastercube.sentinel-2": {
            "root": "https://sentinel-stac.s3.amazonaws.com/sentinel-2-l1c/catalog.json",
            "href": "/api/v1/stac/collections/stac.defaultStac.rastercube.sentinel-2",
        },
    }

    if exist:
        return redis_actinia_interface.read("defaultStac")
    else:
        redis_actinia_interface.create("defaultStac", defaultStac)
        return redis_actinia_interface.read("defaultStac")


def readStacCollection(stac_instance_id: str, stac_collection_id: str):
    try:
        if redis_actinia_interface.exists(stac_collection_id):
            stac = redis_actinia_interface.read(stac_collection_id)
        else:
            stac_dict = redis_actinia_interface.read(stac_instance_id)
            stac_root_url = stac_dict[stac_collection_id]["root"]
            response = requests.get(stac_root_url)
            stac = response.content
    except Exception:
        stac = {
            "Error": "Something went wrong, please check the collection and catalog to retrieved"
        }

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
