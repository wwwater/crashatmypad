from crashatmypad import db
from crashatmypad.util.geocode import geocode_by_query
from crashatmypad.util.coordinates import bounding_box_for_distance
from crashatmypad.persistence.location import Location


def find_locations_by_query(query):
    query_geodata = geocode_by_query(query)
    print query_geodata
    if query_geodata is not None:
        bounding_box = bounding_box_for_distance(
            query_geodata['longitude'], query_geodata['latitude'], 100)
        found_results = build_query_with_bounding_box(bounding_box).all()
    else:
        found_results = []
    print found_results
    search_results_to_display = map(location_to_search_result, found_results)
    print search_results_to_display
    return {
        'locations': search_results_to_display,
        'query': query_geodata
    }


def build_query_with_bounding_box(bounding_box):
    query = db.session.query(Location).filter(
        ((Location.longitude > bounding_box['longitude_min']) &
         (Location.longitude < bounding_box['longitude_max']) &
         (Location.latitude > bounding_box['latitude_min']) &
         (Location.latitude < bounding_box['latitude_max'])))
    print query
    return query


def location_to_search_result(location):
    return {
        'user_name': str(location.user.name),
        'user_id': str(location.user_id),
        'street': str(location.street),
        'city': str(location.city),
        'longitude': location.longitude,
        'latitude': location.latitude
    }

