from datetime import date, timedelta
from app import db
from app.models import (Store, Cart, Product, ProductStoreLink,
                        CartProductLink, Voucher)
from app.tests import BaseTestClass


class CartApiTestCase(BaseTestClass):

    def test_post_new_cart(self):
        with self.app.app_context():
            res = self.client.post('/cart/store/1')
            self.assertEqual(404, res.status_code)
            store = Store(name='Test Store')
            db.session.add(store)
            db.session.commit()
            res = self.client.post(f'/cart/store/{store.id}')
            self.assertEqual(201, res.status_code)
            self.assertIn(b'id', res.data)
            self.assertIn(b'store_id', res.data)
            self.assertTrue(self.is_json_content_type(res.content_type))

    def test_add_product_to_cart(self):
        with self.app.app_context():
            res = self.client.post('/cart/1/product/1')
            self.assertEqual(404, res.status_code)
            store = Store(name='Test Store')
            product = Product(name='Test Product', price=10)
            db.session.add(store)
            db.session.add(product)
            db.session.commit()
            cart = Cart(store_id=store.id)
            db.session.add(cart)
            db.session.commit()
            res = self.client.post(f'/cart/{cart.id}/product/{product.id}')
            self.assertEqual(200, res.status_code)
            self.assertIn(
                b'There is no stock of this product at this store', res.data)
            self.assertTrue(self.is_json_content_type(res.content_type))

    def test_remove_product_from_cart(self):
        with self.app.app_context():
            res = self.client.delete('/cart/1/product/1')
            self.assertEqual(404, res.status_code)
            store = Store(name='Test Store')
            product = Product(name='Test Product', price=10)
            link = ProductStoreLink(product=product, stock=5)
            store.products.append(link)
            db.session.add(store)
            db.session.add(product)
            db.session.commit()
            cart = Cart(store_id=store.id)
            link = CartProductLink(product=product, units=2)
            cart.products.append(link)
            db.session.add(cart)
            db.session.commit()
            res = self.client.delete(f'/cart/{cart.id}/product/{product.id}')
            self.assertEqual(200, res.status_code)
            self.assertIn(b'id', res.data)
            self.assertIn(b'store_id', res.data)
            self.assertIn(b'products', res.data)
            self.assertTrue(self.is_json_content_type(res.content_type))

    def test_apply_voucher_to_cart(self):
        with self.app.app_context():
            res = self.client.get('/cart/1/voucher/1')
            self.assertEqual(404, res.status_code)
            store = Store(name='Test Store')
            db.session.add(store)
            db.session.commit()
            today = date.today()
            voucher = Voucher(code='TESTCODE', store_id=store.id,
                              start_date=today,
                              end_date=today+timedelta(days=5))
            cart = Cart(store_id=store.id)
            db.session.add(cart)
            db.session.add(voucher)
            db.session.commit()
            res = self.client.get(f'/cart/{cart.id}/voucher/{voucher.id}')
            self.assertEqual(200, res.status_code)
            self.assertIn(b'original_price', res.data)
            self.assertIn(b'discounted_price', res.data)
            self.assertTrue(self.is_json_content_type(res.content_type))
