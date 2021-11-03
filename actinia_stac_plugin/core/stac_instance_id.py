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

from actinia_stac_plugin.core.stac_redis_interface import redis_actinia_interface
from actinia_stac_plugin.core.common import connectRedis


def getInstance(stac_instance_id):
    connectRedis()
    exist = redis_actinia_interface.exists(stac_instance_id)

    if exist:
        return redis_actinia_interface.read(stac_instance_id)

    return {"Error": "stac instance ID does not match with the instences stored"}


def deleteStacInstance(stac_instance_id):
    connectRedis()
    try:
        instance = redis_actinia_interface.read(stac_instance_id)
        for i in instance.keys():
            redis_actinia_interface.delete(i)
        redis_actinia_interface.delete(stac_instance_id)
        instances = redis_actinia_interface.read("stac_instances")
        del instances[stac_instance_id]
        redis_actinia_interface.update("stac_instances", instances)
    except Exception:
        return {
            "Error": "Something went wrong please that the element is well typed "
            + stac_instance_id
        }
    return {
        "message": "The instance --"
        + stac_instance_id
        + "-- was deleted with all the collections stored inside"
    }
