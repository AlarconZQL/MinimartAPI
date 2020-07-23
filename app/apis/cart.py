from flask_restx import Namespace, Resource
from app import db
from app.service.cart import CartService
from app.schema import CartCreatedSchema, CartSchema

api = Namespace('cart', description='Cart\'s operations')


@api.route('/store/<int:store_id>')
@api.param('store_id', 'The store identifier')
class StoreCart(Resource):
    @api.response(404, 'Store not found')
    @api.response(201, 'Cart created')
    def post(self, store_id):
        '''Creates a cart on the specified store'''
        new_cart = CartService.create_store_cart(store_id)
        if new_cart == None:
            api.abort(404)
        cart_created_schem = CartCreatedSchema()
        result = cart_created_schem.dump(new_cart)
        return result, 201


@api.route('/<int:cart_id>/product/<int:product_id>')
@api.param('cart_id', 'The cart identifier')
@api.param('product_id', 'The product identifier')
class CartProduct(Resource):
    @api.response(201, 'Product added')
    @api.response(404, 'No stock for that product or non existing cart')
    def post(self, cart_id, product_id):
        '''Adds one unit of the specified product to cart if it has stock'''
        try:
            cart = CartService.add_product_to_cart(cart_id, product_id)
            cart_schema = CartSchema()
            result = cart_schema.dump(cart)
            return result, 201
        except Exception as error:
            api.abort(404, error)
