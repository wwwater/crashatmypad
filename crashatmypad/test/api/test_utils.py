def create_test_user(app):
    assert app.get('/user/1', follow_redirects=True).status_code == 404
    assert app.post('/user', data=dict(
        username='test@test',
        password='test'), follow_redirects=True).status_code == 200
    assert app.get('/user/1', follow_redirects=True).status_code == 200


def create_confirmed_test_user(app):
    create_test_user(app)
    assert app.post('/user/1', data=dict(
        confirm='testing_confirmation_hash'
    ), follow_redirects=True).status_code == 200


def delete_test_user(app):
    assert app.delete('/user/1', data=dict(password='test'),
                      follow_redirects=True).status_code == 200
