from flask import render_template, make_response
from flask_restful import Resource, reqparse

from crashatmypad import logger


class MainResource(Resource):
    def __init__(self):
        self.request_parser = reqparse.RequestParser()
        super(MainResource, self).__init__()

    def get(self):
        """
        Render the home page.
        :return: Flask response
        """
        self.request_parser.add_argument('confirmationSent',
                                         type=bool,
                                         required=False)
        self.request_parser.add_argument('confirm',
                                         type=str,
                                         required=False)
        self.request_parser.add_argument('user',
                                         type=str,
                                         required=False)
        args = self.request_parser.parse_args()
        confirmation_email_sent = args['confirmationSent'] or False
        confirmation_hash = args['confirm']
        user = args['user']
        logger.info('The main page was requested. Confirmation-email-sent '
                    'message: %s', confirmation_email_sent)
        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('landing_page.html',
                            confirmation_email_sent=confirmation_email_sent,
                            user=user,
                            confirmation_hash=confirmation_hash),
            200,
            headers
        )


#
# @app.route('/whatsinanamethatwhichwecallarosebyanyothernamewouldsmellassweet')
# def api_seed():
#     """
#     Reset the database and seed it with a few messages.
#
#     :return: Flask redirect
#     """
#     db.drop_all()
#     db.create_all()
#
#     user1 = User(
#         email='laura@moreaux.com',
#         name='Laura',
#         last_name='Moreaux',
#         birthday=date(1987, 6, 7),
#         profession='Architect'
#     )
#
#     db.session.add(user1)
#     db.session.commit()
#
#     user1_location1 = Location(user=user1,
#                                longitude=9.9711,
#                                latitude=53.5818,
#                                country='Germany',
#                                city='Hamburg',
#                                street='Eppendorfer Weg',
#                                house=219,
#                                corner=True,
#                                shower=True,
#                                bathroom=True)
#
#     user1_location2 = Location(user=user1,
#                                longitude=11.2438,
#                                latitude=49.4869,
#                                country='Germany',
#                                city='Roetenbach an der Pegnitz',
#                                street="Alter Kirchenweg",
#                                house=35,
#                                apartment=True)
#     db.session.add(user1_location1)
#     db.session.add(user1_location2)
#     db.session.commit()
#
#     user2 = User(
#         email='lena@anderson.com',
#         name='Lena',
#         last_name='Anderson',
#         birthday=date(1983, 6, 17),
#         profession='Carpenter'
#     )
#
#     db.session.add(user2)
#     db.session.commit()
#
#     user2_location1 = Location(user=user2,
#                                longitude=10.0325,
#                                latitude=53.5745,
#                                country='Germany',
#                                city='Hamburg',
#                                street='Heitmannstr.',
#                                corner=True,
#                                shower=True,
#                                bathroom=True)
#
#     db.session.add(user2_location1)
#     db.session.commit()
#
#     user3 = User(
#         email='chris@hasselberg.com',
#         name='Chris',
#         last_name='Hasselberg',
#         birthday=date(1981, 2, 9),
#         profession='Manager'
#     )
#
#     db.session.add(user3)
#     db.session.commit()
#
#     user3_location1 = Location(user=user3,
#                                longitude=10.0131,
#                                latitude=53.4902,
#                                country='Germany',
#                                city='Hamburg',
#                                street='Hanseatenweg',
#                                corner=True,
#                                shower=True,
#                                bathroom=True)
#
#     db.session.add(user3_location1)
#     db.session.commit()
#
#     return redirect(url_for('page.index'))
