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


Add endpoints to flask app with endpoint definitions and routes
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"


# from flask import current_app, send_from_directory
# import werkzeug

# from actinia_module_plugin.resources.logging import log

from actinia_stac_plugin.api.stac import Stac
from actinia_stac_plugin.api.stac_collections import StacCollectionList
from actinia_stac_plugin.api.stac_collection_id import StacCollections
from actinia_stac_plugin.api.stac_instances import StacInstanceList
from actinia_stac_plugin.api.stac_instance_id import StacInstances
from actinia_stac_plugin.api.stac_catalogs import StacCatalogList
from actinia_stac_plugin.api.stac_items import StacItems


def create_endpoints(flask_api):
    # app = flask_api.app
    apidoc = flask_api

    # @app.route('/')
    # def index():
    #     try:
    #         # flask cannot reach out of current_app (which is actinia_core)
    #         return current_app.send_static_file('index.html')
    #     except werkzeug.exceptions.NotFound:
    #         log.debug('No index.html found. Serving backup.')
    #         return ("""<h1 style='color:red'>actinia</h1>
    #             <a href="swagger.json">API docs</a>""")
    #
    # @app.route('/<path:filename>')
    # def static_content(filename):
    #     # WARNING: all content from folder "static" will be accessible!
    #     return send_from_directory(app.static_folder, filename)

    apidoc.add_resource(Stac, "/stac")
    apidoc.add_resource(StacCollectionList, "/stac/collections")
    apidoc.add_resource(
        StacCollections, "/stac/collections/<string:stac_collection_id>"
    )
    apidoc.add_resource(StacInstanceList, "/stac/instances")
    apidoc.add_resource(
        StacInstances, "/stac/instances/<string:stac_instance_id>"
    )
    apidoc.add_resource(StacCatalogList, "/stac/catalogs/catalog.json")
    apidoc.add_resource(
        StacItems, "/stac/catalogs/<string:item>/<string:item_id>.json"
    )
