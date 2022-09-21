"""Initialize Flask app."""

from pathlib import Path
import os
from flask import Flask

import music.adapters.repository as repo
from music.adapters.csvdatareader import TrackCSVReader
from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.track import Review
from music.tracks import services as tracks_services
import music.adapters.repository as repo


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('music') / 'adapters' / 'data'

    app.config['SECRET_KEY'] = 'qwerty'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    data = TrackCSVReader(str(data_path) + "/raw_albums_excerpt.csv", str(data_path) + "/raw_tracks_excerpt.csv")
    data.read_csv_files()

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository(data)

    track_id = 3
    track = tracks_services.get_track_by_id(repo.repo_instance, track_id)
    review_text = 'my favourite track'
    track.track_reviews.append(Review(track, review_text, 4))

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.auth, url_prefix='/')

        from .tracks import tracks
        app.register_blueprint(tracks.tracks_blueprint)

        from .artists import artists
        app.register_blueprint(artists.artists_blueprint)

        from .albums import albums
        app.register_blueprint(albums.albums_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

    return app
