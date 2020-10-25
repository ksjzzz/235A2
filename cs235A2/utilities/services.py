from typing import Iterable
import random

from cs235A2.adapters.repository import AbstractRepository
from cs235A2.domain.model import Movie


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre.genre_name for genre in genres]

    return genre_names


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of movies_bp.
        quantity = movie_count - 1

    # Pick distinct and random movies_bp.
    random_ids = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_id(random_ids)

    return movies_to_dict(movies)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'date': movie.release_year,
        'title': movie.title,
        "director": movie.director.director_full_name,
        'actor': ", ".join(actor.actor_full_name for actor in movie.actors),
        'genre': ", ".join(genre.genre_name for genre in movie.genres),
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
