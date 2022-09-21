import pytest

from flask import session

from music.tracks import services as tracks_services
from music.authentication import services as auth_services
import music.adapters.repository as repo


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'blah' in response.data


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

    