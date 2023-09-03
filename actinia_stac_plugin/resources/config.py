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


Configuration file
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2022 mundialis GmbH & Co. KG"
__license__ = "GPLv3"


import configparser
from pathlib import Path

# config can be overwritten by mounting *.ini files into folders inside
# the config folder.
DEFAULT_CONFIG_PATH = "config"
CONFIG_FILES = [
    str(f) for f in Path(DEFAULT_CONFIG_PATH).glob("**/*.ini") if f.is_file()
]
GENERATED_CONFIG = DEFAULT_CONFIG_PATH + "/actinia-stac-plugin.cfg"


class LOGCONFIG:
    """Default config for logging"""

    logfile = "actinia-stac-plugin.log"
    level = "DEBUG"
    type = "stdout"


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

        with open(GENERATED_CONFIG, "w") as configfile:
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
