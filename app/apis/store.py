from flask_restx import Namespace, Resource
from app import db
from app.service import StoreService
from app.schema import StoreProductsSchema

api = Namespace('store', description='Store\'s operations')

store_products_schema = StoreProductsSchema(many=True)


@api.route('/product')
class StoreAvailableProducts(Resource):
    @api.response(200, 'Success')
    def get(self):
        '''Get all available products on each store'''
        stores_available_products = StoreService.get_available_products_per_store()
        result = store_products_schema.dump(stores_available_products)
        return result, 200
