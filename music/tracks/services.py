import string

from music.adapters.repository import AbstractRepository


def get_tracks_by_alphabetical_order(repo: AbstractRepository):

    alphabet_dict = {k: [] for k in string.ascii_uppercase}
    alphabet_dict['Other'] = []
    for track in repo.get_tracks():
        if track.title[0].isalpha():
            alphabet_dict[track.title[0].upper()].append(track)
        else:
            alphabet_dict['Other'].append(track)
    for value in alphabet_dict.values():
        value.sort(key=lambda x: x.title, reverse=False)
    return alphabet_dict


def get_track_by_id(repo: AbstractRepository, track_id):
    return repo.get_track_by_id(track_id)





