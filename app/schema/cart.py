from . import ma
from ..models import Cart
from app.schema.cart_product import CartProductSchema


class CartCreatedSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cart

    id = ma.auto_field()
    store_id = ma.auto_field()


class CartSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cart
        ordered = True

    id = ma.auto_field()
    store_id = ma.auto_field()
    products = ma.List(ma.Nested(CartProductSchema))
