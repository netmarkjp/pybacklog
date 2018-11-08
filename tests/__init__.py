# -*- coding: utf-8 -*-

from pybacklog import BacklogClient
import unittest


class TestBacklogClient(unittest.TestCase):

    def test_init(self):
        try:
            client = BacklogClient("my_space_name", "my_api_key")
            self.fail()
        except Exception as _ex:
            self.assertEqual(str(_ex), "retrive space information failed. maybe space not found in .com nor .jp")

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
