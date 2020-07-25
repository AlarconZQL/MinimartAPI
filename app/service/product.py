from ..models import ProductStoreLink, Product, Store


class ProductService:
    @classmethod
    def get_product(cls, product_id):
        return Product.query.get(product_id)

    @classmethod
    def get_all_products(cls):
        return Product.query.all()

    @classmethod
    def get_product_info_for_store(cls, product_id, store_id):
        product_store_info = ProductStoreLink.query.filter_by(
            store_id=store_id, product_id=product_id).first()
        return product_store_info
