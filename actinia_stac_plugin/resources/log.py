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
Logging interface
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2019-2021, mundialis"
__maintainer__ = "Carmen Tawalika"

# pylint: disable=E1101
# E1101: Instance of 'RootLogger' has no 'loggerDict' member (no-member) - Make no sense

import logging
from datetime import datetime

from actinia_stac_plugin.resources.config import LOGCONFIG
from colorlog import ColoredFormatter
from pythonjsonlogger import jsonlogger

log = logging.getLogger("actinia-stac-plugin")
werkzeugLog = logging.getLogger("werkzeug")
gunicornLog = logging.getLogger("gunicorn")


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
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

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
    werkzeugLog.setLevel(getattr(logging, LOGCONFIG.level))
    fileformat = setLogFormat("veto")
    stdoutformat = setLogFormat()
    setLogHandler(werkzeugLog, "file", fileformat)
    setLogHandler(werkzeugLog, "stdout", stdoutformat)


def createGunicornLogger():
    gunicornLog.setLevel(getattr(logging, LOGCONFIG.level))
    fileformat = setLogFormat("veto")
    stdoutformat = setLogFormat()
    setLogHandler(gunicornLog, "file", fileformat)
    setLogHandler(gunicornLog, "stdout", stdoutformat)
    # gunicorn already has a lot of children logger, e.g gunicorn.http,
    # gunicorn.access. These lines deactivate their default handlers.
    for name in logging.root.manager.loggerDict:
        if "gunicorn." in name:
            logging.getLogger(name).propagate = True
            logging.getLogger(name).handlers = []


createLogger()
createWerkzeugLogger()
createGunicornLogger()
