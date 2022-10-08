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

    track_services.add_review(3, 5, 'my favourite track', 'laptop', repo)
    track_services.add_review(5, 1, 'i hate this track', 'notebook', repo)

