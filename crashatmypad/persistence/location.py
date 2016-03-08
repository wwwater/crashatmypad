import math
from sqlalchemy.ext.hybrid import hybrid_method

from db import db


class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('users', lazy='dynamic'))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    street = db.Column(db.String(80))
    house = db.Column(db.String(10))
    city = db.Column(db.String(30))
    postal_code = db.Column(db.String(10))
    country = db.Column(db.String(30))

    # types of facilities available
    apartment = db.Column(db.Boolean)
    room = db.Column(db.Boolean)
    corner = db.Column(db.Boolean)
    yard = db.Column(db.Boolean)
    trees = db.Column(db.Boolean)
    driveway = db.Column(db.Boolean)
    shower = db.Column(db.Boolean)
    bathroom = db.Column(db.Boolean)

    def __init__(self, user, longitude, latitude, country, city,
                 postal_code=None, street=None, house=None,
                 apartment=False, room=False, corner=False, yard=False,
                 trees=False, driveway=False, shower=False, bathroom=False):
        self.user = user
        self.longitude = longitude
        self.latitude = latitude
        self.street = street
        self.house = house
        self.postal_code = postal_code
        self.city = city
        self.country = country

        self.apartment = apartment
        self.room = room
        self.corner = corner
        self.yard = yard
        self.trees = trees
        self.driveway = driveway
        self.shower = shower
        self.bathroom = bathroom

    def __repr__(self):
        return '<Location in {} of {} {}>'.format(self.city, self.user.name,
                                                  self.user.last_name)

    @hybrid_method
    def distance_to(self, longitude, latitude):
        r_earth = 6371
        phi0 = math.radians(self.latitude)
        phi1 = math.radians(latitude)
        lambda0 = math.radians(self.longitude)
        lambda1 = math.radians(longitude)
        d_phi = phi1 - phi0
        d_lambda = lambda1 - lambda0

        a = math.sin(d_phi / 2) * math.sin(d_phi / 2) + \
            math.cos(phi0) * math.cos(phi1) * \
            math.sin(d_lambda / 2) * math.sin(d_lambda / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return r_earth * c
