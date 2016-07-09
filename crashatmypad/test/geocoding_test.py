import unittest

from crashatmypad.util.geocode import geocode_by_address


class GeoCodingTest(unittest.TestCase):

    def test_geocode_full_address(self):
        data = \
            geocode_by_address(country='Germany', postal_code='22299',
                               city='Hamburg', street='Barmbekerstr.', house='169')
        assert data is not None
        assert float('{0:.2f}'.format(float(data['longitude']))) == 10.00
        assert float('{0:.2f}'.format(float(data['latitude']))) == 53.59

    def test_geocode_wrong_postal_code(self):
        data = \
            geocode_by_address(country='Germany', postal_code='22290',
                               city='Hamburg', street='Barmbekerstr.', house='169')
        assert data is None

    def test_geocode_street_only(self):
        data = \
            geocode_by_address(country='Germany', city='Hamburg',
                               street='Barmbekerstr.')
        assert data is not None
        assert float('{0:.2f}'.format(float(data['longitude']))) == 10.00
        assert float('{0:.2f}'.format(float(data['latitude']))) == 53.59


if __name__ == "__main__":
    unittest.main()

