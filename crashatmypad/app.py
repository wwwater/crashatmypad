import logging

from flask import Blueprint, Flask, render_template, redirect, request, url_for
from flask_redis import FlaskRedis
from redis import StrictRedis

from datetime import date

from persistence.models import db, User, Location

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

redis_store = FlaskRedis.from_custom_provider(StrictRedis)

page = Blueprint('page', __name__)


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    db.init_app(app)
    redis_store.init_app(app)

    app.register_blueprint(page)
    app.logger.addHandler(stream_handler)

    return app


@page.route('/')
def index():
    """
    Render the home page.

    :return: Flask response
    """
    return render_template('landing_page.html')


@page.route('/search')
def search():
    """
    Render the home page.

    :return: Flask response
    """
    return render_template('search.html',
                           query='Hamburg, Germany',
                           results=[
                               {
                                   'user_name': 'Laura',
                                   'street': 'Rotherbaumchausse',
                                   'city': 'Hamburg',
                                   'latitude': 53.57,
                                   'longitude': 10.00
                               },
                               {
                                   'user_name': 'Peter',
                                   'street': 'Alsterallee',
                                   'city': 'Hamburg',
                                   'latitude': 53.558,
                                   'longitude': 10.01
                               },
                               {
                                   'user_name': 'Lena',
                                   'street': 'Elbstrasse',
                                   'city': 'Hamburg',
                                   'latitude': 53.572,
                                   'longitude': 10.03
                               }
                           ])


@page.route('/user/<int:user_id>')
def user_page(user_id):
    """
    Render the user page.
    :parameter user_id: internal user id
    :return: Flask response
    """

    user = db.session.query(User).get(user_id)
    today = date.today()
    diff_pure_years = today.year - user.birthday.year
    age = diff_pure_years if user.birthday.replace(today.year) <= today else \
        diff_pure_years - 1

    user_data_to_display = {
        'name': user.name,
        'last_name': user.last_name,
        'age': age,
        'profession': user.profession
    }

    locations = user.locations
    locations_to_display = []
    for location in locations:
        location_to_display = {
            'country': location.country,
            'city': location.city,
            'apartment': location.apartment,
            'room': location.room,
            'corner': location.corner,
            'yard': location.yard,
            'trees': location.trees,
            'driveway': location.driveway,
            'shower': location.shower,
            'bathroom': location.bathroom
        }
        locations_to_display.append(location_to_display)

    return render_template('user_page.html', user=user_data_to_display,
                           locations=locations_to_display)


@page.route('/whatsinanamethatwhichwecallarosebyanyothernamewouldsmellassweet')
def seed():
    """
    Reset the database and seed it with a few messages.

    :return: Flask redirect
    """
    db.drop_all()
    db.create_all()

    very_first_user = User(
        email='laura@moreaux.com',
        name='Laura',
        last_name='Moreaux',
        birthday=date(1987, 6, 7),
        profession='Architect'
    )

    db.session.add(very_first_user)
    db.session.commit()

    first_user_location = Location(user=very_first_user,
                                   country='Germany',
                                   city='Hamburg',
                                   corner=True,
                                   shower=True,
                                   bathroom=True)

    first_user_secondary_location = Location(user=very_first_user,
                                             country='Germany',
                                             city='Freiburg',
                                             apartment=True)
    db.session.add(first_user_location)
    db.session.add(first_user_secondary_location)
    db.session.commit()

    return redirect(url_for('page.index'))
