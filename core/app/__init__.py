"""
Music API - Core API Service.
Supports local-first "Zero-Gate" access for developers.
"""
from flask import Flask
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restx import Api
from pathlib import Path

from .config import get_config

# Extensions
db = SQLAlchemy()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per minute"]
)

# API with Swagger documentation
api = Api(
    title='🎵 Music API Core',
    version='1.0.0',
    description='''
A frictionless REST API for music streaming based on YouTube Music.

## Zero-Gate Access
This API is designed for local development. By default, it allows anonymous access without API keys.

## Quick Integration
You can use the official Python SDK or simple curl commands to integrate this into your apps.
    ''',
    doc='/docs',
    prefix='/api/v1'
)


def create_app(config_class=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    limiter.init_app(app)
    api.init_app(app)
    
    # Ensure necessary directories exist
    app.config['LYRICS_CACHE_DIR'].mkdir(parents=True, exist_ok=True)
    
    # Ensure database directory exists
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if db_uri.startswith('sqlite:///'):
        db_path = Path(db_uri.replace('sqlite:///', ''))
        if not db_path.is_absolute():
            db_path = app.config['BASE_DIR'] / db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Register error handlers
    from .middleware.error_handler import register_error_handlers
    register_error_handlers(app)

    # Register usage logger
    # from .middleware.usage import register_usage_logger
    # register_usage_logger(app)
    
    # Register blueprints
    from .routes import register_blueprints
    register_blueprints(app)
    
    # Register namespaces
    from .routes import register_namespaces
    register_namespaces(api)
    
    # Import models explicitly
    from . import models
    
    with app.app_context():
        db.create_all()
    
    return app
