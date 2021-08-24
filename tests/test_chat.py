import pytest

from chatapp.db import get_db


def test_index(client, auth):
    # Can't see chat without logging in first
    response = client.get('/')
    assert 'http://localhost/auth/login' == response.headers['Location']

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data


# Tests that messages in the database are shown in the chat when the user enters
def test_message_in_chat(client, auth):
    auth.login()
    response = client.get()
    assert b'test message' in response.data
