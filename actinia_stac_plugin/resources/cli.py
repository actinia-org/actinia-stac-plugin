#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018-present mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Commandline functions, extend later if needed
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-present mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


import os
import json
import sys


def name():
    """Print name to console
    """
    return "actinia-module-plugin"


def about():
    """Print information about actinia-module-plugin to console
    """

    text = "actinia-module-plugin"
    text = text + "\n This package communicates via HTTP"
    text = text + "\n To start application, run "
    text = text + "\n 'python -m actinia_stac_plugin.main'"
    return text


# used in pc2grass
def parseExe(process):
    # no api docs model
    line = process['exe']

    if 'params' in process:
        for param in process['params']:
            line += ' '
            line += param

    return line


# used in pc2grass
def parseModule(process):
    # id: string
    # module: string
    # inputs:  InputParameter
    # outputs:  OutputParameter
    # flags: string
    # stdin: string
    # overwrite: boolean
    # verbose: boolean
    # superquiet: boolean

    line = process['module']

    if 'inputs' in process:
        # param: string
        # value: string
        # import_descr: object
        for input in process['inputs']:
            line += ' '
            line += input['param']
            line += '='
            line += '"' + input['value'] + '"'

        if 'import_descr' in input:
            print('WARNING: Cannot translate import_descr for '
                  + process['id'])

    if 'outputs' in process:
        # param: string
        # value: string
        # export: object
        for output in process['outputs']:
            line += ' '
            line += input['param']
            line += '='
            line += input['value']

        if 'export' in output:
            print('WARNING: Cannot translate export for ' + process['id'])

    if 'flags' in process:
        line += ' -' + process['flags']
    if 'stdin' in process:
        print('WARNING: Cannot translate export for ' + process['id'])
    if 'overwrite' in process and process['overwrite'] == 'true':
        line += ' --overwrite'
    if 'verbose' in process and process['verbose'] == 'true':
        line += ' --verbose'
    if 'superquiet' in process and process['superquiet'] == 'true':
        line += ' --quiet'

    return line


def defineFile(file):
    if os.path.isfile(file):
        file = file
    elif os.path.isfile(os.getcwd() + file):
        file = os.getcwd() + file
    else:
        print('WARNING: Could not find file ' + str(file))
        return
    return file


def pc2grass():
    """Parser for actinia-core process chains to GRASS executables
    """

    input = sys.argv[1]
    output = sys.argv[2]

    if os.path.isfile(input):
        input = input
        output = output
    elif os.path.isfile(os.getcwd() + input):
        input = os.getcwd() + input
        output = os.getcwd() + output
    else:
        print('ERROR: Could not find input file ' + str(input))
        return

    with open(input, 'r') as file:
        pc = json.loads(file.read())

    list = pc['list']
    script = ''

    for process in list:
        line = ''
        if 'exe' in process:
            line = parseExe(process)
        elif 'module' in process:
            line = parseModule(process)
        else:
            print("WARNING: Neither 'exe' nor 'module' found in "
                  + process['id'])

        script += line + '\n'

    try:
        with open(output, 'x') as file:
            file.write(script)
    except FileExistsError:
        print('ERROR: output file already exists.'
              + ' (No overwrite option yet, sorry)')
        return

    print('All written')
