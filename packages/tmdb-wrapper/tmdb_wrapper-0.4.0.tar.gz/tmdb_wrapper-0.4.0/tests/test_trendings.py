import pytest
import unittest

from keys import API_KEY, LANGUAGE, REGION, ERROR_MOVIE

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.trendings import Trendings

class TestTMDb_Trendings(unittest.TestCase):
    """Tests for `tmdb_api` package."""

    def setUp(self):
        """Set up API keys"""
        tmdb = TMDb()
        tmdb.api_key = API_KEY
        tmdb.language = LANGUAGE
        tmdb.region = REGION

    def test_get_trendings(self):
        """Test something."""

        trendigns = Trendings()

        response = trendigns.get_trendings(
            media_type="movie",
            time_window="day",
        )

        print(response)

        assert response != ERROR_MOVIE