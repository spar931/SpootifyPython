from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track, Review, User
from music.domainmodel.genre import Genre


class MemoryRepository(AbstractRepository):

    def __init__(self, data: TrackCSVReader):
        self.__users = list()
        self.__reviews = list()
        self.__data = data

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_tracks(self):
        return self.__data.dataset_of_tracks

    def get_artists(self):
        return self.__data.dataset_of_artists

    def get_albums(self):
        return self.__data.dataset_of_albums

    def add_track(self, track: Track):
        self.__data.dataset_of_tracks.append(track)

    def add_artist(self, artist: Artist):
        self.__data.dataset_of_artists.add(artist)

    def add_album(self, album: Album):
        self.__data.dataset_of_albums.add(album)

    def add_genre(self, genre: Genre):
        self.__data.dataset_of_genres.add(genre)

    def get_number_of_tracks(self) -> int:
        return len(self.__data.dataset_of_tracks)

    def get_number_of_artists(self) -> int:
        return len(self.__data.dataset_of_artists)

    def get_number_of_albums(self) -> int:
        return len(self.__data.dataset_of_albums)

    def get_number_of_genres(self) -> int:
        return len(self.__data.dataset_of_genres)

    def get_track_by_id(self, track_id):
        chosen_track = None
        for track in self.__data.dataset_of_tracks:
            if int(track_id) == track.track_id:
                chosen_track = track
                return chosen_track
        return chosen_track

    def get_artist_by_id(self, artist_id):
        chosen_artist = None
        for artist in self.__data.dataset_of_artists:
            if int(artist_id) == artist.artist_id:
                chosen_artist = artist
                return chosen_artist
        return chosen_artist

    def get_album_by_id(self, album_id):
        chosen_album = None
        for album in self.__data.dataset_of_albums:
            if int(album_id) == album.album_id:
                chosen_album = album
                return chosen_album
        return chosen_album

    def get_genre_by_id(self, genre_id):
        chosen_genre = None
        for genre in self.__data.dataset_of_genres:
            if int(genre_id) == genre.genre_id:
                chosen_genre = genre
                return chosen_genre
        return chosen_genre

    def add_review(self, review: Review):
        # call parent class first, add_review relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

    def get_number_of_users(self):
        return len(self.__users)

