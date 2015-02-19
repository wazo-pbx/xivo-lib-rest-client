# -*- coding: utf-8 -*-

# Copyright (C) 2014-20155555 Avencall
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

from ..base_http_command import BaseHTTPCommand
from hamcrest import assert_that
from hamcrest import equal_to
from mock import Mock


class TestBaseHTTPCommand(unittest.TestCase):

    def test_init_no_resource_specified(self):
        class NoResource(BaseHTTPCommand):
            pass

        self.assertRaises(NotImplementedError,
                          NoResource, Mock())

    def test_init_base_url_built(self):
        class TestCommand(BaseHTTPCommand):
            resource = 'test'

        session_builder = Mock()
        url = session_builder.url.return_value = 'https://example.com:9000/42/test'

        c = TestCommand(session_builder)

        assert_that(c.base_url, equal_to(url))
        session_builder.url.assert_called_once_with(TestCommand.resource)

    def test_raise_from_response_no_message(self):
        class ExpectedError(Exception):
            pass

        response = Mock(text='not a dict with message',
                        raise_for_status=Mock(side_effect=ExpectedError))

        self.assertRaises(ExpectedError, BaseHTTPCommand.raise_from_response, response)

    def test_raise_from_response_substitute_reason_for_the_message(self):
        class ExpectedError(Exception):
            pass

        response = Mock(text='{"message": "Expected reason"}',
                        raise_for_status=Mock(side_effect=ExpectedError))

        self.assertRaises(ExpectedError, BaseHTTPCommand.raise_from_response, response)
        assert_that(response.reason, equal_to('Expected reason'))
