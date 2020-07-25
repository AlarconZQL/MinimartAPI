from flask import Flask
from .extensions import db, ma
from .apis import api


def create_app(settings_module):
    """Create main application"""
    app = Flask(__name__)

    # Load the config file specified by APP_ENV
    app.config.from_object(settings_module)

    # Initialize plugins
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)

    return app
