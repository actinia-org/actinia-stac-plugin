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


Configuration file
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


import configparser
import glob
from pathlib import Path

# config can be overwritten by mounting *.ini files into folders inside
# the config folder.
DEFAULT_CONFIG_PATH = "config"
CONFIG_FILES = [str(f) for f in Path(
    DEFAULT_CONFIG_PATH).glob('**/*.ini') if f.is_file()]
GENERATED_CONFIG = DEFAULT_CONFIG_PATH + '/actinia-stac-plugin.cfg'


class LOGCONFIG:
    """Default config for logging
    """
    logfile = 'actinia-stac-plugin.log'
    level = 'DEBUG'
    type = 'stdout'


class Configfile:

    def __init__(self):
        """
        This class will overwrite the config classes above when config files
        named DEFAULT_CONFIG_PATH/**/*.ini exist.
        On first import of the module it is initialized.
        """

        config = configparser.ConfigParser()
        config.read(CONFIG_FILES)

        if len(config) <= 1:
            print("Could not find any config file, using default values.")
            return
        print("Loading config files: " + str(CONFIG_FILES) + " ...")

        with open(GENERATED_CONFIG, 'w') as configfile:
            config.write(configfile)
        print("Configuration written to " + GENERATED_CONFIG)

        # LOGGING
        if config.has_section("LOGCONFIG"):
            if config.has_option("LOGCONFIG", "logfile"):
                LOGCONFIG.logfile = config.get("LOGCONFIG", "logfile")
            if config.has_option("LOGCONFIG", "level"):
                LOGCONFIG.level = config.get("LOGCONFIG", "level")
            if config.has_option("LOGCONFIG", "type"):
                LOGCONFIG.type = config.get("LOGCONFIG", "type")


init = Configfile()
