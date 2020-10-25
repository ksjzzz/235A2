from cs235A2.domain.model import User, Movie, Genre, make_review, make_genre_association, ModelException
import pytest


@pytest.fixture()
def movie():
    return Movie("Movie d", 2006)


@pytest.fixture()
def user():
    return User("userf", 'Cs235235')


@pytest.fixture()
def genre():
    return Genre('Action')


def test_user_construction(user):
    assert user.user_name == 'userf'
    assert user.password == 'Cs235235'
    assert repr(user) == '<User userf>'

    for review in user.reviews:
        assert False


def test_movie_construction(movie):
    assert movie.id is None
    assert movie.release_year == 2006
    assert movie.title == "Movie d"

    assert movie.number_of_reviews == 0
    assert movie.number_of_genres == 0

    assert repr(movie) == '<Movie Movie d, 2006>'


def test_movie_less_than_operator():
    movie_1 = Movie("movie", 2006)

    movie_2 = Movie("movie", 2016)

    assert movie_1 < movie_2


def test_genre_construction(genre):
    assert genre.genre_name == 'Action'

    for movie in genre.movies:
        assert False

    assert not genre.is_applied_to(Movie("a", 2012))


def test_make_review_establishes_relationships(movie, user):
    review_text = 'whatever, this is a comment'
    review = make_review(review_text, user, movie)

    # Check that the User object knows about the review.
    assert review in user.reviews

    # Check that the review knows about the User.
    assert review.user is user

    # Check that movie knows about the review.
    assert review in movie.reviews

    # Check that the review knows about the movie.
    assert review.movie is movie


def test_make_genre_associations(movie, genre):
    make_genre_association(movie, genre)

    assert movie.is_genre()
    assert movie.is_genre_by(genre)
    assert genre.is_applied_to(movie)
    assert movie in genre.movies


def test_make_genre_associations_with_movie_already_genre(movie, genre):
    make_genre_association(movie, genre)
    with pytest.raises(ModelException):
        make_genre_association(movie, genre)


