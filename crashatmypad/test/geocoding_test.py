from crashatmypad.util.geocode import geocode


def test_geocode_full_address():
    data = \
        geocode(country='Germany', postal_code='20359', city='Hamburg',
                street='Budapesterstr.', house='45')
    assert len(data) == 1
    assert float('{0:.2f}'.format(float(data[0]['lon']))) == 9.96
    assert float('{0:.2f}'.format(float(data[0]['lat']))) == 53.56


def test_geocode_wrong_postal_code():
    data = \
        geocode(country='Germany', postal_code='30359', city='Hamburg',
                street='Budapesterstr.', house='45')
    assert len(data) == 0


def test_geocode_street_only():
    data = \
        geocode(country='Germany', city='Hamburg', street='Budapesterstr.')
    assert len(data) == 1
    assert float('{0:.2f}'.format(float(data[0]['lon']))) == 9.97
    assert float('{0:.2f}'.format(float(data[0]['lat']))) == 53.55


test_geocode_full_address()
test_geocode_wrong_postal_code()
test_geocode_street_only()
