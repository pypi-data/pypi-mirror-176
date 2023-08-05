import unittest
from tmdb_wrapper.tmdb.authentication import Authentication
from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.account import Account
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype
from keys import API_KEY, ERROR_MOVIE, LANGUAGE, REGION, USERNAME, PASSWORD

class TestTMDb_Account(unittest.TestCase):

    def setUp(self):
        """Set up API keys"""
        self.tmdb = TMDb()
        self.tmdb.api_key = API_KEY
        self.tmdb.language = LANGUAGE
        self.tmdb.region = REGION

        self.authentication = Authentication()
        self.authentication.username = USERNAME
        self.authentication.password = PASSWORD

        self.authentication.initialize_session_id(type_session="user_session")

    def test_account(self):
        """Set up API keys"""
        account = Account()
        print(account.account_id)

    def test_account_get_details(self):
        """Set up API keys"""
        account = Account()
        response = account.get_details()
        print(response)
        assert response != ERROR_MOVIE
    
    def test_account_get_created_lists(self):
        """Set up API keys"""
        account = Account()
        print(account.account_id)
        response = account.get_created_lists()
        print(response)
        assert response != ERROR_MOVIE

    def test_account_get_favourite_movies(self):
        """Set up API keys"""
        account = Account()
        print(account.account_id)
        response = account.get_favourite_movies()
        print(response)
        assert response != ERROR_MOVIE

    def test_account_get_favourite_tvs(self):
        """Set up API keys"""
        account = Account()
        print(account.account_id)
        response = account.get_favourite_tvs()
        print(response)
        assert response != ERROR_MOVIE

    def test_account_post_mark_as_favourite(self):
        """Set up API keys"""
        account = Account()
        print(account.account_id)
        response = account.post_mark_as_favourite(
            media_type="movie",
            media_id=550,
            favorite="true"
        )
        print(response)
        assert response != ERROR_MOVIE

    def test_account_get_rated_movies(self):
        """Set up API keys"""
        account = Account()
        print(account.account_id)
        response = account.get_rated_movies()
        print(response)
        assert response != ERROR_MOVIE

    def test_account_get_tv_shows(self):
        """Set up API keys"""
        account = Account()
        print(account.account_id)
        response = account.get_tv_shows()
        print(response)
        assert response != ERROR_MOVIE

    def test_account_get_tv_episodes(self):
        """Set up API keys"""
        account = Account()
        print(account.account_id)
        response = account.get_tv_episodes()
        print(response)
        assert response != ERROR_MOVIE

    def test_account_get_movies_watchlist(self):
        """Set up API keys"""
        account = Account()
        print(account.account_id)
        response = account.get_movies_watchlist()
        print(response)
        assert response != ERROR_MOVIE

    def test_account_get_tv_show_watchlist(self):
        """Set up API keys"""
        account = Account()
        print(account.account_id)
        response = account.get_tv_show_watchlist()
        print(response)
        assert response != ERROR_MOVIE

    def test_account_post_add_to_watchlist(self):
        """Set up API keys"""
        account = Account()
        print(account.account_id)
        response = account.post_add_to_watchlist(
            media_type="movie",
            media_id=11,
            watchlist="true"
        )
        print(response)
        assert response != ERROR_MOVIE
       