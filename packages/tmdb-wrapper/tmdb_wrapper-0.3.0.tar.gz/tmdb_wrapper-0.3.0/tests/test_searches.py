import pytest
import unittest

from keys import API_KEY, LANGUAGE, REGION, ERROR_MOVIE

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.searches import Searches

class TestTMDb_Searches(unittest.TestCase):
    """Tests for `tmdb_api` package."""

    def setUp(self):
        """Set up API keys"""
        tmdb = TMDb()
        tmdb.api_key = API_KEY
        tmdb.language = LANGUAGE
        tmdb.region = REGION

    def test_get_search_company(self):
        """Test something."""

        searches = Searches()

        response = searches.get_search_company(
            query="movie"
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_search_collections(self):
        """Test something."""

        searches = Searches()

        response = searches.get_search_collections(
            query="movie"
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_search_keywords(self):
        """Test something."""

        searches = Searches()

        response = searches.get_search_keywords(
            query="movie"
        )

        print(response)

        assert response != ERROR_MOVIE
    
    def test_get_search_movie(self):
        """Test something."""

        searches = Searches()

        response = searches.get_search_movie(
            query="movie"
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_multi_search(self):
        """Test something."""

        searches = Searches()

        response = searches.get_multi_search(
            query="movie"
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_search_people(self):
        """Test something."""

        searches = Searches()

        response = searches.get_search_people(
            query="movie"
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_search_tv_show(self):
        """Test something."""

        searches = Searches()

        response = searches.get_search_tv_show(
            query="movie"
        )

        print(response)

        assert response != ERROR_MOVIE