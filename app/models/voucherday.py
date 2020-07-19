from sqlalchemy import UniqueConstraint
from . import db
from ..utils import Days


class VoucherDay(db.Model):
    """Data model for voucher's day"""
    __tablename__ = 'voucherday'
    __table_args__ = (UniqueConstraint(
        'day', 'voucher_id', name='_voucherday_uc'),)
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Enum(Days), nullable=False)
    voucher_id = db.Column(db.Integer, db.ForeignKey(
        'voucher.id'), nullable=False)
    voucher = db.relationship('Voucher', back_populates='only_on_days')

    def __repr__(self):
        return '<VoucherDay {} {}>'.format(self.voucher_id, self.day)
