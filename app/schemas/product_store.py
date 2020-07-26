from app import ma
from app.schemas.product import ProductSchema
from app.models import ProductStoreLink


class ProductStockSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProductStoreLink
        ordered = True

    product = ma.Nested(ProductSchema)
    stock = ma.auto_field()
