import pytest

from flask import session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Spootify is a Web Application that assists users to discover and rediscover Music.' in response.data


def test_track_with_review(client):
    # Check that we can retrieve the articles page.
    response = client.get('/display_track_info_comments?track_id=3')
    assert response.status_code == 200

    # Check that all comments for specified track are included on the page.
    assert b'my favourite track' in response.data


@pytest.mark.parametrize(('review', 'messages'), (
        ('Who thinks Trump is a f***wit?', b'Your comment must not contain profanity'),
        ('Hey', b'Your comment is too short'),
        ('ass', (b'Your comment is too short' or b'Your comment must not contain profanity')),
))
def test_comment_with_invalid_input(client, auth, review, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/review',
        data={'review': review, 'track_id': 2}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_track_info(client):
    # Check that we can retrieve the articles page.
    response = client.get('/display_track_info?track_id=3')
    assert response.status_code == 200

    # Check that all articles on the requested date are included on the page.
    assert b'Electric Ave' in response.data
    assert b'AWOL' in response.data


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'



@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit')))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


@pytest.mark.parametrize(('review', 'messages'), (
        ('Who thinks Trump is a f***wit?', b'Your comment must not contain profanity'),
        ('Hey', b'Your comment is too short'),
        ('ass', (b'Your comment is too short' or b'Your comment must not contain profanity')),
))
def test_comment_with_invalid_input(client, auth, review, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/review',
        data={'review': review, 'track_id': 2}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit')))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data



