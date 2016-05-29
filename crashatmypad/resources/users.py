from datetime import date

from flask import render_template, make_response, jsonify, abort
from flask_restful import Resource, reqparse

from crashatmypad.persistence.db import db
from crashatmypad.persistence.user import User
from crashatmypad.persistence.password import Password


class UsersResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(UsersResource, self).__init__()

    def get(self):
        """
        Render the user page.
        :return: Flask response
        """
        self.reqparse.add_argument('user_id',
                                   type=str,
                                   required=True,
                                   help=
                                   'No user id is provided')
        args = self.reqparse.parse_args()
        user_id = args['user_id']
        user = db.session.query(User).get(user_id)
        today = date.today()
        diff_pure_years = today.year - user.birthday.year
        age = diff_pure_years \
            if user.birthday.replace(today.year) <= today \
            else diff_pure_years - 1

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

        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('user_page.html', user=user_data_to_display,
                            locations=locations_to_display),
            200,
            headers
        )

    def post(self):
        self.reqparse.add_argument('username',
                                   type=str,
                                   required=True,
                                   help=
                                   'No username is provided')
        self.reqparse.add_argument('password',
                                   type=str,
                                   required=True,
                                   help=
                                   'No password is provided')
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']
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

