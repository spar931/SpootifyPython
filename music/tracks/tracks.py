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


@tracks_blueprint.route('/review', methods=['GET', 'POST'])
def comment_on_article():
    # Obtain the user name of the currently logged in user.
    # user_name = session['user_name']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        track_id = int(form.track_id.data)

        # Use the service layer to store the new comment.
        services.add_comment(track_id, form.comment.data, user_name, repo.repo_instance)

        # Retrieve the article in dict form.
        article = services.get_article(track_id, repo.repo_instance)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('news_bp.articles_by_date', date=article['date'], view_comments_for=track_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        track_id = int(request.args.get('article'))

        # Store the article id in the form.
        form.article_id.data = track_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        track_id = int(form.article_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    track = services.get_track_by_id(repo.repo_instance, track_id)
    return render_template(
        'tracks/review_on_track.html',
        title='Edit article',
        article=track,
        form=form,
        handler_url=url_for('news_bp.comment_on_article'),
        selected_articles=utilities.get_selected_articles(),
        tag_urls=utilities.get_tags_and_urls()
    )

