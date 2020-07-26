from flask_restx import Api

from app.apis.setup import api as setup_api
from app.apis.store import api as store_api
from app.apis.product import api as product_api
from app.apis.cart import api as cart_api

api = Api(
    title='Minimart API',
    version='1.0',
    description='COCO\'s minimarts simple API'
)

api.add_namespace(setup_api)
api.add_namespace(store_api)
api.add_namespace(product_api)
api.add_namespace(cart_api)
