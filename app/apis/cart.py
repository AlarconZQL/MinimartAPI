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
    @api.response(200, 'Product added')
    @api.response(404, 'No stock for that product or non existing cart')
    def post(self, cart_id, product_id):
        '''Adds one unit of the specified product to cart if it has stock'''
        try:
            cart = CartService.add_product_to_cart(cart_id, product_id)
            cart_schema = CartSchema()
            result = cart_schema.dump(cart)
            return result, 200
        except Exception as error:
            api.abort(404, error)

    @api.response(200, 'Product removed')
    @api.response(404, 'There are not any units of this product the cart or non existing cart')
    def delete(self, cart_id, product_id):
        '''Remove one unit of the specified product from the cart and returns it to the cart's store'''
        try:
            cart = CartService.remove_product_from_cart(cart_id, product_id)
            cart_schema = CartSchema()
            result = cart_schema.dump(cart)
            return result, 200
        except Exception as error:
            api.abort(404, error)


@api.route('/<int:cart_id>/voucher/<int:voucher_id>')
@api.param('cart_id', 'The cart identifier')
@api.param('voucher_id', 'The voucher identifier')
class CartVoucher(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Cart not found')
    def get(self, cart_id, voucher_id):
        '''Check validity of a voucher, applies it to the cart if its valid and return original and discounted price'''
        try:
            original_price = CartService.get_price_from_cart(cart_id)
            discount_price = CartService.get_price_from_cart_applying_voucher(
                cart_id, voucher_id)
            result = {'original_price': original_price,
                      'discount_price': discount_price}
            return result, 200
        except Exception as error:
            api.abort(404, error)
