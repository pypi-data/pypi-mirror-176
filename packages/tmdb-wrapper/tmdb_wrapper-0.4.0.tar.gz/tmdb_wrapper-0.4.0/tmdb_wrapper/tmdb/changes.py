from typing import Any
from tmdb_wrapper.data.movie import ModelMovies, Movie
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.request import GetRequest
from .base import TMDb

class Changes(TMDb):
    '''
    requests that are represented by Changes
    '''
    def get_movie_changes(
        self,
        datatype : Datatype = ModelDatatype(),
        start_date : str = None,
        end_date : str = None,
        page : int = None) -> Any:

        '''
        Get a list of all of the movie ids that have been changed in the past 24 hours.

        You can query it for up to 14 days worth of changed IDs at a time with the
        start_date and end_date query parameters. 100 items are returned per page.

        See more: https://developers.themoviedb.org/3/movies/get-movie-change-list
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(), 
            path = "/movie/changes",
            start_date = start_date,
            end_date = end_date,
            page = page
            )

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)


    def get_tv_changes(self,
        datatype : Datatype = ModelDatatype(),
        start_date : str = None,
        end_date : str = None,
        page : int = None) -> Any:

        '''
        Get a list of all of the TV show ids that have been changed in the past 24 hours.

        You can query it for up to 14 days worth of changed IDs at a time with the start_date
        and end_date query parameters. 100 items are returned per page.
        
        See more: https://developers.themoviedb.org/3/movies/get-tv-change-list
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(), 
            path = "/tv/changes",
            start_date = start_date,
            end_date = end_date,
            page = page
            )


        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)

    def get_person_changes(self,
        datatype : Datatype = ModelDatatype(),
        start_date : str = None,
        end_date : str = None,
        page : int = None) -> Any:

        '''
        Get a list of all of the person ids that have been changed in the past 24 hours.

        You can query it for up to 14 days worth of changed IDs at a time with the start_date
        and end_date query parameters. 100 items are returned per page.

        See more: https://developers.themoviedb.org/3/movies/get-person-change-list
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(), 
            path = "/person/changes",
            start_date = start_date,
            end_date = end_date,
            page = page
            )


        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)
