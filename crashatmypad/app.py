import logging

from flask import Blueprint, Flask, render_template, redirect, request, url_for
from flask_redis import FlaskRedis
from redis import StrictRedis

from datetime import date

from persistence.db import db
from persistence.user import User
from persistence.location import Location

from service.search import find_locations_by_query

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

redis_store = FlaskRedis.from_custom_provider(StrictRedis)

page = Blueprint('page', __name__)


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('config.settings')
    app.config.from_pyfile('../config/settings.py', silent=False)

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


@page.route('/search/')
def search():
    """
    Render the home page.

    :return: Flask response
    """
    # print request
    query = request.args.get('location') or 'Hamburg, Germany'
    results = find_locations_by_query(query)
    return render_template('search.html', query=query,
                           results=results['locations'],
                           query_coordinates=results['query'])


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

    user1 = User(
        email='laura@moreaux.com',
        name='Laura',
        last_name='Moreaux',
        birthday=date(1987, 6, 7),
        profession='Architect'
    )

    db.session.add(user1)
    db.session.commit()

    user1_location1 = Location(user=user1,
                               longitude=9.9711,
                               latitude=53.5818,
                               country='Germany',
                               city='Hamburg',
                               street='Eppendorfer Weg',
                               house=219,
                               corner=True,
                               shower=True,
                               bathroom=True)

    user1_location2 = Location(user=user1,
                               longitude=11.2438,
                               latitude=49.4869,
                               country='Germany',
                               city='Roetenbach an der Pegnitz',
                               street="Alter Kirchenweg",
                               house=35,
                               apartment=True)
    db.session.add(user1_location1)
    db.session.add(user1_location2)
    db.session.commit()

    user2 = User(
        email='lena@anderson.com',
        name='Lena',
        last_name='Anderson',
        birthday=date(1983, 6, 17),
        profession='Carpenter'
    )

    db.session.add(user2)
    db.session.commit()

    user2_location1 = Location(user=user2,
                               longitude=10.0325,
                               latitude=53.5745,
                               country='Germany',
                               city='Hamburg',
                               street='Heitmannstr.',
                               corner=True,
                               shower=True,
                               bathroom=True)

    db.session.add(user2_location1)
    db.session.commit()

    user3 = User(
        email='chris@hasselberg.com',
        name='Chris',
        last_name='Hasselberg',
        birthday=date(1981, 2, 9),
        profession='Manager'
    )

    db.session.add(user3)
    db.session.commit()

    user3_location1 = Location(user=user3,
                               longitude=10.0131,
                               latitude=53.4902,
                               country='Germany',
                               city='Hamburg',
                               street='Hanseatenweg',
                               corner=True,
                               shower=True,
                               bathroom=True)

    db.session.add(user3_location1)
    db.session.commit()

    return redirect(url_for('page.index'))
