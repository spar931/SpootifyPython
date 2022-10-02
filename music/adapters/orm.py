from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track, Review, User
from music.domainmodel.genre import Genre

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.id')),
    Column('review_text', String(1024), nullable=False),
    Column('rating', Integer, nullable=True),
    Column('timestamp', DateTime, nullable=False)
)

tracks_table = Table(
    'tracks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('duration', Integer, nullable=False),
    Column('title', String(255), nullable=False),
    Column('artist_id', ForeignKey('artists.id')),
    Column('album_id', ForeignKey('albums.id')),
    # Column('reviews_id', ForeignKey('reviews.id')),
    # Column('genres_id', ForeignKey('genres.id')),
    Column('url', String(255), nullable=False)
)

artists_table = Table(
    'artists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(64), nullable=False)
)

albums_table = Table(
    'albums', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('url', String(255), nullable=False),
    Column('type', String(255), nullable=False)
    Column('release_year', Integer, nullable=False)
)

genres_table = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password
    })
    mapper(Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.review,
        '_Review__track_id': reviews_table.c.track_id,
        '_Review__rating': reviews_table.c.rating,
        '_Comment__timestamp': reviews_table.c.timestamp
    })
    mapper(Track, tracks_table, properties={
        '_Track__id': tracks_table.c.id,
        '_Track__duration': tracks_table.c.duration,
        '_Track__title': tracks_table.c.title,
        '_Track__artist_id': tracks_table.c.artist_id,
        '_Track__album_id': tracks_table.c.album_id,
        '_Track__url': tracks_table.c.url,
        '_Track__reviews': relationship(Review, backref='_Review__track'),
        '_Track__genres': relationship(Genre, backref='_Genre__track')
    })
    mapper(Artist, artists_table, properties={
        '_Artist__full_name': artists_table.c.full_name
    })
    mapper(Album, albums_table, properties={
        '_Album__title': albums_table.c.title,
        '_Album__url': albums_table.c.url,
        '_Album__type': albums_table.c.type,
        '_Album__release_year': albums_table.c.release_year
    })
    mapper(Genre, genres_table, properties={
        '_Genre__name': genres_table.c.name
    })

