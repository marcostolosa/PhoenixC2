from phoenixc2.server.web import create_web
from phoenixc2.server.commander import Commander
import unittest
import os


class LogsTest(unittest.TestCase):
    def setUp(self):
        os.environ["PHOENIX_TEST"] = "true"
        self.app = create_web(Commander())
        self.client = self.app.test_client()

    def test_logs(self):
        response = self.client.get("/logs?json=true", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(response.is_json, True)


if __name__ == "__main__":
    unittest.main()
