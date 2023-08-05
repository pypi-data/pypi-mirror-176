#!/usr/bin/env python
import pytest
import unittest

from keys import API_KEY, LANGUAGE, REGION, ERROR_MOVIE

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype
from tmdb_wrapper.tmdb.networks import Networks


class TestTMDb_Networks(unittest.TestCase):
    """Tests for `tmdb_api` package."""

    def setUp(self):
        """Set up API keys"""
        tmdb = TMDb()
        tmdb.api_key = API_KEY
        tmdb.language = LANGUAGE
        tmdb.region = REGION

    def test_get_network_details(self):
        """Test something."""

        networks = Networks()

        response = networks.get_network_details(
            network_id=2,
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_network_alternative_names(self):
        """Test something."""

        networks = Networks()

        response = networks.get_network_alternative_names(
            network_id=2,
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_network_images(self):
        """Test something."""

        networks = Networks()

        response = networks.get_network_images(
            network_id=2,
        )

        print(response)

        assert response != ERROR_MOVIE
