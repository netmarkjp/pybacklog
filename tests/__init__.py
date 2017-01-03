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
