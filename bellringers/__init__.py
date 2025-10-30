"""
Bell Ringers Flask Blueprint
A community-driven CS bell ringer generator with Lock & Spin mechanics
"""
from flask import Blueprint
from .routes import bp
from .admin_routes import admin_bp


def init_app(app):
    """Initialize the blueprint with the Flask app"""
    app.register_blueprint(bp)
    app.register_blueprint(admin_bp)
