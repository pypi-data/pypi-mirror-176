import unittest

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.collections import Collections
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype
from keys import API_KEY, ERROR_MOVIE, LANGUAGE, REGION

class TestTMDb_Collections(unittest.TestCase):

    def setUp(self):
        """Set up API keys"""
        self.tmdb = TMDb()
        self.tmdb.api_key = API_KEY
        self.tmdb.language = LANGUAGE
        self.tmdb.region = REGION

    def test_collections_details(self):
        """Test something."""
        certifications = Collections()
        response = certifications.get_details_collection(
            collection_id = 10,
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE

    def test_collections_images(self):
        """Test something."""
        certifications = Collections()
        response = certifications.get_image_collection(
            collection_id = 10,
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE

    def test_collections_translations(self):
        """Test something."""
        certifications = Collections()
        response = certifications.get_translation_collection(
            collection_id = 10,
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE