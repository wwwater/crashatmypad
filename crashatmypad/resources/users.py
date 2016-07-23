from flask import render_template, make_response, redirect, url_for
from flask_restful import Resource, reqparse
from flask_login import login_user

from crashatmypad import logger

import crashatmypad.services.users as service


class UserResource(Resource):
    def __init__(self):
        self.request_parser = reqparse.RequestParser()
        super(UserResource, self).__init__()

    def get(self, user_id):
        """
        Render the user page.
        :param user_id
        :return: Flask response
        """
        user = service.get_user_by_id(user_id)
        if not user:
            return make_response('User with id ' + str(user_id) +
                                 ' does not exist.', 400)

        user_data, user_locations = service.get_user_data_to_display(user)

        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('user_page.html', user=user_data,
                            locations=user_locations),
            200,
            headers
        )

    def post(self, user_id):
        """
        Updates user information.
        :param user_id
        :return: Flask response
        """
        self.request_parser.add_argument('confirm',
                                         type=str,
                                         required=False)
        args = self.request_parser.parse_args()
        user = service.get_user_by_id(user_id)
        if not user:
            return make_response('User with id ' + str(user_id) +
                                 ' does not exist.', 400)

        confirm_hash = args['confirm']
        if confirm_hash:
            if service.confirm_email(user, confirm_hash):
                logger.info('User %s confirmed their email %s', user.id,
                            user.email)
                login_user(user)
                return redirect('/')
            else:
                logger.warn('User with email %s tried to confirm their '
                            'email with wrong hash (expected %s - got %s)',
                            user.email, user.confirmation_hash,
                            confirm_hash)
                return make_response('The confirmation email link is wrong! '
                                     'The email cannot be confirmed.', 400)

        return make_response('No request parameters specified!', 404)


class UsersResource(Resource):
    def __init__(self):
        self.request_parser = reqparse.RequestParser()
        super(UsersResource, self).__init__()

    def post(self):
        self.request_parser.add_argument('username',
                                         type=str,
                                         required=True,
                                         help='No username is provided')
        self.request_parser.add_argument('password',
                                         type=str,
                                         required=True,
                                         help='No password is provided')
        self.request_parser.add_argument('name', type=str, required=False)

        args = self.request_parser.parse_args()
        username = args['username']
        password = args['password']
        if not username or not password:
            return make_response('Username and password are mandatory!', 400)

        user = service.find_user_by_email(username)

        if user is not None:
            logger.warn('User %s already exists', user.email)
            return make_response('User already exists', 400)

        user = service.create_new_user(username, password, args['name'])
        logger.info('New user %d with email %s has been created!', user.id,
                    user.email)
        return redirect(url_for('main', confirmationSent=True))
