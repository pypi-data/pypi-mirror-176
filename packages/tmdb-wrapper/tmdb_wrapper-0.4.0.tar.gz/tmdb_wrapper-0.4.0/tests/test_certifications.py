import unittest

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.certifications import Certifications
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype
from keys import API_KEY, ERROR_MOVIE, LANGUAGE, REGION

class TestTMDb_Certifications(unittest.TestCase):

    def setUp(self):
        """Set up API keys"""
        self.tmdb = TMDb()
        self.tmdb.api_key = API_KEY
        self.tmdb.language = LANGUAGE
        self.tmdb.region = REGION

    def test_movie_certifications(self):
        """Test something."""
        certifications = Certifications()

        print(certifications.api_key)

        response = certifications.get_movie_certifications(
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE

    def test_tv_certifications(self):
        """Test something."""
        certifications = Certifications()
        response = certifications.get_tv_certifications(
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE