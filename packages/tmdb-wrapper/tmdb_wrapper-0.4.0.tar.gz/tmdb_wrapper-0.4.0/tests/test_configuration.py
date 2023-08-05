import unittest

from tmdb_wrapper.tmdb.configurations import Configurations
from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype
from keys import API_KEY, ERROR_MOVIE, LANGUAGE, REGION

class TestTMDb_Configuration(unittest.TestCase):

    def setUp(self):
        """Set up API keys"""
        self.tmdb = TMDb()
        self.tmdb.api_key = API_KEY
        self.tmdb.language = LANGUAGE
        self.tmdb.region = REGION

    def test_configurations_first(self):
        """Test something."""
        configurations = Configurations()
        response = configurations.get_configuration(
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE

    def test_configurations_country(self):
        """Test something."""
        configurations = Configurations()
        response = configurations.get_configuration_country(
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE

    def test_configurations_job(self):
        """Test something."""
        configurations = Configurations()
        response = configurations.get_configuration_job(
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE

    def test_configurations_language(self):
        """Test something."""
        configurations = Configurations()
        response = configurations.get_configuration_language(
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE

    def test_configurations_primary_translations(self):
        """Test something."""
        configurations = Configurations()
        response = configurations.get_configuration_primary_translations(
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE

    def test_configurations_timezones(self):
        """Test something."""
        configurations = Configurations()
        response = configurations.get_configuration_timezones(
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE