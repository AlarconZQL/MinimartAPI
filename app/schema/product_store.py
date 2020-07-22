from . import ma
from .product import ProductSchema
from ..models import ProductStoreLink


class StockSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProductStoreLink

    product = ma.Nested(ProductSchema)
    stock = ma.auto_field()
