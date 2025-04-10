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

This code shows the functions for STAC instance endpoint
"""
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"
__maintainer__ = "__mundialis__"

import re
from werkzeug.exceptions import BadRequest

from actinia_stac_plugin.core.stac_kvdb_interface import (
    kvdb_actinia_interface,
)
from actinia_stac_plugin.core.common import connectKvdb, defaultInstance


def createStacItemList():
    connectKvdb()
    exist = kvdb_actinia_interface.exists("stac_instances")

    if not exist:
        defaultInstance()
        kvdb_actinia_interface.create(
            "stac_instances",
            {
                "defaultStac": {
                    "path": "stac.defaultStac.rastercube.<stac_collection_id>"
                }
            },
        )

    instances = kvdb_actinia_interface.read("stac_instances")

    return instances


def addInstance2User(jsonparameters):
    """
    Add the STAC Collection to kvdb
        1. Update the Collection to the initial list GET /stac
        2. Store the JSON as a new variable in kvdb
    """
    # Initializing Kvdb
    connectKvdb()

    # Splitting the inputs
    stac_instance_id = jsonparameters["stac_instance_id"]
    # Verifying the existence of the instances - Adding the item to the Default List
    list_instances_exist = kvdb_actinia_interface.exists("stac_instances")
    if not list_instances_exist:
        defaultInstance()

    stac_instance_exist = kvdb_actinia_interface.exists(stac_instance_id)

    if not stac_instance_exist:
        kvdb_actinia_interface.create(stac_instance_id, {})

        instances_list = kvdb_actinia_interface.read("stac_instances")
        instances_list[stac_instance_id] = {
            "path": "stac."
            + stac_instance_id
            + ".rastercube.<stac_collection_id>"
        }

        list_of_instances_updated = kvdb_actinia_interface.update(
            "stac_instances", instances_list
        )

        if list_of_instances_updated:
            response = kvdb_actinia_interface.read(stac_instance_id)
        else:
            raise BadRequest("Check the stac_instance_id given")

        return response


def addInstance(parameters):
    """
    The function validate the inputs syntax and STAC validity
    Input:
        - parameters - JSON array with the Instance ID
    """
    stac_instance_id = "stac_instance_id" in parameters
    msg = {}

    if stac_instance_id:
        instance_validation = re.match(
            "^[a-zA-Z0-9_]*$", parameters["stac_instance_id"]
        )

        if instance_validation:
            return addInstance2User(parameters)
        elif not instance_validation:
            raise BadRequest(
                "Please check the ID given (no spaces or undercore characters)."
            )

        return msg
    else:
        raise BadRequest("Check the parameters (stac_instance_id)")
