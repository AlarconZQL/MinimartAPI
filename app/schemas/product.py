from app import ma
from app.models import Product


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
