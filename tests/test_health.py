import unittest

from fastapi.testclient import TestClient

from app import app


class HealthTests(unittest.TestCase):
    def test_health_returns_success(self):
        response = TestClient(app).get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
