from . import ma
from .product import ProductSchema
from ..models import CartProductLink


class CartProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CartProductLink
        ordered = True

    product = ma.Nested(ProductSchema)
    units = ma.auto_field()
