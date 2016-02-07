from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    birthday = db.Column(db.Date)
    profession = db.Column(db.String(120))
    phone = db.Column(db.Integer)
    locations = db.relationship('Location')

    def __init__(self, email, name, last_name, birthday=None, profession=None,
                 phone=None):
        self.email = email
        self.name = name
        self.last_name = last_name
        self.birthday = birthday
        self.profession = profession
        self.phone = phone

    def __repr__(self):
        return '<User {} {}>'.format(self.name, self.last_name)


class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('users', lazy='dynamic'))
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

    def __init__(self, user, country, city, postal_code=None, street=None,
                 house=None, apartment=False, room=False, corner=False,
                 yard=False, trees=False, driveway=False, shower=False,
                 bathroom=False):
        self.user = user
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

