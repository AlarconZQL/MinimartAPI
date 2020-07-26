from flask import Flask
from app.extensions import db, ma
from app.apis import api


def create_app(settings_module):
    """Creates an application instance based on the specified settings"""
    app = Flask(__name__)

    # Load config file
    app.config.from_object(settings_module)

    # Initialize plugins
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)

    return app
