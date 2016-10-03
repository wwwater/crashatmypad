import unittest
from mock import MagicMock
from datetime import date


from crashatmypad.persistence.user import User
from crashatmypad.persistence.location import Location
from crashatmypad.services.users import update_user
from crashatmypad import db


class UserTest(unittest.TestCase):
    def test_update_user(self):
        user = User('rene.descartes@gmail.com')
        assert user.name is None
        assert user.last_name is None
        assert user.profession is None
        assert user.birthday is None
        args = dict(
            name=u'Ren\xe8',
            last_name=u'Descartes',
            profession='Philosopher',
            birthday='1596-03-31'
        )
        db.session = MagicMock(return_value=True)
        update_user(args, user)
        assert user.birthday == date(1596, 3, 31)
        assert user.name == args['name'].encode('utf-8')
        assert user.last_name == args['last_name']
        assert user.profession == args['profession']


if __name__ == "__main__":
    unittest.main()
