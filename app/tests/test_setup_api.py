from app.tests import BaseTestClass
from app.models import Store


class SetupApiTestCase(BaseTestClass):

    def test_setup_endpoint(self):
        with self.app.app_context():
            stores = Store.query.all()
            self.assertEqual(0, len(stores))
            res = self.client.get('/setup', follow_redirects=True)
            self.assertEqual(201, res.status_code)
            stores = Store.query.all()
            self.assertEqual(3, len(stores))
