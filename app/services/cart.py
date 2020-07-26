import calendar
from datetime import date
from app import db
from app.models import (Cart, ProductStoreLink, CartProductLink, Voucher,
                        ProductVoucherLink)
from app.utils import DateUtils
from app.exceptions import (NoStockException, ProductNotFoundInCart,
                            VoucherNotValidException)


class CartService:
    @classmethod
    def get_cart(cls, cart_id):
        return Cart.query.get(cart_id)

    @classmethod
    def create_store_cart(cls, store_id):
        new_cart = Cart(store_id=store_id)
        db.session.add(new_cart)
        db.session.commit()
        return new_cart

    @classmethod
    def add_product_to_cart(cls, cart, product):
        # Check if the store has stock of the product
        store_product = ProductStoreLink.query.filter_by(
            store_id=cart.store_id, product_id=product.id).first()
        if store_product is not None and store_product.stock > 0:
            store_product.stock = store_product.stock - 1
            # Add product to the cart
            cart_product = CartProductLink.query.filter_by(
                cart_id=cart.id, product_id=product.id).first()
            if cart_product is not None:
                cart_product.units = cart_product.units + 1
            else:
                cart.products.append(CartProductLink(
                    cart_id=cart.id, product_id=product.id, units=1))
            db.session.add(cart)
            db.session.commit()
            return cart
        else:
            raise NoStockException()

    @classmethod
    def remove_product_from_cart(cls, cart, product):
        # Check if any unit of the product is in the cart
        cart_product = CartProductLink.query.filter_by(
            cart_id=cart.id, product_id=product.id).first()
        if cart_product is not None:
            # Remove product from cart and delete the relation if units reach zero
            cart_product.units = cart_product.units - 1
            if cart_product.units == 0:
                db.session.delete(cart_product)
                db.session.commit()
            # Increase the product's stock on the store
            store_product = ProductStoreLink.query.filter_by(
                store_id=cart.store_id, product_id=product.id).first()
            if store_product is not None:
                store_product.stock = store_product.stock + 1
            db.session.add(cart)
            db.session.commit()
            return cart
        else:
            raise ProductNotFoundInCart()

    @classmethod
    def get_price_from_cart(cls, cart):
        total_price = 0
        for product_cart in cart.products:
            total_price += product_cart.units * product_cart.product.price
        return total_price

    @classmethod
    def get_discounted_price_from_cart(cls, cart, voucher):
        cls.check_voucher_validity_on_cart(cart, voucher)
        voucher_promos = ProductVoucherLink.query.filter_by(
            voucher_id=voucher.id)
        product_ids_on_promos = list(
            (map(lambda vd: vd.product.id, voucher_promos)))
        total_price = 0
        for product_cart in cart.products:
            product = product_cart.product
            if product.id in product_ids_on_promos:
                promo = list(filter(lambda a: a.product.id ==
                                    product.id, voucher_promos))[0]
                product_total = cls.calculate_price_with_discount(
                    product_cart.units, product.price, promo.discount,
                    promo.on_unit, promo.max_units)
            else:
                product_total = product_cart.units * product.price
            total_price += product_total
        return total_price

    @classmethod
    def calculate_price_with_discount(cls, total_units, unit_price, discount,
                                      on_unit, max_units):
        total_price = 0
        reached_max = False
        for unit in range(1, total_units+1):
            if (unit % on_unit == 0) and not reached_max:
                total_price += unit_price - unit_price * discount / 100
            else:
                total_price += unit_price
            reached_max = (max_units > 0 and unit >= max_units)
        return total_price

    @classmethod
    def check_voucher_validity_on_cart(cls, cart, voucher):
        # Check if store applies
        if voucher.store_id != cart.store_id:
            raise VoucherNotValidException(
                message='Voucher does not apply on the cart\'s store')
        # Check if today's date applies
        if not DateUtils.today_is_between_dates(voucher.start_date,
                                                voucher.end_date):
            raise VoucherNotValidException(
                message='Current date is not in the voucher\'s valid dates')
        # Check if today's day of week applies
        if len(voucher.only_on_days) > 0 and not(
                DateUtils.today_is_included_on_voucherdays(voucher.only_on_days)):
            raise VoucherNotValidException(
                message='Voucher does not apply this day of the week')
