# -*- coding: utf-8 -*-

from pybacklog import BacklogClient
import unittest


class TestBacklogClient(unittest.TestCase):
    def test_init(self):
        try:
            _ = BacklogClient("my_space_name", "my_api_key")
            self.fail()
        except Exception as _ex:
            self.assertEqual(str(_ex), "retrive space information failed. maybe space not found in .com nor .jp")

    def test_remove_mb4(self):
        testing = (
            ({"equal1": "あいう", "equal2": "123１２３"}, {"equal1": "あいう", "equal2": "123１２３"}),
            ({"replaced1": "あい💔", "replaced2": "123♥２３"}, {"replaced1": "あい\ufffd", "replaced2": "123♥２３"}),
        )
        for t in testing:
            self.assertEqual(BacklogClient.remove_mb4(t[0]), t[1])
