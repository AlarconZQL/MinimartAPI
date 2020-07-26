from app.tests import BaseTestClass
from app.utils.seed_database import seed_database
from app.models import *


class SeedDatabaseTestCase(BaseTestClass):

    def test_initial_amounts(self):
        with self.app.app_context():
            seed_database()
            stores = Store.query.all()
            self.assertEqual(3, len(stores))
            products = Product.query.all()
            self.assertEqual(22, len(products))
            categories = Category.query.all()
            self.assertEqual(4, len(categories))
            vouchers = Voucher.query.all()
            self.assertEqual(5, len(vouchers))
