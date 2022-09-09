from flask import request, render_template, redirect, url_for, session, Blueprint

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import music.adapters.repository as repo
import music.albums.services as services

# Configure Blueprint.
albums_blueprint = Blueprint(
    'albums_bp', __name__)


@albums_blueprint.route('/browse_albums_alphabetical', methods=['GET'])
def browse_albums_alphabetical_order():
    tracks_alphabet_dict = services.get_albums_by_alphabetical_order(repo.repo_instance)
    return render_template('albums/simple_album.html', albums=tracks_alphabet_dict)


@albums_blueprint.route('/display_album_info/<album_id>', methods=['GET'])
def display_album_info(album_id):
    chosen_album = services.get_album_by_id(repo.repo_instance, album_id)
    tracks_in_chosen_album = services.get_tracks_in_album(repo.repo_instance, chosen_album)
    return render_template('albums/album_info.html', tracks=tracks_in_chosen_album, album=chosen_album)
