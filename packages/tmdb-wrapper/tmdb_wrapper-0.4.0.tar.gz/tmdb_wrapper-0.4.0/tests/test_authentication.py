import sys
import os

from pathlib import Path

import unittest
from tmdb_wrapper.tmdb.authentication import Authentication

from tmdb_wrapper.tmdb.configurations import Configurations
from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.datatype import PrettifyDatatype
from keys import API_KEY, ERROR_MOVIE, LANGUAGE, REGION, USERNAME, PASSWORD

import sys

sys.path.append("./")
print(sys.path)


class TestTMDb_Authentication(unittest.TestCase):

    def setUp(self):
        """Set up API keys"""
        self.tmdb = TMDb()
        self.tmdb.api_key = API_KEY
        self.tmdb.language = LANGUAGE
        self.tmdb.region = REGION


    def test_guest_authentication(self):
        '''
        test_authentication
        '''
        print(sys.path)

        authentication = Authentication()
        authentication.username = USERNAME
        authentication.password = PASSWORD

        authentication.initialize_session_id(
            type_session="guest_session"
        )
        
        print(authentication.expires_at)
        print(authentication.session_id)

    def test_user_authentication(self):
        '''
        test_authentication
        '''
        authentication = Authentication()
        authentication.username = USERNAME
        authentication.password = PASSWORD

        authentication.initialize_session_id(type_session="user_session")

        print(authentication.expires_at)
        print(authentication.session_id)
        print(authentication.request_token)

    def test_user_delete_session(self):

        authentication = Authentication()
        authentication.username = USERNAME
        authentication.password = PASSWORD

        authentication.initialize_session_id(type_session="user_session")

        print(authentication.session_id)

        authentication.delete_session()
