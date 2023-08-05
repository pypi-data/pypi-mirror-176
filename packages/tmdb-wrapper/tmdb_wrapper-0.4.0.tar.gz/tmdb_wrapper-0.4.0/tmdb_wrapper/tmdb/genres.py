from typing import Any
from tmdb_wrapper.data.genre import Genre
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.request import GetRequest
from .base import TMDb

class Genres(TMDb):
    '''
    Get a movie or TV credit details by id.
    '''
    def get_genre_movie(
        self,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get the list of official genres for movies.


        See more: https://developers.themoviedb.org/3/genres/get-movie-list
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/genre/movie/list")

        return datatype.to_datatype(parse_data = parse_data, model_data = Genre)

    def get_genre_tv(
        self,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get the list of official genres for TV shows.

        See more: https://developers.themoviedb.org/3/genres/get-tv-list
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/genre/tv/list")

        return datatype.to_datatype(parse_data = parse_data, model_data = Genre)