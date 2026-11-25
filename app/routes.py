"""HTTP REST API routes for MenuMargin Optimizer."""

from flask import Blueprint, jsonify, request
from app.optimizer import ENGINE_VERSION, evaluate_dish

api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def health_check():
    """Liveness probe endpoint."""
    return jsonify(
        {
            "status": "healthy",
            "service": "menumargin-optimizer",
            "engine_version": ENGINE_VERSION,
        }
    ), 200


@api_bp.post("/api/v1/evaluate-dish")
def evaluate_dish_endpoint():
    """Evaluate dish unit economics and supplier shock scenario."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Request body must be a valid JSON object."}), 400

    try:
        result = evaluate_dish(payload)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(result), 200
