import logging

from flask import Flask
from flask_restful import Api

from persistence.db import db

from resources.main import MainResource
from resources.cities import CitiesResource
from resources.locations import LocationsResource
from resources.users import UsersResource


stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)


app = Flask(__name__, instance_relative_config=False)
app.logger.addHandler(stream_handler)
app.config.from_object('config.settings')
app.config.from_pyfile('../config/settings.py', silent=False)
db.init_app(app)


api = Api(app)
api.add_resource(MainResource, '/')
api.add_resource(CitiesResource, '/city')
api.add_resource(LocationsResource, '/location')
api.add_resource(UsersResource, '/user')
