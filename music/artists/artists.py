from flask import request, render_template, redirect, url_for, session, Blueprint

import music.adapters.repository as repo
import music.artists.services as services

# Configure Blueprint.
artists_blueprint = Blueprint(
    'artists_bp', __name__)


@artists_blueprint.route('/browse_artists_alphabetical', methods=['GET'])
def browse_artists_alphabetical_order():
    artists_alphabet_dict = services.get_artists_by_alphabetical_order(repo.repo_instance)
    return render_template('artists/simple_artist.html', artists=artists_alphabet_dict)


@artists_blueprint.route('/display_artist_info/<artist_id>', methods=['GET'])
def display_artist_info(artist_id):
    chosen_artist = services.get_artist_by_id(repo.repo_instance, artist_id)
    tracks_by_chosen_artist = services.get_tracks_by_artist(repo.repo_instance, chosen_artist)
    return render_template('artists/artist_info.html', artist=chosen_artist, tracks=tracks_by_chosen_artist)

