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

import requests

from requests import Session
from stevedore import extension


class _HTTPCommandProxy(object):

    def __init__(self, host, port, version, username, password, Command):
        use_https = username is not None and password is not None
        self.command = Command(host, port, version, use_https)
        self.username = username
        self.password = password

    def __call__(self, *args, **kwargs):
        return self._query_url(self.command)(*args, **kwargs)

    def __getattr__(self, name):
        return self._query_url(getattr(self.command, name))

    def _query_url(self, callable_):
        def decorated(*args, **kwargs):
            session = Session()
            if self.username and self.password:
                session.verify = False
                session.auth = requests.auth.HTTPDigestAuth(self.username, self.password)
            # headers
            # ...
            return callable_(session, *args, **kwargs)
        return decorated


class _BaseClient(object):

    @property
    def namespace(self):
        raise NotImplementedError('The implementation of a command must have a namespace field')

    def __init__(self, host='localhost', port=9487, version='1.1', username=None, password=None):
        self._host = host
        self._port = port
        self._version = version
        self._username = username
        self._password = password
        self._load_plugins()

    def _load_plugins(self):
        extension_manager = extension.ExtensionManager(self.namespace)
        extension_manager.map(self._add_command_to_client)

    def _add_command_to_client(self, extension):
        self.__setattr__(extension.name, _HTTPCommandProxy(self._host,
                                                           self._port,
                                                           self._version,
                                                           self._username,
                                                           self._password,
                                                           extension.plugin))


def make_client(ns):

    class Client(_BaseClient):
        namespace = ns

    return Client
