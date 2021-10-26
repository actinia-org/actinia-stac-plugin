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

import re

import requests
from actinia_stac_plugin.core.stac_redis_interface import redis_actinia_interface
from actinia_stac_plugin.core.common import (
    connectRedis,
    defaultInstance,
    collectionValidation,
    resolveCollectionURL,
)


def createStacItemList():
    connectRedis()
    exist = redis_actinia_interface.exists("stac_instances")

    if not exist:
        defaultInstance()
        redis_actinia_interface.create(
            "stac_instances",
            {
                "defaultStac": {
                    "path": "stac.defaultStac.rastercube.<stac_collection_id>"
                }
            },
        )

    instances = redis_actinia_interface.read("stac_instances")

    return instances


def addStac2User(jsonParameters):
    """
    Add the STAC Catalog to redis
        1. Update the catalog to the initial list GET /stac
        2. Store the JSON as a new variable in redis
    """
    # Initializing Redis
    connectRedis()

    # Splitting the inputs
    stac_instance_id = jsonParameters["stac_instance_id"]
    stac_collection_id = jsonParameters["stac_collection_id"]
    stac_root = resolveCollectionURL(jsonParameters["stac_url"])
    stac_unique_id = "stac." + stac_instance_id + ".rastercube." + stac_collection_id

    # Caching JSON from the STAC collection
    stac_json_collection = requests.get(stac_root)
    redis_actinia_interface.create(stac_unique_id, stac_json_collection)

    # Verifying the existence of the instances - Adding the item to the Default List
    list_instances_exist = redis_actinia_interface.exists("stac_instances")
    if not list_instances_exist:
        defaultInstance()

    stac_instance_exist = redis_actinia_interface.exists(stac_instance_id)

    if not stac_instance_exist:
        redis_actinia_interface.create(stac_instance_id, {})

    defaultJson = redis_actinia_interface.read(stac_instance_id)

    instances_list = redis_actinia_interface.read("stac_instances")

    instances_list[stac_instance_id] = {
        "path": "stac." + stac_instance_id + ".rastercube.<stac_collection_id>"
    }

    defaultJson[stac_unique_id] = {
        "root": stac_root,
        "href": "api/v1/stac/collections/" + stac_unique_id,
    }

    list_of_instances_updated = redis_actinia_interface.update(
        "stac_instances", instances_list
    )
    instance_updated = redis_actinia_interface.update(stac_instance_id, defaultJson)

    if instance_updated and list_of_instances_updated:
        response = {
            "message": "The STAC Collection has been added successfully",
            "StacCatalogs": redis_actinia_interface.read(stac_instance_id),
        }
    else:
        response = {
            "message": "Check the stac_instance_id , stac_url or stac_collection_id given"
        }

    return response


def addStacValidator(parameters):
    """
    The function validate the inputs syntax and STAC validity
    Input:
        - parameters - JSON array with the Instance ID , Collection ID and STAC URL
    """
    stac_instance_id = "stac_instance_id" in parameters
    stac_collecion_id = "stac_collection_id" in parameters
    stac_root = "stac_url" in parameters
    msg = {}
    if stac_instance_id and stac_collecion_id and stac_root:
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
                "message": "Please check the URL provided (Should be a STAC Catalog)."
            }
        elif not instance_validation:
            msg["Error_instance"] = {
                "message": "Please check the ID given (no spaces or undercore characters)."
            }

        return msg
    else:
        return {
            "message": "Check the parameters (stac_instance_id,stac_collection_id,stac_url)"
        }
