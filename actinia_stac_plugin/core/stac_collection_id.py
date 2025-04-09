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

This code shows the functions for STAC collection id endpoint
"""
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"
__maintainer__ = "__mundialis__"


import json
from werkzeug.exceptions import BadRequest

from actinia_stac_plugin.core.stac_kvdb_interface import (
    kvdb_actinia_interface,
)
from actinia_stac_plugin.core.common import readStacCollection, connectKvdb


def callStacCollection(stac_collection_id: str):
    try:
        instance_id = stac_collection_id.split(".")[1]
        stac = readStacCollection(instance_id, stac_collection_id)
        resp = json.loads(stac)
        # overwrite original ID with generated ID
        resp["id"] = stac_collection_id
    except Exception:
        raise BadRequest("Please check the collection id provided")

    return resp


def deleteStacCollection(stac_instance_id: str, stac_collection_id: str):
    connectKvdb()

    try:
        stac_instance = kvdb_actinia_interface.read(stac_instance_id)
        del stac_instance[stac_collection_id]
        kvdb_actinia_interface.update(stac_instance_id, stac_instance)
        if kvdb_actinia_interface.exists(stac_collection_id):
            kvdb_actinia_interface.delete(stac_collection_id)
    except Exception:
        raise BadRequest(
            "Please check that the parameters given are well typed and exist"
        )

    return kvdb_actinia_interface.read(stac_instance_id)
