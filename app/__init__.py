"""Flask application factory for MenuMargin Optimizer."""

from flask import Flask
from app.routes import api_bp


def create_app() -> Flask:
    """Create and configure the Flask application instance."""
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    return app
