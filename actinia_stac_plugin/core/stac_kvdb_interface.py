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

Kvdb interface
This file is not yet fitted to STAC plugin usability,
however, the file will be adjusted in further steps of the development.
"""
__author__ = "Carmen Tawalika, Jorge Herrera"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"
__maintainer__ = "__mundialis__"


import pickle

from actinia_core.core.common.kvdb_base import KvdbBaseInterface


class KvdbActiniaInterface(KvdbBaseInterface):
    """
    The Kvdb actinia_template database interface
    A single actinia_template is stored as Hash with:
        - actinia_template id aka actinia_template name that must be unique
        - actinia-actinia_template dictionary
    In addition is the actinia_template_id saved in a hash that contains all
    actinia_template ids.
    """

    # We use two databases:
    # The actinia_template ID and the actinia_template name database
    # The actinia_template ID and actinia_template name databases are hashes
    actinia_template_id_hash_prefix = "ACTINIA-STAC-ID-PREFIX::"
    actinia_template_id_db = "ACTINIA-STAC-ID-DATABASE"

    def __init__(self):
        KvdbBaseInterface.__init__(self)

    def create(self, actinia_id, actinia_template):
        """
        Add an actinia_stac to the actinia_stac database
        Args:
            actinia_stac (dict): A dictionary of permissions
        Returns:
            bool:
            True is success, False if actinia_stac is already in database
        """
        actinia_template_id = actinia_id

        keyname = self.actinia_template_id_hash_prefix + actinia_template_id
        exists = self.kvdb_server.exists(keyname)
        if exists == 1 or exists is True:
            return False

        actinia_template_bytes = pickle.dumps(actinia_template)
        mapping = {
            "actinia_template_id": actinia_template_id,
            "actinia_template": actinia_template_bytes,
        }

        lock = self.kvdb_server.lock(
            name="add_actinia_template_lock", timeout=1
        )
        lock.acquire()
        # First add the actinia_template-id to the actinia_template id database
        self.kvdb_server.hset(
            self.actinia_template_id_db,
            actinia_template_id,
            actinia_template_id,
        )

        self.kvdb_server.hset(
            self.actinia_template_id_hash_prefix + actinia_template_id,
            mapping=mapping,
        )
        lock.release()

        return True

    def read(self, actinia_template_id):
        """Return the actinia_template
        HGET actinia_template-id actinia_template_group
        Args:
            actinia_template_id: The actinia_template id
        Returns:
             str:
             The actinia_template group
        """

        try:
            actinia_template = pickle.loads(
                self.kvdb_server.hget(
                    self.actinia_template_id_hash_prefix + actinia_template_id,
                    "actinia_template",
                )
            )
        except Exception:
            return False

        return actinia_template

    def update(self, actinia_template_id, actinia_template):
        """Update the actinia_template.
        Renaming an entry is not allowed, only existing entries with the
        same actinia_template_id can be updated.
        Args:
            actinia_template_id (str): The actinia_template id
            actinia_template (dict): The actinia_template as dictionary
        Returns:
            bool:
            True is success, False if actinia_template is not in the database
        """
        keyname = self.actinia_template_id_hash_prefix + actinia_template_id
        exists = self.kvdb_server.exists(keyname)
        if exists == 0 or exists is False:
            return False

        actinia_template_bytes = pickle.dumps(actinia_template)
        mapping = {
            "actinia_template_id": actinia_template_id,
            "actinia_template": actinia_template_bytes,
        }

        lock = self.kvdb_server.lock(
            name="update_actinia_template_lock", timeout=1
        )
        lock.acquire()

        self.kvdb_server.hset(
            self.actinia_template_id_hash_prefix + actinia_template_id,
            mapping=mapping,
        )

        lock.release()

        return True

    def delete(self, actinia_template_id):
        """Remove an actinia_template id from the database
        Args:
            actinia_template_id (str): The actinia_template id
        Returns:
            bool:
            True is actinia_template exists, False otherwise
        """
        exists = self.exists(actinia_template_id)
        if exists == 0 or exists is False:
            return False

        lock = self.kvdb_server.lock(
            name="delete_actinia_template_lock", timeout=1
        )
        lock.acquire()
        # Delete the entry from the actinia_template id database
        self.kvdb_server.hdel(self.actinia_template_id_db, actinia_template_id)
        # Delete the actual actinia_template entry
        self.kvdb_server.delete(
            self.actinia_template_id_hash_prefix + actinia_template_id
        )
        lock.release()

        return True

    def list_all_ids(self):
        """
        List all actinia_template id's that are in the database
        HKEYS on the actinia_template id database
        Returns:
            list:
            A list of all actinia_template ids in the database
        """
        values = []
        list = self.kvdb_server.hkeys(self.actinia_template_id_db)
        for entry in list:
            entry = entry.decode()
            values.append(entry)

        return values

    def exists(self, actinia_template_id):
        """Check if the actinia_template is in the database
        Args:
            actinia_template_id (str): The actinia_template id
        Returns:
            bool:
            True is actinia_template exists, False otherwise
        """
        return self.kvdb_server.exists(
            self.actinia_template_id_hash_prefix + actinia_template_id
        )


# Create the Kvdb interface instance
kvdb_actinia_interface = KvdbActiniaInterface()
