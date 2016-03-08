from __future__ import division
import math

R = 6371


def bounding_box_for_distance(longitude, latitude, distance):

    d_lon = math.degrees(distance / (R * math.cos(math.radians(latitude))))
    d_lat = math.degrees(distance / R)

    return {
        'longitude_min': longitude - d_lon,
        'longitude_max': longitude + d_lon,
        'latitude_min': latitude - d_lat,
        'latitude_max': latitude + d_lat
    }