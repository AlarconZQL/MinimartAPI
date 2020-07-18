from . import db

categories = db.Table('categories',
                      db.Column('product_id',
                                db.Integer,
                                db.ForeignKey('product.id'),
                                primary_key=True),
                      db.Column('category_id',
                                db.Integer,
                                db.ForeignKey('category.id'),
                                primary_key=True))


class Product(db.Model):
    """Data model for products"""

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(100),
                     nullable=False,
                     unique=True)
    price = db.Column(db.Numeric(8, 2))
    categories = db.relationship('Category',
                                 secondary=categories,
                                 lazy='subquery',
                                 backref=db.backref('products', lazy=True))

    def __repr__(self):
        return '<Product {}>'.format(self.name)
