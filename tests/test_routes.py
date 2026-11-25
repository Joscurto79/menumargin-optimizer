"""HTTP integration tests for MenuMargin Optimizer Flask routes."""

import unittest
from app import create_app


class TestApiRoutes(unittest.TestCase):
    """Verify HTTP status codes, JSON responses, and error handling."""

    def setUp(self):
        """Create a fresh Flask test client before each test."""
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_endpoint_returns_200(self):
        """GET /health should return 200 OK with service status."""
        response = self.client.get("/health")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "healthy")

    def test_evaluate_dish_happy_path_returns_200(self):
        """POST /api/v1/evaluate-dish with valid JSON returns 200 and classification."""
        payload = {
            "dish_id": "DISH-402",
            "dish_name": "Grilled Sea Bass",
            "dish_price_ttc": 22.0,
            "vat_rate": 0.10,
            "dish_cost": 4.0,
            "spoilage_rate": 0.20,
            "wholesale_change_pct": 0.30,
        }
        response = self.client.post("/api/v1/evaluate-dish", json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["classification"], "Star_Performer")
        self.assertEqual(data["projected_classification"], "Reprice_Alert")

    def test_evaluate_dish_missing_field_returns_400(self):
        """POST /api/v1/evaluate-dish with incomplete payload returns 400 Bad Request."""
        bad_payload = {"dish_id": "DISH-999"}
        response = self.client.post("/api/v1/evaluate-dish", json=bad_payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)

    def test_evaluate_dish_malformed_json_returns_400(self):
        """POST /api/v1/evaluate-dish with non-JSON body returns 400 Bad Request."""
        response = self.client.post(
            "/api/v1/evaluate-dish",
            data="not-valid-json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
