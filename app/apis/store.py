from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, abort
from app import db
from app.service import StoreService
from app.schema import StoreProductsSchema, StoreDetailSchema

api = Namespace('store', description='Store\'s operations')


@api.route('/product')
class StoreAvailableProducts(Resource):
    @api.response(200, 'Success')
    def get(self):
        """Get all available products from each store"""
        store_products_schema = StoreProductsSchema(many=True)
        stores_available_products = StoreService.get_available_products_per_store()
        result = store_products_schema.dump(stores_available_products)
        return result, 200


@api.doc(params={'openedAt':
                 {'description': 'Filter by those which are available'
                  'today at certain time', 'in': 'query',
                  'type': 'time(HH:MM)'}
                 })
@api.route('/')
class StoreList(Resource):

    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    def get(self):
        """Get stores basic information"""
        time_format = '%H:%M'
        opened_at = request.args.get('openedAt')
        if opened_at is not None:
            try:
                parsed_time = datetime.strptime(opened_at, time_format).time()
            except ValueError:
                error_message = '{} does not match {} format'.format(
                    opened_at, time_format)
                abort(400, error_message)
            opened_stores = StoreService.get_stores_opened_today_at(
                parsed_time)
            stores = opened_stores
        else:
            stores = StoreService.get_all_stores()
        stores_detail_schema = StoreDetailSchema(many=True)
        result = stores_detail_schema.dump(stores)
        return result, 200


@api.route('/<int:store_id>/product')
@api.param('store_id', 'The store identifier')
class StoreProductsList(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Resource not found')
    def get(self, store_id):
        """Get available products on a specific store"""
        store = StoreService.get_store(store_id)
        if store is None:
            abort(404, 'Store not found')
        store_available_products = StoreService.get_store_available_products(
            store)
        store_products_schema = StoreProductsSchema()
        result = store_products_schema.dump(store_available_products)
        return result, 200
