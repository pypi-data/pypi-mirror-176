from typing import Any
from tmdb_wrapper.data.change import Change
from tmdb_wrapper.data.external_id import ExternalIDs
from tmdb_wrapper.data.keyword import Keywords
from tmdb_wrapper.data.release_date import ReleaseDates
from tmdb_wrapper.data.review import Reviews
from tmdb_wrapper.data.translation import Translation
from tmdb_wrapper.data.video import Videos
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.data.movie import Movie, ModelMovies
from tmdb_wrapper.data.title import Title
from tmdb_wrapper.data.now_playing import NowPlaying

from .request import GetRequest
from .base import TMDb

class Movies(TMDb):
    '''
    TODO: Get Watch Providers GET
    TODO: Account States GET
    TODO: Rate movie POST
    TODO: Rate movie DELETE
    '''
    def get_details_movie(self, movie_id: int, datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get all the details about a movie.

        See more: https://developers.themoviedb.org/3/movies/get-movie-details
        '''

        parse_data = self.request_data(request_operation = GetRequest(), path = f"movie/{movie_id}")

        return datatype.to_datatype(parse_data = parse_data, model_data = Movie)


    def get_alternative_titles(self, movie_id: int, datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get all of the alternative titles for a movie.

        See more: https://developers.themoviedb.org/3/movies/get-movie-details
        '''

        parse_data = self.request_data(request_operation = GetRequest(), path = f"movie/{movie_id}/alternative_titles")

        return datatype.to_datatype(parse_data = parse_data, model_data = Title)

    def get_changes(
        self,
        movie_id: int, 
        datatype : Datatype = ModelDatatype(),
        start_date : str = None,
        end_date : str = None,
        page : int = None) -> Any:
        '''
        Get the changes for a movie. By default only the last 24 hours are returned.

        You can query up to 14 days in a single query by using the start_date and end_date query parameters.

        See more: https://developers.themoviedb.org/3/movies/get-movie-changes
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"movie/{movie_id}/changes",
            start_date=start_date,
            end_date=end_date,
            page=page)

        return datatype.to_datatype(parse_data = parse_data, model_data = Change)

    def get_credits(
        self,
        movie_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get the cast and crew for a movie.

        See more: https://developers.themoviedb.org/3/movies/get-movie-credits
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"movie/{movie_id}/credits")

        return datatype.to_datatype(parse_data = parse_data, model_data = Change)
        

    def get_external_ids(
        self,
        movie_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get the external ids for a movie. We currently support the following external sources.

        See more: https://developers.themoviedb.org/3/movies/get-movie-external-ids
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(), 
            path = f"movie/{movie_id}/external_ids")

        return datatype.to_datatype(parse_data = parse_data, model_data = ExternalIDs)

    def get_images(
        self,
        movie_id: int,
        datatype : Datatype = ModelDatatype(),
        include_image_language : str = "en") -> Any:
        '''
        Get the images that belong to a movie.

        Querying images with a language parameter will filter the results.
        If you want to include a fallback language (especially useful for backdrops)
        you can use the include_image_language parameter. This should be a comma
        seperated value like so: include_image_language=en,null.

        See more: https://developers.themoviedb.org/3/movies/get-movie-changes
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(), 
            path = f"movie/{movie_id}/external_ids",
            include_image_language = include_image_language)

        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = ExternalIDs)

    def get_keywords(
        self,
        movie_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get the keywords that have been added to a movie.

        See more: https://developers.themoviedb.org/3/movies/get-movie-keywords
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"movie/{movie_id}/keywords")

        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = Keywords)


    def get_lists(
        self,
        movie_id: int,
        datatype : Datatype = ModelDatatype(),
        page : int = 1) -> Any:
        '''
        Get a list of lists that this movie belongs to.

        See more: https://developers.themoviedb.org/3/movies/get-movie-lists
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"movie/{movie_id}/lists",
            page = page)

        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = ModelMovies)

    def get_recommendations(
        self,
        movie_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get a list of recommended movies for a movie.

        See more: https://developers.themoviedb.org/3/movies/get-movie-recommendations
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"movie/{movie_id}/recommendations")

        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = ModelMovies)

    def get_release_dates(
        self,
        movie_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get the release date along with the certification for a movie.

        Release dates support different types:

        Premiere
        Theatrical (limited)
        Theatrical
        Digital
        Physical
        TV

        See more: https://developers.themoviedb.org/3/movies/get-movie-release-dates
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"movie/{movie_id}/release_dates")

        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = ReleaseDates)


    def get_reviews(
        self,
        movie_id: int,
        datatype : Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get the user reviews for a movie.

        See more: https://developers.themoviedb.org/3/movies/get-movie-reviews
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"movie/{movie_id}/reviews",
            page = page)

        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = Reviews)


    def get_similar_movies(
        self,
        movie_id: int,
        datatype : Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get a list of similar movies. This is not the same as the "Recommendation" system
        you see on the website.

        These items are assembled by looking at keywords and genres.

        See more: https://developers.themoviedb.org/3/movies/get-similar-movies
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"movie/{movie_id}/similar",
            page = page)

        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = ModelMovies)


    def get_translations(
        self,
        movie_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get a list of translations that have been created for a movie.

        See more: https://developers.themoviedb.org/3/movies/get-similar-movies
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"movie/{movie_id}/translations")

        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = Translation)

    def get_videos(
        self,
        movie_id: int,
        datatype: Datatype = ModelDatatype(),
        include_video_language: str = "en") -> Any:
        '''
        Get the videos that have been added to a movie.

        See more: https://developers.themoviedb.org/3/movies/get-movie-videos
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"movie/{movie_id}/videos",
            include_video_language = include_video_language)

        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = Videos)

    def get_latest(
        self,
        datatype: Datatype = ModelDatatype()) -> Any:
        '''
        Get the most newly created movie. This is a live response and will continuously change.

        See more: https://developers.themoviedb.org/3/movies/get-latest-movie
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "movie/latest")

        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = Movie)


    def get_now_playing(
        self,
        datatype: Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get a list of movies in theatres. This is a release type query that
        looks for all movies that have a release type of 2 or 3 within the specified date range.

        You can optionally specify a region prameter which will narrow the search to only
        look for theatrical release dates within the specified country.

        See more: https://developers.themoviedb.org/3/movies/get-now-playing
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "movie/now_playing",
            page = page,
            region = self.region)
    
        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = NowPlaying)


    def get_popular(
        self,
        datatype: Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get a list of the current popular movies on TMDB. This list updates daily.

        See more: https://developers.themoviedb.org/3/movies/get-popular-movies
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "movie/popular",
            page = page,
            region = self.region)
    
        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = ModelMovies)

    def get_top_rated(
        self,
        datatype: Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get the top rated movies on TMDB.

        See more: https://developers.themoviedb.org/3/movies/get-top-rated-movies
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "movie/top_rated",
            page = page,
            region = self.region)
     
        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = ModelMovies)

    def get_upcoming(
        self,
        datatype: Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get a list of upcoming movies in theatres. This is a release type query that looks for 
        all movies that have a release type of 2 or 3 within the specified date range.

        You can optionally specify a region prameter which will narrow the search to only look 
        for theatrical release dates within the specified country.

        See more: https://developers.themoviedb.org/3/movies/get-upcoming
        '''
        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "movie/upcoming",
            page = page,
            region = self.region)
      
        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = ModelMovies)
