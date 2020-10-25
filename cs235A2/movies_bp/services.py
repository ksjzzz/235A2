from typing import List, Iterable

from cs235A2.adapters.repository import AbstractRepository
from cs235A2.domain.model import make_review, Movie, Review, Genre


class NonExistentmovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_comment(movie_id: int, comment_text: str, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentmovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = make_review(comment_text, user, movie)

    # Update the repository.
    repo.add_review(comment)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentmovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):

    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):

    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_movies_by_date(date, repo: AbstractRepository):
    movies = repo.get_movies_by_date(target_date=date)

    movies_dto = list()
    prev_date = next_date = None

    if len(movies) > 0:
        prev_date = repo.get_date_of_previous_movie(movies[0])
        next_date = repo.get_date_of_next_movie(movies[0])

        # Convert movies_bp to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_date, next_date


def get_movie_ids_for_genre(genre_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_genre(genre_name)

    return movie_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert movies_bp to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_comments_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentmovieException

    return comments_to_dict(movie.reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        "director": movie.director.director_full_name,
        'actor': ", ".join(actor.actor_full_name for actor in movie.actors),
        'genre': ", ".join(genre.genre_name for genre in movie.genres),
        "description": movie.description,
        'id': movie.id,
        'date': movie.release_year,
        'title': movie.title,
        'comments': comments_to_dict(movie.reviews),
        'genres': genres_to_dict(movie.genres),
        'rating': movie.rating
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def comment_to_dict(review: Review):
    comment_dict = {
        'username': review.user.user_name,
        'movie_id': review.movie.id,
        'comment_text': review.review_text,
        'timestamp': review.timestamp
    }
    return comment_dict


def comments_to_dict(comments: Iterable[Review]):
    return [comment_to_dict(comment) for comment in comments]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'name': genre.genre_name,
        'movies_bp': [movie.id for movie in genre.movies]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


def dict_to_movie(dict):
    movie = Movie(dict.title, dict.date)
    # Note there's no comments or genres.
    return movie
