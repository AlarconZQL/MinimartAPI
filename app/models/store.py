from . import db


class Store(db.Model):
    """Data model for stores"""
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    logo_url = db.Column(db.String(255))
    address = db.Column(db.String(255))
    products = db.relationship('ProductStoreLink', back_populates='store')

    def __repr__(self):
        return '<Store {}>'.format(self.name)
