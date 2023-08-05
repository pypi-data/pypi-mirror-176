import unittest
from tmdb_wrapper.tmdb.authentication import Authentication
from tmdb_wrapper.tmdb.base import TMDb
from keys import API_KEY, ERROR_MOVIE, LANGUAGE, REGION, USERNAME, PASSWORD
from tmdb_wrapper.tmdb.lists import Lists

class TestTMDb_Lists(unittest.TestCase):

    def setUp(self):
        """Set up API keys"""
        self.tmdb = TMDb()
        self.tmdb.api_key = API_KEY
        self.tmdb.language = LANGUAGE
        self.tmdb.region = REGION

        self.authentication = Authentication()
        self.authentication.username = USERNAME
        self.authentication.password = PASSWORD

        self.authentication.initialize_session_id(type_session="user_session")

    def test_get_list_details(self):
        """Test something."""
        
        lists = Lists()

        response = lists.get_list_details(
            list_id=5
        )
        assert response != ERROR_MOVIE

    def test_get_list_items_status(self):
        """Test something."""
        
        lists = Lists()

        response = lists.get_list_items_status(
            list_id=5,
            movie_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_post_create_lists(self):
        """Test something."""
        
        lists = Lists()

        response = lists.post_create_list(
            name="joao",
            description="algoooo",
            language="asfasfasf"
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_post_add_movie_to_list(self):
        """Test something."""
        
        lists = Lists()
        print('a')
        response = lists.post_add_movie_to_list(
            list_id=8226293,
            media_id=425
        )
        print(response)

        assert response != ERROR_MOVIE

    def test_post_remove_movie(self):
        """Test something."""
        
        lists = Lists()
        response = lists.post_remove_movie(
            list_id=8226293,
            media_id=425
        )
        print(response)

        assert response != ERROR_MOVIE

    def test_post_clear_list(self):
        """Test something."""
        
        lists = Lists()
        response = lists.post_clear_list(
            list_id=8226293
        )
        print(response)

        assert response != ERROR_MOVIE

    def test_delete_list(self):
        """Test something."""
        
        lists = Lists()
        response = lists.delete_list(
            list_id=8226293
        )
        print(response)

        assert response != ERROR_MOVIE