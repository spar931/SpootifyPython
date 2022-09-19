import pytest

from music import create_app
from music.adapters import memory_repository
from music.adapters.memory_repository import MemoryRepository
from music.adapters.csvdatareader import TrackCSVReader

from utils import get_project_root

TEST_DATA_PATH = get_project_root() / "tests" / "data"


@pytest.fixture
def in_memory_repo():
    data = TrackCSVReader(str(TEST_DATA_PATH) + "/raw_albums_excerpt.csv", str(TEST_DATA_PATH) + "/raw_tracks_excerpt.csv")
    data.read_csv_files()
    repo = MemoryRepository(data)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='thorke', password='cLQ^C#oFXloS'):
        return self.__client.post(
            'authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)