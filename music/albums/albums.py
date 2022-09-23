from flask import request, render_template, redirect, url_for, session, Blueprint

import music.adapters.repository as repo
import music.albums.services as services
from music.utilities import utilities

# Configure Blueprint.
albums_blueprint = Blueprint(
    'albums_bp', __name__)


@albums_blueprint.route('/browse_albums_alphabetical', methods=['GET'])
def browse_albums_alphabetical_order():
    albums_alphabet_dict = services.get_albums_by_alphabetical_order(repo.repo_instance)

    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 'A'

    albums_per_page = 45

    cursor2 = request.args.get('cursor2')

    if cursor2 is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor2 = 0
    else:
        # Convert cursor from string to int.
        cursor2 = int(cursor2)

    return render_template('albums/simple_album.html', cursor=cursor, cursor2=cursor2, albums=albums_alphabet_dict[cursor], selected_tracks=utilities.get_top_tracks(), dict=albums_alphabet_dict, albums_per_page=albums_per_page)


@albums_blueprint.route('/display_album_info', methods=['GET'])
def display_album_info():
    album_id = request.args.get('album_id')

    chosen_album = services.get_album_by_id(repo.repo_instance, album_id)

    tracks_in_chosen_album = services.get_tracks_in_album(repo.repo_instance, chosen_album)

    return render_template('albums/album_info.html', album=chosen_album, album_id=album_id, selected_tracks=utilities.get_top_tracks(), tracks=tracks_in_chosen_album)

