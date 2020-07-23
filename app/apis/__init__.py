from flask_restx import Api

from .setup import api as setup_api
from .store import api as store_api
from .product import api as product_api

api = Api(
    title='Minimart API',
    version='1.0',
    description='This is COCO\'s minimarts simple API'
)

api.add_namespace(setup_api)
api.add_namespace(store_api)
api.add_namespace(product_api)
