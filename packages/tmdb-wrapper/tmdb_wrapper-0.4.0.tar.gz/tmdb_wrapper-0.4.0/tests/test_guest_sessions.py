import unittest
from tmdb_wrapper.tmdb.authentication import Authentication
from tmdb_wrapper.tmdb.base import TMDb
from keys import API_KEY, ERROR_MOVIE, LANGUAGE, REGION, USERNAME, PASSWORD
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype
from tmdb_wrapper.tmdb.guest_sessions import GuestSessions

class TestTMDb_GuestSessions(unittest.TestCase):

    def setUp(self):
        """Set up API keys"""
        self.tmdb = TMDb()
        self.tmdb.api_key = API_KEY
        self.tmdb.language = LANGUAGE
        self.tmdb.region = REGION

        self.authentication = Authentication()
        self.authentication.username = USERNAME
        self.authentication.password = PASSWORD

        self.authentication.initialize_session_id(type_session="guest_session")

    def test_account(self):
        """Set up API keys"""
        guest_session = GuestSessions()
        print(guest_session)

    def test_get_guest_session_rated_movies(self):
        """Set up API keys"""
        guest_session = GuestSessions()
        response = guest_session.get_guest_session_rated_movies(
            datatype = PrettifyDatatype()
        )
        print(response)
        assert response != ERROR_MOVIE

    def test_get_guest_session_rated_tv_shows(self):
        """Set up API keys"""
        guest_session = GuestSessions()
        response = guest_session.get_guest_session_rated_tv_shows(
            datatype = PrettifyDatatype()
        )
        print(response)
        assert response != ERROR_MOVIE

    def test_get_guest_session_rated_tv_episodes(self):
        """Set up API keys"""
        guest_session = GuestSessions()
        response = guest_session.get_guest_session_rated_tv_episodes(
            datatype = PrettifyDatatype()
        )
        print(response)
        assert response != ERROR_MOVIE