from crashatmypad.util.geocode import geocode


def test_geocode_full_address():
    data = \
        geocode(country='Germany', postal_code='22299', city='Hamburg',
                street='Barmbekerstr.', house='169')
    assert len(data) == 1
    assert float('{0:.2f}'.format(float(data[0]['lon']))) == 10.00
    assert float('{0:.2f}'.format(float(data[0]['lat']))) == 53.59


def test_geocode_wrong_postal_code():
    data = \
        geocode(country='Germany', postal_code='22290', city='Hamburg',
                street='Barmbekerstr.', house='169')
    assert len(data) == 0


def test_geocode_street_only():
    data = \
        geocode(country='Germany', city='Hamburg', street='Barmbekerstr.')
    assert len(data) == 1
    assert float('{0:.2f}'.format(float(data[0]['lon']))) == 10.01
    assert float('{0:.2f}'.format(float(data[0]['lat']))) == 53.59


test_geocode_full_address()
test_geocode_wrong_postal_code()
test_geocode_street_only()
