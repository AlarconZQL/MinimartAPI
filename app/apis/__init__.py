from flask_restx import Api

from .setup import api as setup_api

api = Api(
    title='Minimart API',
    version='1.0',
    description='This is COCO\'s minimarts simple API'
)

api.add_namespace(setup_api)
