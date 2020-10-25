import csv
import os
from typing import List
from bisect import bisect_left, insort_left
from werkzeug.security import generate_password_hash
from cs235A2.adapters.repository import AbstractRepository
from cs235A2.domain.model import User, Movie, Genre, make_review, make_genre_association, Review,Director, Actor, make_actor_association, make_director_association


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()
        self._genres = list()
        self._users = list()
        self._reviews = list()
        self._directors = list()
        self._actors = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.user_name == username), None)

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.id] = movie

    def get_movie(self, id: int) -> Movie:
        movie = None
        try:
            movie = self._movies_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def get_actor(self, actor_name):
        return next((actor for actor in self._actors if actor.actor_full_name == actor_name), None)

    def get_director(self, d):
        return next((director for director in self._directors if director.director_full_name == d), None)

    def add_directors(self, director):
        self._directors.append(director)

    def add_actor(self, actor):
        self._actors.append(actor)

    def add_genre(self, genre: Genre):
        self._genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self._genres

    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    def get_movies_by_date(self, target_date: int) -> List[Movie]:
        target_movie = Movie("none", target_date)
        matching = list()

        try:
            index = self.movie_index(target_movie)
            for movie in self._movies[index:None]:
                if movie.release_year == target_date:
                    matching.append(movie)
                else:
                    break
        except ValueError:
            pass

        return matching

    def get_number_of_movies(self):
        return len(self._movies)

    def get_first_movie(self):
        if self._movies:
            movie = self._movies[0]
        else:
            return None
        return movie

    def get_last_movie(self):
        if self._movies:
            movie = self._movies[-1]
        else:
            return None
        return movie

    def get_movies_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent movie ids in the repository.
        existing_ids = [id for id in id_list if id in self._movies_index]

        # Fetch the movies_bp.
        movies = [self._movies_index[id] for id in existing_ids]
        return movies

    def get_movie_ids_for_genre(self, genre_name: str):
        # Linear search, to find the first occurrence of a genre with the name genre_name.
        genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)

        # Retrieve the ids of movies_bp associated with the genre.
        if genre is not None:
            movie_ids = [movie.id for movie in genre.movies]
        else:
            # No genre with name genre_name, so return an empty list.
            movie_ids = list()

        return movie_ids

    def get_date_of_previous_movie(self, movie: Movie):
        previous_date = None

        try:
            index = self.movie_index(movie)
            for stored_movie in reversed(self._movies[0:index]):
                if stored_movie.release_year < movie.release_year:
                    previous_date = stored_movie.release_year
                    break
        except ValueError:
            # No earlier movies_bp, so return None.
            pass

        return previous_date

    def get_date_of_next_movie(self, movie: Movie):
        next_date = None

        try:
            index = self.movie_index(movie)
            for stored_movie in self._movies[index + 1:len(self._movies)]:
                if stored_movie.release_year > movie.release_year:
                    next_date = stored_movie.release_year
                    break
        except ValueError:
            # No subsequent movies_bp, so return None.
            pass

        return next_date

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].release_year == movie.release_year:
            return index
        raise ValueError

    def movies_index(self):
        return self._movies_index

    def get_genre(self, genre_name):
        return next((genre for genre in self._genres if genre.genre_name == genre_name), None)

    def get_movies_by_actor(self, actor_name):
        actor = next((actor for actor in self._actors if actor.actor_full_name == actor_name), None)
        if actor is not None:
            return actor.movies
        else:
            return list()

    def get_movies_by_director(self,director_name):
        director = next((director for director in self._directors if director.director_full_name == director_name), None)
        if director is not None:
            return director.movies
        else:
            return list()


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies_and_genres(data_path: str, repo: MemoryRepository):

    for data_row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):

        movie_id = data_row[0]
        title = data_row[1]
        genres = data_row[2]
        description = data_row[3]
        director = data_row[4]
        actor = data_row[5]
        release_year = data_row[6]
        runtime = data_row[7]
        rating = data_row[8]
        movie = Movie(title, int(release_year))
        movie.id = int(movie_id)
        movie.description = description
        movie.runtime_minutes = int(runtime)
        movie.rating = rating
        repo.add_movie(movie)

        director_of_movie = repo.get_director(director)
        if not director_of_movie:
            director_of_movie = Director(director)
            repo.add_directors(director_of_movie)
        make_director_association(movie, director_of_movie)

        for actor_name in actor.split(","):
            actor = repo.get_actor(actor_name)
            if not actor:
                actor = Actor(actor_name)
                repo.add_actor(actor)
            make_actor_association(movie, actor)


        for genre_name in genres.split(","):
            genre = repo.get_genre(genre_name)
            if not genre:
                genre = Genre(genre_name)
                repo.add_genre(genre)
            make_genre_association(movie, genre)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(user_name=data_row[1],password=generate_password_hash(data_row[2]))
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_reviews(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'reviews.csv')):
        review = make_review(
            review_text=data_row[3],
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
        )
        repo.add_review(review)


def populate(data_path: str, repo: MemoryRepository):
    # Load movies_bp and genres into the repository.
    load_movies_and_genres(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load reviews into the repository.
    load_reviews(data_path, repo, users)
