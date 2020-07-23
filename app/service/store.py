import calendar
from datetime import date
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

    @staticmethod
    def get_stores_opened_today_at(time):
        print('Received time', time)
        today_name = calendar.day_name[date.today().weekday()]
        #print('Today name', today_name)
        stores = Store.query.all()
        opened_stores = []
        for store in stores:
            print('Store', store.name)
            today_workindays = list(
                filter(lambda current: current.day.name == today_name, store.workingdays))
            print('Today workingdays', today_workindays)
            for workingday in today_workindays:
                if workingday.starts_at <= time and time <= workingday.finishes_at:
                    opened_stores.append(store)
                    break
        print('Today (', today_name, ') at', time,
              'the following stores are opened:', opened_stores)
        return opened_stores

    @staticmethod
    def get_all_stores():
        return Store.query.all()

    @staticmethod
    def get_available_products_for_store(store_id):
        store = Store.query.get(store_id)
        if store != None:
            availables = list(
                filter(lambda link: link.stock > 0, store.products))
            return ({
                'name': store.name,
                'id': store.id,
                'products': availables
            })
        else:
            return None
