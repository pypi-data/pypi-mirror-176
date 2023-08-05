#!/usr/bin/env python
import pytest
import unittest

from keys import API_KEY, LANGUAGE, REGION, ERROR_MOVIE

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.genres import Genres
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype


class TestTMDb_Genres(unittest.TestCase):
    """Tests for `tmdb_api` package."""

    def setUp(self):
        """Set up API keys"""
        tmdb = TMDb()
        tmdb.api_key = API_KEY
        tmdb.language = LANGUAGE
        tmdb.region = REGION
    
    
    def test_discover_movie(self):
        """Test something."""
        
        genres = Genres()

        response = genres.get_genre_movie(
            datatype = PrettifyDatatype()
        )
        assert response != ERROR_MOVIE

    def test_discover_tv(self):
        """Test something."""
        
        genres = Genres()

        response = genres.get_genre_movie(
            datatype = PrettifyDatatype()
        )
        assert response != ERROR_MOVIE