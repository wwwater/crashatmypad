from db import db


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

    def __init__(self, email, name=None, last_name=None, birthday=None,
                 profession=None, phone=None):
        self.email = email
        self.name = name
        self.last_name = last_name
        self.birthday = birthday
        self.profession = profession
        self.phone = phone

    def __repr__(self):
        return '<User {} {}>'.format(self.name, self.last_name)