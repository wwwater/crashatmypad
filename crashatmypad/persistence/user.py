import uuid

from crashatmypad import db


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
    email_is_confirmed = db.Column(db.Boolean)
    confirmation_hash = db.Column(db.String(36))

    def __init__(self, email, name=None, last_name=None, birthday=None,
                 profession=None, phone=None):
        self.email = email
        self.name = name
        self.last_name = last_name
        self.birthday = birthday
        self.profession = profession
        self.phone = phone
        self.email_is_confirmed = False
        self.confirmation_hash = str(uuid.uuid4())

    def __repr__(self):
        return '<User {} {} with email {}>'.format(self.name, self.last_name,
                                                   self.email)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.email_is_confirmed

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.email)