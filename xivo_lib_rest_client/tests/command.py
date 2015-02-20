# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import unittest
from mock import Mock
from requests.exceptions import HTTPError


class HTTPCommandTestCase(unittest.TestCase):

    scheme = 'http'
    host = 'xivo.io'
    port = 9486
    version = '1.0'

    def setUp(self):
        self.session_builder = Mock()
        self.session = self.session_builder.session.return_value
        self.command = self.Command(self.session_builder)
        self.base_url = self.command.base_url

    def assertRaisesHTTPError(self, function, *args, **kwargs):
        self.assertRaises(HTTPError, function, *args, **kwargs)

    @staticmethod
    def new_response(status_code, json=None):
        response = Mock()
        response.status_code = status_code
        response.raise_for_status.side_effect = HTTPError()
        if json is None:
            response.json.side_effect = ValueError()
        else:
            response.json.return_value = json
        return response
