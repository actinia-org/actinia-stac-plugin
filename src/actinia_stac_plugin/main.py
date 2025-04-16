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


Application entrypoint. Creates Flask app and swagger docs, adds endpoints
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"


from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api

from actinia_stac_plugin.resources.log import log

app = Flask(__name__)
CORS(app)

apidoc = Api(
    app,
    title="actinia-stac-plugin",
    api_spec_url="/latest/api/swagger",
    schemes=["https", "http"],
    consumes=["application/json"],
    description="""STAC.
                   """,
)

if __name__ == "__main__":
    # call this for development only with
    # `python -m actinia_stac_plugin.main`
    log.debug("starting app in development mode...")
    app.run(debug=False, use_reloader=False)
    # for production environent use application in wsgy.py
