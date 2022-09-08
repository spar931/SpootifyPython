from typing import List

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review

from music.adapters.repository import AbstractRepository


def get_tracks(repo: AbstractRepository):
    return repo.get_tracks()
