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


Application entrypoint. Creates Flask app and swagger docs, adds endpoints
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from actinia_stac_plugin.resources.log import log
from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api

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
