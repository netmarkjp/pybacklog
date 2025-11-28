# -*- coding: utf-8 -*-

from pybacklog import BacklogClient
import unittest
from unittest.mock import patch


class TestBacklogClient(unittest.TestCase):
    def test_init(self):
        # pass
        BacklogClient("my_space_name", "my_api_key")

        # raise exception
        with patch("pybacklog.requests.get") as mock_get:
            mock_get.side_effect = Exception("retrive space information failed. maybe space not found in .com nor .jp")
            try:
                BacklogClient("my_space_name", "my_api_key").endpoint()
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
