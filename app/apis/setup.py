from flask_restx import Namespace, Resource

api = Namespace('setup', description='System\'s setup operations')


@api.route('/')
class Setup(Resource):
    @api.doc('create_database_info')
    def get(self):
        '''Create initial database information'''
        # CREATE THE INFO HERE!
        print("Creating initial database info")
        return 201
