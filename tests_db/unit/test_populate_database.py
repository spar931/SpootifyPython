from sqlalchemy import select, inspect

from music.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['albums', 'article_genres', 'artists', 'genres', 'reviews', 'tracks', 'users']


def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['laptop', 'notebook']


def test_database_populate_select_all_reviews(database_engine): #still need to do this

    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table comments
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['id'], row['track_id'], row['user_id'], row['review_text'], row['rating'], row['reviewer']))

        assert all_reviews == [(1, 3, 0, 'my favourite track', 5, 'laptop'), (2, 5, 1, 'i hate this track', 1, 'notebook')]


def test_database_populate_select_all_tracks(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_tracks_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table tracks
        select_statement = select([metadata.tables[name_of_tracks_table]])
        result = connection.execute(select_statement)

        all_tracks = []
        for row in result:
            all_tracks.append((row['track_id'], row['title']))

        nr_articles = len(all_tracks)
        assert nr_articles == 2000

        assert all_tracks[0] == (2, 'Food')


def test_database_populate_select_all_albums(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_albums_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table albums
        select_statement = select([metadata.tables[name_of_albums_table]])
        result = connection.execute(select_statement)

        all_albums = []
        for row in result:
            all_albums.append((row['album_id'], row['title']))

        nr_albums = len(all_albums)
        assert nr_albums == 427

        assert all_albums[0] == (1, 'AWOL - A Way Of Life')


def test_database_populate_select_all_artists(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_artists_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table artists
        select_statement = select([metadata.tables[name_of_artists_table]])
        result = connection.execute(select_statement)

        all_artists = []
        for row in result:
            all_artists.append((row['artist_id'], row['full_name']))

        nr_artists = len(all_artists)
        assert nr_artists == 263

        assert all_artists[0] == (1, 'AWOL')


def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genres = []
        for row in result:
            all_genres.append((row['genre_id'], row['name']))

        nr_genres = len(all_genres)
        assert nr_genres == 60

        assert all_genres[0] == (1, 'Avant-Garde')

