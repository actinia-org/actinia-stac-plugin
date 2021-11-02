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
from actinia_stac_plugin.core.common import readStacCollection, connectRedis


def callStacCollection(stac_collection_id: str):
    try:
        instance_id = stac_collection_id.split(".")[1]
        stac = readStacCollection(instance_id, stac_collection_id)
    except Exception:
        stac = {
            "Error": "Something went wrong, please check the collection to retrieved"
        }

    return stac


def deleteStacCollection(stac_instance_id: str, stac_collection_id: str):
    connectRedis()

    try:
        stac_instance = redis_actinia_interface.read(stac_instance_id)
        del stac_instance[stac_collection_id]
        redis_actinia_interface.update(stac_instance_id, stac_instance)
        if redis_actinia_interface.exists(stac_collection_id):
            redis_actinia_interface.delete(stac_collection_id)
    except Exception:
        return {
            "Error": "Please check that the parameters given are well typed and exist"
        }

    return redis_actinia_interface.read(stac_instance_id)
