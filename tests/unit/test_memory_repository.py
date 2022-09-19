from datetime import date, datetime
from typing import List

import pytest

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track, Review, User
from music.domainmodel.genre import Genre

from music.adapters.repository import RepositoryException


