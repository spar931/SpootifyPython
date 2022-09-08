import abc
from typing import List

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_id) -> User:
        """ Returns the User id from the repository.

        If there is no User with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track: Track):
        """ Adds a Track to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_tracks(self) -> int:
        """ Returns the number of Tracks in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with a track, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.Track is None or review not in review.Track.reviews:
            raise RepositoryException('review not correctly attached to a track')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError
