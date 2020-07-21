from flask import Flask
from .extensions import db, ma
from .apis import api


def create_app():
    """Create main application"""
    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coco-minimart.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    """Initialize plugins"""
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)

    with app.app_context():
        from .models import Product, Category, Store, WorkingDay, Voucher, VoucherDay
        from .models import ProductStoreLink, ProductVoucherLink
        db.create_all()
        return app
