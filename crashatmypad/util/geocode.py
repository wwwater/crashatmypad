import urllib
import urllib2
import json


def geocode_by_address(country, city, postal_code=None, street=None, house=None):
    street_house = street + (' ' + house if house else '') if street else ''
    query = urllib.urlencode({
        'country': country,
        'postalcode': postal_code if postal_code else '',
        'city': city,
        'street': street_house,
        'limit': 1})
    url = 'http://nominatim.openstreetmap.org/search.php?format=json&' + query
    # print url
    request = urllib2.Request(url, None, {'Content-Type': 'application/json'})
    response = urllib2.urlopen(request)
    data = response.read()
    data = json.loads(data)
    return __to_latitude_longitude__(data)


def geocode_by_query(query):
    url = 'http://nominatim.openstreetmap.org/search.php?format=json&' + \
          'limit=1&' + urllib.urlencode({'q': query})
    request = urllib2.Request(url, None, {'Content-Type': 'application/json'})
    response = urllib2.urlopen(request)
    data = response.read()
    data = json.loads(data)
    return __to_latitude_longitude__(data)


def __to_latitude_longitude__(geocode_data):
    if len(geocode_data) > 0:
        result = geocode_data[0]
        return {'latitude': float(result['lat']),
                'longitude': float(result['lon']),
                'bounding_box': {
                    'longitude_min': float(result['boundingbox'][2]),
                    'latitude_min': float(result['boundingbox'][0]),
                    'longitude_max': float(result['boundingbox'][3]),
                    'latitude1_max': float(result['boundingbox'][1])
                }}
    return None

