import calendar
from datetime import date
from app.models import Store, Product, ProductStoreLink


class StoreService:
    @classmethod
    def get_available_products_per_store(cls):
        stores = cls.get_all_stores()
        result = []
        for store in stores:
            result.append(cls.get_store_available_products(store))
        return result

    @classmethod
    def get_store_available_products(cls, store):
        store_available_products = list(
            filter(lambda link: link.stock > 0, store.products))
        return ({
            'name': store.name,
            'id': store.id,
            'products': store_available_products
        })

    @classmethod
    def get_stores_opened_today_at(cls, time):
        today_name = calendar.day_name[date.today().weekday()]
        stores = cls.get_all_stores()
        opened_stores = []
        for store in stores:
            today_workindays = list(
                filter(lambda current: current.day.name == today_name, store.workingdays))
            for workingday in today_workindays:
                if workingday.starts_at <= time <= workingday.finishes_at:
                    opened_stores.append(store)
                    break
        return opened_stores

    @classmethod
    def get_all_stores(cls):
        return Store.query.all()

    @classmethod
    def get_store(cls, store_id):
        return Store.query.get(store_id)
