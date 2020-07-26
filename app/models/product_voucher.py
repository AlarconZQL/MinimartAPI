from app.models import db


class ProductVoucherLink(db.Model):
    """Data model for product-voucher link"""
    __tablename__ = 'product_voucher'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           primary_key=True)
    voucher_id = db.Column(db.Integer, db.ForeignKey('voucher.id'),
                           primary_key=True)
    discount = db.Column(db.Float, nullable=False)
    on_unit = db.Column(db.Integer, nullable=False)
    max_units = db.Column(db.Integer, nullable=False)
    product = db.relationship("Product", back_populates="vouchers")
    voucher = db.relationship("Voucher", back_populates="products")
