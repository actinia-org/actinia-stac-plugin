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

import json
import re

import requests

from actinia_stac_plugin.core.stac_redis_interface import redis_actinia_interface
from actinia_stac_plugin.core.common import (
    collectionValidation,
    connectRedis,
    defaultInstance,
    readStacCollection,
    resolveCollectionURL,
)


def StacCollectionsList():
    connectRedis()
    stac_inventary = {"collections": []}
    exist = redis_actinia_interface.exists("stac_instances")

    if exist:
        instances = redis_actinia_interface.read("stac_instances")
        for k, v in instances.items():
            collections = redis_actinia_interface.read(k)
            for i, j in collections.items():
                stac = readStacCollection(k, i)
                try:
                    stac = stac.decode("utf8").replace("'", '"')
                except Exception:
                    stac = stac
                stac_inventary["collections"].append(json.loads(stac))
    else:
        collections = defaultInstance()
        stac_inventary["defaultStac"] = collections
        redis_actinia_interface.create(
            "stac_instances",
            {
                "defaultStac": {
                    "path": "stac.defaultStac.rastercube.<stac_collection_id>"
                }
            },
        )

    return stac_inventary


def addStac2User(jsonParameters):
    """
    Add the STAC Collection to redis
        1. Update the Collection to the initial list GET /stac
        2. Store the JSON as a new variable in redis
    """
    # Initializing Redis
    connectRedis()

    # Splitting the inputs
    stac_instance_id = jsonParameters["stac_instance_id"]
    stac_root = resolveCollectionURL(jsonParameters["stac_url"])

    # Verifying the existence of the instances - Adding the item to the Default List
    list_instances_exist = redis_actinia_interface.exists("stac_instances")
    if not list_instances_exist:
        defaultInstance()

    stac_instance_exist = redis_actinia_interface.exists(stac_instance_id)

    if not stac_instance_exist:
        return {"message": "No Instance name matched"}

    if stac_instance_id and stac_root:

        # Caching JSON from the STAC collection
        stac_json_collection = requests.get(stac_root)
        stac_collection_id = stac_json_collection.json()["id"]
        stac_unique_id = (
            "stac." + stac_instance_id + ".rastercube." + stac_collection_id
        )
        redis_actinia_interface.create(stac_unique_id, stac_json_collection.content)

        defaultJson = redis_actinia_interface.read(stac_instance_id)

        defaultJson[stac_unique_id] = {
            "root": stac_root,
            "href": "api/v1/stac/collections/" + stac_unique_id,
        }

        instance_updated = redis_actinia_interface.update(stac_instance_id, defaultJson)

        if instance_updated:
            response = {
                "message": "The STAC Collection has been added successfully",
                "StacCollection": redis_actinia_interface.read(stac_instance_id),
            }
        else:
            response = {
                "message": "Check the stac_instance_id , stac_url or stac_collection_id given"
            }

        return response


def addStacCollection(parameters):
    """
    The function validate the inputs syntax and STAC validity
    Input:
        - json - JSON array with the Instance ID , Collection ID and STAC URL
    """
    stac_instance_id = "stac_instance_id" in parameters
    stac_root = "stac_url" in parameters
    msg = {}

    if stac_instance_id and stac_root:
        root_validation = collectionValidation(parameters["stac_url"])
        collection_validation = re.match(
            "^[a-zA-Z0-9_]*$", parameters["stac_collection_id"]
        )
        instance_validation = re.match(
            "^[a-zA-Z0-9_]*$", parameters["stac_instance_id"]
        )

        if root_validation and instance_validation and collection_validation:
            return addStac2User(parameters)
        elif not root_validation:
            msg["Error_root"] = {
                "message": "Check the URL provided (Should be a STAC Collection)."
            }
        elif not collection_validation:
            msg["Error_collection"] = {
                "message": "Please check the URL provided (Should be a STAC Collection)."
            }
        elif not instance_validation:
            msg["Error_instance"] = {
                "message": "Please check the ID given (no spaces or hypens)."
            }

        return msg
    else:
        return {
            "message": "Check the parameters (stac_instance_id,stac_collection_id,stac_url)"
        }
