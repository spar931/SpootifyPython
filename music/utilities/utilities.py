from flask import Blueprint, request, render_template, redirect, url_for, session

import music.adapters.repository as repo
import music.utilities.services as services

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_top_tracks(quantity=10):

    sorted_tracks = services.sort_tracks_by_reviews(repo.repo_instance)
    top_tracks = sorted_tracks[:quantity]
    return top_tracks

