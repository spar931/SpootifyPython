from datetime import date, datetime
from typing import List

import pytest

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track, Review, User
from music.domainmodel.genre import Genre

from music.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User(1513, 'dave', 'wibfu56789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User(1234, 'fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None