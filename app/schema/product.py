from . import ma
from ..models import Product


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
