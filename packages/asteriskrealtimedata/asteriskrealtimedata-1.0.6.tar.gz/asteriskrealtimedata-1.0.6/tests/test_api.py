import unittest
from AsteriskRealtimeData.api import Api


class TestAPI(unittest.TestCase):
    def test_pause_reason_list(self):
        result = Api.PauseReason.list()
        print(result)
        self.assertIsNotNone(result)
