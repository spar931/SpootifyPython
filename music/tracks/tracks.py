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


@tracks_blueprint.route('/browse_tracks', methods=['GET'])
def browse_tracks():
    tracks = services.get_tracks(repo.repo_instance)
    return render_template('tracks/simple_track.html', tracks=tracks)
