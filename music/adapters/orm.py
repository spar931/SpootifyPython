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
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.track_id')),
    Column('review_text', String(1024), nullable=False),
    Column('rating', Integer, nullable=True),
    Column('timestamp', DateTime, nullable=False)
)

tracks_table = Table(
    'tracks', metadata,
    Column('track_id', Integer, primary_key=True),
    Column('track_duration', Integer, nullable=False),
    Column('title', String(255), nullable=False),
    Column('artist_id', ForeignKey('artists.artist_id')),
    Column('album_id', ForeignKey('albums.album_id')),
    Column('genres_id', ForeignKey('genres.genre_id')),
    Column('track_url', String(255), nullable=False)
)

artists_table = Table(
    'artists', metadata,
    Column('artist_id', Integer, primary_key=True),
    Column('full_name', String(64), nullable=False)
)

albums_table = Table(
    'albums', metadata,
    Column('album_id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('album_url', String(1024), nullable=False),
    Column('album_type', String(255), nullable=False),
    Column('release_year', Integer, nullable=True)
)

genres_table = Table(
    'genres', metadata,
    Column('genre_id', Integer, primary_key=True),
    Column('name', String(255), nullable=False)
)


def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__user_id': users_table.c.user_id,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password
    })
    mapper(Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__track_id': reviews_table.c.track_id,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp
    })
    mapper(Track, tracks_table, properties={
        '_Track__track_id': tracks_table.c.track_id,
        '_Track__track_duration': tracks_table.c.track_duration,
        '_Track__title': tracks_table.c.title,
        '_Track__track_url': tracks_table.c.track_url,
        '_Track__reviews': relationship(Review, backref='_Review__track')
    })
    mapper(Artist, artists_table, properties={
        '_Artist__artist_id': artists_table.c.artist_id,
        '_Artist__full_name': artists_table.c.full_name,
        '_Artist__tracks': relationship(Track, backref='_Track__artist')
    })
    mapper(Album, albums_table, properties={
        '_Album__album_id': albums_table.c.album_id,
        '_Album__title': albums_table.c.title,
        '_Album__album_url': albums_table.c.album_url,
        '_Album__album_type': albums_table.c.album_type,
        '_Album__release_year': albums_table.c.release_year,
        '_Album__tracks': relationship(Track, backref='_Track__album')
    })
    mapper(Genre, genres_table, properties={
        '_Genre__genre_id': genres_table.c.genre_id,
        '_Genre__name': genres_table.c.name,
        '_Genre__track': relationship(Track, backref='_Track__genre')
    })

