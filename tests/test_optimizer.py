"""Unit tests for MenuMargin Optimizer business logic."""

import unittest
from app.optimizer import evaluate_dish


class TestOptimizerLogic(unittest.TestCase):
    """Verify unit-economics calculations, classifications, and validation."""

    def test_star_performer_and_shock_reprice_alert(self):
        """Verify baseline Star_Performer shifts to Reprice_Alert under +30% shock."""
        payload = {
            "dish_id": "DISH-402",
            "dish_name": "Grilled Sea Bass",
            "dish_price_ttc": 22.0,
            "vat_rate": 0.10,
            "dish_cost": 4.0,
            "spoilage_rate": 0.20,
            "wholesale_change_pct": 0.30,
        }
        result = evaluate_dish(payload)

        self.assertEqual(result["net_price_ht"], 20.0)
        self.assertEqual(result["effective_cost"], 5.0)
        self.assertEqual(result["food_cost_pct"], 25.0)
        self.assertEqual(result["contribution_margin"], 15.0)
        self.assertEqual(result["classification"], "Star_Performer")
        self.assertEqual(result["projected_effective_cost"], 6.5)
        self.assertEqual(result["projected_food_cost_pct"], 32.5)
        self.assertEqual(result["projected_contribution_margin"], 13.5)
        self.assertEqual(result["projected_classification"], "Reprice_Alert")

    def test_default_optional_rates(self):
        """Verify spoilage_rate and wholesale_change_pct default to 0.0 when omitted."""
        payload = {
            "dish_id": "DISH-101",
            "dish_name": "Margherita Pizza",
            "dish_price_ttc": 13.2,
            "vat_rate": 0.10,
            "dish_cost": 3.0,
        }
        result = evaluate_dish(payload)

        self.assertEqual(result["net_price_ht"], 12.0)
        self.assertEqual(result["effective_cost"], 3.0)
        self.assertEqual(result["food_cost_pct"], 25.0)
        self.assertEqual(result["contribution_margin"], 9.0)
        self.assertEqual(result["classification"], "Star_Performer")
        self.assertEqual(result["projected_classification"], "Star_Performer")

    def test_classification_menu_removal_precedence(self):
        """Verify Menu_Removal triggers on either food_cost_pct > 35% or margin < 5.0."""
        high_cost_payload = {
            "dish_id": "DISH-201",
            "dish_name": "Prime Ribeye",
            "dish_price_ttc": 33.0,
            "vat_rate": 0.10,
            "dish_cost": 12.0,  # 12 / 30 = 40% food cost, margin = 18.0
        }
        result = evaluate_dish(high_cost_payload)
        self.assertEqual(result["classification"], "Menu_Removal")

    def test_classification_low_margin_menu_removal(self):
        """Verify Menu_Removal triggers when contribution margin < 5.0 despite low food cost %."""
        low_margin_payload = {
            "dish_id": "DISH-202",
            "dish_name": "Side Salad",
            "dish_price_ttc": 6.6,
            "vat_rate": 0.10,
            "dish_cost": 1.5,  # 1.5 / 6.0 = 25% food cost, margin = 4.50 (< 5.0)
        }
        result = evaluate_dish(low_margin_payload)
        self.assertEqual(result["classification"], "Menu_Removal")

    def test_invalid_spoilage_rate_raises_value_error(self):
        """Verify spoilage_rate >= 1.0 raises a descriptive ValueError."""
        invalid_payload = {
            "dish_id": "DISH-500",
            "dish_name": "Spoiled Dish",
            "dish_price_ttc": 15.0,
            "vat_rate": 0.10,
            "dish_cost": 4.0,
            "spoilage_rate": 1.0,
        }
        with self.assertRaises(ValueError):
            evaluate_dish(invalid_payload)


if __name__ == "__main__":
    unittest.main()
