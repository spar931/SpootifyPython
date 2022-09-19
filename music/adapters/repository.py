import abc

from music.domainmodel.track import Track, Review, User


repo_instance = None


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
    def get_tracks(self):
        """ Gets all Tracks """
        raise NotImplementedError

    def get_artists(self):
        """ Gets all Artists """
        raise NotImplementedError

    def get_albums(self):
        """ Gets all Albums """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_by_id(self, track_id):
        """ Gets specific track based on track_id """
        raise NotImplementedError

    @abc.abstractmethod
    def get_artist_by_id(self, track_id):
        """ Gets specific artist based on artist_id """
        raise NotImplementedError

    @abc.abstractmethod
    def get_album_by_id(self, album_id):
        """ Gets specific album based on album_id """
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
        if review.track is None:
            raise RepositoryException('review not correctly attached to a track')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_users(self):
        raise NotImplementedError
