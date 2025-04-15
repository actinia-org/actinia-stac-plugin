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

This code shows the functions for STAC item endpoint
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


def getStacItem(item: str, item_id: str):
    connectKvdb()
    exist = kvdb_actinia_interface.exists(item)

    if not exist:
        raise BadRequest("No Item found with the provided parameters")

    item = kvdb_actinia_interface.read(item)

    return item
