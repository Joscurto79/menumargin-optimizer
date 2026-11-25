"""Core unit-economics calculation, validation, and classification engine."""

ENGINE_VERSION = "1.0.0"

REQUIRED_FIELDS = (
    "dish_id",
    "dish_name",
    "dish_price_ttc",
    "vat_rate",
    "dish_cost",
)


def classify_dish(food_cost_pct: float, contribution_margin: float) -> str:
    """Classify dish profitability using strict top-down precedence rules."""
    if food_cost_pct > 35.0 or contribution_margin < 5.0:
        return "Menu_Removal"
    if food_cost_pct > 30.0 or contribution_margin < 8.0:
        return "Reprice_Alert"
    return "Star_Performer"


def evaluate_dish(payload: dict) -> dict:
    """Validate dish inputs, compute unit economics, and simulate price shocks."""
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a JSON object.")

    missing = [field for field in REQUIRED_FIELDS if field not in payload]
    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(missing)}")

    dish_id = str(payload["dish_id"]).strip()
    dish_name = str(payload["dish_name"]).strip()
    if not dish_id or not dish_name:
        raise ValueError("dish_id and dish_name must be non-empty strings.")

    try:
        dish_price_ttc = float(payload["dish_price_ttc"])
        vat_rate = float(payload["vat_rate"])
        dish_cost = float(payload["dish_cost"])
        spoilage_rate = float(payload.get("spoilage_rate", 0.0))
        wholesale_change_pct = float(payload.get("wholesale_change_pct", 0.0))
    except (TypeError, ValueError) as exc:
        raise ValueError("Numeric pricing, cost, and rate fields must be valid numbers.") from exc

    if dish_price_ttc <= 0:
        raise ValueError("dish_price_ttc must be strictly positive.")
    if vat_rate < 0 or vat_rate >= 1.0:
        raise ValueError("vat_rate must be between 0.0 and less than 1.0.")
    if dish_cost < 0:
        raise ValueError("dish_cost cannot be negative.")
    if spoilage_rate < 0 or spoilage_rate >= 1.0:
        raise ValueError("spoilage_rate must be between 0.0 and less than 1.0.")
    if wholesale_change_pct <= -1.0:
        raise ValueError("wholesale_change_pct must be greater than -1.0.")

    # Baseline unit economics
    net_price_ht = dish_price_ttc / (1.0 + vat_rate)
    effective_cost = dish_cost / (1.0 - spoilage_rate)
    food_cost_pct = (effective_cost / net_price_ht) * 100.0
    contribution_margin = net_price_ht - effective_cost
    classification = classify_dish(food_cost_pct, contribution_margin)

    # Wholesale supplier shock simulation
    projected_effective_cost = effective_cost * (1.0 + wholesale_change_pct)
    projected_food_cost_pct = (projected_effective_cost / net_price_ht) * 100.0
    projected_contribution_margin = net_price_ht - projected_effective_cost
    projected_classification = classify_dish(
        projected_food_cost_pct, projected_contribution_margin
    )

    return {
        "dish_id": dish_id,
        "dish_name": dish_name,
        "engine_version": ENGINE_VERSION,
        "net_price_ht": round(net_price_ht, 2),
        "effective_cost": round(effective_cost, 2),
        "food_cost_pct": round(food_cost_pct, 2),
        "contribution_margin": round(contribution_margin, 2),
        "classification": classification,
        "projected_effective_cost": round(projected_effective_cost, 2),
        "projected_food_cost_pct": round(projected_food_cost_pct, 2),
        "projected_contribution_margin": round(projected_contribution_margin, 2),
        "projected_classification": projected_classification,
    }
