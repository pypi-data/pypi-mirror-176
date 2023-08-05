from typing import Any
from tmdb_wrapper.data.person import GetCredits
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.request import GetRequest
from tmdb_wrapper.tmdb.base import TMDb

class Credits(TMDb):
    '''
    Get a movie or TV credit details by id.
    '''
    def get_credit_details(
        self,
        credit_id,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get a movie or TV credit details by id.


        See more: https://developers.themoviedb.org/3/credits/get-credit-details
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/credit/{credit_id}")

        return datatype.to_datatype(parse_data = parse_data, model_data = GetCredits)
