from app.models import Store, Product, ProductStoreLink


class StoreService:
    @staticmethod
    def get_available_products_per_store():
        stores = Store.query.all()
        result = []
        for store in stores:
            availables = list(
                filter(lambda link: link.stock > 0, store.products))
            result.append({
                'name': store.name,
                'id': store.id,
                'products': availables
            })
        return result
