from typing import List

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader


class MemoryRepository(AbstractRepository):

    def __init__(self, data: TrackCSVReader):
        self.__users = list()
        self.__reviews = list()
        self.__data = data

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_id) -> User:
        return next((user for user in self.__users if user.user_name == user_id), None)

    def get_tracks(self):
        return self.__data.dataset_of_tracks

    def add_track(self, track: Track):
        self.__data.dataset_of_tracks.append(track)

    def get_number_of_tracks(self) -> int:
        return len(self.__data.dataset_of_tracks)

    def get_track_by_id(self, track_id):
        chosen_track = None
        for track in self.__data.dataset_of_tracks:
            if int(track_id) == track.track_id:
                chosen_track = track
                return chosen_track
        return chosen_track

    def add_review(self, review: Review):
        # call parent class first, add_review relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews
