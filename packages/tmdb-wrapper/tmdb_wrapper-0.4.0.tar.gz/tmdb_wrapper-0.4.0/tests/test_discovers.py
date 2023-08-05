#!/usr/bin/env python
import pytest
import unittest

from keys import API_KEY, LANGUAGE, REGION, ERROR_MOVIE

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype
from tmdb_wrapper.tmdb.discovers import Discovers


class TestTMDb_Discovers(unittest.TestCase):
    """Tests for `tmdb_api` package."""

    def setUp(self):
        """Set up API keys"""
        tmdb = TMDb()
        tmdb.api_key = API_KEY
        tmdb.language = LANGUAGE
        tmdb.region = REGION
    
    
    def test_discover_movie(self):
        """Test something."""
        
        discovers = Discovers()

        response = discovers.get_movie_discover(
            datatype = PrettifyDatatype(),
            page = 4
        )
        assert response != ERROR_MOVIE

    def test_discover_tv(self):
        """Test something."""
        
        discovers= Discovers()

        response = discovers.get_tv_discover(
            datatype = PrettifyDatatype(),
            page = 10
        )
        assert response != ERROR_MOVIE