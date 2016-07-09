from flask import make_response, redirect, url_for
from flask_restful import Resource, reqparse
from flask_login import login_user, logout_user, login_required, current_user

from crashatmypad import logger, login_manager

import crashatmypad.services.users as users_service


class SessionResource(Resource):
    def __init__(self):
        self.request_parser = reqparse.RequestParser()
        super(SessionResource, self).__init__()

    def post(self):
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
            return make_response('Username and password are mandatory!', 400)

        user = users_service.find_user_by_email(username)

        if user is None:
            return make_response('User ' + username + ' does not exist!', 400)
        else:
            logger.info('Logging in with an existing username: %s',
                        user.email)
            existing_password_entry = \
                users_service.find_user_password_by_email(username)
            if not existing_password_entry.verify_password(password):
                logger.warn('User %s tried to login with a wrong password',
                            user.email)
                return make_response('Wrong password', 403)
            elif not user.email_is_confirmed:
                logger.warn('User %s has not verified their email yet.'
                            ' Login attempt denied.',
                            user.email)
                return make_response(
                    'Please confirm the email first.'
                    'The confirmation link is sent to your email.', 403)
            else:
                login_user(user)
                logger.info('User %s logged in', user.email)
                return redirect('/')

    @login_required
    def delete(self):
        logger.info('User %s logging out.', current_user.email)
        logout_user()
        print current_user
        return redirect('/', code=303)


@login_manager.user_loader
def load_user(username):
    return users_service.find_user_by_email(username)
