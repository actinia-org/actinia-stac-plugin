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


Test
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2018-2021, mundialis"


import unittest

from actinia_stac_plugin.resources.cli import about, name


class CliTest(unittest.TestCase):
    def test_cli_name(self):
        """Test basic cli command"""
        assert name() == "actinia-stac-plugin"

    def test_cli_about(self):
        """Test basic cli command"""
        text = "actinia-stac-plugin"
        text = text + "\n This package communicates via HTTP"
        text = text + "\n To start application, run "
        text = text + "\n 'python -m actinia_stac_plugin.main'"

        assert about() == text
