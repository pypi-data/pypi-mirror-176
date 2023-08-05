#!/usr/bin/env python
import pytest
import unittest

from keys import API_KEY, LANGUAGE, REGION, ERROR_MOVIE

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype
from tmdb_wrapper.tmdb.keywords import Keywords


class TestTMDb_Keywords(unittest.TestCase):
    """Tests for `tmdb_api` package."""

    def setUp(self):
        """Set up API keys"""
        tmdb = TMDb()
        tmdb.api_key = API_KEY
        tmdb.language = LANGUAGE
        tmdb.region = REGION
    
    
    def test_get_keyword(self):
        """Test something."""
        
        keywords = Keywords()

        response = keywords.get_keyword(
            datatype = PrettifyDatatype(),
            keyword_id= 3417
        )
        assert response != ERROR_MOVIE

    def test_get_keyword_movie(self):
        """Test something."""
        
        keywords = Keywords()

        response = keywords.get_keyword_movie(
            keyword_id= 3417
        )
        print(response)

        assert response != ERROR_MOVIE