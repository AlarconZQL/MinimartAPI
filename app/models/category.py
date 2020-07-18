from . import db


class Category(db.Model):
    """Data model for product categories"""

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(100),
                     nullable=False,
                     unique=True)

    def __repr__(self):
        return '<Category {}>'.format(self.name)
