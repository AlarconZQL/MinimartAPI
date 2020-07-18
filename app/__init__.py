from flask import Flask
from .extensions import db


def create_app():
    """Create main application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coco-minimart.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    """Initialize plugins"""
    db.init_app(app)
    with app.app_context():
        from .models import Product, Category
        db.create_all()
        return app
