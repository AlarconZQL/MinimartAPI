from . import db

category_product = db.Table('category_product',
                            db.Column('product_id', db.Integer,
                                      db.ForeignKey('product.id'), primary_key=True),
                            db.Column('category_id', db.Integer,
                                      db.ForeignKey('category.id'), primary_key=True))
