import calendar
from datetime import date
from app import db
from app.models import Cart, Store, ProductStoreLink, CartProductLink, Voucher, ProductVoucherLink
from app.utils import DateUtils


class CartService:
    @staticmethod
    def create_store_cart(store_id):
        store = Store.query.get(store_id)
        if store != None:
            new_cart = Cart(store_id=store_id)
            db.session.add(new_cart)
            db.session.commit()
            return new_cart
        else:
            return None

    @staticmethod
    def add_product_to_cart(cart_id, product_id):
        cart = Cart.query.get(cart_id)
        # Check if the cart exists
        if cart != None:
            # Check if the store has stock of the product
            store_product = ProductStoreLink.query.filter_by(
                store_id=cart_id, product_id=product_id).first()
            if store_product != None and store_product.stock > 0:
                store_product.stock = store_product.stock - 1
                # Add product to the cart
                cart_product = CartProductLink.query.filter_by(
                    cart_id=cart.id, product_id=product_id).first()
                if cart_product != None:
                    cart_product.units = cart_product.units + 1
                else:
                    cart.products.append(CartProductLink(
                        cart_id=cart.id, product_id=product_id, units=1))
                db.session.add(cart)
                db.session.commit()
                return cart
            else:
                raise Exception('No stock for that product')
        raise Exception('Cart not found')

    @staticmethod
    def remove_product_from_cart(cart_id, product_id):
        cart = Cart.query.get(cart_id)
        # Check if the cart exists
        if cart != None:
            # Check if any unit of the product is in the cart
            cart_product = CartProductLink.query.filter_by(
                cart_id=cart.id, product_id=product_id).first()
            if cart_product != None:
                # Remove product from cart and delete the relation if units reach zero
                cart_product.units = cart_product.units - 1
                if cart_product.units == 0:
                    db.session.delete(cart_product)
                # Increase the product's stock on the store
                store_product = ProductStoreLink.query.filter_by(
                    store_id=cart_id, product_id=product_id).first()
                if store_product != None:
                    store_product.stock = store_product.stock + 1
                db.session.add(cart)
                db.session.commit()
                return cart
            else:
                raise Exception(
                    'This cart does not have any unit of this product')
        else:
            raise Exception('Cart not found')

    @staticmethod
    def get_price_from_cart(cart_id):
        cart = Cart.query.get(cart_id)
        # Check if the cart exists
        if cart == None:
            raise Exception('Cart not found')
        total_price = 0
        for product_cart in cart.products:
            total_price += product_cart.units * product_cart.product.price
        return total_price

    @classmethod
    def get_price_from_cart_applying_voucher(cls, cart_id, voucher_id):
        cart = Cart.query.get(cart_id)
        voucher = Voucher.query.get(voucher_id)
        cls.check_voucher_validity_on_cart(cart, voucher)
        voucher_promos = ProductVoucherLink.query.filter_by(
            voucher_id=voucher_id)
        product_ids_on_promos = list(
            (map(lambda vd: vd.product.id, voucher_promos)))
        total_price = 0
        for product_cart in cart.products:
            product = product_cart.product
            if product.id in product_ids_on_promos:
                promo = list(filter(lambda a: a.product.id ==
                                    product.id, voucher_promos))[0]
                product_total = cls.calculate_price_with_discount(product_cart.units,
                                                                  product.price,
                                                                  promo.discount,
                                                                  promo.on_unit,
                                                                  promo.max_units)
            else:
                product_total = product_cart.units * product.price
            total_price += product_total
        return total_price

    @classmethod
    def calculate_price_with_discount(cls, total_units, unit_price, discount, on_unit, max_units):
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
        if cart == None:
            raise Exception('Cart not found')
        if voucher == None:
            raise Exception('Voucher not found')
        # Check if store applies
        if voucher.store_id != cart.store_id:
            raise Exception('Voucher does not apply on the cart\'s store')
        # Check if today's date applies
        if not DateUtils.today_is_between_dates(voucher.start_date, voucher.end_date):
            raise Exception(
                'Current date is not in the voucher\'s valid dates')
        # Check if today's  day of week applies
        if len(voucher.only_on_days) > 0 and not DateUtils.today_is_included_on_weekdays(voucher.only_on_days):
            raise Exception('Voucher does not apply this day of the week')
        return
