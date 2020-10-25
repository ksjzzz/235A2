from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import cs235A2.utilities.utilities as utilities
import cs235A2.search_bp.services as services
import cs235A2.adapters.repository as repo

# Configure Blueprint.
search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search', methods=['GET'])
def search():
    actorForm = search_actor_Form()
    directorForm = search_director_Form()
    return render_template(
        'search.html',
        actorForm=actorForm,
        directorForm=directorForm,
        handler_url_for_actor=url_for('search_bp.search_actor'),
        handler_url_for_director=url_for('search_bp.search_director'),
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls()
    )


@search_blueprint.route('/search_by_actor', methods=['GET', 'POST'])
def search_actor():
    form = search_actor_Form()
    search_result = None

    if form.validate_on_submit():
        content = form.content.data
        return redirect(url_for('search_bp.search_actor', search=content))

    if request.method == 'GET':
        search_result = services.get_movies_by_actor(repo.repo_instance, request.args.get('search'))

    return render_template(
        "movies_bp/movies.html",
        movies=search_result,
        movies_title="Search result",
        genre_urls=utilities.get_genres_and_urls(),
    )


@search_blueprint.route('/search_by_director', methods=['GET', 'POST'])
def search_director():
    form = search_director_Form()
    search_result = None

    if form.validate_on_submit():
        content = form.content.data
        return redirect(url_for('search_bp.search_director', search=content))

    if request.method == 'GET':
        search_result = services.get_movies_by_director(repo.repo_instance, request.args.get('search'))

    return render_template(
        "movies_bp/movies.html",
        movies=search_result,
        movies_title="Search result",
        genre_urls=utilities.get_genres_and_urls()
    )


class search_actor_Form(FlaskForm):
    content = StringField("content", [DataRequired()])
    submit = SubmitField("search")


class search_director_Form(FlaskForm):
    content = StringField("content", [DataRequired()])
    submit = SubmitField("search")
