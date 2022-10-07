from datetime import date, datetime

import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.domainmodel.track import User, Review, Track, make_comment
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.adapters.repository import RepositoryException


# need to check if duplicate track_ids and for all other entities can be added, i believe i have not accounted for this yet


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(2, 'Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User(3, 'Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('laptop')
    assert user == User(0, 'laptop', 'Mercury00')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_track_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_tracks = repo.get_number_of_tracks()

    # Check that the query returned 2000 tracks.
    assert number_of_tracks == 2000


def test_repository_can_add_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_tracks = repo.get_number_of_tracks()

    new_track_id = number_of_tracks * 3

    track = Track(
            new_track_id,
            'new_track'
    )
    track.track_duration = 696
    track.track_url = 'www.pony.com'
    track.artist = repo.get_artist_by_id(1)
    track.album = repo.get_album_by_id(1)

    repo.add_track(track)

    assert repo.get_track_by_id(new_track_id) == track


def test_repository_can_retrieve_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track_by_id(3)

    # Check that the track has the expected title.
    assert track.title == 'Electric Ave'

    # Check that the track is reviewed as expected.
    review_one = [review for review in track.reviews if review.review_text == 'my favourite track'][0]

    assert review_one.reviewer == 'laptop'


def test_repository_does_not_retrieve_a_non_existent_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track_by_id(0)
    assert track is None


## artist, genre, album tests here


def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('laptop')
    track = repo.get_track_by_id(10)
    review = make_comment("addicting track", user, track, 5)

    repo.add_review(review)

    assert review in repo.get_reviews()


# def test_repository_does_not_add_a_review_without_a_user(session_factory):
#    repo = SqlAlchemyRepository(session_factory)
#
#    track = repo.get_track_by_id(2)
#    review = Review(track, "addicting track!", 5)
#
#    with pytest.raises(RepositoryException):
#        repo.add_review(review)


def test_repository_can_retrieve_comments(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_reviews()) == 2


def test_can_retrieve_a_track_and_add_a_review_to_it(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Fetch Track and User.
    track = repo.get_track_by_id(5)
    author = repo.get_user('laptop')

    # Create a new Review, connecting it to the Track and User.
    review = make_comment('wow', author, track, 5)

    track_fetched = repo.get_track_by_id(5)
    author_fetched = repo.get_user('laptop')

    assert review in track_fetched.reviews
    assert review in author_fetched.reviews

