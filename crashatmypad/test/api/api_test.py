import unittest
import json

from crashatmypad import create_app
from test_utils import create_test_user, create_confirmed_test_user, \
    delete_test_user

app = create_app('TESTING').test_client()


class ApiMainTest(unittest.TestCase):
    def test_api_main_get(self):
        response = app.get('/')
        assert response.status_code is 200
        assert response.headers['Content-Type'] == 'text/html'


class ApiUsersTest(unittest.TestCase):

    def test_api_new_user_post_same_email_fails(self):
        assert app.post('/user', data=dict(
            username='test@test',
            password='test'), follow_redirects=True).status_code == 200
        assert app.post('/user', data=dict(
            username='test@test',
            password='test'), follow_redirects=True).status_code == 400
        assert app.delete('/user/1', data=dict(password='test'),
                          follow_redirects=True).status_code == 200

    def test_api_new_user_with_name_post(self):
        # TODO: test that the user has the specified name
        # (when json response exists)
        assert app.get('/user/1', follow_redirects=True).status_code == 404
        assert app.post('/user', data=dict(
            username='test2@test',
            password='test',
            name='My name'), follow_redirects=True).status_code == 200
        assert app.get('/user/1', follow_redirects=True).status_code == 200
        assert app.delete('/user/1', data=dict(password='test'),
                          follow_redirects=True).status_code == 200

    def test_api_users_post_failed(self):
        """
        Tests that a new user is created only when username and password are
        given and valid
        """
        assert app.post(
            '/user',
            data=dict(username='test@test')
        ).status_code == 400
        assert app.post(
            '/user',
            data=dict(username='', password='test')
        ).status_code == 400
        assert app.post(
            '/user',
            data=dict(password='test')
        ).status_code == 400
        assert app.post(
            '/user',
            data=dict(username='test@test', password='')
        ).status_code == 400

    def test_api_new_user_confirm_failed_post(self):
        """
        Tests that a new user is created
        and their email cannot be confirmed with a wrong hash
        """
        create_test_user(app)
        assert app.post(
            '/user/1',
            data=dict(confirm='wrong_testing_confirmation_hash'),
            follow_redirects=True).status_code == 400
        delete_test_user(app)

    def test_api_user_update(self):
        """
        Tests that the users' data is updated
        """
        create_test_user(app)
        assert app.post(
            '/user/1',
            data=dict(name='Marcus',
                      last_name='Aurelius',
                      profession='Emperor',
                      birthday='0121-04-26')).status_code == 201
        # TODO test that the user has really been updated,
        # when a json-response exists
        delete_test_user(app)

    def test_api_user_post_fails_when_no_args(self):
        """
        Tests that user-post request fails when none of possible args is given
        """
        create_test_user(app)
        assert app.post('/user/1').status_code == 400
        delete_test_user(app)

    def test_api_user_not_exists(self):
        """
        Tests that no user with this id exists and the not_found is given back
        """
        assert app.get('/user/200').status_code == 404
        assert app.post('/user/200').status_code == 404
        assert (app.delete('/user/200', data=dict(password='test'))
                .status_code == 404)

    def test_delete_user(self):
        # no password
        assert app.delete('/user/200').status_code == 400

        # no password or wrong password
        create_test_user(app)
        assert (app.delete('/user/1', data=dict(password=''))
                .status_code == 400)
        assert (app.delete('/user/1', data=dict(password='wrong'))
                .status_code == 400)
        delete_test_user(app)


class SessionApiTest(unittest.TestCase):
    def test_login_logout(self):
        """
        Tests that a user can login and logout successfully
        """
        create_confirmed_test_user(app)
        assert app.post('/session', data=dict(
            username='test@test',
            password='test'), follow_redirects=True).status_code == 200
        assert app.delete('/session', follow_redirects=True).status_code == 204
        delete_test_user(app)

    def test_login_fail(self):
        """
        Tests that a user cannot login when the email is not confirmed, or
        username/password are wrong
        """

        # missing password
        assert app.post('/session', data=dict(
            username='test@test',
            password=''), follow_redirects=True).status_code == 400

        # not existing user
        assert app.post('/session', data=dict(
            username='test@test',
            password='test'), follow_redirects=True).status_code == 404

        create_test_user(app)
        # wrong password
        assert app.post('/session', data=dict(
            username='test@test',
            password='wrong-test'), follow_redirects=True).status_code == 404

        # email is not confirmed
        assert app.post('/session', data=dict(
            username='test@test',
            password='test'), follow_redirects=True).status_code == 403
        delete_test_user(app)


class LocationApiTest(unittest.TestCase):
    def test_find_locations(self):
        assert (app.get('/location', data=dict(q='Berlin,Germany'))
                .status_code == 200)


class CitiesApiTest(unittest.TestCase):
    def test_find_cities(self):
        response = app.get('/city', data=dict(q='Berlin,Berlin,Germany'))
        data = json.loads(response.data)
        assert len(data['cities']) == 1

if __name__ == "__main__":
    unittest.main()
