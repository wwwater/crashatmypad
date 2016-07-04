from flask_restful import Api

from persistence.db import db

from resources.main import MainResource
from resources.cities import CitiesResource
from resources.locations import LocationsResource
from resources.users import UsersResource, LogoutResource, login_manager, mail


def init_app(app):
    login_manager.init_app(app)
    mail.init_app(app)

    db.init_app(app)
    db.create_all(app=app)  # creates new tables but does not overwrite existing

    api = Api(app)
    api.add_resource(MainResource, '/')
    api.add_resource(CitiesResource, '/city')
    api.add_resource(LocationsResource, '/location')
    api.add_resource(UsersResource, '/user/<user_id>')
    api.add_resource(LogoutResource, '/logout')


    app.logger.info('App has started!')
