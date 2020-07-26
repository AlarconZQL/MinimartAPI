from sqlalchemy import UniqueConstraint
from app.models import db


class Cart(db.Model):
    """Data model for shopping carts"""
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    products = db.relationship('CartProductLink', back_populates='cart')

    def __repr__(self):
        return f'<Cart {self.id}, store_id {self.store_id}>'
