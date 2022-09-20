import pytest

from music.domainmodel.track import User
from music.authentication.services import AuthenticationException
from music.tracks import services as news_services
from music.authentication import services as auth_services
from music.tracks.services import NonExistentArticleException


def test_repository_can_add_a_user(in_memory_repo):
    user = User(1513, 'dave', 'wibfu56789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = User(0, 'fmercury', '8734gfe2058v')
    in_memory_repo.add_user(user)

    user = in_memory_repo.get_user('fmercury')
    assert user == User(0, 'fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None