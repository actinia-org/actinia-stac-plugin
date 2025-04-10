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


Test code for STAC module api endpoints
"""
__author__ = "Jorge Herrera"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"


import base64
import unittest
from typing import Dict, List

import pwgen
from actinia_core.endpoints import create_endpoints
from actinia_core.core.common import kvdb_interface
from actinia_core.core.common.app import flask_app
from actinia_core.core.common.config import global_config
from actinia_core.core.common.user import ActiniaUser
from werkzeug.datastructures import Headers


# actinia-stac-plugin endpoints are included as defined in actinia_core
# config
create_endpoints()


class ActiniaTestCase(unittest.TestCase):
    # guest = None
    # admin = None
    # superadmin = None
    user = None
    auth_header: Dict[str, Headers] = {}
    users_list: List[str] = []

    def setUp(self):
        """Overwrites method setUp from unittest.TestCase class"""

        self.app_context = flask_app.app_context()
        self.app_context.push()
        # from http://flask.pocoo.org/docs/0.12/api/#flask.Flask.test_client:
        # Note that if you are testing for assertions or exceptions in your
        # application code, you must set app.testing = True in order for the
        # exceptions to propagate to the test client.  Otherwise, the exception
        # will be handled by the application (not visible to the test client)
        # and the only indication of an AssertionError or other exception will
        # be a 500 status code response to the test client.
        flask_app.testing = True
        self.app = flask_app.test_client()

        # Start and connect the kvdb interface
        kvdb_args = (
            global_config.KVDB_SERVER_URL,
            global_config.KVDB_SERVER_PORT,
        )
        if (
            global_config.KVDB_SERVER_PW
            and global_config.KVDB_SERVER_PW is not None
        ):
            kvdb_args = (*kvdb_args, global_config.KVDB_SERVER_PW)
        kvdb_interface.connect(*kvdb_args)

        # create test user for roles user (more to come)
        accessible_datasets = {
            "nc_spm_08": ["PERMANENT", "user1", "modis_lst"]
        }
        password = pwgen.pwgen()
        self.user_id, self.user_group, self.user_auth_header = self.createUser(
            name="user",
            role="user",
            password=password,
            process_num_limit=3,
            process_time_limit=4,
            accessible_datasets=accessible_datasets,
        )

        # # create process queue
        # from actinia_core.core.common.process_queue import \
        #    create_process_queue
        # create_process_queue(config=global_config)

    def tearDown(self):
        """Overwrites method tearDown from unittest.TestCase class"""

        self.app_context.pop()

        # remove test user; disconnect kvdb
        for user in self.users_list:
            user.delete()
        kvdb_interface.disconnect()

    def createUser(
        self,
        name="guest",
        role="guest",
        group="group",
        password="abcdefgh",
        accessible_datasets=None,
        process_num_limit=1000,
        process_time_limit=6000,
    ):
        auth = bytes("%s:%s" % (name, password), "utf-8")

        # We need to create an HTML basic authorization header
        self.auth_header[role] = Headers()
        self.auth_header[role].add(
            "Authorization", "Basic " + base64.b64encode(auth).decode()
        )

        # Make sure the user database is empty
        user = ActiniaUser(name)
        if user.exists():
            user.delete()
        # Create a user in the database
        user = ActiniaUser.create_user(
            name,
            group,
            password,
            user_role=role,
            accessible_datasets=accessible_datasets,
            process_num_limit=process_num_limit,
            process_time_limit=process_time_limit,
        )
        user.add_accessible_modules(["uname", "sleep"])
        self.users_list.append(user)

        return name, group, self.auth_header[role]
