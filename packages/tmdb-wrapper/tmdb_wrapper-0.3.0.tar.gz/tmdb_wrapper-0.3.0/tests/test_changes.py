import unittest

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.changes import Changes
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype
from keys import API_KEY, ERROR_MOVIE, LANGUAGE, REGION

class TestTMDb_Changes(unittest.TestCase):

    def setUp(self):
        """Set up API keys"""
        self.tmdb = TMDb()
        self.tmdb.api_key = API_KEY
        self.tmdb.language = LANGUAGE
        self.tmdb.region = REGION

    def test_movie_changes(self):
        """Test something."""
        certifications = Changes()
        response = certifications.get_movie_changes(
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE

    def test_tv_changes(self):
        """Test something."""
        certifications = Changes()
        response = certifications.get_tv_changes(
            datatype = PrettifyDatatype()
        )
        assert response != ERROR_MOVIE

    def test_person_changes(self):
        """Test something."""
        certifications = Changes()
        response = certifications.get_person_changes(
            datatype = PrettifyDatatype()
        )
        assert response != ERROR_MOVIE
