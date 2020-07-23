from sqlalchemy import UniqueConstraint
from . import db


class Cart(db.Model):
    """Data model for shopping carts"""
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    products = db.relationship('CartProductLink', back_populates='cart')

    def __repr__(self):
        return '<Cart {}, store_id {}>'.format(self.name, self.store_id)
