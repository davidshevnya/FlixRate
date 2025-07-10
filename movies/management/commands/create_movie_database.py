import threading
import time
import json

import requests

from django.core.management.base import BaseCommand, CommandError

from core.settings import env
from movies.models import Genre, Movie


class Command(BaseCommand):
    help = "Create a movie database from https://www.themoviedb.org/ API"

    api_read_token = env("API_READ_TOKEN")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_read_token}",
    }

    def get_all_genres(self):
        url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
        response = requests.get(url, headers=self.headers)
        return [genre.get("name") for genre in response.json().get("genres")]

    def get_movie_genres_by_ids(self, genres_id):
        url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
        response = requests.get(url, headers=self.headers)
        genres = response.json().get("genres")
        genre_names = []
        for genre in genres:
            if genre.get("id") in genres_id:
                genre_names.append(genre.get("name"))
        return genre_names

    def create_genres(self):
        genres = self.get_all_genres()
        for genre in genres:
            Genre.objects.get_or_create(title=genre)

    def get_videos_by_movie_id(self, movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=en-US"
        response = requests.get(url, headers=self.headers)
        results = response.json()["results"]
        if not results:
            return json.dumps([])
        base_url = "https://www.youtube.com/embed/"
        videos = []
        for video in results:
            videos.append(base_url + video.get("key"))
        return json.dumps(videos)

    def get_or_create_movie(self, movie_data):
        movie_id = movie_data.get("id")
        title = movie_data.get("title")
        overview = movie_data.get("overview")
        poster = (
            f"https://image.tmdb.org/t/p/original/{movie_data.get('poster_path', '#')}"
        )
        language = movie_data.get("original_language", "en")
        vote_average = movie_data.get("vote_average", "0")
        release_date = movie_data.get("release_date", "2000-01-01")
        popularity = movie_data.get("popularity", "0.0")

        genres = self.get_movie_genres_by_ids(movie_data.get("genre_ids", []))
        video = self.get_videos_by_movie_id(movie_id=movie_id)

        movie, created = Movie.objects.get_or_create(
            movie_id=movie_id,
            title=title,
            defaults={
                "overview": overview,
                "poster": poster,
                "language": language,
                "vote_average": vote_average,
                "release_date": release_date,
                "popularity": popularity,
                "video": video,
            },
        )
        return movie, created, genres

    def update_movie_fields(self, movie, movie_data, video):
        movie.overview = movie_data.get("overview")
        movie.poster = (
            f"https://image.tmdb.org/t/p/original/{movie_data.get('poster_path', '#')}"
        )
        movie.language = movie_data.get("original_language", "en")
        movie.vote_average = movie_data.get("vote_average", "0")
        movie.release_date = movie_data.get("release_date", "2000-01-01")
        movie.popularity = movie_data.get("popularity", "0.0")
        movie.video = video
        movie.save()

    def assign_genres_to_movie(self, movie, genres):
        for genre_name in genres:
            genre_obj, _ = Genre.objects.get_or_create(title=genre_name)
            movie.genre.add(genre_obj)

    def get_all_movies(self, start_page, end_page):
        self.create_genres()
        self.stdout.write(self.style.NOTICE(f"Threading {threading.current_thread()}"))

        for page in range(start_page, end_page):
            self.stdout.write(self.style.NOTICE(f"PAGE: {page}"))

            url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc"
            response = requests.get(url, headers=self.headers)

            movie_data = response.json().get("results")[0]

            try:
                movie, created, genres = self.get_or_create_movie(movie_data)
                if created:
                    self.assign_genres_to_movie(movie, genres)
                    self.stdout.write(
                        self.style.SUCCESS(f"{movie.title} successfully created")
                    )
                else:
                    self.update_movie_fields(
                        movie,
                        movie_data,
                        video=self.get_videos_by_movie_id(movie_data.get("id")),
                    )
                    self.stdout.write(
                        self.style.NOTICE(
                            f"{movie.title} already exists. Movie fields updated."
                        )
                    )
            except Exception as _ex:
                self.stderr.write(self.style.ERROR(f"Error creating movie: {_ex}"))

    def handle(self, *args, **options):
        total_pages = 500
        threads_per_batch = 13
        for j in range(39):
            threads = list()
            for i in range(threads_per_batch):
                page = j * threads_per_batch + i + 1
                if page <= total_pages:
                    thread = threading.Thread(
                        target=self.get_all_movies, args=(page, page + 1)
                    )
                    threads.append(thread)
                    thread.start()

            for thread in threads:
                thread.join()

            time.sleep(10)
