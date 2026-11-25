# MenuMargin Optimizer

A stateless REST microservice that evaluates restaurant dish unit economics (VAT extraction, spoilage-adjusted cost, food cost percentage, and contribution margin) and simulates wholesale supplier price shocks.

---

## Architecture & Project Structure

```text
menumargin-optimizer/
├── app/
│   ├── __init__.py          # Flask application factory (create_app)
│   ├── optimizer.py         # Core unit-economics math, validation & classification engine
│   └── routes.py            # HTTP REST endpoints (/health, /api/v1/evaluate-dish)
├── tests/
│   ├── __init__.py
│   ├── test_optimizer.py    # Unit tests for business logic & boundary conditions
│   └── test_routes.py       # HTTP integration tests via Flask test_client()
├── .gitignore
├── Dockerfile               # Production container recipe (Python 3.12-slim + Gunicorn)
├── README.md
├── requirements.txt         # Pinned dependencies (Flask 3.0.3, Gunicorn 22.0.0)
└── run.py                   # Local development server entry point (127.0.0.1:5000)

Business Rules & Classification Matrix
Unit-Economics Formulas
Net Price (HT): dish_price_ttc / (1 + vat_rate)

Effective Cost: dish_cost / (1 - spoilage_rate)

Food Cost %: (effective_cost / net_price_ht) * 100

Contribution Margin: net_price_ht - effective_cost

Projected Effective Cost (Wholesale Shock): effective_cost * (1 + wholesale_change_pct)

Priority,Classification,Trigger Condition,Business Action
1,Menu_Removal,food_cost_pct > 35.0% OR contribution_margin < 5.00,Remove dish or overhaul portioning/recipe immediately.
2,Reprice_Alert,30.0% < food_cost_pct <= 35.0% OR 5.00 <= contribution_margin < 8.00,Increase menu price or renegotiate supplier cost.
3,Star_Performer,food_cost_pct <= 30.0% AND contribution_margin >= 8.00,Healthy margin; promote on menu.

Gherkin
Feature: Evaluate dish margin and simulate wholesale supplier price shock

  Scenario: Profitable dish triggers a reprice alert under a +30% wholesale shock
    Given a dish "Grilled Sea Bass" priced at 22.00 TTC with 10% VAT, 4.00 base cost, and 20% spoilage
    When the API evaluates the dish with a +30% wholesale cost shock
    Then the baseline classification is "Star_Performer" (25.0% food cost, 15.00 margin)
    And the projected classification shifts to "Reprice_Alert" (32.5% food cost, 13.50 margin)

  Scenario: Missing mandatory input fields are rejected
    Given a request payload missing required pricing or cost fields
    When the client sends a POST request to /api/v1/evaluate-dish
    Then the service returns HTTP 400 Bad Request with a descriptive error message

API Reference
1. Health Check
Endpoint: GET /health

Response (200 OK):
{
  "status": "healthy",
  "service": "menumargin-optimizer",
  "engine_version": "1.0.0"
}
