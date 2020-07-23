from . import db
from .category_product import category_product


class Product(db.Model):
    """Data model for products"""
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Float)
    description = db.Column(db.String(255))
    categories = db.relationship(
        'Category', secondary=category_product, back_populates='products')
    stores = db.relationship('ProductStoreLink', back_populates='product')
    vouchers = db.relationship('ProductVoucherLink', back_populates='product')
    carts = db.relationship('CartProductLink', back_populates='product')

    def __repr__(self):
        return '<Product {}>'.format(self.name)
