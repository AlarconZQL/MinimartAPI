from app import ma
from app.schemas.product import ProductSchema
from app.models import CartProductLink


class CartProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CartProductLink
        ordered = True

    product = ma.Nested(ProductSchema)
    units = ma.auto_field()
