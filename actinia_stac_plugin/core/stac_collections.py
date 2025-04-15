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

This code shows the functions for STAC collections endpoint
"""
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"
__maintainer__ = "__mundialis__"

import json
import re

import requests
from werkzeug.exceptions import BadRequest
from actinia_api import URL_PREFIX

from actinia_stac_plugin.core.stac_kvdb_interface import (
    kvdb_actinia_interface,
)
from actinia_stac_plugin.core.common import (
    collectionValidation,
    connectKvdb,
    defaultInstance,
    readStacCollection,
    resolveCollectionURL,
)


def StacCollectionsList():
    connectKvdb()
    stac_inventary = {"collections": []}
    exist = kvdb_actinia_interface.exists("stac_instances")

    if exist:
        instances = kvdb_actinia_interface.read("stac_instances")
        for k, v in instances.items():
            collections = kvdb_actinia_interface.read(k)
            for i, j in collections.items():
                stac = readStacCollection(k, i)
                try:
                    stac = stac.decode("utf8").replace("'", '"')
                except Exception:
                    stac = stac
                # if response is slow (especially with growing collections),
                # it might be an option to use pickle to store json in kvdb
                json_collection = json.loads(stac)
                json_collection["id"] = i
                stac_inventary["collections"].append(json_collection)
    else:
        collections = defaultInstance()
        stac_inventary["defaultStac"] = collections
        kvdb_actinia_interface.create(
            "stac_instances",
            {
                "defaultStac": {
                    "path": "stac.defaultStac.rastercube.<stac_collection_id>"
                }
            },
        )

    return stac_inventary


def addStac2User(jsonparameters):
    """
    Add the STAC Collection to kvdb
        1. Update the Collection to the initial list GET /stac
        2. Store the JSON as a new variable in kvdb
    """
    # Initializing Kvdb
    connectKvdb()

    # Splitting the inputs
    stac_instance_id = jsonparameters["stac_instance_id"]
    stac_root = resolveCollectionURL(jsonparameters["stac_url"])
    stac_json_collection = jsonparameters["collection"]
    stac_collection_id = jsonparameters["stac_collection_id"]

    # Verifying the existence of the instances - Adding the item to the Default List
    list_instances_exist = kvdb_actinia_interface.exists("stac_instances")
    if not list_instances_exist:
        defaultInstance()

    stac_instance_exist = kvdb_actinia_interface.exists(stac_instance_id)

    if not stac_instance_exist:
        raise BadRequest("No Instance name matched")

    if not stac_root:
        raise BadRequest(
            "<%s> is not a valid STAC collection" % jsonparameters["stac_url"]
        )

    if stac_instance_id and stac_root:
        # Caching JSON from the STAC collection
        stac_unique_id = (
            "stac." + stac_instance_id + ".rastercube." + stac_collection_id
        )
        kvdb_actinia_interface.create(
            stac_unique_id, stac_json_collection.content
        )

        defaultJson = kvdb_actinia_interface.read(stac_instance_id)

        defaultJson[stac_unique_id] = {
            "root": stac_root,
            "href": URL_PREFIX[1:] + "/stac/collections/" + stac_unique_id,
        }

        instance_updated = kvdb_actinia_interface.update(
            stac_instance_id, defaultJson
        )

        if instance_updated:
            response = {
                "message": "The STAC Collection has been added successfully",
                "StacCollection": kvdb_actinia_interface.read(
                    stac_instance_id
                ),
            }
        else:
            raise BadRequest(
                "Check the stac_instance_id , stac_url or stac_collection_id given"
            )

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

        parameters["collection"] = requests.get(parameters["stac_url"])
        parameters["stac_collection_id"] = parameters["collection"].json()[
            "id"
        ]

        collection_validation = re.match(
            "^[a-zA-Z0-9-_]*$", parameters["stac_collection_id"]
        )
        instance_validation = re.match(
            "^[a-zA-Z0-9_]*$", parameters["stac_instance_id"]
        )

        if root_validation and instance_validation and collection_validation:
            return addStac2User(parameters)
        elif not root_validation:
            raise BadRequest(
                "Check the URL provided (Should be a STAC Collection)."
            )
        elif not collection_validation:
            raise BadRequest(
                "Please check the URL provided (Should be a STAC Collection)."
            )
        elif not instance_validation:
            raise BadRequest(
                "Please check the ID given (no spaces or hypens)."
            )

        return msg
    else:
        raise BadRequest("Check the parameters (stac_instance_id,stac_url)")
