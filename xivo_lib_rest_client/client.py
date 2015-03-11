# -*- coding: utf-8 -*-

# Copyright (C) 2014-2015 Avencall
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
import logging

from functools import partial
from requests import Session
from stevedore import extension

logger = logging.getLogger(__name__)


class _SessionBuilder(object):

    def __init__(self, host, port, version, username, password, https, timeout):
        self.scheme = 'https' if https else 'http'
        self.host = host
        self.port = port
        self.version = version
        self.username = username
        self.password = password
        self.timeout = timeout

    def session(self):
        session = Session()
        if self.timeout is not None:
            session.request = partial(session.request, timeout=self.timeout)
        if self.scheme == 'https':
            session.verify = False
        if self.username and self.password:
            session.auth = requests.auth.HTTPDigestAuth(self.username, self.password)
        session.headers = {'Connection': 'close'}
        return session

    def url(self, resource=None):
        return '{scheme}://{host}:{port}/{version}/{resource}'.format(scheme=self.scheme,
                                                                      host=self.host,
                                                                      port=self.port,
                                                                      version=self.version,
                                                                      resource=resource or '')


class _Client(object):

    def __init__(self, namespace, session_builder):
        self._namespace = namespace
        self._session_builder = session_builder
        self._load_plugins()

    def _load_plugins(self):
        extension_manager = extension.ExtensionManager(self._namespace)
        try:
            extension_manager.map(self._add_command_to_client)
        except RuntimeError:
            logger.warning('No commands found')

    def _add_command_to_client(self, extension):
        command = extension.plugin(self._session_builder)
        setattr(self, extension.name, command)


def new_client_factory(ns, port, version):

    def new_client(host='localhost', port=port, version=version,
                   username=None, password=None, https=False, timeout=10):
        session_builder = _SessionBuilder(host, port, version, username, password, https, timeout)
        return _Client(ns, session_builder)

    return new_client
