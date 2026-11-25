import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

class MonitorTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_dashboard_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cloud Deployment Monitor", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")

    def test_metrics_endpoint(self):
        response = self.client.get("/api/metrics")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        for key in ("cpu_percent", "memory_percent", "uptime", "request_count", "logs"):
            self.assertIn(key, data)

    def test_demo_event(self):
        response = self.client.get("/api/event?message=test-event")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["ok"])

if __name__ == "__main__":
    unittest.main()
