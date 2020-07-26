from app import db
from app.tests import BaseTestClass
from app.models import Store


class StoreApiTestCase(BaseTestClass):

    def test_get_available_stores_products(self):
        with self.app.app_context():
            res = self.client.get('/store?openedAt=1233',
                                  follow_redirects=True)
            self.assertEqual(400, res.status_code)
            self.assertIn(b'does not match %H:%M format', res.data)
            res = self.client.get('/store?openedAt=12:33',
                                  follow_redirects=True)
            self.assertEqual(200, res.status_code)
            self.assertTrue(self.is_json_content_type(res.content_type))

    def test_get_product_from_each_store(self):
        with self.app.app_context():
            res = self.client.get('/store/product', follow_redirects=True)
            self.assertEqual(200, res.status_code)
            self.assertTrue(self.is_json_content_type(res.content_type))

    def test_get_product_availability_at_store(self):
        with self.app.app_context():
            res = self.client.get('store/1/product')
            self.assertEqual(404, res.status_code)
            store = Store(name='TestStore')
            db.session.add(store)
            db.session.commit()
            res = self.client.get(f'store/{store.id}/product')
            self.assertEqual(200, res.status_code)
            self.assertTrue(self.is_json_content_type(res.content_type))
            self.assertIn(b'id', res.data)
            self.assertIn(b'name', res.data)
            self.assertIn(b'products', res.data)
