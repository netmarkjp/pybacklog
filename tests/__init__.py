# -*- coding: utf-8 -*-

from pybacklog import BacklogClient
import unittest


class TestBacklogClient(unittest.TestCase):

    def test_init(self):
        client = BacklogClient("my_space_name", "my_api_key")
        self.assertEqual(client.space_name, "my_space_name")
        self.assertEqual(client.api_key, "my_api_key")
        self.assertEqual(
            client.endpoint, "https://my_space_name.backlog.jp/api/v2/{path}")

    def test_remove_mb4(self):
        testing = (
            (
                {"equal1": u"あいう", "equal2": u"123１２３"},
                {"equal1": u"あいう", "equal2": u"123１２３"}
            ),
            (
                {"replaced1": u"あい💔", "replaced2": u"123♥２３"},
                {"replaced1": u"あい\uFFFD", "replaced2": u"123♥２３"}
            ),
        )
        for t in testing:
            self.assertEqual(BacklogClient.remove_mb4(t[0]), t[1])
