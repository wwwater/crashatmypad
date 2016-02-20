import urllib
import urllib2
import json


def geocode(country, city, postal_code=None, street=None, house=None):
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
    return data
