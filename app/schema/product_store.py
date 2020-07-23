from . import ma
from .product import ProductSchema
from ..models import ProductStoreLink


class ProductStockSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProductStoreLink
        ordered = True

    product = ma.Nested(ProductSchema)
    stock = ma.auto_field()
