from ..models import ProductStoreLink, Product


class ProductService:
    @staticmethod
    def get_all_products():
        return Product.query.all()

    @staticmethod
    def get_product_info_for_store(product_id, store_id):
        link = ProductStoreLink.query.filter_by(
            store_id=store_id, product_id=product_id).first()
        if link != None and link.stock > 0:
            return link
        return None
