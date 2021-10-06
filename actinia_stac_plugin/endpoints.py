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


Add endpoints to flask app with endpoint definitions and routes
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


# from flask import current_app, send_from_directory
# import werkzeug

# from actinia_module_plugin.resources.logging import log

from actinia_stac_plugin.api.stac import Stac
from actinia_stac_plugin.api.stac import StacCollections
from actinia_stac_plugin.api.stac import StacCollectionList
from actinia_stac_plugin.api.stac import StacInstanceList
from actinia_stac_plugin.api.stac import StacInstances


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
    apidoc.add_resource(StacInstances, "/stac/instances/<string:stac_instance_id>")
