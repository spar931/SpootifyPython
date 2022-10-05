from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track, Review, User
from music.domainmodel.genre import Genre
from music.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return user

    def get_tracks(self):
        return self._session_cm.session.query(Track)

    def get_artists(self):
        return self._session_cm.session.query(Artist)

    def get_albums(self):
        return self._session_cm.session.query(Album)

    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.merge(track)
            scm.commit()

    def add_artist(self, artist: Artist):
        with self._session_cm as scm:
            scm.session.merge(artist)
            scm.commit()

    def add_album(self, album: Album):
        with self._session_cm as scm:
            scm.session.merge(album)
            scm.commit()

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def get_number_of_tracks(self) -> int:
        return self._session_cm.session.query(Track).count()

    def get_number_of_artists(self) -> int:
        return self._session_cm.session.query(Artist).count()

    def get_number_of_albums(self) -> int:
        return self._session_cm.session.query(Album).count()

    def get_number_of_genres(self) -> int:
        return self._session_cm.session.query(Genre).count()

    def get_track_by_id(self, track_id):
        track = None
        try:
            track = self._session_cm.session.query(Track).filter(Track._Track__track_id == track_id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return track

    def get_artist_by_id(self, artist_id):
        artist = None
        try:
            artist = self._session_cm.session.query(Artist).filter(Artist._Artist__artist_id == artist_id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return artist

    def get_album_by_id(self, album_id):
        album = None
        try:
            album = self._session_cm.session.query(Album).filter(Album._Album__album_id == album_id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return album

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self):
        return self._session_cm.session.query(Review)

    def get_number_of_users(self):
        return self._session_cm.session.query(User).count()

