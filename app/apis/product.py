from flask_restx import Namespace, Resource, abort
from app import db
from app.service import ProductService, StoreService
from app.schema import ProductSchema, ProductStockSchema

api = Namespace('product', description='Product\'s operations')


@api.route('/')
class Product(Resource):
    @api.response(200, 'Success')
    def get(self):
        """Get products catalogue information"""
        products = ProductService.get_all_products()
        products_schema = ProductSchema(many=True)
        return products_schema.dump(products), 200


@api.route('/<int:product_id>/store/<int:store_id>')
@api.param('product_id', 'The product identifier')
@api.param('store_id', 'The store identifier')
class ProductAvailable(Resource):
    @api.response(404, 'Resource not found')
    @api.response(200, 'Success')
    def get(self, product_id, store_id):
        """Get product's information if it is available on the specified
        store"""
        if ProductService.get_product(product_id) is None:
            abort(404, 'Product not found')
        if StoreService.get_store(store_id) is None:
            abort(404, 'Store not found')
        product_stock = ProductService.get_product_info_for_store(
            product_id, store_id)
        if product_stock is not None and product_stock.stock > 0:
            product_stock_schema = ProductStockSchema()
            return product_stock_schema.dump(product_stock), 200
        else:
            return {'message': 'Product has no stock at this store'}, 200
