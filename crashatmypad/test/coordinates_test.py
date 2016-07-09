import unittest

from crashatmypad.util.coordinates import bounding_box_for_distance


class BoundingBoxText(unittest.TestCase):
    def test_bounding_box(self):
        # 100 km from Hamburg
        bounding_box = bounding_box_for_distance(53.57, 10.03, 100)
        #print bounding_box

        assert float('{0:.2f}'.format(bounding_box['longitude_min'])) == 52.66
        assert float('{0:.2f}'.format(bounding_box['longitude_max'])) == 54.48
        assert float('{0:.2f}'.format(bounding_box['latitude_min'])) == 9.13
        assert float('{0:.2f}'.format(bounding_box['latitude_max'])) == 10.93

if __name__ == "__main__":
    unittest.main()
