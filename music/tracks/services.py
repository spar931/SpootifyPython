import string

from music.adapters.repository import AbstractRepository

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review


class NonExistentArticleException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_tracks_by_alphabetical_order(repo: AbstractRepository):

    alphabet_dict = {k: [] for k in string.ascii_uppercase}
    alphabet_dict['Other'] = []
    for track in repo.get_tracks():
        if track.title[0].isalpha():
            alphabet_dict[track.title[0].upper()].append(track)
        else:
            alphabet_dict['Other'].append(track)
    for value in alphabet_dict.values():
        value.sort(key=lambda x: x.title, reverse=False)
    return alphabet_dict


def get_track_by_id(repo: AbstractRepository, track_id):
    return repo.get_track_by_id(track_id)


def add_review(track_id: int, rating: int, review_text: str, user_name: str, repo: AbstractRepository):
    # Check that the track exists.
    track = repo.get_track_by_id(track_id)
    if track is None:
        raise NonExistentArticleException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = Review(track, review_text, rating)
    user.add_review(review)
    track.add_review(review)

    # Update the repository.
    repo.add_review(review)
