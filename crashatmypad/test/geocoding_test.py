from crashatmypad.util.geocode import geocode_by_address


def test_geocode_full_address():
    data = \
        geocode_by_address(country='Germany', postal_code='22299',
                           city='Hamburg', street='Barmbekerstr.', house='169')
    assert data is not None
    assert float('{0:.2f}'.format(float(data['longitude']))) == 10.00
    assert float('{0:.2f}'.format(float(data['latitude']))) == 53.59


def test_geocode_wrong_postal_code():
    data = \
        geocode_by_address(country='Germany', postal_code='22290',
                           city='Hamburg', street='Barmbekerstr.', house='169')
    assert data is None


def test_geocode_street_only():
    data = \
        geocode_by_address(country='Germany', city='Hamburg',
                           street='Barmbekerstr.')
    assert data is not None
    assert float('{0:.2f}'.format(float(data['longitude']))) == 10.01
    assert float('{0:.2f}'.format(float(data['latitude']))) == 53.59


test_geocode_full_address()
test_geocode_wrong_postal_code()
test_geocode_street_only()
