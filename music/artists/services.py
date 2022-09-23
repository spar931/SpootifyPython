import string

from music.adapters.repository import AbstractRepository


class NonExistentArtistException(Exception):
    pass


def get_artists_by_alphabetical_order(repo: AbstractRepository):

    alphabet_dict = {k: [] for k in string.ascii_uppercase}
    alphabet_dict['Other'] = []
    for artist in repo.get_artists():
        if artist.full_name[0].isalpha():
            alphabet_dict[artist.full_name[0].upper()].append(artist)
        else:
            alphabet_dict['Other'].append(artist)
    for value in alphabet_dict.values():
        value.sort(key=lambda x: x.full_name, reverse=False)
    return alphabet_dict


def get_artist_by_id(repo: AbstractRepository, artist_id):
    artist = repo.get_artist_by_id(artist_id)
    if artist is None:
        raise NonExistentArtistException
    return artist


def get_tracks_by_artist(repo: AbstractRepository, chosen_artist):

    tracks_by_artist = []
    for track in repo.get_tracks():
        if track.artist.artist_id == chosen_artist.artist_id:
            tracks_by_artist.append(track)

    tracks_by_artist.sort(key=lambda x: x.title, reverse=False)
    return tracks_by_artist
