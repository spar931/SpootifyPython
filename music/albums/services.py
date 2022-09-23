import string

from music.adapters.repository import AbstractRepository


class NonExistentAlbumException(Exception):
    pass


def get_album_by_id(repo: AbstractRepository, album_id):
    album = repo.get_album_by_id(album_id)
    if album is None:
        raise NonExistentAlbumException
    return album


def get_albums_by_alphabetical_order(repo: AbstractRepository):

    alphabet_dict = {k: [] for k in string.ascii_uppercase}
    alphabet_dict['Other'] = []
    for album in repo.get_albums():
        if album.title[0].isalpha():
            alphabet_dict[album.title[0].upper()].append(album)
        else:
            alphabet_dict['Other'].append(album)
    for value in alphabet_dict.values():
        value.sort(key=lambda x: x.title, reverse=False)
    return alphabet_dict


def get_tracks_in_album(repo: AbstractRepository, chosen_album):

    tracks_in_album = []
    for track in repo.get_tracks():
        if track.album is not None:
            if track.album.album_id == chosen_album.album_id:
                tracks_in_album.append(track)

    tracks_in_album.sort(key=lambda x: x.title, reverse=False)
    return tracks_in_album
