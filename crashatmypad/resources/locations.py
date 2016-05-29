from flask import render_template, make_response
from flask_restful import Resource, reqparse

from crashatmypad.services.search import find_locations_by_query


class LocationsResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('q',
                                   type=str,
                                   required=True,
                                   help=
                                   'No search query for location is provided')
        super(LocationsResource, self).__init__()

    def get(self):
        """
        Render the home page.
        :return: Flask response
        """
        args = self.reqparse.parse_args()
        query = args['q'] or 'Hamburg, Germany'
        print query
        results = find_locations_by_query(query)
        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('search.html',
                            query=query,
                            results=results['locations'],
                            query_coordinates=results['query']),
            200,
            headers
        )

