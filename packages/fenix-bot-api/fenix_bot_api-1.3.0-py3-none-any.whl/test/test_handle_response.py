import unittest
from fenix_bot_api.responses import handle_response

class TestResponse(unittest.TestCase):
    def test_handle_response(self):
        self.assertEqual(handle_response("status", False), "Running")

if __name__ == '__main__':
    unittest.main()