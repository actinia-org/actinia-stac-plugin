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

This code shows the functions for STAC instance id endpoint
"""
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"
__maintainer__ = "__mundialis__"

from werkzeug.exceptions import BadRequest

from actinia_stac_plugin.core.stac_kvdb_interface import (
    kvdb_actinia_interface,
)
from actinia_stac_plugin.core.common import connectKvdb


def getInstance(stac_instance_id):
    connectKvdb()
    exist = kvdb_actinia_interface.exists(stac_instance_id)

    if not exist:
        raise BadRequest(
            "stac instance ID does not match with the instences stored"
        )

    return kvdb_actinia_interface.read(stac_instance_id)


def deleteStacInstance(stac_instance_id):
    connectKvdb()
    try:
        instance = kvdb_actinia_interface.read(stac_instance_id)
        for i in instance.keys():
            kvdb_actinia_interface.delete(i)
        kvdb_actinia_interface.delete(stac_instance_id)
        instances = kvdb_actinia_interface.read("stac_instances")
        del instances[stac_instance_id]
        kvdb_actinia_interface.update("stac_instances", instances)
    except Exception:
        raise BadRequest(
            "Something went wrong please that the element is well typed "
            + stac_instance_id
        )
    return stac_instance_id
