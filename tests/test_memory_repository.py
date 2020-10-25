from typing import List
import pytest
from cs235A2.adapters.memory_repository import make_review
from cs235A2.adapters.repository import RepositoryException
from cs235A2.domain.model import User, Movie, Genre, Review



def test_repository_can_add_a_user(in_memory_repo):
    user = User('user', 'user12345')
    in_memory_repo.add_user(user)


    assert in_memory_repo.get_user('user') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('usera')
    assert user == User('usera', 'CS235235')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('usere')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()
    assert number_of_movies == 4


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie("movie", 2016)
    movie.id = 5
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie(5) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    assert movie.title == 'a'
    review_one = [review for review in movie.reviews if review.review_text== "Oh no, COVID-19 has hit New Zealand"][0]
    assert review_one.user.user_name == "userb"


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(10)
    assert movie is None


def test_repository_can_retrieve_movies_by_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_date(2012)

    assert len(movies) == 2


def test_repository_does_not_retrieve_an_movie_when_there_are_no_movies_for_a_given_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_date(12514)
    assert len(movies) == 0


def test_repository_can_retrieve_genres(in_memory_repo):
    genres: List[Genre] = in_memory_repo.get_genres()

    assert len(genres) == 3

    assert Genre("Action") in genres
    assert Genre("Adventure") in genres
    assert Genre("Horror") in genres
    assert Genre("Comedy") not in genres


def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'a'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'c'


def test_repository_can_get_movies_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([1,2])

    assert len(movies) == 2
    assert movies[0].title == 'a'
    assert movies[1].title == "b"


def test_repository_does_not_retrieve_movie_for_non_existent_rid(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([1, 100])

    assert len(movies) == 1
    assert movies[
               0].title == 'a'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 1000])

    assert len(movies) == 0


def test_repository_returns_movie_ids_for_existing_genre(in_memory_repo):
    movie_ranks = in_memory_repo.get_movie_ids_for_genre('Action')

    assert movie_ranks == [1, 4]


def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    movie_ranks = in_memory_repo.get_movie_ids_for_genre('Sci-F')

    assert len(movie_ranks) == 0


def test_repository_returns_date_of_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    previous_year = in_memory_repo.get_date_of_previous_movie(movie)

    assert previous_year == 2010


def test_repository_returns_none_when_there_are_no_previous_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    previous_year = in_memory_repo.get_date_of_previous_movie(movie)

    assert previous_year is None


def test_repository_returns_date_of_next_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    next_year = in_memory_repo.get_date_of_next_movie(movie)

    assert next_year == 2012


def test_repository_returns_none_when_there_are_no_subsequent_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(4)
    next_year = in_memory_repo.get_date_of_next_movie(movie)

    assert next_year is None


def test_repository_can_add_a_genre(in_memory_repo):
    genre = Genre('Comedy')
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genres()


def test_repository_can_add_a_review(in_memory_repo):
    user = in_memory_repo.get_user('usera')
    movie = in_memory_repo.get_movie(2)
    review = make_review ("a comment",user, movie)
    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    review = Review(None,movie, "a comment!")

    with pytest.raises(RepositoryException): in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_an_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('userb')
    movie = in_memory_repo.get_movie(0)
    review = Review( user, movie, "a comment!")
    user.add_review(review)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 3
