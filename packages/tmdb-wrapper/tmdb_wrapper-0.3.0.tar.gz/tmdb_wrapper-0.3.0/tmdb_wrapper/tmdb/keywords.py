from typing import Any
from tmdb_wrapper.data.genre import Genre
from tmdb_wrapper.data.keyword import Keyword
from tmdb_wrapper.data.movie import ModelMovies
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.request import GetRequest
from .base import TMDb

class Keywords(TMDb):
    '''
    Keywords Class
    '''
    def get_keyword(
        self,
        datatype : Datatype = ModelDatatype(),
        keyword_id: int = 1) -> Any:

        '''
        Get keywords.

        See more: https://developers.themoviedb.org/3/keywords/get-keyword-details
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/keyword/{keyword_id}")

        return datatype.to_datatype(parse_data = parse_data, model_data = Keyword)

    def get_keyword_movie(
        self,
        datatype : Datatype = ModelDatatype(),
        keyword_id: int = None,
        include_adult: bool = None) -> Any:

        '''
        Get the movies that belong to a keyword.

        We highly recommend using "movie discover" instead of this method as
        it is much more flexible.

        See more: https://developers.themoviedb.org/3/keywords/get-movies-by-keyword
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/keyword/{keyword_id}/movies",
            include_adult = include_adult)

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)
