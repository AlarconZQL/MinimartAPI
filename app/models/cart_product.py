from . import db


class CartProductLink(db.Model):
    """Data model for cart-product link"""
    __tablename__ = 'cart_product'
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey(
        'cart.id'), primary_key=True)
    units = db.Column(db.Integer)
    product = db.relationship("Product", back_populates="carts")
    cart = db.relationship("Cart", back_populates="products")
