# -*- coding: utf-8 -*-
#
#   UDP: User Datagram Protocol
#
#                                Written in 2020 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2020 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from abc import ABC
from typing import Optional

from tcp import BaseHub

from ..mtp import Package

from .pack_conn import PackageConnection


class BasePackageHub(BaseHub, ABC):

    def get_package_connection(self, remote: tuple, local: tuple) -> Optional[PackageConnection]:
        conn = self.connect(remote=remote, local=local)
        if isinstance(conn, PackageConnection):
            return conn

    def receive_package(self, source: tuple, destination: tuple) -> Optional[Package]:
        conn = self.get_package_connection(remote=source, local=destination)
        if conn is not None:
            try:
                return conn.receive_package(source=source, destination=destination)
            except IOError as error:
                print('PackageHub error: %s' % error)

    def send_package(self, pack: Package, source: tuple, destination: tuple) -> bool:
        conn = self.get_package_connection(remote=source, local=destination)
        if conn is not None:
            try:
                conn.send_package(pack=pack, source=source, destination=destination)
                return True
            except IOError as error:
                print('PackageHub error: %s' % error)
