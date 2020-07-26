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
        """Retrieves a single virtual cart"""
        return Cart.query.get(cart_id)

    @classmethod
    def create_store_cart(cls, store_id):
        """Creates a virtual cart for the specified store"""
        new_cart = Cart(store_id=store_id)
        db.session.add(new_cart)
        db.session.commit()
        return new_cart

    @classmethod
    def add_product_to_cart(cls, cart, product):
        """Adds the product to the virtual cart if the
        cart's store has stock for the product"""
        store_product = ProductStoreLink.query.filter_by(
            store_id=cart.store_id, product_id=product.id).first()
        if store_product is not None and store_product.stock > 0:
            store_product.stock = store_product.stock - 1
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
        """Removes one unit of the product from the virtual cart if the cart 
        has any units of it"""
        cart_product = CartProductLink.query.filter_by(
            cart_id=cart.id, product_id=product.id).first()
        if cart_product is not None:
            cart_product.units = cart_product.units - 1
            if cart_product.units == 0:
                db.session.delete(cart_product)
                db.session.commit()
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
        """Calculates the total price for the cart based on the products
        it has"""
        total_price = 0
        for product_cart in cart.products:
            total_price += product_cart.units * product_cart.product.price
        return total_price

    @classmethod
    def get_discounted_price_from_cart(cls, cart, voucher):
        """Checks if the voucher applies to the current cart. If so,
        calculates the total price for the cart based on the products
        it has and applies the voucher discounts to the final price"""
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
        """Calculates the price for the current product based on its units 
        and the voucher's discount rules"""
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
        """Checks if the voucher applies on the cart considering the cart's 
        store, the voucher's valid dates and week days"""
        if voucher.store_id != cart.store_id:
            raise VoucherNotValidException(
                message='Voucher does not apply on the cart\'s store')
        if not DateUtils.today_is_between_dates(voucher.start_date,
                                                voucher.end_date):
            raise VoucherNotValidException(
                message='Current date is not in the voucher\'s valid dates')
        if len(voucher.only_on_days) > 0 and not(
                DateUtils.today_is_included_on_voucherdays(voucher.only_on_days)):
            raise VoucherNotValidException(
                message='Voucher does not apply this day of the week')
