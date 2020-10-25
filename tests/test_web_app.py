import pytest
from flask import session


def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    response = client.post(
        '/authentication/register',
        data={'username': 'userf', 'password': 'Cs235235'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('1', '', b'Your username is too short'),
        ('abcd', '', b'Your password is required'),
        ('abcd', '123', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit')))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'
    with client:
        client.get('/')
        assert session['username'] == "usera"


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Movie' in response.data


def test_login_required_to_comment(client):
    response = client.post('/comment')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_comment(client, auth):
    auth.login()
    response = client.get('/comment?movie=2')
    response = client.post(
        '/comment',
        data={'comment': 'Who needs quarantine?', 'movie_id': 2}
    )
    assert response.headers['Location'] == 'http://localhost/movies_by_date?date=2011&view_comments_for=2'


@pytest.mark.parametrize(('comment', 'messages'), (
        ('Who thinks Trump is a fuckwit?', (b'Your review must not contain profanity')),
        ('a', (b'Your review is too short')),
))
def test_comment_with_invalid_input(client, auth, comment, messages):
    auth.login()
    response = client.post(
        '/comment',
        data={'comment': comment, 'movie_id': 2}
    )
    for message in messages:
        assert message in response.data


def test_movies_without_date(client):
    response = client.get('/movies_by_date')
    assert response.status_code == 200

    assert b'2010' in response.data
    assert b'movie a' in response.data


def test_movies_with_date(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_date?date=2012')
    assert response.status_code == 200

    assert b'2012' in response.data


def test_movies_with_comment(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_date?date=2010&view_comments_for=1')
    assert response.status_code == 200
    assert b'Oh no, COVID-19 has hit New Zealand' in response.data


def test_movies_with_genre(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_genre?genre=Action')
    assert response.status_code == 200

    # Check that all movies tagged with 'Health' are included on the page.
    assert b'movie a' in response.data
    assert b'movie d' in response.data
