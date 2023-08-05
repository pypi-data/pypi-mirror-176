import unittest

from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.companies import Companies
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype
from keys import API_KEY, ERROR_MOVIE, LANGUAGE, REGION

class TestTMDb_Companies(unittest.TestCase):

    def setUp(self):
        """Set up API keys"""
        self.tmdb = TMDb()
        self.tmdb.api_key = API_KEY
        self.tmdb.language = LANGUAGE
        self.tmdb.region = REGION

    def test_companies_details(self):
        """Test something."""
        companies = Companies()
        response = companies.get_company_details(
            company_id = 3,
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE

    def test_companies_alternative_names(self):
        """Test something."""
        companies = Companies()
        response = companies.get_company_alternative_names(
            company_id = 3,
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE

    def test_companies_images(self):
        """Test something."""
        companies = Companies()
        response = companies.get_company_images(
            company_id = 3,
            datatype = PrettifyDatatype()
        )

        assert response != ERROR_MOVIE