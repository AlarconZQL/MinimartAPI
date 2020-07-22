from . import ma
from .product_store import StockSchema
from ..models import Store


class StoreProductsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Store
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    products = ma.List(ma.Nested(StockSchema))
