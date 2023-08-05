from typing import Any
from tmdb_wrapper.data.review import Review
from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.request import  GetRequest

class Reviews(TMDb):
    '''
    Reviews Class
    '''
    def get_reviews(
        self,
        datatype : Datatype = ModelDatatype(),
        review_id: str = None) -> Any:

        '''
        Retrieve the details of a movie or TV show review.


        See more: https://developers.themoviedb.org/3/trending/get-trending
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/review/{review_id}")

        return datatype.to_datatype(parse_data = parse_data, model_data = Review)