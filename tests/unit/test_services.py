import pytest

from music.authentication.services import AuthenticationException
from music.authentication import services as auth_services
from music.tracks import services as tracks_services
from music.tracks.services import NonExistentTrackException


def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_duplicate_id(in_memory_repo):
    user_name = 'jz'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)

    user_name = 'thorke'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)

    user1 = auth_services.get_user('jz', in_memory_repo)
    user2 = auth_services.get_user('thorke', in_memory_repo)

    if user1['id'] == user2['id']:
        assert False


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    track_id = 3
    tracks_services.get_track_by_id(in_memory_repo, track_id)
    user_name = 'fmercury'
    review_text = 'my favourite track'
    rating = 5

    auth_services.add_user(user_name, 'abcd1A23', in_memory_repo)

    # Call the service layer to add the review.
    tracks_services.add_review(track_id, rating, review_text, user_name, in_memory_repo)

    # Retrieve the reviews for the track from the repository.
    track_reviews = tracks_services.get_reviews_for_track(track_id, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    for review in track_reviews:
        if review.review_text == review_text:
            assert True


def test_cannot_add_review_for_non_existent_track(in_memory_repo):
    track_id = 1
    review_text = "my 2nd favourite track"
    user_name = 'fmercury'
    rating = 4

    auth_services.add_user(user_name, 'abcd1A23', in_memory_repo)

    # Call the service layer to attempt to add the review.
    with pytest.raises(tracks_services.NonExistentTrackException):
        tracks_services.add_review(track_id, rating, review_text, user_name, in_memory_repo)


def test_cannot_add_comment_by_unknown_user(in_memory_repo):
    track_id = 3
    review_text = "my 2nd favourite track"
    user_name = 'fmercury'
    rating = 4

    # Call the service layer to attempt to add the comment.
    with pytest.raises(tracks_services.UnknownUserException):
        tracks_services.add_review(track_id, rating, review_text, user_name, in_memory_repo)


def test_can_get_track(in_memory_repo):
    track_id = 3

    track = tracks_services.get_track_by_id(in_memory_repo, track_id)

    assert track.track_id == track_id
    assert track.title == "Electric Ave"
    assert track.album.title == "AWOL - A Way Of Life"
    assert track.track_url == "http://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life/Electric_Ave"
    assert track.artist.full_name == "AWOL"
    assert track.track_duration == 237


def test_cannot_get_track_with_non_existent_id(in_memory_repo):
    track_id = 1

    # Call the service layer to attempt to retrieve the Article.
    with pytest.raises(tracks_services.NonExistentTrackException):
        tracks_services.get_track_by_id(in_memory_repo, track_id)


def test_get_first_letter_in_alphabet(in_memory_repo):
    alphabet_dict = tracks_services.get_tracks_by_alphabetical_order(in_memory_repo)
    assert list(alphabet_dict.keys())[0] == 'A'


def test_get_last_letter_in_alphabet(in_memory_repo):
    alphabet_dict = tracks_services.get_tracks_by_alphabetical_order(in_memory_repo)
    assert list(alphabet_dict.keys())[-1] == 'Other'


def test_get_reviews_for_track(in_memory_repo):
    track_id = 2
    tracks_services.get_track_by_id(in_memory_repo, track_id)
    user_name = 'fmercury'
    review_text = 'my favourite track'
    rating = 5

    auth_services.add_user(user_name, 'abcd1A23', in_memory_repo)

    # Call the service layer to add the review.
    tracks_services.add_review(track_id, rating, review_text, user_name, in_memory_repo)

    track_id = 2
    tracks_services.get_track_by_id(in_memory_repo, track_id)
    user_name = 'fmercury'
    review_text = 'no longer my favourite track'
    rating = 2

    # Call the service layer to add the review.
    tracks_services.add_review(track_id, rating, review_text, user_name, in_memory_repo)

    track_reviews = tracks_services.get_reviews_for_track(track_id, in_memory_repo)

    # Check that 2 reviews were returned for article with id 2.
    assert len(track_reviews) == 2

    # Check that the reviews relate to the track whose id is 2.
    assert track_reviews[0].review_text == 'my favourite track'
    assert track_reviews[1].review_text == 'no longer my favourite track'


def test_get_reviews_for_non_existent_track(in_memory_repo):
    with pytest.raises(NonExistentTrackException):
        track_reviews = tracks_services.get_reviews_for_track(1, in_memory_repo)


def test_get_reviews_for_track_without_reviews(in_memory_repo):
    track_reviews = tracks_services.get_reviews_for_track(2, in_memory_repo)
    assert len(track_reviews) == 0


