from datetime import date, timedelta
from app import db
from app.tests import BaseTestClass
from app.models import (Cart, Store, Product, ProductStoreLink, CartProductLink,
                        Voucher, ProductVoucherLink)
from app.service.cart import CartService


class CartServiceTestCase(BaseTestClass):

    def test_create_store_cart(self):
        with self.app.app_context():
            self.assertEqual(0, len(Cart.query.all()))
            store = Store(name='Test Store')
            db.session.add(store)
            db.session.commit()
            CartService.create_store_cart(store.id)
            self.assertEqual(1, len(Cart.query.all()))

    def test_add_product_to_cart(self):
        with self.app.app_context():
            store = Store(name='Test Store')
            db.session.add(store)
            db.session.commit()
            cart = Cart(store_id=store.id)
            db.session.add(cart)
            product = Product(name='Test Product', price=15)
            link = ProductStoreLink(product=product, stock=8)
            store.products.append(link)
            db.session.commit()
            self.assertEqual(0, len(cart.products))
            CartService.add_product_to_cart(cart, product)
            self.assertEqual(1, len(cart.products))
            self.assertEqual(1, cart.products[0].units)
            self.assertEqual(7, store.products[0].stock)

    def test_remove_product_from_cart(self):
        with self.app.app_context():
            store = Store(name='Test Store')
            db.session.add(store)
            db.session.commit()
            product = Product(name='Test Product', price=10)
            link = ProductStoreLink(product=product, stock=20)
            store.products.append(link)
            cart = Cart(store_id=store.id)
            link = CartProductLink(product=product, units=1)
            cart.products.append(link)
            db.session.add(cart)
            db.session.commit()
            self.assertEqual(1, len(cart.products))
            self.assertEqual(1, cart.products[0].units)
            CartService.remove_product_from_cart(cart, product)
            self.assertEqual(0, len(cart.products))
            self.assertEqual(21, store.products[0].stock)

    def test_get_price_from_cart(self):
        with self.app.app_context():
            store = Store(name='Test Store')
            db.session.add(store)
            db.session.commit()
            product = Product(name='Test Product', price=10)
            link = ProductStoreLink(product=product, stock=20)
            store.products.append(link)
            cart = Cart(store_id=store.id)
            link = CartProductLink(product=product, units=9)
            cart.products.append(link)
            db.session.add(cart)
            db.session.commit()
            cart_price = CartService.get_price_from_cart(cart)
            self.assertEqual(9*10, cart_price)

    def test_get_discounted_price_from_cart(self):
        with self.app.app_context():
            store = Store(name='Test Store')
            db.session.add(store)
            db.session.commit()
            product = Product(name='Test Product', price=10)
            link = ProductStoreLink(product=product, stock=20)
            store.products.append(link)
            product2 = Product(name='Test Product 2', price=5)
            link = ProductStoreLink(product=product2, stock=10)
            store.products.append(link)
            cart = Cart(store_id=store.id)
            link = CartProductLink(product=product, units=10)
            cart.products.append(link)
            today = date.today()
            link = CartProductLink(product=product2, units=2)
            cart.products.append(link)
            voucher = Voucher(code='TESTCODE', store_id=store.id, start_date=today -
                              timedelta(days=5), end_date=today + timedelta(days=5))
            link = ProductVoucherLink(
                discount=50, on_unit=1, max_units=0, product=product)
            voucher.products.append(link)
            db.session.add(cart)
            db.session.add(voucher)
            db.session.commit()
            price = CartService.get_discounted_price_from_cart(cart, voucher)
            self.assertEqual(60, price)
