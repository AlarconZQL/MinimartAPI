from flask_restx import Namespace, Resource

from ..utils.seed_database import seed_database

api = Namespace('setup', description='System\'s setup operations')


@api.route('/')
class Setup(Resource):
    @api.doc('create_database_info')
    def get(self):
        '''Create initial database information'''
        # CREATE THE INFO HERE!
        seed_database()
        return 201
