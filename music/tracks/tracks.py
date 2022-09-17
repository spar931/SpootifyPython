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
import music.tracks.services as services

# Configure Blueprint.
tracks_blueprint = Blueprint(
    'tracks_bp', __name__)


@tracks_blueprint.route('/browse_tracks_alphabetical', methods=['GET'])
def browse_tracks_alphabetical_order():
    tracks_alphabet_dict = services.get_tracks_by_alphabetical_order(repo.repo_instance)
    return render_template('tracks/simple_track.html', tracks=tracks_alphabet_dict)


@tracks_blueprint.route('/display_track_info/<track_id>', methods=['GET'])
def display_track_info(track_id):
    chosen_track = services.get_track_by_id(repo.repo_instance, track_id)
    return render_template('tracks/track_info.html', track=chosen_track)

