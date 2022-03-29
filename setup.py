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


Setup file for actinia_stac_plugin.

This file was generated with PyScaffold 3.0.2.
PyScaffold helps you to put up the scaffold of your new Python project.
Learn more under: http://pyscaffold.org/
"""

__author__ = "Jorge Herrera, Carmen Tawalika"
__copyright__ = "2021-2021 mundialis GmbH & Co. KG"
__license__ = "GPLv3"


from setuptools import setup


def setup_package():
    setup(
        setup_requires=["pyscaffold>=3.0a0,<3.1a0 "],
        packages=["actinia_stac_plugin"],
        package_dir={"actinia_stac_plugin ": "actinia_stac_plugin "},
        include_package_data=True,
        use_pyscaffold=True,
        install_requires=["stac-validator>=2.2.0"],
    )


if __name__ == "__main__":
    setup_package()
