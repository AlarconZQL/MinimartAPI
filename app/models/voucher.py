from . import db


class Voucher(db.Model):
    """Data model for vouchers"""
    __tablename__ = 'voucher'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), nullable=False, unique=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    only_on_days = db.relationship('VoucherDay', back_populates='voucher')
    store = db.relationship('Store', back_populates='vouchers')
    products = db.relationship('ProductVoucherLink', back_populates='voucher')

    def __repr__(self):
        return '<Voucher {}>'.format(self.code)
