import pytest

from chatapp.db import get_db


def test_index(client, auth):
    # Can't see chat without logging in first
    response = client.get('/')
    assert 'http://localhost/auth/login' == response.headers['Location']

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data


def test_message_in_chat(client, auth):
    auth.login()
    response = client.get()
    assert b'test message' in response.data
