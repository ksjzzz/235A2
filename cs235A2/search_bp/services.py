from typing import Iterable

from cs235A2.domain.model import Movie



class UnValidInput(Exception):
    pass


def is_year(n: object) -> bool:
    if type(n) is not int:
        raise UnValidInput
    else:
        return True


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def get_movies_by_actor(repo,actor):
    result = repo.get_movies_by_actor(actor)
    if result:
        return movies_to_dict(result)

    return []


def get_movies_by_director(repo,director):
    result = repo.get_movies_by_director(director)
    if result:
        return movies_to_dict(result)

    return []


def movie_to_dict(movie: Movie):
    movie_dict = {
        'id': movie.id,
        'date': movie.release_year,
        'title': movie.title,
        'description': movie.description,
        'review': movie.reviews,
        'genre': ", ".join(genre.genre_name for genre in movie.genres),
        'director': movie.director.director_full_name,
        'actor': ", ".join(actor.actor_full_name for actor in movie.actors),
        'rating': movie.rating
    }

    return movie_dict
