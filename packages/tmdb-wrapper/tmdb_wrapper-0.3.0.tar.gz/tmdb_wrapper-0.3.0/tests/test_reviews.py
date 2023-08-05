import pytest
import unittest

from keys import API_KEY, LANGUAGE, REGION, ERROR_MOVIE

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.reviews import Reviews

class TestTMDb_Reviews(unittest.TestCase):
    """Tests for `tmdb_api` package."""

    def setUp(self):
        """Set up API keys"""
        tmdb = TMDb()
        tmdb.api_key = API_KEY
        tmdb.language = LANGUAGE
        tmdb.region = REGION

    def test_get_reviews(self):
        """Test something."""

        reviews = Reviews()

        response = reviews.get_reviews(
            review_id="58aa82f09251416f92006a3a"
        )

        print(response)

        assert response != ERROR_MOVIE