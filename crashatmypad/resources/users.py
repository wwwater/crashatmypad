from datetime import date

from flask import render_template, make_response, redirect, url_for
from flask_restful import Resource, reqparse
from flask.ext.login import LoginManager, login_user, logout_user, login_required
from flask_mail import Mail


from crashatmypad.persistence.db import db
from crashatmypad.persistence.user import User
from crashatmypad.persistence.password import Password

from crashatmypad.services.users import send_confirmation_email, confirm_email

login_manager = LoginManager()
mail = Mail()


class UsersResource(Resource):
    def __init__(self):
        self.request_parser = reqparse.RequestParser()
        super(UsersResource, self).__init__()

    def get(self, user_id):
        """
        Render the user page.
        :param user_id
        :return: Flask response
        """
        self.request_parser.add_argument('confirm',
                                         type=str,
                                         required=False)
        args = self.request_parser.parse_args()
        user = db.session.query(User).get(user_id)
        confirm_hash = args['confirm']
        if confirm_hash:
            if confirm_email(user, confirm_hash):
                print 'Email is confirmed!'
                login_user(user)
                return redirect('/')
            else:
                print 'Email is not confirmed!'
                return make_response('The confirmation email link is wrong! '
                                     'The email cannot be confirmed.', 400)
        if user.birthday:
            today = date.today()
            diff_pure_years = today.year - user.birthday.year
            age = diff_pure_years \
                if user.birthday.replace(today.year) <= today \
                else diff_pure_years - 1
        else:
            age = 21

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

    def post(self, user_id):
        self.request_parser.add_argument('username',
                                         type=str,
                                         required=True,
                                         help='No username is provided')
        self.request_parser.add_argument('password',
                                         type=str,
                                         required=True,
                                         help='No password is provided')
        args = self.request_parser.parse_args()
        username = args['username']
        password = args['password']
        if not username or not password:
            return make_response('Username and password are mandatory! ;)', 400)
        user = User.query.filter_by(email=username).first()
        if user is not None:
            print 'The user already exists. Checking if the email is confirmed.'
            existing_password_entry = Password.query\
                .filter_by(username=username).first()
            if existing_password_entry.verify_password(password):
                if user.email_is_confirmed:
                    login_user(user)
                    return redirect('/')
                else:
                    return make_response(
                        'Please confirm the email first.'
                        'The confirmation link is sent to your email.', 403)
            else:
                print 'Wrong password!'
                return make_response('User with this email already exists and '
                                     'it has different password', 400)

        user = User(email=username)
        password_entry = Password(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        db.session.add(password_entry)
        db.session.commit()
        send_confirmation_email(user)
        print 'New user created!'
        return redirect(url_for('mainresource', c=True))


class LogoutResource(Resource):
    def __init__(self):
        super(LogoutResource, self).__init__()

    @login_required
    def get(self):
        print 'Logging out...'
        logout_user()
        return redirect('/')


@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(email=username).first()
