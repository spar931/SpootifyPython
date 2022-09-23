from flask import request, render_template, redirect, url_for, session, Blueprint

import music.adapters.repository as repo
import music.artists.services as services
from music.utilities import utilities

# Configure Blueprint.
artists_blueprint = Blueprint(
    'artists_bp', __name__)


@artists_blueprint.route('/browse_artists_alphabetical', methods=['GET'])
def browse_artists_alphabetical_order():
    artists_alphabet_dict = services.get_artists_by_alphabetical_order(repo.repo_instance)

    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 'A'

    artists_per_page = 45

    cursor2 = request.args.get('cursor2')

    if cursor2 is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor2 = 0
    else:
        # Convert cursor from string to int.
        cursor2 = int(cursor2)

    return render_template('artists/simple_artist.html', cursor=cursor, cursor2=cursor2, artists=artists_alphabet_dict[cursor], selected_tracks=utilities.get_top_tracks(), dict=artists_alphabet_dict, artists_per_page=artists_per_page)


@artists_blueprint.route('/display_artist_info', methods=['GET'])
def display_artist_info():
    artist_id = request.args.get('artist_id')

    chosen_artist = services.get_artist_by_id(repo.repo_instance, artist_id)

    tracks_by_chosen_artist = services.get_tracks_by_artist(repo.repo_instance, chosen_artist)

    return render_template('artists/artist_info.html', artist=chosen_artist, artist_id=artist_id, selected_tracks=utilities.get_top_tracks(), tracks=tracks_by_chosen_artist)

