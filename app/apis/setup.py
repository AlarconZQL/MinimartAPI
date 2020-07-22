from flask_restx import Namespace, Resource

from ..utils.seed_database import seed_database

api = Namespace('setup', description='System\'s setup operations')


@api.route('/')
class Setup(Resource):
    @api.response(201, 'Content created')
    def get(self):
        '''Drop all database current information and create initial information'''
        seed_database()
        return {}, 201
