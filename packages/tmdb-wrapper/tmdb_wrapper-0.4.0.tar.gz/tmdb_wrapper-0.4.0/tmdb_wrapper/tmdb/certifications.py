from typing import Any

from tmdb_wrapper.data.certification import Certification
from tmdb_wrapper.tmdb.request import GetRequest
from .base import TMDb

from .datatype import Datatype, ModelDatatype


class Certifications(TMDb):
    '''
    requests that are represented by Certifications
    '''
    def get_movie_certifications(self, datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get an up to date list of the officially supported movie certifications on TMDB.

        See more: https://developers.themoviedb.org/3/movies/certifications/get-movie-certifications
        '''

        parse_data = self.request_data(request_operation = GetRequest(), path = "/certification/movie/list")

        return datatype.to_datatype(parse_data = parse_data, model_data = Certification)

    def get_tv_certifications(self, datatype: Datatype = ModelDatatype()) -> Any:
        '''
        Get an up to date list of the officially supported TV show certifications on TMDB.

        See more: https://developers.themoviedb.org/3/movies/certifications/get-tv-certifications
        '''

        parse_data = self.request_data(request_operation = GetRequest(), path = "/certification/movie/list")

        return datatype.to_datatype(parse_data = parse_data, model_data = Certification)
