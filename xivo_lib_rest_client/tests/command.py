# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

import unittest
from mock import Mock, sentinel
from requests.exceptions import HTTPError


class HTTPCommandTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Mock()
        self.client.timeout = sentinel.timeout
        self.session = self.client.session.return_value
        self.session.headers = {}
        self.command = self.Command(self.client)

    def assertRaisesHTTPError(self, function, *args, **kwargs):
        self.assertRaises(HTTPError, function, *args, **kwargs)

    @staticmethod
    def new_response(status_code, json=None, body=None):
        response = Mock()
        response.status_code = status_code
        response.raise_for_status.side_effect = HTTPError()
        if json is not None:
            response.json.return_value = json
        elif body is not None:
            response.text = body
            response.content = body
        else:
            response.json.side_effect = ValueError()
        return response

    def set_response(self, action, status_code, body=None):
        mock_action = getattr(self.session, action)
        mock_action.return_value = self.new_response(status_code, json=body)
        return body

    def assert_request_sent(self, action, url, **kwargs):
        mock_action = getattr(self.session, action)
        mock_action.assert_called_once_with(url, **kwargs)


class RESTCommandTestCase(HTTPCommandTestCase):

    scheme = 'http'
    host = 'wazo.community'
    port = 9486
    version = '1.0'

    def setUp(self):
        super(RESTCommandTestCase, self).setUp()
        self.base_url = self.command.base_url
