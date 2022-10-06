from pathlib import Path

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader
from music.authentication import services as auth_services
from music.tracks import services as track_services
from music.domainmodel.track import Review, Track


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    reader = TrackCSVReader()
    # Load tracks, albums and artists into the repository.
    reader.read_csv_files(data_path, repo, database_mode)

    auth_services.add_user('laptop', 'Mercury00', repo)
    auth_services.add_user('notebook', 'Mercury00', repo)

    # track = Track(0, 'test_track')
    # review_text = 'my favourite track'
    # track.track_reviews.append(Review(track, review_text, 4))
