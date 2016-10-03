import unittest
from mock import MagicMock
from datetime import date


from crashatmypad.persistence.user import User
from crashatmypad.persistence.location import Location
from crashatmypad.services.users import update_user
from crashatmypad import db, logger


class UserTest(unittest.TestCase):
    def test_update_user(self):
        user = User('rene.descartes@example.com')
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
        db.session = MagicMock()
        logger.warn = MagicMock()
        update_user(args, user)
        assert user.birthday == date(1596, 3, 31)
        assert user.name == args['name'].encode('utf-8')
        assert user.last_name == args['last_name']
        assert user.profession == args['profession']
        assert logger.warn.call_count == 0

    def test_update_user_birthday_fail(self):
        user = User('julius.caesar@example.com')
        assert user.birthday is None
        args = dict(
            birthday='-100-07-13'
        )
        logger.warn = MagicMock()
        assert update_user(args, user) is False
        assert user.birthday is None
        assert logger.warn.call_count == 1


if __name__ == "__main__":
    unittest.main()
