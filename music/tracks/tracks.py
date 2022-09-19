from flask import request, render_template, redirect, url_for, session, Blueprint

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField, validators
from wtforms.validators import DataRequired, Length, ValidationError

import music.adapters.repository as repo
import music.tracks.services as services

from music.authentication.authentication import login_required
from music.domainmodel.track import Track, Review, make_comment
from music.utilities import utilities

# Configure Blueprint.
tracks_blueprint = Blueprint(
    'tracks_bp', __name__)


@tracks_blueprint.route('/browse_tracks_alphabetical', methods=['GET'])
def browse_tracks_alphabetical_order():
    tracks_alphabet_dict = services.get_tracks_by_alphabetical_order(repo.repo_instance)

    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 'A'

    tracks_per_page = 45

    cursor2 = request.args.get('cursor2')

    if cursor2 is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor2 = 0
    else:
        # Convert cursor from string to int.
        cursor2 = int(cursor2)

    return render_template('tracks/simple_track.html', cursor=cursor, cursor2=cursor2, tracks=tracks_alphabet_dict[cursor], selected_tracks=utilities.get_top_tracks(), dict=tracks_alphabet_dict, tracks_per_page=tracks_per_page)


@tracks_blueprint.route('/display_track_info_comments', methods=['GET'])
def display_track_info_comments():
    track_id = request.args.get('track_id')

    if track_id is None:
        # No view-comments query parameter, so set to a non-existent article id.
        article_to_show_comments = -1
    else:
        # Convert article_to_show_comments from string to int.
        article_to_show_comments = int(track_id)

    chosen_track = services.get_track_by_id(repo.repo_instance, track_id)

    # Construct urls for viewing article comments and adding comments.
    view_comment_url = url_for('tracks_bp.display_track_info', track_id=chosen_track.track_id)
    add_comment_url = url_for('tracks_bp.review_track', track_id=chosen_track.track_id)

    return render_template('tracks/track_info_comments.html', track=chosen_track, view_comment_url=view_comment_url
                           , add_comment_url=add_comment_url, track_id=track_id, selected_tracks=utilities.get_top_tracks())


@tracks_blueprint.route('/display_track_info', methods=['GET'])
def display_track_info():
    track_id = request.args.get('track_id')

    if track_id is None:
        # No view-comments query parameter, so set to a non-existent article id.
        article_to_show_comments = -1
    else:
        # Convert article_to_show_comments from string to int.
        article_to_show_comments = int(track_id)

    chosen_track = services.get_track_by_id(repo.repo_instance, track_id)

    # Construct urls for viewing article comments and adding comments.
    view_comment_url = url_for('tracks_bp.display_track_info_comments', track_id=chosen_track.track_id)
    add_comment_url = url_for('tracks_bp.review_track', track_id=chosen_track.track_id)

    return render_template('tracks/track_info.html', track=chosen_track, view_comment_url=view_comment_url
                           , add_comment_url=add_comment_url, track_id=track_id, selected_tracks=utilities.get_top_tracks())


@tracks_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_track():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        track_id = int(form.track_id.data)

        # Use the service layer to store the new comment.
        services.add_review(track_id, 1, form.review.data, user_name, repo.repo_instance)

        # Retrieve the article in dict form.
        track = services.get_track_by_id(repo.repo_instance, track_id)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('tracks_bp.display_track_info_comments', track_id=track_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        track_id = int(request.args.get('track_id'))

        # Store the article id in the form.
        form.track_id.data = track_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        track_id = int(form.track_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    track = services.get_track_by_id(repo.repo_instance, track_id)
    return render_template(
        'tracks/review_on_track.html',
        title='Edit track',
        track=track,
        form=form,
        handler_url=url_for('tracks_bp.review_track'),
        user_name=user_name,
        selected_tracks=utilities.get_top_tracks()
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    track_id = HiddenField("Track id")
    submit = SubmitField('Submit')
