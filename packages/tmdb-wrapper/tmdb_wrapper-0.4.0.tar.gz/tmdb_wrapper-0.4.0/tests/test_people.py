import pytest
import unittest

from keys import API_KEY, LANGUAGE, REGION, ERROR_MOVIE

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.people import People

class TestTMDb_People(unittest.TestCase):
    """Tests for `tmdb_api` package."""

    def setUp(self):
        """Set up API keys"""
        tmdb = TMDb()
        tmdb.api_key = API_KEY
        tmdb.language = LANGUAGE
        tmdb.region = REGION

    def test_get_people_details(self):
        """Test something."""

        people = People()

        response = people.get_people_details(
            person_id=3
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_people_changes(self):
        """Test something."""

        people = People()

        response = people.get_people_changes(
            person_id=3
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_people_movie_credits(self):
        """Test something."""

        people = People()

        response = people.get_people_movie_credits(
            person_id=3
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_people_tv_credits(self):
        """Test something."""

        people = People()

        response = people.get_people_tv_credits(
            person_id=3
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_people_combined_credits(self):
        """Test something."""

        people = People()

        response = people.get_people_combined_credits(
            person_id=3
        )

        print(response)

        assert response != ERROR_MOVIE
    
    def test_get_people_external_ids(self):
        """Test something."""

        people = People()

        response = people.get_people_external_ids(
            person_id=3
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_people_images(self):
        """Test something."""

        people = People()

        response = people.get_people_images(
            person_id=3
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_people_translations(self):
        """Test something."""

        people = People()

        response = people.get_people_translations(
            person_id=3
        )

        print(response)

        assert response != ERROR_MOVIE
    
    def test_get_people_latest(self):
        """Test something."""

        people = People()

        response = people.get_people_latest()

        print(response)

        assert response != ERROR_MOVIE

    def test_get_people_popular(self):
        """Test something."""

        people = People()

        response = people.get_people_popular()

        print(response)

        assert response != ERROR_MOVIE