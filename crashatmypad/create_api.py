from flask_restful import Api

from resources.main import MainResource
from resources.cities import CitiesResource
from resources.locations import LocationsResource
from resources.users import UserResource, UsersResource
from resources.session import SessionResource


def create_api(app):
    api = Api(app)
    api.add_resource(MainResource, '/', endpoint='main')
    api.add_resource(CitiesResource, '/city', endpoint='cities')
    api.add_resource(LocationsResource, '/location', endpoint='location')
    api.add_resource(UserResource, '/user/<int:user_id>', endpoint='user')
    api.add_resource(UsersResource, '/user', endpoint='users')
    api.add_resource(SessionResource, '/session', endpoint='session')
