import unittest
from MZscript import MZClient

class TestClient(unittest.TestCase):
    def test_init(self):
        bot = MZClient(db_warns=True, debug_log=True, debug_console=True)
        self.assertIsInstance(bot, MZClient)

if __name__ == "__main__":
    unittest.main()