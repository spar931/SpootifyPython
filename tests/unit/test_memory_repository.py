import pytest

from music.adapters.repository import RepositoryException
from music.domainmodel.track import Track, User, make_comment, Review
from music.authentication.services import AuthenticationException
from music.tracks import services as news_services
from music.authentication import services as auth_services
from music.tracks.services import NonExistentTrackException


def test_repository_can_add_a_user(in_memory_repo):
    user = User(1513, 'dave', 'wibfu56789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = User(0, 'fmercury', '8734gfe2058v')
    in_memory_repo.add_user(user)

    user = in_memory_repo.get_user('fmercury')
    assert user == User(1234, 'fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_track_count(in_memory_repo):
    number_of_tracks = in_memory_repo.get_number_of_tracks()

    # Check that the query returned 2000 tracks.
    assert number_of_tracks == 2000


def test_repository_can_retrieve_artist_count(in_memory_repo):
    number_of_artists = in_memory_repo.get_number_of_artists()

    # Check that the query returned 263 artists.
    assert number_of_artists == 263


def test_repository_can_retrieve_album_count(in_memory_repo):
    number_of_albums = in_memory_repo.get_number_of_albums()

    # Check that the query returned 427 albums.
    assert number_of_albums == 427


def test_repository_can_retrieve_genre_count(in_memory_repo):
    number_of_genres = in_memory_repo.get_number_of_genres()

    # Check that the query returned 60 genres.
    assert number_of_genres == 60


def test_repository_can_retrieve_user_count(in_memory_repo):
    user1 = User(0, 'fmercury', 'abcd1A23')
    user2 = User(1, 'bmercury', 'abcd1A23')
    in_memory_repo.add_user(user1)
    in_memory_repo.add_user(user2)

    assert in_memory_repo.get_number_of_users() == 2


def test_repository_can_add_track(in_memory_repo):
    track = Track(1, 'new track')

    in_memory_repo.add_track(track)

    assert in_memory_repo.get_track_by_id(1) is track


def test_repository_can_get_track_by_id(in_memory_repo):
    track = Track(1, 'new track')
    in_memory_repo.add_track(track)

    find_track = in_memory_repo.get_track_by_id(1)

    assert find_track.title == 'new track'


def test_repository_does_not_retrieve_a_non_existent_track(in_memory_repo):
    track = in_memory_repo.get_track_by_id(1)
    assert track is None


def test_repository_returns_an_empty_list_for_no_reviews(in_memory_repo):
    reviews = in_memory_repo.get_reviews()

    assert len(reviews) == 0


def test_repository_can_add_a_review(in_memory_repo):
    user = User(0, 'fmercury', 'abcd1A23')
    in_memory_repo.add_user(user)

    track = in_memory_repo.get_track_by_id(3)

    review = make_comment('great track', user, track, 4)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_track_attached(in_memory_repo):
    track = in_memory_repo.get_track_by_id(3)
    review = Review(None, "This track doesn't exist", 2)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_comments(in_memory_repo):
    user = User(0, 'fmercury', 'abcd1A23')
    in_memory_repo.add_user(user)

    track = in_memory_repo.get_track_by_id(2)

    review1 = make_comment('great track', user, track, 4)
    review2 = make_comment('eh', user, track, 3)

    in_memory_repo.add_review(review1)
    in_memory_repo.add_review(review2)

    assert len(in_memory_repo.get_reviews()) == 2

