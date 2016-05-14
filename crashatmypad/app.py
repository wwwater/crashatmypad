import logging
from os import path
import string

from flask import Blueprint, Flask, render_template, redirect, request, url_for, jsonify, abort

from datetime import date

from persistence.db import db
from persistence.user import User
from persistence.password import Password
from persistence.location import Location

from service.search import find_locations_by_query
from util.trie import Trie

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)


page = Blueprint('page', __name__)

cities = Trie()


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('config.settings')
    app.config.from_pyfile('../config/settings.py', silent=False)

    db.init_app(app)

    app.register_blueprint(page)
    app.logger.addHandler(stream_handler)

    cities_file = path.join(path.dirname(__file__), '../world-cities.csv')
    with open(cities_file, 'r') as f:
        for line in f:
            parts = line.split(',')
            if len(parts) == 4:
                city = parts[0]
                country = parts[1]
                state = parts[2]
                cities.add(string.join([city, state, country],  ','))
    print cities.size
    print cities.get('Moscow')

    return app


@page.route('/')
def index():
    """
    Render the home page.

    :return: Flask response
    """
    return render_template('landing_page.html')


@page.route('/city')
def get_world_cities():
    """
    Searches world cities that start with the query argument.
    :return: List of cities with their state and country
    """

    query = str(string.replace(request.args.get('q'), ', ', ','))
    print query

    def world_city_to_display_format(entry):
        parts = entry.split(',')
        return {
            'city': string.capwords(parts[0]),
            'state': string.capwords(parts[1]),
            'country': string.capwords(parts[2])
        }

    results = map(world_city_to_display_format, cities.get(query))
    return jsonify(cities=results)


@page.route('/search')
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


@page.route('/user/<int:user_id>', methods=['GET'])
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


@page.route('/user', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(email=username).first() is not None:
        abort(400)  # existing user

    user = User(email=username)
    password_entry = Password(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    db.session.add(password_entry)
    db.session.commit()
    return jsonify({'username': password_entry.username}), 201


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
