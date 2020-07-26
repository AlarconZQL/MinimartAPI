from app.models import db
from app.models.category_product import category_product


class Category(db.Model):
    """Data model for product categories"""
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    products = db.relationship(
        'Product', secondary=category_product, back_populates='categories')

    def __repr__(self):
        return f'<Category {self.name}>'
