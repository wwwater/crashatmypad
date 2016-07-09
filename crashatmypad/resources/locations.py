from flask import render_template, make_response
from flask_restful import Resource, reqparse

from crashatmypad import logger
from crashatmypad.services.search import find_locations_by_query


class LocationsResource(Resource):
    def __init__(self):
        self.request_parser = reqparse.RequestParser()
        self.request_parser.add_argument(
            'q', type=str, required=True,
            help='No search query for location is provided')
        super(LocationsResource, self).__init__()

    def get(self):
        """
        Render the home page.
        :return: Flask response
        """
        args = self.request_parser.parse_args()
        query = args['q'] or 'Hamburg, Germany'
        logger.info('Search for a location with query %s', query)
        results = find_locations_by_query(query)
        logger.info('Found %d locations', len(results))
        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('search.html',
                            query=query,
                            results=results['locations'],
                            query_coordinates=results['query']),
            200,
            headers
        )

