import string
from os import path

from flask import jsonify
from flask_restful import Resource, reqparse

from crashatmypad.util.trie import Trie

cities = Trie()


def _build_cities_trie():
    print "Meow"
    cities_file = path.join(path.dirname(__file__), '../../world-cities.csv')
    with open(cities_file, 'r') as f:
        for line in f:
            parts = line.split(',')
            if len(parts) == 4:
                city = parts[0]
                country = parts[1]
                state = parts[2]
                cities.add(string.join([city, state, country], ','))

    print cities.size
    print cities.get("Moscow")


_build_cities_trie()


class CitiesResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('q', type=str, required=True,
                                   help='No search query for city provided')
        super(CitiesResource, self).__init__()

    def get(self):
        """
        Searches world cities that start with the query argument.
        :return: List of cities with their state and country
        """

        args = self.reqparse.parse_args()

        query = str(string.replace(args['q'], ', ', ','))
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
