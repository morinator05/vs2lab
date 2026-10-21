"""
Unit tests for the server backend
"""

import unittest

import clientserver

# pylint: disable=protected-access


class TestBackend(unittest.TestCase):
    """Tests the backend directly, without sockets"""
    # create server instance without __init__, so no socket gets bound
    _server = clientserver.Server.__new__(clientserver.Server)

    def test_get(self):
        """GET returns the number of a known name"""
        self.assertEqual(self._server.handle_request("GET jack"), "4098")

    def test_get_unknown_name(self):
        """GET with an unknown name reports it as not found"""
        self.assertEqual(self._server.handle_request("GET bob"), "Name not found")

    def test_get_all(self):
        """GETALL returns the whole directory"""
        self.assertEqual(self._server.handle_request("GETALL"),
                         str(clientserver.Server._tel))


if __name__ == '__main__':
    unittest.main()
