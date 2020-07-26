from flask_restx import Namespace, Resource, abort
from app import db
from app.service.cart import CartService
from app.service.store import StoreService
from app.service.product import ProductService
from app.service.voucher import VoucherService
from app.schema import CartCreatedSchema, CartSchema
from app.exceptions import (
    NoStockException, ProductNotFoundInCart, VoucherNotValidException)

api = Namespace('cart', description='Cart\'s operations')


@api.route('/store/<int:store_id>')
@api.param('store_id', 'The store identifier')
class StoreCart(Resource):
    @api.response(404, 'Resource not found')
    @api.response(201, 'Cart created')
    def post(self, store_id):
        """Creates a cart on the specified store"""
        if StoreService.get_store(store_id) is None:
            abort(404, 'Store not found')
        new_cart = CartService.create_store_cart(store_id)
        cart_created_schem = CartCreatedSchema()
        result = cart_created_schem.dump(new_cart)
        return result, 201


@api.route('/<int:cart_id>/product/<int:product_id>')
@api.param('cart_id', 'The cart identifier')
@api.param('product_id', 'The product identifier')
class CartProduct(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Resource not found')
    def post(self, cart_id, product_id):
        """Adds one unit of the specified product to cart if it has stock"""
        cart = CartService.get_cart(cart_id)
        if cart is None:
            abort(404, 'Cart not found')
        product = ProductService.get_product(product_id)
        if product is None:
            abort(404, 'Product not found')
        try:
            cart = CartService.add_product_to_cart(cart, product)
            cart_schema = CartSchema()
            result = cart_schema.dump(cart)
            return result, 200
        except NoStockException as exc:
            return {'message': exc.message}, 200

    @api.response(200, 'Success')
    @api.response(404, 'Resource not found')
    def delete(self, cart_id, product_id):
        """Remove one unit of the specified product from the cart and returns
        it to the cart's store"""
        cart = CartService.get_cart(cart_id)
        if cart is None:
            abort(404, 'Cart not found')
        product = ProductService.get_product(product_id)
        if product is None:
            abort(404, 'Product not found')
        try:
            cart = CartService.remove_product_from_cart(cart, product)
            cart_schema = CartSchema()
            result = cart_schema.dump(cart)
            return result, 200
        except ProductNotFoundInCart as exc:
            return {'message': exc.message}, 200


@api.route('/<int:cart_id>/voucher/<int:voucher_id>')
@api.param('cart_id', 'The cart identifier')
@api.param('voucher_id', 'The voucher identifier')
class CartVoucher(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Resource not found')
    def get(self, cart_id, voucher_id):
        """Check validity of a voucher, applies it to the cart if its valid and
        return original and discounted price"""
        cart = CartService.get_cart(cart_id)
        if cart is None:
            abort(404, 'Cart not found')
        voucher = VoucherService.get_voucher(voucher_id)
        if voucher is None:
            abort(404, 'Voucher not found')
        try:
            original_price = CartService.get_price_from_cart(cart)
            discounted_price = CartService.get_discounted_price_from_cart(
                cart, voucher)
            result = {'original_price': original_price,
                      'discounted_price': discounted_price}
            return result, 200
        except VoucherNotValidException as exc:
            return {'message': exc.message}, 200
