import unittest
from app import create_app, db


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(settings_module="config.testing")
        self.client = self.app.test_client()
        # Create an application context
        with self.app.app_context():
            # Create database tables
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            # Drop all database tables
            db.session.remove()
            db.drop_all()

    def is_json_content_type(self, content_type):
        return content_type == 'application/json'
