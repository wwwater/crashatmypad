from passlib.apps import custom_app_context as pwd_context
from crashatmypad import db


class Password(db.Model):
    __tablename__ = 'passwords'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), db.ForeignKey('users.email'),
                         unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)