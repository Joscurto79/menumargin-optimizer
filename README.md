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
