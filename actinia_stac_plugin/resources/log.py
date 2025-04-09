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


Logging interface
"""

__license__ = "GPLv3"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2019-2021, mundialis"
__maintainer__ = "Carmen Tawalika"

# pylint: disable=E1101
# E1101: Instance of 'RootLogger' has no 'loggerDict' member (no-member) - Make no sense

import logging
from datetime import datetime

from colorlog import ColoredFormatter
from pythonjsonlogger import jsonlogger

from actinia_stac_plugin.resources.config import LOGCONFIG

log = logging.getLogger("actinia-stac-plugin")
werkzeuglog = logging.getLogger("werkzeug")
gunicornlog = logging.getLogger("gunicorn")


def setLogFormat(veto=None):
    logformat = ""
    if LOGCONFIG.type == "json" and not veto:
        logformat = CustomJsonFormatter(
            "%(time) %(level) %(component)"
            "%(module) %(message) %(pathname)"
            "%(lineno) %(processName)"
            "%(threadName)"
        )
    else:
        logformat = ColoredFormatter(
            "%(log_color)s[%(asctime)s] %(levelname)-10s: %(name)s.%(module)-"
            "10s -%(message)s [in %(pathname)s:%(lineno)d]%(reset)s"
        )
    return logformat


def setLogHandler(logger, type, format):
    if type == "stdout":
        handler = logging.StreamHandler()
    elif type == "file":
        # For readability, json is never written to file
        handler = logging.FileHandler(LOGCONFIG.logfile)
    handler.setFormatter(format)
    logger.addHandler(handler)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict
        )

        # (Pdb) dir(record)
        # ... 'args', 'created', 'exc_info', 'exc_text', 'filename', 'funcName'
        # ,'getMessage', 'levelname', 'levelno', 'lineno', 'message', 'module',
        # 'msecs', 'msg', 'name', 'pathname', 'process', 'processName',
        # 'relativeCreated', 'stack_info', 'thread', 'threadName']

        now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        log_record["time"] = now
        log_record["level"] = record.levelname
        log_record["component"] = record.name


def createLogger():
    # create logger, set level and define format
    log.setLevel(getattr(logging, LOGCONFIG.level))
    fileformat = setLogFormat("veto")
    stdoutformat = setLogFormat()
    setLogHandler(log, "file", fileformat)
    setLogHandler(log, "stdout", stdoutformat)


def createWerkzeugLogger():
    werkzeuglog.setLevel(getattr(logging, LOGCONFIG.level))
    fileformat = setLogFormat("veto")
    stdoutformat = setLogFormat()
    setLogHandler(werkzeuglog, "file", fileformat)
    setLogHandler(werkzeuglog, "stdout", stdoutformat)


def createGunicornLogger():
    gunicornlog.setLevel(getattr(logging, LOGCONFIG.level))
    fileformat = setLogFormat("veto")
    stdoutformat = setLogFormat()
    setLogHandler(gunicornlog, "file", fileformat)
    setLogHandler(gunicornlog, "stdout", stdoutformat)
    # gunicorn already has a lot of children logger, e.g gunicorn.http,
    # gunicorn.access. These lines deactivate their default handlers.
    for name in logging.root.manager.loggerDict:
        if "gunicorn." in name:
            logging.getLogger(name).propagate = True
            logging.getLogger(name).handlers = []


createLogger()
createWerkzeugLogger()
createGunicornLogger()
