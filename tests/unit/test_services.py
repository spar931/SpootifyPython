import pytest

from music.authentication.services import AuthenticationException
from music.authentication import services as auth_services


def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_duplicate_id(in_memory_repo):
    user_name = 'jz'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)

    user_name = 'thorke'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)

    user1 = auth_services.get_user('jz', in_memory_repo)
    user2 = auth_services.get_user('thorke', in_memory_repo)

    if user1['id'] == user2['id']:
        assert False


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)