import os

from app import create_app, db

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)
with app.app_context():
    db.create_all()
