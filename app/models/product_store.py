from . import db


class ProductStoreLink(db.Model):
    """Data model for product-store link"""
    __tablename__ = 'product_store'
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey(
        'store.id'), primary_key=True)
    stock = db.Column(db.Integer)
    product = db.relationship("Product", back_populates="stores")
    store = db.relationship("Store", back_populates="products")
