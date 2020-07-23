from flask_restx import Namespace, Resource
from app import db
from app.service import ProductService
from app.schema import ProductSchema, ProductStockSchema

api = Namespace('product', description='Product\'s operations')


@api.route('/')
class Product(Resource):
    @api.response(200, 'Products information')
    def get(self):
        '''Get products catalogue'''
        products = ProductService.get_all_products()
        products_schema = ProductSchema(many=True)
        return products_schema.dump(products), 200


@api.route('/<int:product_id>/store/<int:store_id>')
@api.param('product_id', 'The product identifier')
@api.param('store_id', 'The store identifier')
class ProductAvailable(Resource):
    @api.response(404, 'Product not available')
    @api.response(200, 'Product\'s information')
    def get(self, product_id, store_id):
        '''Get product's information if it is available on the specified store'''
        product_stock = ProductService.get_product_info_for_store(
            product_id, store_id)
        if product_stock != None:
            product_stock_schema = ProductStockSchema()
            return product_stock_schema.dump(product_stock), 200
        api.abort(404)
