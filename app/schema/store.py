from . import ma
from .product_store import ProductStockSchema
from ..models import Store


class StoreProductsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Store
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    products = ma.List(ma.Nested(ProductStockSchema))


class StoreDetailSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Store
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    address = ma.auto_field()
    logo_url = ma.auto_field()
