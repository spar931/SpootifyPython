from flask import Blueprint, request, render_template, redirect, url_for, session

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)
