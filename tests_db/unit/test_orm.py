import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from music.domainmodel.genre import Genre
from music.domainmodel.track import User, Review, Track, make_comment
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album

track_date = datetime.date(2020, 2, 28)


def insert_user(empty_session, values=None):
    new_user_id = 0
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[1]
        new_password = values[2]
        new_user_id = values[0]

    empty_session.execute('INSERT INTO users (user_id, user_name, password) VALUES (:user_id, :user_name, :password)',
                          {'user_id': new_user_id, 'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT user_id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_id, user_name, password) VALUES (:user_id, :user_name, :password)',
                              {'user_id': value[0], 'user_name': value[1], 'password': value[2]})
    rows = list(empty_session.execute('SELECT user_id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks (track_id, track_duration, title, artist_id, album_id, track_url) VALUES '
        '(1, 696, '
        '"pony", '
        '"10", '
        '"61",'
        '"http://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life/Electric_Ave")')
    row = empty_session.execute('SELECT track_id from tracks').fetchone()
    return row[0]


def insert_artist(empty_session):
    empty_session.execute(
        'INSERT INTO artists (artist_id, full_name) VALUES (2, "pony"), (3, "bear")'
    )
    rows = list(empty_session.execute('SELECT artist_id from artists'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_album(empty_session):
    empty_session.execute(
        'INSERT INTO albums (album_id, title) VALUES (2, "pony_alb"), (3, "bear_alb")'
    )
    rows = list(empty_session.execute('SELECT album_id from albums'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_track_genre_associations(empty_session, track_key, genre_keys):
    stmt = 'INSERT INTO article_genres (genre_id, track_id) VALUES (:genre_id, :track_id)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'track_id': track_key, 'genre_id': genre_key})


def insert_commented_track(empty_session):
    track_key = insert_track(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, review_text, rating, timestamp, reviewer) VALUES '
        '(:user_id, "Comment 1", :rating, :timestamp_1, :reviewer),'
        '(:user_id, "Comment 2", :rating, :timestamp_2, :reviewer)',
        {'user_id': user_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2, 'rating': 5, 'reviewer': 'uncle sam'}
    )

    row = empty_session.execute('SELECT track_id from tracks').fetchone()
    return row[0]


def make_track():
    track = Track(
        1,
        "Pony"
    )
    track.track_url = 'www.pony.com'
    track.track_duration = 696
    return track


def make_artist():
    artist = Artist(
        2,
        "Pony_man"
    )
    return artist


def make_album():
    album = Album(
        2,
        "Pony_alb"
    )
    return album


def make_genre():
    genre = Genre(
        5,
        "Pony_genre"
    )
    return genre


def make_user():
    user = User(0, "Andrew", "Mercury00")
    return user


def test_loading_of_users(empty_session):
    users = list()
    users.append((0, "Andrew", "1234"))
    users.append((1, "Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User(0, "Andrew", "1234"),
        User(1, "Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, user_name, password FROM users'))
    assert rows == [(0, "andrew", "Mercury00")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, (0, "Andrew", "Mercury00"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(0, "Andrew", "Mercury00")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_track(empty_session):
    track_key = insert_track(empty_session)
    expected_track = make_track()
    fetched_track = empty_session.query(Track).one()

    assert expected_track == fetched_track
    assert track_key == fetched_track.track_id


def test_loading_of_reviewed_track(empty_session):
    insert_commented_track(empty_session)

    rows = empty_session.query(Track).all()
    track = rows[0]

    for review in track.track_reviews:
        assert review.article is track


def test_saving_of_review(empty_session):
    track_key = insert_track(empty_session)
    user_key = insert_user(empty_session, (0, "Andrew", "1234"))

    rows = empty_session.query(Track).all()
    track = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "Andrew").one()

    # Create a new review that is bidirectionally linked with the User and Article.
    review_text = "Some comment text."
    review = make_comment(review_text, user, track, 5)

    # Note: if the bidirectional links between the new Comment and the User and
    # Article objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, track_id, review_text FROM reviews'))

    assert rows == [(user_key, track_key, review_text)]


def test_saving_of_track(empty_session):
    track = make_track()
    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT track_id, track_duration, title, track_url FROM tracks'))
    assert rows == [(1,
                     696,
                    'Pony',
                     'www.pony.com'
                     )]


def test_save_reviewed_track(empty_session):
    # Create Track User objects.
    track = make_track()
    user = make_user()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    review_text = "Some comment text."
    review = make_comment(review_text, user, track, 5)

    # Save the new Article.
    empty_session.add(track)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT track_id FROM tracks'))
    track_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT user_id FROM users'))
    user_key = rows[0][0]

    # Check that the reviews table has a new record that links to the track and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, track_id, review_text FROM reviews'))
    assert rows == [(user_key, track_key, review_text)]

