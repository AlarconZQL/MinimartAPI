from app.models import db
from app.models.store_workingday import store_workingday


class Store(db.Model):
    """Data model for stores"""
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    logo_url = db.Column(db.String(255))
    address = db.Column(db.String(255))
    products = db.relationship('ProductStoreLink', back_populates='store')
    workingdays = db.relationship(
        'WorkingDay', secondary=store_workingday, back_populates='stores')
    vouchers = db.relationship('Voucher', back_populates='store')

    def __repr__(self):
        return f'<Store {self.name}>'
