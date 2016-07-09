import unittest

from crashatmypad import create_app

app = create_app('TESTING').test_client()


class ApiMainTest(unittest.TestCase):

    def test_api_main_get(self):
        response = app.get('/')
        assert response.status_code is 200
        assert response.headers['Content-Type'] == 'text/html'


class ApiUsersTest(unittest.TestCase):

    def test_api_users_post(self):
        """
        Tests that a new user is created (with id 1)
        and it get be requested afterwards
        """
        response = app.post('/user', data=dict(
            username='test@test',
            password='test'), follow_redirects=True)
        assert response.status_code == 200
        response = app.get('/user/1', follow_redirects=True)
        assert response.status_code == 200

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

    def test_api_users_get(self):
        """
        Tests that no user with id 2 exists and the 400 is given back
        """
        response = app.get('/user/2', follow_redirects=True)
        assert response.status_code == 400


if __name__ == "__main__":
    unittest.main()
