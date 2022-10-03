import os
import csv
import ast

from pathlib import Path

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track, Review, User
from music.domainmodel.genre import Genre
from music.adapters.repository import AbstractRepository


def create_track_object(track_row):
    track = Track(int(track_row['track_id']), track_row['track_title'])
    track.track_url = track_row['track_url']
    track_duration = round(float(
        track_row['track_duration'])) if track_row['track_duration'] is not None else None
    if type(track_duration) is int:
        track.track_duration = track_duration
    return track


def create_artist_object(track_row):
    artist_id = int(track_row['artist_id'])
    artist = Artist(artist_id, track_row['artist_name'])
    return artist


def create_album_object(row):
    album_id = int(row['album_id'])
    album = Album(album_id, row['album_title'])
    album.album_url = row['album_url']
    album.album_type = row['album_type']

    album.release_year = int(
        row['album_year_released']) if row['album_year_released'].isdigit() else None

    return album


def extract_genres(track_row: dict):
    # List of dictionaries inside the string.
    track_genres_raw = track_row['track_genres']
    # Populate genres. track_genres can be empty (None)
    genres = []
    if track_genres_raw:
        try:
            genre_dicts = ast.literal_eval(
                track_genres_raw) if track_genres_raw != "" else []

            for genre_dict in genre_dicts:
                genre = Genre(
                    int(genre_dict['genre_id']), genre_dict['genre_title'])
                genres.append(genre)
        except Exception as e:
            print(track_genres_raw)
            print(f'Exception occurred while parsing genres: {e}')

    return genres


class TrackCSVReader:

    def __init__(self, albums_csv_file: str, tracks_csv_file: str):
        if type(albums_csv_file) is str:
            self.__albums_csv_file = albums_csv_file
        else:
            raise TypeError('albums_csv_file should be a type of string')

        if type(tracks_csv_file) is str:
            self.__tracks_csv_file = tracks_csv_file
        else:
            raise TypeError('tracks_csv_file should be a type of string')

        # List of unique tracks
        self.__dataset_of_tracks = []
        # Set of unique artists
        self.__dataset_of_artists = set()
        # Set of unique albums
        self.__dataset_of_albums = set()
        # Set of unique genres
        self.__dataset_of_genres = set()

    @property
    def dataset_of_tracks(self) -> list:
        return self.__dataset_of_tracks

    @property
    def dataset_of_albums(self) -> set:
        return self.__dataset_of_albums

    @property
    def dataset_of_artists(self) -> set:
        return self.__dataset_of_artists

    @property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres

    def read_albums_file_as_dict(self, data_path: Path) -> dict:
        if not os.path.exists(str(data_path / "raw_albums_excerpt.csv")):
            print(str(data_path / "raw_albums_excerpt.csv") + " does not exist!")

        album_dict = dict()
        # encoding of unicode_escape is required to decode successfully
        with open(self.__albums_csv_file, encoding="unicode_escape") as album_csv:
            reader = csv.DictReader(album_csv)
            for row in reader:
                album_id = int(
                    row['album_id']) if row['album_id'].isdigit() else row['album_id']
                if type(album_id) is not int:
                    print(f'Invalid album_id: {album_id}')
                    print(row)
                    continue
                album = create_album_object(row)
                album_dict[album_id] = album

        return album_dict

    def read_tracks_file(self, data_path: Path):
        if not os.path.exists(str(data_path / "raw_tracks_excerpt.csv")):
            print(str(data_path / "raw_tracks_excerpt.csv") + " does not exist!")
            return
        track_rows = []
        # encoding of unicode_escape is required to decode successfully
        with open(self.__tracks_csv_file, encoding='unicode_escape') as track_csv:
            reader = csv.DictReader(track_csv)
            for track_row in reader:
                track_rows.append(track_row)
        return track_rows

    def read_csv_files(self, data_path: Path, repo: AbstractRepository, database_mode: bool):
        # key is album_id
        albums_dict: dict = self.read_albums_file_as_dict(data_path)
        # list of track csv rows, not track objects
        track_rows: list = self.read_tracks_file(data_path)

        # Make sure re-initialize to empty list, so that calling this function multiple times does not create
        # duplicated dataset.
        self.__dataset_of_tracks = []
        for track_row in track_rows:
            track = create_track_object(track_row)
            artist = create_artist_object(track_row)
            track.artist = artist

            # Extract track_genres attributes and assign genres to the track.
            track_genres = extract_genres(track_row)
            for genre in track_genres:
                track.add_genre(genre)

            album_id = int(
                track_row['album_id']) if track_row['album_id'].isdigit() else None

            album = albums_dict[album_id] if album_id in albums_dict else None
            track.album = album

            if not database_mode:
                # Populate datasets for Artist and Genre
                if artist not in self.__dataset_of_artists:
                    self.__dataset_of_artists.add(artist)

                if album is not None and album not in self.__dataset_of_albums:
                    self.__dataset_of_albums.add(album)

                for genre in track_genres:
                    if genre not in self.__dataset_of_genres:
                        self.__dataset_of_genres.add(genre)

                self.__dataset_of_tracks.append(track)
            else:
                repo.add_album(album)
                repo.add_artist(artist)
                for genre in track_genres:
                    repo.add_genre(genre)
                repo.add_track(track)

        return self.__dataset_of_tracks


