import pytest
from cs235A2.movies_bp import services as movie_services
from cs235A2.authentication import services as auth_services
from cs235A2.authentication.services import AuthenticationException
from cs235A2.movies_bp.services import NonExistentmovieException


def test_can_add_user(in_memory_repo):
    new_username = 'newuser'
    new_password = 'Cs235123'
    auth_services.add_user(new_username, new_password, in_memory_repo)
    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'usera'
    password = 'asfasafasfirjwn10u3ht1gb1'
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    username = 'usera'
    password = 'CS235235'

    try:
        auth_services.authenticate_user(username, password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    username = 'usera'
    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(username, 'aajfbaogbounenfqoe8', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_id = 1
    review_text = 'whatever, this is a comment'
    username = 'usera'
    movie_services.add_comment(movie_id, review_text, username, in_memory_repo)
    movies_as_dict = movie_services.get_comments_for_movie(movie_id , in_memory_repo)
    assert next((dictionary['comment_text'] for dictionary in movies_as_dict if dictionary['comment_text'] == review_text),None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_id = 12345
    review_text = 'whatever, this is a comment'
    username = 'usera'
    with pytest.raises(movie_services.NonExistentmovieException):
        movie_services.add_comment(movie_id, review_text, username, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_id = 1
    review_text = 'whatever, this is a comment'
    username = 'userf'
    with pytest.raises(movie_services.UnknownUserException):
        movie_services.add_comment(movie_id, review_text, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 1

    movie_as_dict = movie_services.get_movie(movie_id, in_memory_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['date'] == 2010
    assert movie_as_dict['title'] == "a"
    assert movie_as_dict['description'] == "movie a"
    assert len(movie_as_dict['comments']) == 1

    reviews = [dictionary['name'] for dictionary in movie_as_dict['genres']]
    assert 'Action' in reviews
    assert 'Sci-Fi' not in reviews



def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 123456

    # Call the service layer to attempt to retrieve the Movie.
    with pytest.raises(movie_services.NonExistentmovieException):
        movie_services.get_movie(movie_id, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movie_services.get_first_movie(in_memory_repo)
    assert movie_as_dict['id'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movie_services.get_last_movie(in_memory_repo)
    assert movie_as_dict['id'] == 3


def test_get_movies_by_year_with_one_year(in_memory_repo):
    target_year = 2012

    movies_as_dict, prev_year, next_year = movie_services.get_movies_by_date(target_year, in_memory_repo)

    assert len(movies_as_dict) == 2
    assert movies_as_dict[0]['id'] == 4

    assert next_year is None


def test_get_movies_by_year_with_multiple_years(in_memory_repo):
    target_year = 2011

    movies_as_dict, prev_year, next_year = movie_services.get_movies_by_date(target_year, in_memory_repo)

    assert len(movies_as_dict) == 1

    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert [2] == movie_ids

    assert prev_year == 2010
    assert next_year == 2012


def test_get_movies_by_year_with_non_existent_year(in_memory_repo):
    target_year = 1992

    movies_as_dict, prev_year, next_year = movie_services.get_movies_by_date(target_year, in_memory_repo)


    assert len(movies_as_dict) == 0


def test_get_movies_by_id(in_memory_repo):
    target_movie_ids = [1,2,20]
    movies_as_dict = movie_services.get_movies_by_id(target_movie_ids, in_memory_repo)

    assert len(movies_as_dict) == 2

    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert {2, 1}.issubset(movie_ids)


def test_get_reviews_for_movie(in_memory_repo):
    reviews_as_dict = movie_services.get_comments_for_movie(1, in_memory_repo)

    assert len(reviews_as_dict) == 1

    ids = [review['movie_id'] for review in reviews_as_dict]
    ids = set(ids)
    assert 1 in ids
    assert len(ids) == 1


def test_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentmovieException):
        review= movie_services.get_comments_for_movie(12345, in_memory_repo)


def test_get_reviews_for_movie_without_reviews(in_memory_repo):
    reviews_as_dict = movie_services.get_comments_for_movie(4, in_memory_repo)
    assert len(reviews_as_dict) == 0



