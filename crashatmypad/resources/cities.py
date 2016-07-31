import string
from os import path

from flask import jsonify
from flask_restful import Resource, reqparse

from crashatmypad import logger
from crashatmypad.util.trie import Trie

cities = Trie()


def _build_cities_trie():
    cities_file = path.join(path.dirname(__file__), '../../world-cities.csv')
    with open(cities_file, 'r') as f:
        for line in f:
            parts = line.split(',')
            if len(parts) == 4:
                city = parts[0]
                country = parts[1]
                state = parts[2]
                cities.add(string.join([city, state, country], ','))
    logger.info('Loaded cities into the trie in memory, size: %d',
                cities.size)


_build_cities_trie()


class CitiesResource(Resource):
    def __init__(self):
        self.request_parser = reqparse.RequestParser()
        self.request_parser.add_argument(
            'q', type=unicode, required=True,
            help='No search query for city provided')
        super(CitiesResource, self).__init__()

    def get(self):
        """
        Searches world cities that start with the query argument.
        :return: List of cities with their state and country
        """

        args = self.request_parser.parse_args()

        query = str(string.replace(args['q'].encode('utf-8'), ', ', ','))
        logger.info('Search a world city with query %s', query)

        def world_city_to_display_format(entry):
            parts = entry.split(',')
            return {
                'city': string.capwords(parts[0]),
                'state': string.capwords(parts[1]),
                'country': string.capwords(parts[2])
            }

        results = map(world_city_to_display_format, cities.get(query))
        return jsonify(cities=results)
