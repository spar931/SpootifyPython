from pathlib import Path

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    # Load tracks, albums and artists into the repository.
    load_info(data_path, repo, database_mode)
