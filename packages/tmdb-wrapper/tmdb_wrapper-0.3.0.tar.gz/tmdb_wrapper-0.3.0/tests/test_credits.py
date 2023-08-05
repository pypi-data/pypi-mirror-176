#!/usr/bin/env python
import pytest
import unittest

from keys import API_KEY, LANGUAGE, REGION, ERROR_MOVIE

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.credits import Credits
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype


class TestTMDb_Credits(unittest.TestCase):
    """Tests for `tmdb_api` package."""

    def setUp(self):
        """Set up API keys"""
        tmdb = TMDb()
        tmdb.api_key = API_KEY
        tmdb.language = LANGUAGE
        tmdb.region = REGION
    
    
    def test_movie_get_details(self):
        """Test something."""
        
        credit = Credits()

        response = credit.get_credit_details(
            credit_id = "52542282760ee313280017f9",
            datatype = PrettifyDatatype(),
        )
        assert response != ERROR_MOVIE