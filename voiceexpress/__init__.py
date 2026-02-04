"""VoiceExpress Flask application factory."""
from __future__ import annotations

from flask import Flask

from .routes import public_bp
from .auth import auth_bp
from .admin import admin_bp
from .api import api_bp


def create_app() -> Flask:
    """Create and configure the VoiceExpress Flask app."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "voiceexpress-secret"

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    return app
