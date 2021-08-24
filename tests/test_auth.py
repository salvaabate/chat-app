import pytest
from chatapp.db import get_db


# Testing user registration
def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


# Testing more user registration
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', 'sadsdas', b'Username is required'),
    ('a', '', b'Password is required'),
    ('test', 'test', b'already exists'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


# Testing registered users
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('test', 'a', b'Incorrect password'),
    ('a', 'a', b'Username not found')
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

