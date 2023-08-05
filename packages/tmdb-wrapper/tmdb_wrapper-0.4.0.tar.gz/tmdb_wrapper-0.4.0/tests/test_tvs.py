import unittest
from tmdb_wrapper.tmdb.authentication import Authentication
from tmdb_wrapper.tmdb.base import TMDb
from keys import API_KEY, ERROR_MOVIE, LANGUAGE, REGION, USERNAME, PASSWORD
from tmdb_wrapper.tmdb.tvs import Tvs

class TestTMDb_Tvs(unittest.TestCase):

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

    def test_get_details(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_details(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_account_states(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_account_states(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_aggregate_credits(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_aggregate_credits(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_alternative_titles(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_alternative_titles(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_changes(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_changes(
            tv_id=5,
            start_date="2016-05-01",
            end_date="2020-05-01"
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_content_ratings(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_content_ratings(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_credits(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_credits(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_episode_group(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_episode_group(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_external_ids(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_external_ids(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_images(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_images(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_keywords(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_keywords(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_recommendations(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_recommendations(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_reviews(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_reviews(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE
        
    def test_get_screened_theatrically(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_screened_theatrically(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_similar(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_similar(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_translations(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_translations(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_get_videos(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_videos(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_post_rate_video(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.post_rate_video(
            tv_id=5,
            value=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def test_delete_video(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.delete_video(
            tv_id=5
        )

        print(response)

        assert response != ERROR_MOVIE

    def get_latest(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_latest()

        print(response)

        assert response != ERROR_MOVIE

    def get_airing_today(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_airing_today()

        print(response)

        assert response != ERROR_MOVIE

    def get_on_air(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_on_air()

        print(response)

        assert response != ERROR_MOVIE
    
    def get_popular(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_popular()

        print(response)

        assert response != ERROR_MOVIE

    def get_top_rated(self):
        """Test something."""
        
        tvs = Tvs()

        response = tvs.get_top_rated()

        print(response)

        assert response != ERROR_MOVIE