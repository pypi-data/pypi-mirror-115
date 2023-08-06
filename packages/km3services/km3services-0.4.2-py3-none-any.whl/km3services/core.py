#!/usr/bin/env python3


class KM3Service:
    """Base class for a KM3NeT service"""

    def __init__(self, server, port, protocol="http"):
        self._server = server
        self._port = port
        self._protocol = protocol

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, value):
        self._server = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        self._protocol = value

    @property
    def url(self):
        return f"{self.protocol}://{self.server}:{self.port}"
