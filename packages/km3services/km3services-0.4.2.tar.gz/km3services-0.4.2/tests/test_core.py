#!/usr/bin/env python3
import unittest

from km3services.core import KM3Service


class TestKM3Service:
    def test_km3service(self):
        class AService(KM3Service):
            pass

        server = "a_server"
        port = 12345
        protocol = "https"

        a_service = AService(server, port, protocol)

        assert a_service.server == server
        assert a_service.port == port
        assert a_service.protocol == protocol
        assert a_service.url == "https://a_server:12345"
