from app import db
from app.tests import BaseTestClass
from app.models import Product, Store, ProductStoreLink


class ProductApiTestCase(BaseTestClass):

    def test_get_all_products(self):
        with self.app.app_context():
            res = self.client.get('/product', follow_redirects=True)
            self.assertEqual(200, res.status_code)
            self.assertTrue(self.is_json_content_type(res.content_type))

    def test_get_product_information_from_store(self):
        with self.app.app_context():
            res = self.client.get('/product/1/store/1', follow_redirects=True)
            self.assertEqual(404, res.status_code)
            product = Product(name='Test Product', price=10)
            store = Store(name='Test Store')
            link = ProductStoreLink(product=product, stock=5)
            store.products.append(link)
            db.session.add(store)
            db.session.commit()
            res = self.client.get(
                f'/product/{product.id}/store/{store.id}',
                follow_redirects=True)
            self.assertEqual(200, res.status_code)
            self.assertTrue(self.is_json_content_type(res.content_type))
