#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2021 mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Test Template CRUD
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"


from flask import Response
import json
import uuid

from actinia_core.core.common.app import URL_PREFIX

from testsuite import ActiniaTestCase


global allTemplatesCount
global templateUUID


class ActiniaTemplatesTest(ActiniaTestCase):

    def test_1001_read_all(self):
        """Test HTTP GET /actinia_templates and rememberes number of templates
        """
        global allTemplatesCount

        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + '/actinia_templates',
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

        assert type(resp.json) is list
        allTemplatesCount = len(resp.json)

    def test_1002_create(self):
        """Test HTTP POST /actinia_templates (template creation)"""
        global templateUUID

        respStatusCode = 201

        with open('tests/resources/actinia_templates/pc_tpl.json') as file:
            pc_template = json.load(file)
        templateUUID = str(uuid.uuid4())
        pc_template['id'] = templateUUID

        resp = self.app.post(URL_PREFIX + '/actinia_templates',
                             headers=self.user_auth_header,
                             data=json.dumps(pc_template),
                             content_type="application/json")

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')
        assert "Success" in resp.json['message']

    def test_1003_create_fail(self):
        """Test HTTP POST /actinia_templates (template creation) of already
        existing template
        """
        global templateUUID

        respStatusCode = 400

        with open('tests/resources/actinia_templates/pc_tpl.json') as file:
            pc_template = json.load(file)
        pc_template['id'] = templateUUID

        resp = self.app.post(URL_PREFIX + '/actinia_templates',
                             headers=self.user_auth_header,
                             data=json.dumps(pc_template),
                             content_type="application/json")

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

    def test_1004_read_single(self):
        """Test HTTP GET /actinia_templates/<template_id> of new created
        template
        """
        global templateUUID

        respStatusCode = 200

        resp = self.app.get(URL_PREFIX + '/actinia_templates/' + templateUUID,
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

        with open('tests/resources/actinia_templates/pc_tpl.json') as file:
            pc_template = json.load(file)
        pc_template['id'] = templateUUID
        assert resp.json == pc_template

    def test_1005_update(self):
        """Test HTTP PUT /actinia_templates/<template_id> (update)"""
        global templateUUID

        respStatusCode = 201
        with open('tests/resources/actinia_templates/pc_tpl2.json') as file:
            pc_template = json.load(file)
        pc_template['id'] = templateUUID

        resp = self.app.put(URL_PREFIX + '/actinia_templates/' + templateUUID,
                            headers=self.user_auth_header,
                            data=json.dumps(pc_template),
                            content_type="application/json")

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')
        assert resp.json is True

    def test_1006_read_update(self):
        """Test HTTP GET /actinia_templates/<template_id> of updated template
        """
        global templateUUID

        respStatusCode = 200

        resp = self.app.get(URL_PREFIX + '/actinia_templates/' + templateUUID,
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

        with open('tests/resources/actinia_templates/pc_tpl2.json') as file:
            pc_template = json.load(file)
        pc_template['id'] = templateUUID
        assert resp.json == pc_template

    def test_1007_read_all_after_create(self):
        """Test HTTP GET /actinia_templates and compares number of templates
        from before (+1)
        """
        global allTemplatesCount

        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + '/actinia_templates',
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

        assert type(resp.json) is list
        assert len(resp.json) == (allTemplatesCount + 1)

    def test_1008_delete(self):
        """Test HTTP DELETE /actinia_templates/<template_id> (deletion)"""
        global templateUUID

        respStatusCode = 200
        resp = self.app.delete(URL_PREFIX + '/actinia_templates/'
                               + templateUUID,
                               headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')
        assert resp.json is True

    def test_1009_read_all_after_delete(self):
        """Test HTTP GET /actinia_templates and compares number of templates
        from before (-1)
        """
        global allTemplatesCount

        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + '/actinia_templates',
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

        assert type(resp.json) is list
        assert len(resp.json) == allTemplatesCount

    def test_1010_read_fail(self):
        """Test HTTP GET /actinia_templates/<template_id> of non-existing
        template
        """
        respStatusCode = 404
        resp = self.app.get(URL_PREFIX + '/actinia_templates/not_exist',
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

    def test_1011_update_fail(self):
        """Test HTTP PUT /actinia_templates/<template_id> (update) of
        non-existing template
        """
        global templateUUID
        respStatusCode = 404

        with open('tests/resources/actinia_templates/pc_tpl.json') as file:
            pc_template = json.load(file)
        pc_template['id'] = templateUUID

        resp = self.app.put(URL_PREFIX + '/actinia_templates/not_exist',
                            headers=self.user_auth_header,
                            data=json.dumps(pc_template),
                            content_type="application/json")

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

    def test_1012_delete_fail(self):
        """Test HTTP DELETE /actinia_templates/<template_id> (deletion) of
        non-existing template
        """
        respStatusCode = 404
        resp = self.app.delete(URL_PREFIX + '/actinia_templates/not_exist',
                               headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

    def test_1013_read_global_template(self):
        """Test HTTP GET /actinia_templates/<template_id> of global template"""
        respStatusCode = 200
        # path = 'tests/resources/actinia_templates/user_default_value.json'

        resp = self.app.get(URL_PREFIX + '/actinia_templates/default_value',
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

        # with open(path) as file:
        #     pc_template = json.load(file)
        # pc_template['id'] = 'default_value'
        # TODO: compare to file
        # assert resp.json[0]['template'] == pc_template['template']
